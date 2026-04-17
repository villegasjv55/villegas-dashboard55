"""
app.py  –  Insurance Sales Performance Dashboard
A professional Streamlit web application for insurance agencies.
"""

import sys
from pathlib import Path

# Make sure local modules are importable
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import io

from modules.analytics import (
    load_data, apply_filters, calc_kpis,
    agent_performance_table, funnel_data,
    monthly_sales, premium_by_agent, commission_by_month,
    close_rate_by_agent, lead_source_performance, daily_activity,
    generate_insights,
)
from modules.charts import (
    chart_monthly_sales, chart_premium_by_agent,
    chart_commission_by_month, chart_close_rate_by_agent,
    chart_lead_source, chart_daily_activity, chart_funnel,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Villegas Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp {
    background: #E8EAED;
}

/* ── Top header bar ── */
.dashboard-header {
    background: linear-gradient(135deg, #0D1B2A 0%, #1565C0 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.dashboard-header h1 {
    font-family: 'DM Serif Display', serif;
    color: white;
    font-size: 2rem;
    margin: 0;
    letter-spacing: 0.5px;
}
.dashboard-header p {
    color: rgba(255,255,255,0.75);
    margin: 4px 0 0;
    font-size: 0.9rem;
}
.header-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    font-size: 0.85rem;
    font-weight: 500;
}

/* ── KPI cards ── */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 22px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 5px solid #1565C0;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.10);
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #78909C;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0D1B2A;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    font-size: 0.8rem;
    color: #43A047;
    font-weight: 500;
}
.kpi-sub.down { color: #E53935; }

/* ── Section headers ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #0D1B2A;
    border-bottom: 2px solid #1565C0;
    padding-bottom: 8px;
    margin: 28px 0 18px;
}

/* ── Chart cards ── */
.chart-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* ── Insight pills ── */
.insight-pill {
    background: white;
    border-left: 4px solid #1565C0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    font-size: 0.92rem;
    color: #1A1A2E;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0D1B2A !important;
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.85) !important;
}
[data-testid="stSidebar"] .stMultiSelect span {
    color: #0D1B2A !important;
}

/* ── Dataframe ── */
.dataframe-container {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* ── Calculator card ── */
.calc-card {
    background: linear-gradient(135deg, #E3F2FD 0%, #ffffff 100%);
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #BBDEFB;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: white;
    border-radius: 10px;
    padding: 6px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: #1565C0 !important;
    color: white !important;
}

button[kind="primary"] {
    background: #1565C0 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING  (cached)
# ─────────────────────────────────────────────

DEFAULT_CSV = Path(__file__).parent / "data" / "sample_sales.csv"

@st.cache_data
def get_data(filepath: str) -> pd.DataFrame:
    return load_data(filepath)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🛡️ Dashboard Controls")
    st.markdown("---")

    # ── File upload ──
    uploaded = st.file_uploader(
        "Upload Sales CSV", type=["csv"],
        help="CSV must match the required schema."
    )
    if uploaded:
        tmp_path = Path("/tmp/uploaded_sales.csv")
        tmp_path.write_bytes(uploaded.read())
        csv_path = str(tmp_path)
    else:
        csv_path = str(DEFAULT_CSV)

    raw_df = get_data(csv_path)

    st.markdown("### 📅 Date Range")
    min_d = raw_df["date"].min().date()
    max_d = raw_df["date"].max().date()
    date_start = st.date_input("From", min_d, min_value=min_d, max_value=max_d)
    date_end   = st.date_input("To",   max_d, min_value=min_d, max_value=max_d)

    st.markdown("### 👤 Agents")
    all_agents = sorted(raw_df["agent_name"].unique())
    sel_agents = st.multiselect("Select agents", all_agents, default=[])

    st.markdown("### 📦 Product Type")
    all_prods = sorted(raw_df["product_type"].unique())
    sel_prods = st.multiselect("Select products", all_prods, default=[])

    st.markdown("### 📢 Lead Source")
    all_sources = sorted(raw_df["lead_source"].unique())
    sel_sources = st.multiselect("Select sources", all_sources, default=[])

    st.markdown("### 🗺️ Region")
    all_regions = sorted(raw_df["region"].unique())
    sel_regions = st.multiselect("Select regions", all_regions, default=[])

    st.markdown("---")
    st.caption("Insurance Sales Dashboard v1.0")


# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────

df = apply_filters(
    raw_df,
    date_range=(date_start, date_end),
    agents=sel_agents,
    products=sel_prods,
    sources=sel_sources,
    regions=sel_regions,
)

# Previous period (same duration, shifted back) for MoM growth
delta = (pd.Timestamp(date_end) - pd.Timestamp(date_start))
prev_start = pd.Timestamp(date_start) - delta - timedelta(days=1)
prev_end   = pd.Timestamp(date_start) - timedelta(days=1)
prev_df = raw_df[(raw_df["date"] >= prev_start) & (raw_df["date"] <= prev_end)]


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

today_str = date.today().strftime("%B %d, %Y")
st.markdown(f"""
<div class="dashboard-header">
  <div>
    <h1>🛡️ Villegas Dashboard</h1>
    <p>Insurance Sales Performance — Real-time analytics for leads, quotes, policies & commissions</p>
  </div>
  <div class="header-badge">📅 {today_str}</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tabs = st.tabs([
    "📊 Overview",
    "👥 Agent Performance",
    "📈 Charts",
    "🔻 Funnel",
    "💡 Insights",
    "🧮 Commission Calculator",
    "📥 Data",
])

kpis = calc_kpis(df, prev_df if not prev_df.empty else None)


# ══════════════════════════════════════════════
# TAB 1 – OVERVIEW
# ══════════════════════════════════════════════

with tabs[0]:
    st.markdown('<div class="section-title">Executive KPIs</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "Total Leads",      f"{kpis['total_leads']:,}",       "📋", "#1565C0"),
        (c2, "Quotes Sent",      f"{kpis['quotes_sent']:,}",        "📤", "#00ACC1"),
        (c3, "Policies Sold",    f"{kpis['policies_sold']:,}",      "✅", "#43A047"),
        (c4, "Close Rate",       f"{kpis['close_rate']}%",          "🎯", "#FFB300"),
    ]
    for col, label, val, icon, color in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:{color}">
                <div class="kpi-label">{icon} {label}</div>
                <div class="kpi-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    c5, c6, c7, c8 = st.columns(4)
    growth_cls = "down" if kpis['monthly_growth'] < 0 else ""
    growth_icon = "▼" if kpis['monthly_growth'] < 0 else "▲"
    cards2 = [
        (c5, "Total Premium",       f"${kpis['total_premium']:,.0f}",      "💵", "#1565C0"),
        (c6, "Est. Commissions",    f"${kpis['total_commission']:,.0f}",    "💰", "#00ACC1"),
        (c7, "Top Agent",           kpis['top_agent'],                      "🏆", "#FFB300"),
        (c8, "Period Growth",       f"{growth_icon} {abs(kpis['monthly_growth'])}%", "📈", "#43A047"),
    ]
    for col, label, val, icon, color in cards2:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:{color}">
                <div class="kpi-label">{icon} {label}</div>
                <div class="kpi-value" style="font-size:1.5rem">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(
            chart_monthly_sales(monthly_sales(df)),
            use_container_width=True,
            key="overview_monthly_sales"
        )
    with col_right:
        st.plotly_chart(
            chart_funnel(funnel_data(df)),
            use_container_width=True,
            key="overview_funnel"
        )


# ══════════════════════════════════════════════
# TAB 2 – AGENT PERFORMANCE
# ══════════════════════════════════════════════

with tabs[1]:
    st.markdown('<div class="section-title">Agent Performance Table</div>', unsafe_allow_html=True)

    agent_tbl = agent_performance_table(df)

    # Sort control
    sort_col = st.selectbox(
        "Sort by",
        options=agent_tbl.columns.tolist(),
        index=agent_tbl.columns.tolist().index("Close Rate (%)"),
    )
    sort_asc = st.radio("Order", ["Descending", "Ascending"], horizontal=True) == "Ascending"
    agent_tbl_sorted = agent_tbl.sort_values(sort_col, ascending=sort_asc)

    st.dataframe(
        agent_tbl_sorted.style
            .format({
                "Premium Volume ($)": "${:,.2f}",
                "Commission Earned ($)": "${:,.2f}",
                "Close Rate (%)": "{:.1f}%",
            }),
        use_container_width=True,
        height=320,
    )

    st.download_button(
        "⬇️ Export Agent Table (CSV)",
        data=agent_tbl_sorted.to_csv(index=False),
        file_name="agent_performance.csv",
        mime="text/csv",
    )


# ══════════════════════════════════════════════
# TAB 3 – CHARTS
# ══════════════════════════════════════════════

with tabs[2]:
    st.markdown('<div class="section-title">Interactive Charts</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(chart_premium_by_agent(premium_by_agent(df)), use_container_width=True, key="charts_premium_agent")
    with col2:
        st.plotly_chart(chart_commission_by_month(commission_by_month(df)), use_container_width=True, key="charts_commission_month")

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(chart_close_rate_by_agent(close_rate_by_agent(df)), use_container_width=True, key="charts_close_rate")
    with col4:
        st.plotly_chart(chart_lead_source(lead_source_performance(df)), use_container_width=True, key="charts_lead_source")

    st.plotly_chart(chart_daily_activity(daily_activity(df)), use_container_width=True, key="charts_daily_activity")


# ══════════════════════════════════════════════
# TAB 4 – FUNNEL
# ══════════════════════════════════════════════

with tabs[3]:
    st.markdown('<div class="section-title">Sales Conversion Funnel</div>', unsafe_allow_html=True)

    fdf = funnel_data(df)
    col_f, col_t = st.columns([2, 1])
    with col_f:
        st.plotly_chart(chart_funnel(fdf), use_container_width=True, key="funnel_tab_chart")
    with col_t:
        st.markdown("### Stage Breakdown")
        for _, row in fdf.iterrows():
            st.metric(
                label=row["Stage"],
                value=f"{int(row['Count']):,}",
                delta=f"{row['Conv %']}% from prev" if row["Stage"] != "Leads" else "100% — baseline",
            )


# ══════════════════════════════════════════════
# TAB 5 – INSIGHTS
# ══════════════════════════════════════════════

with tabs[4]:
    st.markdown('<div class="section-title">🤖 Auto-Generated Insights</div>', unsafe_allow_html=True)
    st.caption("Insights are auto-derived from your filtered dataset.")

    for insight in generate_insights(df):
        st.markdown(f'<div class="insight-pill">{insight}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Lead Source Deep-Dive")
    st.dataframe(
        lead_source_performance(df).style.format({
            "Premium": "${:,.0f}",
            "Conv %": "{:.1f}%",
        }),
        use_container_width=True,
    )


# ══════════════════════════════════════════════
# TAB 6 – COMMISSION CALCULATOR
# ══════════════════════════════════════════════

with tabs[5]:
    st.markdown('<div class="section-title">🧮 Commission Calculator</div>', unsafe_allow_html=True)
    st.markdown(
        "Override the commission rate and instantly recalculate earnings across all sold policies."
    )

    with st.container():
        st.markdown('<div class="calc-card">', unsafe_allow_html=True)

        col_rate, col_btn = st.columns([3, 1])
        with col_rate:
            override_rate = st.slider(
                "Custom Commission Rate (%)",
                min_value=1.0, max_value=30.0,
                value=12.0, step=0.5,
                format="%.1f%%",
            )
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            recalc = st.button("Recalculate", type="primary")

        override_rate_dec = override_rate / 100
        sold_df = df[df["policy_sold"] == 1].copy()
        sold_df["original_commission"] = sold_df["commission_earned"]
        sold_df["new_commission"] = sold_df["premium_amount"] * override_rate_dec
        sold_df["delta"] = sold_df["new_commission"] - sold_df["original_commission"]

        total_new  = sold_df["new_commission"].sum()
        total_orig = sold_df["original_commission"].sum()
        diff       = total_new - total_orig

        m1, m2, m3 = st.columns(3)
        m1.metric("Original Commission",   f"${total_orig:,.2f}")
        m2.metric("New Commission",         f"${total_new:,.2f}", delta=f"${diff:,.2f}")
        m3.metric("Rate Applied",           f"{override_rate:.1f}%")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Per-Agent Commission at New Rate")
    if not sold_df.empty:
        agent_recalc = (
            sold_df.groupby("agent_name")
            .agg(
                Policies=("policy_sold", "sum"),
                Original_Commission=("original_commission", "sum"),
                New_Commission=("new_commission", "sum"),
                Delta=("delta", "sum"),
            )
            .reset_index()
            .rename(columns={"agent_name": "Agent"})
        )
        st.dataframe(
            agent_recalc.style.format({
                "Original_Commission": "${:,.2f}",
                "New_Commission":      "${:,.2f}",
                "Delta":               "${:+,.2f}",
            }),
            use_container_width=True,
        )


# ══════════════════════════════════════════════
# TAB 7 – DATA
# ══════════════════════════════════════════════

with tabs[6]:
    st.markdown('<div class="section-title">📥 Raw Data Explorer</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search (agent, source, product…)", "")
    view_df = df.copy()
    if search:
        mask = view_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        view_df = view_df[mask]

    st.markdown(f"**{len(view_df):,} records** matching current filters")
    st.dataframe(view_df, use_container_width=True, height=450)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "⬇️ Export Filtered Data (CSV)",
            data=view_df.to_csv(index=False),
            file_name="filtered_sales.csv",
            mime="text/csv",
        )
    with col_dl2:
        # Excel export
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            view_df.to_excel(writer, index=False, sheet_name="Sales")
            agent_performance_table(df).to_excel(writer, index=False, sheet_name="Agents")
        st.download_button(
            "⬇️ Export to Excel (.xlsx)",
            data=buf.getvalue(),
            file_name="insurance_sales_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.markdown("---")
    st.markdown("#### 📤 Add a New Record")
    with st.expander("Expand to enter a new sale"):
        with st.form("new_record"):
            nc1, nc2, nc3 = st.columns(3)
            r_date    = nc1.date_input("Date", value=date.today())
            r_agent   = nc2.selectbox("Agent", all_agents)
            r_source  = nc3.selectbox("Lead Source", all_sources)

            nc4, nc5, nc6 = st.columns(3)
            r_product = nc4.selectbox("Product", all_prods)
            r_status  = nc5.selectbox("Status", ["Sold", "Quoted", "Lost"])
            r_region  = nc6.selectbox("Region", all_regions)

            nc7, nc8, nc9 = st.columns(3)
            r_premium = nc7.number_input("Premium ($)", min_value=0.0, value=1500.0, step=100.0)
            r_rate    = nc8.number_input("Commission Rate", min_value=0.0, max_value=1.0, value=0.12, step=0.01)
            r_calls   = nc9.number_input("Calls Made", min_value=0, value=3, step=1)

            submitted = st.form_submit_button("Add Record")
            if submitted:
                new_row = pd.DataFrame([{
                    "date": pd.Timestamp(r_date),
                    "agent_name": r_agent,
                    "lead_source": r_source,
                    "product_type": r_product,
                    "lead_status": r_status,
                    "premium_amount": r_premium,
                    "commission_rate": r_rate,
                    "region": r_region,
                    "calls_made": r_calls,
                    "quote_sent": 1 if r_status in ["Sold", "Quoted"] else 0,
                    "policy_sold": 1 if r_status == "Sold" else 0,
                }])
                new_row.to_csv(csv_path, mode="a", header=False, index=False)
                st.cache_data.clear()
                st.success("✅ Record added! Refresh the page to see updates.")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; color:#90A4AE; font-size:0.8rem; margin-top:40px; padding:20px; 
            border-top:1px solid #E0E0E0;">
    🛡️ Villegas Dashboard &nbsp;|&nbsp; 
    Built with Streamlit &amp; Plotly &nbsp;|&nbsp; 
    All data is for demonstration purposes
</div>
""", unsafe_allow_html=True)
