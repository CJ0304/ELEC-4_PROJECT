"""
add_record.py — Add Record page for ServiSense
"""

from datetime import date, datetime

import streamlit as st

from constants import OFFICES, DEPARTMENTS
from data import add_record
from ui_components import page_header


def render(rec_df, svc_df):
    office      = st.session_state.assigned_office
    active_svcs = svc_df[svc_df["is_active"] == 1]["name"].tolist()

    page_header(
        "➕", "Add Service Record",
        f"Office: {office}" if office else "Admin — Add record for any office",
    )

    with st.form("add_record_form"):
        c1, c2 = st.columns(2)
        student_id   = c1.text_input("Student ID *",   placeholder="e.g. 2024-01001")
        student_name = c2.text_input("Student Name *", placeholder="e.g. Juan Dela Cruz")

        if office:
            svc_choice = office
            c1.text_input("Service Type", value=office, disabled=True)
        else:
            svc_choice = c1.selectbox("Service Type *", active_svcs if active_svcs else OFFICES)

        dept     = c2.selectbox("Department *", DEPARTMENTS)
        svc_date = c1.date_input("Service Date *", value=date.today())
        cur_h    = datetime.now().hour
        svc_hour = c2.number_input("Hour (8–17) *", 8, 17, cur_h if 8 <= cur_h <= 17 else 8)
        remarks  = st.text_area("Remarks", placeholder="Optional notes...")
        submitted = st.form_submit_button("💾 Save Record", type="primary", use_container_width=True)

    if submitted:
        if not student_id.strip() or not student_name.strip():
            st.error("⚠️ Student ID and Student Name are required.")
            return

        add_record({
            "student_id":   student_id.strip(),
            "student_name": student_name.strip(),
            "department":   dept,
            "service_name": svc_choice,
            "service_date": str(svc_date),
            "service_hour": int(svc_hour),
            "remarks":      remarks.strip(),
            "created_by":   st.session_state.user_name,
            "created_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        st.success(f"✅ Record saved for **{student_name.strip()}** under **{svc_choice}**!")
        st.balloons()
