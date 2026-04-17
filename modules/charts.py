"""
charts.py - All Plotly chart factories
Insurance Sales Performance Dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Brand palette ──────────────────────────────────────────────────────────────
PALETTE = {
    "navy":       "#0D1B2A",
    "blue":       "#1565C0",
    "sky":        "#42A5F5",
    "teal":       "#00ACC1",
    "green":      "#43A047",
    "amber":      "#FFB300",
    "red":        "#E53935",
    "gray":       "#607D8B",
    "bg":         "#F4F6F9",
    "card":       "#FFFFFF",
    "text":       "#1A1A2E",
    "muted":      "#78909C",
}

AGENT_COLORS = px.colors.qualitative.Bold
LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=PALETTE["text"]),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
)


def _ax(fig, gridcolor="#E0E0E0"):
    fig.update_xaxes(showgrid=False, linecolor=gridcolor, tickfont=dict(size=12))
    fig.update_yaxes(gridcolor=gridcolor, linecolor="rgba(0,0,0,0)", tickfont=dict(size=12))
    return fig


# ─────────────────────────────────────────────
# 1. SALES BY MONTH
# ─────────────────────────────────────────────

def chart_monthly_sales(df_monthly: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_monthly["Month"], y=df_monthly["Premium"],
        name="Premium ($)", marker_color=PALETTE["blue"],
        opacity=0.9, yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=df_monthly["Month"], y=df_monthly["Policies"],
        name="Policies", mode="lines+markers",
        marker=dict(color=PALETTE["amber"], size=8),
        line=dict(width=2.5, color=PALETTE["amber"]),
        yaxis="y2",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Monthly Sales & Premium",
        yaxis=dict(title="Premium ($)", tickprefix="$"),
        yaxis2=dict(title="Policies Sold", overlaying="y", side="right", showgrid=False),
        barmode="group",
        hovermode="x unified",
    )
    return _ax(fig)


# ─────────────────────────────────────────────
# 2. PREMIUM BY AGENT
# ─────────────────────────────────────────────

def chart_premium_by_agent(df_agent: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_agent, x="Agent", y="Premium",
        color="Agent", color_discrete_sequence=AGENT_COLORS,
        text_auto=".2s",
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    fig.update_layout(
        **LAYOUT_BASE,
        title="Premium Volume by Agent",
        yaxis_tickprefix="$",
        showlegend=False,
    )
    return _ax(fig)


# ─────────────────────────────────────────────
# 3. COMMISSION BY MONTH
# ─────────────────────────────────────────────

def chart_commission_by_month(df_comm: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=df_comm["Month"], y=df_comm["Commission"],
        fill="tozeroy", fillcolor=f"rgba(21,101,192,0.15)",
        line=dict(color=PALETTE["blue"], width=2.5),
        mode="lines+markers",
        marker=dict(color=PALETTE["sky"], size=7),
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Monthly Commission Earned",
        yaxis_tickprefix="$",
        hovermode="x unified",
    )
    return _ax(fig)


# ─────────────────────────────────────────────
# 4. CLOSE RATE BY AGENT
# ─────────────────────────────────────────────

def chart_close_rate_by_agent(df_cr: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_cr.sort_values("Close Rate"),
        x="Close Rate", y="Agent",
        orientation="h",
        color="Close Rate",
        color_continuous_scale=["#E3F2FD", "#1565C0"],
        text="Close Rate",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        **LAYOUT_BASE,
        title="Close Rate by Agent (%)",
        xaxis_ticksuffix="%",
        coloraxis_showscale=False,
    )
    return _ax(fig)


# ─────────────────────────────────────────────
# 5. LEAD SOURCE PERFORMANCE
# ─────────────────────────────────────────────

def chart_lead_source(df_src: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_src["Source"], y=df_src["Leads"],
        name="Leads", marker_color=PALETTE["gray"], opacity=0.7,
    ))
    fig.add_trace(go.Bar(
        x=df_src["Source"], y=df_src["Sold"],
        name="Sold", marker_color=PALETTE["green"],
    ))
    fig.add_trace(go.Scatter(
        x=df_src["Source"], y=df_src["Conv %"],
        name="Conv %", mode="lines+markers",
        marker=dict(color=PALETTE["amber"], size=9),
        line=dict(width=2, dash="dot", color=PALETTE["amber"]),
        yaxis="y2",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Lead Source Performance",
        barmode="group",
        yaxis2=dict(title="Conversion %", overlaying="y", side="right",
                    showgrid=False, ticksuffix="%"),
        hovermode="x unified",
    )
    return _ax(fig)


# ─────────────────────────────────────────────
# 6. DAILY ACTIVITY TREND
# ─────────────────────────────────────────────

def chart_daily_activity(df_daily: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for col, color, dash in [
        ("Calls", PALETTE["gray"], "dash"),
        ("Quotes", PALETTE["sky"], "dot"),
        ("Sold", PALETTE["green"], "solid"),
    ]:
        fig.add_trace(go.Scatter(
            x=df_daily["Date"], y=df_daily[col],
            name=col, mode="lines",
            line=dict(width=2, color=color, dash=dash),
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Daily Activity Trend",
        hovermode="x unified",
    )
    return _ax(fig)


# ─────────────────────────────────────────────
# 7. FUNNEL
# ─────────────────────────────────────────────

def chart_funnel(df_funnel: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Funnel(
        y=df_funnel["Stage"],
        x=df_funnel["Count"],
        textinfo="value+percent initial",
        marker=dict(
            color=[PALETTE["blue"], PALETTE["sky"], PALETTE["teal"], PALETTE["green"]],
            line=dict(width=1.5, color="white"),
        ),
        connector=dict(line=dict(color="rgba(0,0,0,0.1)", width=1)),
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Sales Funnel",
    )
    return fig
