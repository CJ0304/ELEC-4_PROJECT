"""
pages/dashboard.py — Dashboard page for ServiSense
"""

from datetime import datetime

import streamlit as st
import plotly.express as px

from constants import PLOTLY_COLORS
from styles import plotly_layout
from ui_components import page_header


def render(rec_df, svc_df):
    office = st.session_state.assigned_office

    if office:
        page_header("📊", "Dashboard", f"Showing data for {office}")
        df = rec_df[rec_df["service_name"] == office].copy()
    else:
        page_header("📊", "Dashboard", "System-wide overview of all student services")
        df = rec_df.copy()

    if df.empty:
        st.info("📭 No service records available yet.")
        return

    # ── KPI calculations ──────────────────────────────────────────────────────
    df["month"]  = df["service_date"].dt.to_period("M").astype(str)
    this_month   = df[df["service_date"].dt.month == datetime.now().month]
    vc           = df["service_name"].value_counts()
    most_used    = vc.idxmax()
    least_used   = vc.idxmin()
    avg_daily    = df.groupby(df["service_date"].dt.date).size().mean()
    ph           = df.groupby("service_hour").size()
    peak_h       = f"{int(ph.idxmax()):02d}:00" if not ph.empty else "N/A"
    unique_stu   = df["student_id"].nunique()

    def kpi(label, value, sub="", small_val=False):
        val_class = "kpi-value-sm" if small_val else "kpi-value"
        return (
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="{val_class}">{value}</div>'
            + (f'<div class="kpi-sub">{sub}</div>' if sub else '')
            + '</div>'
        )

    # Row 1
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("Total Records",   f"{len(df):,}",       "All time"),      unsafe_allow_html=True)
    c2.markdown(kpi("Unique Students", f"{unique_stu:,}",    "Served"),        unsafe_allow_html=True)
    c3.markdown(kpi("This Month",      f"{len(this_month):,}","Records"),      unsafe_allow_html=True)
    c4.markdown(kpi("Peak Hour",       peak_h,               "Busiest time"),  unsafe_allow_html=True)

    # Row 2
    c5, c6, c7, c8 = st.columns(4)
    c5.markdown(kpi("Most Used",  most_used,  "Top service",  small_val=True), unsafe_allow_html=True)
    c6.markdown(kpi("Least Used", least_used, "Lowest usage", small_val=True), unsafe_allow_html=True)
    c7.markdown(kpi("Avg Daily",  f"{avg_daily:.1f}", "Records/day"),           unsafe_allow_html=True)
    c8.markdown(kpi("Services",   len(df["service_name"].unique()), "Active"),  unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    svc_cnt = df["service_name"].value_counts().reset_index()
    svc_cnt.columns = ["Service", "Count"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-card"><div class="chart-title">📊 Service Usage Distribution</div>',
                    unsafe_allow_html=True)
        fig = px.pie(svc_cnt, names="Service", values="Count",
                     color_discrete_sequence=PLOTLY_COLORS, hole=0.42)
        fig.update_traces(textinfo="percent+label", textfont_size=11,
                          hovertemplate="<b>%{label}</b><br>Usage: %{value}<extra></extra>")
        fig = plotly_layout(fig, height=290)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        pct = round(svc_cnt.iloc[0]["Count"] / svc_cnt["Count"].sum() * 100, 1)
        st.markdown(
            f"<div class='chart-insight'>💡 <b>{svc_cnt.iloc[0]['Service']}</b> leads with {pct}% of total usage.</div>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><div class="chart-title">📈 Service Comparison</div>',
                    unsafe_allow_html=True)
        fig2 = px.bar(svc_cnt.sort_values("Count"), x="Count", y="Service", orientation="h",
                      color="Count",
                      color_continuous_scale=[[0, "#1A3460"], [0.5, "#D4AF37"], [1, "#E8CC6A"]])
        fig2.update_traces(hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>")
        fig2 = plotly_layout(fig2, height=290)
        fig2.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            f"<div class='chart-insight'>💡 <b>{svc_cnt.iloc[-1]['Service']}</b> has the lowest utilization rate.</div>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card"><div class="chart-title">📅 Monthly Service Usage Trend</div>',
                unsafe_allow_html=True)
    monthly = df.groupby("month").size().reset_index(name="Count")
    fig3 = px.area(monthly, x="month", y="Count", color_discrete_sequence=["#D4AF37"])
    fig3.update_traces(
        hovertemplate="Month: %{x}<br>Records: %{y}<extra></extra>",
        line=dict(width=2.5),
        fillcolor="rgba(212,175,55,0.12)",
    )
    fig3 = plotly_layout(fig3, height=250)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    if len(monthly) >= 2:
        trend = "increasing 📈" if monthly["Count"].iloc[-1] > monthly["Count"].iloc[0] else "decreasing 📉"
        st.markdown(
            f"<div class='chart-insight'>💡 Service usage is <b>{trend}</b> over the tracked period.</div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
