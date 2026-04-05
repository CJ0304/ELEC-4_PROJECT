"""
app.py — ServiSense entry point
================================
Run with:  streamlit run app.py

File layout (flat — all modules in root directory)
--------------------------------------------------
app.py              ← this file (router only)
constants.py        ← shared constants (offices, departments, colours)
auth.py             ← login / logout / session init
db.py               ← PostgreSQL connection, table creation, seeding
data.py             ← DB loaders, savers, filter_df(), password hashing
exports.py          ← PDF and Excel export
styles.py           ← CSS injection + plotly_layout()
ui_components.py    ← sidebar_nav(), page_header(), page_login()
dashboard.py        ← KPI dashboard with charts
records.py          ← view / filter / edit / export service records
add_record.py       ← single record entry form
upload_records.py   ← batch CSV/Excel import
analytics.py        ← admin analytics & reporting
system_settings.py  ← admin service catalog management
user_management.py  ← admin user & staff management
"""

import streamlit as st

from auth import init_session
from db import init_tables, seed_defaults
from data import load_records, load_services
from styles import inject_css_login, inject_css_app
from ui_components import page_login, sidebar_nav

import dashboard        as pg_dashboard
import records          as pg_records
import add_record       as pg_add_record
import upload_records   as pg_upload
import analytics        as pg_analytics
import system_settings  as pg_settings
import user_management  as pg_users


def main():
    # Must be the very first Streamlit call
    st.set_page_config(
        page_title="ServiSense — Student Services Analytics",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session()

    # ── Database must be ready before login (login queries the users table) ──
    init_tables()
    seed_defaults()

    # ── Login gate ────────────────────────────────────────────────────────────
    if not st.session_state.authenticated:
        inject_css_login()
        page_login()
        return

    # ── Authenticated app ─────────────────────────────────────────────────────
    inject_css_app()

    with st.spinner("Loading data..."):
        rec_df = load_records()
        svc_df = load_services()

    page = sidebar_nav()

    if "Dashboard" in page:
        pg_dashboard.render(rec_df, svc_df)

    elif "Service Records" in page:
        pg_records.render(rec_df, svc_df)

    elif "Add Record" in page:
        pg_add_record.render(rec_df, svc_df)

    elif "Upload Records" in page:
        pg_upload.render(rec_df, svc_df)

    elif "Analytics" in page:
        if st.session_state.user_role == "Admin":
            pg_analytics.render(rec_df)
        else:
            st.error("⛔ Admin access required.")

    elif "System Settings" in page:
        if st.session_state.user_role == "Admin":
            pg_settings.render(svc_df)
        else:
            st.error("⛔ Admin access required.")

    elif "User Management" in page:
        if st.session_state.user_role == "Admin":
            pg_users.render()
        else:
            st.error("⛔ Admin access required.")



if __name__ == "__main__":
    main()
