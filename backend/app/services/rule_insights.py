"""
Deterministic rule-based insights engine.
Generates useful spending insights from analytics data without any external AI API.
Returns JSON in the same shape the frontend InsightsPanel expects.
"""
from sqlalchemy.orm import Session
from app.services.analytics import (
    get_summary, get_category_breakdown,
    get_monthly_trends, get_top_merchants,
)


def _fmt(amount: float) -> str:
    """Format amount as ₹X,XXX."""
    return f"₹{amount:,.0f}"


def _pct(part: float, total: float) -> str:
    if total == 0:
        return "0%"
    return f"{(part / total) * 100:.0f}%"


DISCRETIONARY = {"Food & Dining", "Shopping", "Entertainment", "Personal Care"}


# ── Summary ─────────────────────────────────────────────────────────────

def get_summary_insights(db: Session) -> dict:
    s = get_summary(db)
    cats = get_category_breakdown(db)
    trends = get_monthly_trends(db)

    total_spend = s["total_completed_spend_excluding_self_transfers"]
    completed = s["completed_transactions"]

    # Top category
    top_cat = cats[0] if cats else None
    top_cat_name = top_cat["category"] if top_cat else "N/A"
    top_cat_spend = top_cat["total_spend"] if top_cat else 0

    # Active months
    active_months = len([t for t in trends if t["total_spend"] > 0])

    # Monthly average
    monthly_avg = total_spend / active_months if active_months > 0 else 0

    # Build summary text
    parts = [f"You've spent {_fmt(total_spend)} across {completed} completed transactions."]
    if top_cat:
        parts.append(f"Your biggest spending category is {top_cat_name} at {_fmt(top_cat_spend)} ({_pct(top_cat_spend, total_spend)} of total).")
    if active_months > 1:
        parts.append(f"Your monthly average is {_fmt(monthly_avg)} over {active_months} active months.")

    highlights = [
        {"label": "Total Spend", "value": _fmt(total_spend)},
        {"label": "Top Category", "value": top_cat_name},
        {"label": "Monthly Avg", "value": _fmt(monthly_avg)},
        {"label": "Active Months", "value": str(active_months)},
        {"label": "Avg per Transaction", "value": _fmt(s["average_completed_transaction_amount_excluding_self_transfers"])},
    ]
    if len(cats) > 1:
        highlights.append({"label": "Categories Used", "value": str(len(cats))})

    return {
        "status": "success",
        "summary": " ".join(parts),
        "highlights": highlights,
    }


# ── Monthly Insights ────────────────────────────────────────────────────

def get_monthly_insights(db: Session) -> dict:
    cats = get_category_breakdown(db)
    trends = get_monthly_trends(db)
    merchants = get_top_merchants(db)
    s = get_summary(db)

    total_spend = s["total_completed_spend_excluding_self_transfers"]
    insights = []

    # 1. Top spending category
    if cats:
        top = cats[0]
        share = (top["total_spend"] / total_spend * 100) if total_spend > 0 else 0
        insights.append({
            "title": f"{top['category']} is your top category",
            "description": f"You spent {_fmt(top['total_spend'])} on {top['category']}, which makes up {share:.0f}% of your total spending across {top['transaction_count']} transactions.",
            "type": "info",
        })

    # 2. Category concentration warning
    if cats and total_spend > 0:
        top_share = cats[0]["total_spend"] / total_spend
        if top_share > 0.4:
            insights.append({
                "title": f"High concentration in {cats[0]['category']}",
                "description": f"{cats[0]['category']} accounts for {top_share * 100:.0f}% of your spending. Consider diversifying or reviewing if all transactions here are necessary.",
                "type": "warning",
            })

    # 3. Highest spending month
    if trends:
        peak = max(trends, key=lambda t: t["total_spend"])
        insights.append({
            "title": f"Peak spending in {peak['month_label']}",
            "description": f"Your highest spending month was {peak['month_label']} at {_fmt(peak['total_spend'])} across {peak['transaction_count']} transactions.",
            "type": "info",
        })

    # 4. Top merchant
    if merchants:
        top_m = merchants[0]
        insights.append({
            "title": f"{top_m['merchant_name']} is your top merchant",
            "description": f"You spent {_fmt(top_m['total_spend'])} at {top_m['merchant_name']} ({top_m['category']}) over {top_m['transaction_count']} transactions.",
            "type": "info",
        })

    # 5. Discretionary spending check
    disc_spend = sum(c["total_spend"] for c in cats if c["category"] in DISCRETIONARY)
    if disc_spend > 0 and total_spend > 0:
        disc_pct = disc_spend / total_spend * 100
        if disc_pct > 30:
            insights.append({
                "title": f"Discretionary spending at {disc_pct:.0f}%",
                "description": f"You're spending {_fmt(disc_spend)} ({disc_pct:.0f}%) on Food, Shopping, Entertainment and Personal Care. Keeping this under 30% can help build savings.",
                "type": "tip",
            })

    return {"status": "success", "insights": insights}


# ── Savings Recommendations ─────────────────────────────────────────────

def get_savings_insights(db: Session) -> dict:
    cats = get_category_breakdown(db)
    merchants = get_top_merchants(db)
    trends = get_monthly_trends(db)
    s = get_summary(db)

    total_spend = s["total_completed_spend_excluding_self_transfers"]
    active_months = len([t for t in trends if t["total_spend"] > 0]) or 1
    recs = []

    # Build category lookup
    cat_map = {c["category"]: c for c in cats}

    # 1. Food & Dining
    food = cat_map.get("Food & Dining")
    if food and food["total_spend"] > 0:
        monthly_food = food["total_spend"] / active_months
        save_pct = 0.15
        recs.append({
            "title": "Reduce dining out",
            "description": f"You spend ~{_fmt(monthly_food)}/month on Food & Dining. Cooking at home 2-3 more times a week could cut this by 15%.",
            "potential_savings": f"~{_fmt(monthly_food * save_pct)}/month",
            "priority": "high" if monthly_food > 2000 else "medium",
        })

    # 2. Shopping
    shopping = cat_map.get("Shopping")
    if shopping and shopping["total_spend"] > 0:
        monthly_shop = shopping["total_spend"] / active_months
        recs.append({
            "title": "Review shopping spending",
            "description": f"You're spending ~{_fmt(monthly_shop)}/month on Shopping. Try a 24-hour wait rule before non-essential purchases.",
            "potential_savings": f"~{_fmt(monthly_shop * 0.20)}/month",
            "priority": "high" if monthly_shop > 3000 else "medium",
        })

    # 3. Entertainment
    ent = cat_map.get("Entertainment")
    if ent and ent["total_spend"] > 0:
        monthly_ent = ent["total_spend"] / active_months
        recs.append({
            "title": "Audit subscriptions",
            "description": f"You've spent {_fmt(ent['total_spend'])} on Entertainment. Review active subscriptions — cancel any you don't use weekly.",
            "potential_savings": f"~{_fmt(monthly_ent * 0.30)}/month",
            "priority": "medium",
        })

    # 4. Top merchant over-reliance
    if merchants:
        top_m = merchants[0]
        if total_spend > 0 and top_m["total_spend"] / total_spend > 0.10:
            recs.append({
                "title": f"Diversify from {top_m['merchant_name']}",
                "description": f"{top_m['merchant_name']} accounts for {_fmt(top_m['total_spend'])} ({top_m['total_spend'] / total_spend * 100:.0f}% of total). Compare prices at alternatives.",
                "potential_savings": f"~{_fmt(top_m['total_spend'] * 0.10)}/month",
                "priority": "low",
            })

    # 5. Transportation
    transport = cat_map.get("Transportation")
    if transport and transport["total_spend"] > 0:
        monthly_t = transport["total_spend"] / active_months
        if monthly_t > 1000:
            recs.append({
                "title": "Optimize transportation costs",
                "description": f"You're spending ~{_fmt(monthly_t)}/month on transport. Consider carpooling, public transit, or booking rides in advance for better rates.",
                "potential_savings": f"~{_fmt(monthly_t * 0.15)}/month",
                "priority": "medium",
            })

    if not recs:
        recs.append({
            "title": "Great job!",
            "description": "Your spending looks well-managed. Keep tracking your expenses to maintain healthy habits.",
            "potential_savings": "N/A",
            "priority": "low",
        })

    return {"status": "success", "recommendations": recs}
