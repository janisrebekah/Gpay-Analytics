from typing import Dict, List, Tuple

# Centralized category list
class Categories:
    FOOD_DINING = "Food & Dining"
    GROCERIES = "Groceries"
    TRANSPORTATION = "Transportation"
    SHOPPING = "Shopping"
    BILLS_UTILITIES = "Bills & Utilities"
    ENTERTAINMENT = "Entertainment"
    HEALTH_FITNESS = "Health & Fitness"
    EDUCATION = "Education"
    PERSONAL_CARE = "Personal Care"
    TRAVEL_ACCOMMODATION = "Travel & Accommodation"
    INVESTMENTS_SAVINGS = "Investments & Savings"
    OTHER = "Other"

# Ordered list of rules: (Category, [keywords])
# First-match-wins logic — order matters!
# More specific patterns MUST come before general ones.
CATEGORY_RULES: List[Tuple[str, List[str]]] = [

    # ── Explicit overrides (most specific first) ────────────────────────
    (Categories.OTHER, ["google cloud"]),
    (Categories.SHOPPING, ["amazon seller services"]),

    # ── Entertainment (before generic "amazon" in Shopping) ─────────────
    (Categories.ENTERTAINMENT, [
        "amazon prime", "netflix", "spotify", "hotstar", "disney",
        "cinema", "movie", "google play", "youtube premium",
    ]),

    # ── Education ───────────────────────────────────────────────────────
    (Categories.EDUCATION, [
        "institute", "educational", "cit", "chennai institute of technology",
        "college", "iit", "school", "university", "academy",
        "udemy", "nptel", "coursera", "xerox", "student",
        "gate",
    ]),

    # ── Health & Fitness ───────────────────────────────────────────────
    (Categories.HEALTH_FITNESS, [
        "apollo pharmacy", "pharmacy", "hospital", "clinic",
        "health", "fitness", "gym", "medical", "medicals",
    ]),

    # ── Bills & Utilities ──────────────────────────────────────────────
    (Categories.BILLS_UTILITIES, [
        "airtel", "jio", "vi ", "bsnl", "electricity",
        "broadband", "dth", "recharge", "bescom", "tneb",
        "bharti airtel", "payments bank", "prepaid",
        "phonepe", "amazon pay",
        "eb015",
    ]),

    # ── Food & Dining (before Groceries — "sweet", "bakery" match here) 
    (Categories.FOOD_DINING, [
        "swiggy", "zomato", "restaurant", "cafe", "bakery",
        "sweet", "food", "kitchen", "eatery", "pizza",
        "burger", "kfc", "dominos", "domino", "cater",
        "transit cafe",
    ]),

    # ── Groceries ──────────────────────────────────────────────────────
    (Categories.GROCERIES, [
        "supermarket", "super market", "mart", "grocery",
        "fresh", "reliance smart", "dmart", "spencers",
        "bigbasket", "zepto", "blinkit", "bazzar",
        "vendolite",
    ]),

    # ── Transportation ─────────────────────────────────────────────────
    (Categories.TRANSPORTATION, [
        "uber", "ola", "rapido", "namma yatri",
        "irctc", "uts", "indian railways", "metro",
        "transport", "petrol", "fuel",
    ]),

    # ── Shopping ───────────────────────────────────────────────────────
    (Categories.SHOPPING, [
        "amazon", "flipkart", "ekart", "myntra", "ajio", "meesho",
        "zudio", "trent limited", "reliance trends", "trends",
        "max", "max retail", "lifestyle", "life style", "naidu hall",
        "mall", "store", "clothing", "fashion", "readymade",
        "cutpiece", "beauty", "fae beauty", "heels",
        "enterprises", "traders",
        "shopping singappore",
    ]),

    # ── Personal Care ──────────────────────────────────────────────────
    (Categories.PERSONAL_CARE, [
        "salon", "spa", "hair", "cosmetics",
    ]),

    # ── Travel & Accommodation ─────────────────────────────────────────
    (Categories.TRAVEL_ACCOMMODATION, [
        "makemytrip", "goibibo", "agoda",
        "hotel", "resort", "oyo", "flight", "airlines",
    ]),

    # ── Investments & Savings ──────────────────────────────────────────
    (Categories.INVESTMENTS_SAVINGS, [
        "zerodha", "groww", "upstox",
        "mutual fund", "stocks", "fixed deposit",
    ]),
]


def determine_category(name: str, raw_text: str, transaction_type: str) -> str:
    """
    Determines the spending category based on the transaction name
    and raw text using deterministic rules.
    """
    name_low = name.lower()
    raw_low = raw_text.lower()

    # Ordered rule scan — first match wins
    for category, keywords in CATEGORY_RULES:
        if any(kw in name_low or kw in raw_low for kw in keywords):
            return category

    # Default fallbacks for specific structural types
    if transaction_type == "Self Transfer":
        return Categories.OTHER

    if transaction_type == "P2P Payment":
        return Categories.OTHER

    # Default fallback
    return Categories.OTHER
