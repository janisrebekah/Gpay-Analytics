
# GPay Analytics

A full-stack expense analytics dashboard that parses Google Pay transaction data from Google Takeout HTML files, classifies transactions by category, and generates actionable spending insights.

## Features

- **Upload & Parse** — drag-and-drop Google Takeout `My Activity.html` files
- **Smart Classification** — 100+ rule-based keyword patterns assign spending categories (Food, Shopping, Education, etc.)
- **Analytics Dashboard** — summary cards, category breakdown (donut chart), monthly trends (bar chart), top merchants
- **Smart Insights** — deterministic spending analysis with summary highlights, monthly trends, and savings recommendations
- **Duplicate-safe** — re-uploading the same file won't create duplicate records

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python, FastAPI, SQLAlchemy, SQLite |
| Frontend | React, Vite, Tailwind CSS, Recharts, Lucide Icons |

## Project Structure

```
gpay/
├── backend/
│   ├── app/
│   │   ├── core/           # Config & settings
│   │   ├── db/             # Database session & engine
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API endpoints (takeout, analytics, insights)
│   │   ├── schemas/        # Pydantic response models
│   │   └── services/       # Business logic
│   │       ├── extractor.py      # HTML block extraction
│   │       ├── parser.py         # Regex-based transaction parsing
│   │       ├── normalizer.py     # Date/amount normalization
│   │       ├── classifier.py     # Rule-based category classification
│   │       ├── analytics.py      # Spending analytics queries
│   │       ├── rule_insights.py  # Deterministic insights engine
│   │       └── crud.py           # Database operations
│   └── requirements.txt
└── frontend/
    └── src/
        ├── api/            # API client & service layers
        ├── components/     # Reusable UI components
        ├── pages/          # Upload & Dashboard pages
        └── utils/          # Formatting helpers
```
<img width="1919" height="906" alt="Screenshot 2026-04-11 023611" src="https://github.com/user-attachments/assets/2e8064b4-c401-490f-9582-7000a98cbee5" />
<img width="1919" height="962" alt="Screenshot 2026-04-11 023658" src="https://github.com/user-attachments/assets/7a9d60e2-28de-4725-a2a9-f6f6503e2937" />
<img width="1910" height="831" alt="Screenshot 2026-04-11 023813" src="https://github.com/user-attachments/assets/bdaee5ca-08c3-4f20-adf0-efa7721304fa" />


## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000` — Swagger docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at `http://localhost:5173`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload-html` | Upload & parse Google Takeout HTML |
| GET | `/analytics/summary` | Transaction summary stats |
| GET | `/analytics/category-breakdown` | Spending by category |
| GET | `/analytics/monthly-trends` | Monthly spending trends |
| GET | `/analytics/top-merchants` | Top 10 merchants by spend |
| GET | `/insights/summary` | Spending overview & highlights |
| GET | `/insights/monthly` | Monthly spending insights |
| GET | `/insights/savings` | Savings recommendations |

## How It Works

1. **Upload** your Google Takeout `My Activity.html` file
2. The backend **extracts** transaction blocks using regex
3. Each block is **parsed** for amount, date, merchant, and status
4. Transactions are **normalized** (dates, amounts) and **classified** into spending categories
5. Data is stored in **SQLite** with duplicate detection
6. The dashboard **visualizes** your spending patterns
7. **Smart Insights** analyze your data and surface actionable recommendations

## License

MIT
