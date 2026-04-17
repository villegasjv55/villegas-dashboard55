"""
analytics.py - Core business logic and KPI calculations
Insurance Sales Performance Dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load and preprocess the sales CSV."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    df["commission_earned"] = df["premium_amount"] * df["commission_rate"]
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["week"] = df["date"].dt.to_period("W").astype(str)
    df["contacted"] = 1  # Every lead was at minimum contacted
    return df


def apply_filters(
    df: pd.DataFrame,
    date_range: tuple,
    agents: list,
    products: list,
    sources: list,
    regions: list,
) -> pd.DataFrame:
    """Apply sidebar filters to the dataframe."""
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    mask = (df["date"] >= start) & (df["date"] <= end)
    if agents:
        mask &= df["agent_name"].isin(agents)
    if products:
        mask &= df["product_type"].isin(products)
    if sources:
        mask &= df["lead_source"].isin(sources)
    if regions:
        mask &= df["region"].isin(regions)
    return df[mask].copy()


# ─────────────────────────────────────────────
# EXECUTIVE KPIs
# ─────────────────────────────────────────────

def calc_kpis(df: pd.DataFrame, prev_df: pd.DataFrame = None) -> dict:
    """Return the headline KPI dictionary."""
    total_leads = len(df)
    quotes_sent = df["quote_sent"].sum()
    policies_sold = df["policy_sold"].sum()
    close_rate = (policies_sold / total_leads * 100) if total_leads else 0
    total_premium = df.loc[df["policy_sold"] == 1, "premium_amount"].sum()
    total_commission = df.loc[df["policy_sold"] == 1, "commission_earned"].sum()

    # Top agent by policies sold
    if not df.empty:
        top_agent = (
            df[df["policy_sold"] == 1]
            .groupby("agent_name")["policy_sold"]
            .sum()
            .idxmax()
            if policies_sold > 0
            else "N/A"
        )
    else:
        top_agent = "N/A"

    # Month-over-month growth in premium
    monthly_growth = 0.0
    if prev_df is not None and not prev_df.empty:
        prev_premium = prev_df.loc[prev_df["policy_sold"] == 1, "premium_amount"].sum()
        if prev_premium > 0:
            monthly_growth = ((total_premium - prev_premium) / prev_premium) * 100

    return {
        "total_leads": int(total_leads),
        "quotes_sent": int(quotes_sent),
        "policies_sold": int(policies_sold),
        "close_rate": round(close_rate, 1),
        "total_premium": round(total_premium, 2),
        "total_commission": round(total_commission, 2),
        "top_agent": top_agent,
        "monthly_growth": round(monthly_growth, 1),
    }


# ─────────────────────────────────────────────
# AGENT PERFORMANCE TABLE
# ─────────────────────────────────────────────

def agent_performance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-agent metrics."""
    grp = df.groupby("agent_name")

    tbl = pd.DataFrame({
        "Leads": grp.size(),
        "Calls": grp["calls_made"].sum(),
        "Quotes": grp["quote_sent"].sum(),
        "Policies Sold": grp["policy_sold"].sum(),
        "Premium Volume ($)": grp.apply(
            lambda x: x.loc[x["policy_sold"] == 1, "premium_amount"].sum()
        ),
        "Commission Earned ($)": grp.apply(
            lambda x: x.loc[x["policy_sold"] == 1, "commission_earned"].sum()
        ),
    }).reset_index().rename(columns={"agent_name": "Agent"})

    tbl["Close Rate (%)"] = (
        (tbl["Policies Sold"] / tbl["Leads"]) * 100
    ).round(1)

    tbl["Premium Volume ($)"] = tbl["Premium Volume ($)"].round(2)
    tbl["Commission Earned ($)"] = tbl["Commission Earned ($)"].round(2)

    return tbl[[
        "Agent", "Leads", "Calls", "Quotes",
        "Policies Sold", "Close Rate (%)",
        "Premium Volume ($)", "Commission Earned ($)",
    ]]


# ─────────────────────────────────────────────
# FUNNEL DATA
# ─────────────────────────────────────────────

def funnel_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return funnel stage counts and conversion rates."""
    total = len(df)
    contacted = int(df["contacted"].sum())
    quoted = int(df["quote_sent"].sum())
    sold = int(df["policy_sold"].sum())

    stages = ["Leads", "Contacted", "Quote Sent", "Sold"]
    counts = [total, contacted, quoted, sold]

    conv = []
    for i, c in enumerate(counts):
        if i == 0:
            conv.append(100.0)
        else:
            prev = counts[i - 1]
            conv.append(round((c / prev * 100), 1) if prev else 0)

    return pd.DataFrame({"Stage": stages, "Count": counts, "Conv %": conv})


# ─────────────────────────────────────────────
# CHART DATA HELPERS
# ─────────────────────────────────────────────

def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    sold = df[df["policy_sold"] == 1].copy()
    return (
        sold.groupby("month")
        .agg(Policies=("policy_sold", "sum"), Premium=("premium_amount", "sum"))
        .reset_index()
        .rename(columns={"month": "Month"})
    )


def premium_by_agent(df: pd.DataFrame) -> pd.DataFrame:
    sold = df[df["policy_sold"] == 1]
    return (
        sold.groupby("agent_name")["premium_amount"]
        .sum()
        .reset_index()
        .rename(columns={"agent_name": "Agent", "premium_amount": "Premium"})
        .sort_values("Premium", ascending=False)
    )


def commission_by_month(df: pd.DataFrame) -> pd.DataFrame:
    sold = df[df["policy_sold"] == 1].copy()
    return (
        sold.groupby("month")["commission_earned"]
        .sum()
        .reset_index()
        .rename(columns={"month": "Month", "commission_earned": "Commission"})
    )


def close_rate_by_agent(df: pd.DataFrame) -> pd.DataFrame:
    grp = df.groupby("agent_name")
    tbl = pd.DataFrame({
        "Agent": grp.size().index,
        "Leads": grp.size().values,
        "Sold": grp["policy_sold"].sum().values,
    })
    tbl["Close Rate"] = (tbl["Sold"] / tbl["Leads"] * 100).round(1)
    return tbl.sort_values("Close Rate", ascending=False)


def lead_source_performance(df: pd.DataFrame) -> pd.DataFrame:
    grp = df.groupby("lead_source")
    tbl = pd.DataFrame({
        "Source": grp.size().index,
        "Leads": grp.size().values,
        "Sold": grp["policy_sold"].sum().values,
        "Premium": df[df["policy_sold"] == 1]
        .groupby("lead_source")["premium_amount"]
        .sum()
        .reindex(grp.size().index, fill_value=0)
        .values,
    })
    tbl["Conv %"] = (tbl["Sold"] / tbl["Leads"] * 100).round(1)
    return tbl.sort_values("Premium", ascending=False)


def daily_activity(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("date")
        .agg(
            Leads=("date", "count"),
            Calls=("calls_made", "sum"),
            Quotes=("quote_sent", "sum"),
            Sold=("policy_sold", "sum"),
        )
        .reset_index()
        .rename(columns={"date": "Date"})
    )


# ─────────────────────────────────────────────
# INSIGHT ENGINE
# ─────────────────────────────────────────────

def generate_insights(df: pd.DataFrame) -> list[str]:
    """Auto-generate bullet-point insights from the filtered data."""
    insights = []
    if df.empty:
        return ["⚠️ No data available for the selected filters."]

    sold = df[df["policy_sold"] == 1]

    # 1. Top converting agent this period
    agent_cr = close_rate_by_agent(df)
    if not agent_cr.empty:
        top = agent_cr.iloc[0]
        insights.append(
            f"🏆 **{top['Agent']}** leads all agents with a **{top['Close Rate']}%** close rate this period."
        )

    # 2. Best lead source vs second-best
    src = lead_source_performance(df)
    if len(src) >= 2:
        best = src.iloc[0]
        second = src.iloc[1]
        diff = round(best["Conv %"] - second["Conv %"], 1)
        if diff > 0:
            insights.append(
                f"📣 **{best['Source']}** leads convert **{diff}%** higher than {second['Source']} leads ({best['Conv %']}% vs {second['Conv %']}%)."
            )

    # 3. Top product by revenue
    if not sold.empty:
        prod_rev = sold.groupby("product_type")["premium_amount"].sum()
        top_prod = prod_rev.idxmax()
        share = round(prod_rev[top_prod] / prod_rev.sum() * 100, 1)
        insights.append(
            f"📋 **{top_prod}** insurance drives **{share}%** of total premium revenue."
        )

    # 4. Underperforming region
    region_cr = (
        df.groupby("region")
        .apply(lambda x: x["policy_sold"].sum() / len(x) * 100)
        .reset_index()
    )
    region_cr.columns = ["Region", "Close Rate"]
    overall_cr = sold.shape[0] / df.shape[0] * 100 if df.shape[0] > 0 else 0
    under = region_cr[region_cr["Close Rate"] < overall_cr]
    if not under.empty:
        worst = under.sort_values("Close Rate").iloc[0]
        gap = round(overall_cr - worst["Close Rate"], 1)
        insights.append(
            f"⚠️ **{worst['Region']}** region is **{gap}%** below the overall close rate target."
        )

    # 5. Overall close rate
    cr = round(sold.shape[0] / df.shape[0] * 100, 1) if df.shape[0] > 0 else 0
    insights.append(
        f"📊 Overall close rate is **{cr}%** across **{df.shape[0]}** total leads."
    )

    # 6. Avg premium
    if not sold.empty:
        avg_p = round(sold["premium_amount"].mean(), 2)
        insights.append(
            f"💰 Average policy premium is **${avg_p:,.2f}** for sold policies this period."
        )

    return insights
