"""
pages/analytics.py — Analytics page for ServiSense (Admin only)
"""

import streamlit as st
import plotly.express as px

from constants import PLOTLY_COLORS, DEPARTMENTS
from data import filter_df
from exports import export_pdf, export_excel
from styles import plotly_layout
from ui_components import page_header


def render(rec_df):
    page_header("📈", "Performance Analytics", "Admin view — Comprehensive service utilization insights")

    if rec_df.empty:
        st.info("No data available.")
        return

    df = rec_df.copy()
    df["month"]   = df["service_date"].dt.to_period("M").astype(str)
    df["weekday"] = df["service_date"].dt.day_name()

    # ── Filter / export panel ──────────────────────────────────────────────────
    with st.expander("🔍 Filter & Generate Report", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        asd  = c1.date_input("From", value=df["service_date"].min().date(), key="ana_sd")
        aed  = c2.date_input("To",   value=df["service_date"].max().date(), key="ana_ed")
        asvc = c3.selectbox("Service",    ["All Services"]    + sorted(df["service_name"].unique().tolist()), key="ana_svc")
        adpt = c4.selectbox("Department", ["All Departments"] + DEPARTMENTS, key="ana_dpt")

        if st.button("📥 Generate Filtered Report", type="primary", key="ana_gen"):
            fdf = filter_df(
                df,
                start=asd, end=aed,
                service=None if asvc == "All Services"    else asvc,
                dept=None    if adpt == "All Departments" else adpt,
            )
            rc1, rc2 = st.columns(2)
            rc1.download_button(
                "⬇️ PDF",
                export_pdf(fdf, "Analytics Report"),
                "analytics.pdf",
                "application/pdf",
            )
            rc2.download_button(
                "⬇️ Excel",
                export_excel(fdf, "Analytics Report"),
                "analytics.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅  Monthly Trends",
        "⏰  Peak Hours",
        "🏢  By Department",
        "📊  Service Comparison",
    ])

    # ── Tab 1: Monthly Trends ─────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="chart-card"><div class="chart-title">Monthly Usage by Service</div>',
                    unsafe_allow_html=True)
        monthly = df.groupby(["month", "service_name"]).size().reset_index(name="Count")
        fig = px.line(monthly, x="month", y="Count", color="service_name",
                      markers=True, color_discrete_sequence=PLOTLY_COLORS)
        fig.update_layout(xaxis_title="Month", yaxis_title="Records", legend_title="Service")
        fig = plotly_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)
        avg_daily = df.groupby(df["service_date"].dt.date).size().mean()
        st.metric("📊 Average Daily Usage", f"{avg_daily:.1f} records/day")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card"><div class="chart-title">Monthly Totals (All Services)</div>',
                    unsafe_allow_html=True)
        mt2 = df.groupby("month").size().reset_index(name="Total")
        fig2 = px.bar(mt2, x="month", y="Total", color_discrete_sequence=["#0B1F3A"])
        fig2 = plotly_layout(fig2, height=260)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 2: Peak Hours ─────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="chart-card"><div class="chart-title">Peak Hour Analysis</div>',
                    unsafe_allow_html=True)
        hd = df.dropna(subset=["service_hour"])
        if not hd.empty:
            hc = hd.groupby("service_hour").size().reset_index(name="Count")
            hc["Label"] = hc["service_hour"].apply(
                lambda h: f"{int(h):02d}:00 {'AM' if int(h) < 12 else 'PM'}"
            )
            fig = px.bar(hc, x="Label", y="Count", color="Count",
                         color_continuous_scale=[[0, "#1A3460"], [0.5, "#D4AF37"], [1, "#E8CC6A"]])
            fig.update_layout(coloraxis_showscale=False, xaxis_title="Hour", yaxis_title="Visits")
            fig = plotly_layout(fig, height=300)
            st.plotly_chart(fig, use_container_width=True)
            peak = hc.loc[hc["Count"].idxmax()]
            st.info(f"🕐 **Peak Hour:** {peak['Label']} — {int(peak['Count'])} visits")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card"><div class="chart-title">Visits by Day of Week</div>',
                    unsafe_allow_html=True)
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dc = (
            df.groupby("weekday").size()
            .reindex(day_order, fill_value=0)
            .reset_index(name="Count")
        )
        fig2 = px.bar(dc, x="weekday", y="Count", color="Count",
                      color_continuous_scale=[[0, "#1A3460"], [1, "#D4AF37"]])
        fig2.update_layout(coloraxis_showscale=False, xaxis_title="Day", yaxis_title="Records")
        fig2 = plotly_layout(fig2, height=260)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 3: By Department ──────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="chart-card"><div class="chart-title">Department-wise Service Utilization</div>',
                    unsafe_allow_html=True)
        ds = df.groupby(["department", "service_name"]).size().reset_index(name="Count")
        fig = px.bar(ds, x="department", y="Count", color="service_name",
                     barmode="group", color_discrete_sequence=PLOTLY_COLORS)
        fig.update_layout(xaxis_title="Department", yaxis_title="Records", legend_title="Service")
        fig = plotly_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card"><div class="chart-title">Top Departments by Usage</div>',
                    unsafe_allow_html=True)
        top = df["department"].value_counts().head(10).reset_index()
        top.columns = ["Department", "Total Records"]
        st.dataframe(top, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 4: Service Comparison ─────────────────────────────────────────────
    with tab4:
        sc = df["service_name"].value_counts().reset_index()
        sc.columns = ["Service", "Count"]
        sc["Percentage"] = (sc["Count"] / sc["Count"].sum() * 100).round(1)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card"><div class="chart-title">Usage Share</div>',
                        unsafe_allow_html=True)
            fig = px.pie(sc, names="Service", values="Count",
                         color_discrete_sequence=PLOTLY_COLORS, hole=0.35)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig = plotly_layout(fig, height=300)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-card"><div class="chart-title">Volume by Service</div>',
                        unsafe_allow_html=True)
            fig2 = px.bar(sc, x="Service", y="Count", color="Service",
                          color_discrete_sequence=PLOTLY_COLORS)
            fig2 = plotly_layout(fig2, height=300)
            fig2.update_layout(showlegend=False, xaxis_tickangle=-30)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card"><div class="chart-title">Summary Table</div>',
                    unsafe_allow_html=True)
        st.dataframe(sc, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
