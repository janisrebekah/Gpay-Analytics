# GPay Analytics — Frontend

React dashboard for the GPay Analytics project.

## Setup

```bash
npm install
npm run dev
```

Runs at `http://localhost:5173`. Requires the backend running on `http://localhost:8000`.

## Environment

Create a `.env` file:

```
VITE_API_BASE_URL=http://localhost:8000
```

## Pages

- **Upload** — drag-and-drop HTML file upload with summary
- **Dashboard** — stats cards, category chart, monthly trends, top merchants, smart insights

## Components

| Component | Purpose |
|-----------|---------|
| `StatCard` | Metric card with icon and subtitle |
| `CategoryChart` | Donut chart for category breakdown |
| `MonthlyChart` | Bar chart for monthly trends |
| `TopMerchants` | Ranked merchant table |
| `InsightsPanel` | Tabbed insights (Summary / Monthly / Savings) |
| `Navbar` | Navigation header |

## Built With

React, Vite, Tailwind CSS, Recharts, Lucide React
