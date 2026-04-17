# 🛡️ Insurance Sales Performance Dashboard

A professional, interactive web dashboard built with **Streamlit**, **Plotly**, and **pandas** for insurance agencies to track leads, quotes, closes, commissions, and agent performance.

---

## 📸 Features

| Feature | Description |
|---|---|
| **Executive KPIs** | Total leads, quotes, close rate, premium, commissions, top agent, growth % |
| **Agent Table** | Sortable/filterable performance table with export |
| **Sales Charts** | 6 interactive Plotly charts |
| **Funnel View** | Visual conversion funnel with stage metrics |
| **Insight Engine** | Auto-generated text insights from your data |
| **Commission Calculator** | Override commission rate and recalculate instantly |
| **Data Explorer** | Search, filter, export to CSV & Excel, add records |
| **Sidebar Filters** | Date range, agent, product, source, region |

---

## 🗂️ File Structure

```
insurance_dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/
│   └── sample_sales.csv      # Sample dataset (130 records)
└── modules/
    ├── __init__.py
    ├── analytics.py          # KPI calculations & insight engine
    ├── charts.py             # All Plotly chart factories
    └── database.py           # SQLite/PostgreSQL persistence layer
```

---

## 🚀 Quick Start (Run Locally)

### Prerequisites
- Python 3.10 or higher
- Git

### Step 1 — Clone or download the project

```bash
git clone https://github.com/YOUR_USERNAME/insurance-dashboard.git
cd insurance-dashboard
```

### Step 2 — Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the app

```bash
streamlit run app.py
```

The dashboard will open automatically at **http://localhost:8501**

---

## 📊 Using Your Own Data

Upload any CSV via the sidebar **Upload Sales CSV** button. Your CSV must include these columns:

| Column | Type | Example |
|---|---|---|
| `date` | YYYY-MM-DD | 2024-03-15 |
| `agent_name` | string | Sarah Mitchell |
| `lead_source` | string | Facebook, Google, Referral, Direct |
| `product_type` | string | Auto, Home, Life |
| `lead_status` | string | Sold, Quoted, Lost |
| `premium_amount` | float | 1850.00 |
| `commission_rate` | float (0–1) | 0.12 |
| `region` | string | North, South, East, West |
| `calls_made` | int | 3 |
| `quote_sent` | int (0/1) | 1 |
| `policy_sold` | int (0/1) | 1 |

---

## ☁️ Deploy to Streamlit Cloud (Free)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Insurance Sales Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/insurance-dashboard.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository and set:
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

Your app will be live at:
`https://YOUR_USERNAME-insurance-dashboard-app-XXXXX.streamlit.app`

---

## 🐘 Optional: PostgreSQL Backend

To switch from SQLite to PostgreSQL, use the database module:

```python
from modules.database import get_engine, csv_to_db, read_from_db

# Connect to PostgreSQL
engine = get_engine("postgresql://user:password@host:5432/dbname")

# Load CSV into database
csv_to_db("data/sample_sales.csv", engine=engine)

# Read back as DataFrame
df = read_from_db(engine=engine)
```

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** — Web framework
- **[Plotly](https://plotly.com)** — Interactive charts
- **[pandas](https://pandas.pydata.org)** — Data manipulation
- **[SQLAlchemy](https://sqlalchemy.org)** — Database ORM
- **[SQLite](https://sqlite.org)** — Default local database
- **[openpyxl](https://openpyxl.readthedocs.io)** — Excel export

---

## 📄 License

MIT License — free for personal and commercial use.

---

*Built with ❤️ for insurance sales teams*
