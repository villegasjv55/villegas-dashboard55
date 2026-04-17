# Villegas Dashboard

So I've been wanting to dig into insurance sales data for a while now. Always been curious about how leads actually convert, which agents are closing, where the money is coming from — that kind of stuff. Finally just built something to actually look at it properly instead of staring at spreadsheets.

This is a sales performance dashboard for insurance agencies. Built it with Python, Streamlit and Plotly. You can track leads, quotes, closed deals, commissions, agent performance — all in one place with actual charts that are interactive and filters that work.

---

## What it does

- **KPI overview** — total leads, close rate, premium volume, commissions, top agent, month over month growth all on one screen
- **Agent table** — see every agent's numbers side by side, sortable by whatever column you want
- **Charts** — monthly sales, premium by agent, commission trends, close rate comparisons, lead source breakdown, daily activity
- **Sales funnel** — shows you exactly where leads are dropping off between stages
- **Insight engine** — auto generates observations from your data like which agent is converting best or which region is underperforming
- **Commission calculator** — slide to any commission rate and it recalculates everything instantly
- **Data tab** — search through raw records, add new entries, export to CSV or Excel

---

## Running it locally

You need Python 3.10+ installed.

```bash
git clone https://github.com/villegasjv55/villegas-dashboard55.git
cd villegas-dashboard55
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501

---

## Using your own data

Hit the Upload CSV button in the sidebar. Your file needs these columns:

```
date, agent_name, lead_source, product_type, lead_status,
premium_amount, commission_rate, region, calls_made, quote_sent, policy_sold
```

There's a sample CSV in the data folder if you want to see the format.

---

## Stack

Python, Streamlit, Plotly, pandas, SQLAlchemy, SQLite, openpyxl

---

Built this mostly to learn more about how insurance sales pipelines actually work and what the numbers look like at an agency level. Ended up being a pretty solid tool.
