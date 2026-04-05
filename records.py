"""
records.py — Service Records page for ServiSense
"""

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from constants import OFFICES, DEPARTMENTS
from data import filter_df, load_records, delete_record, update_record
from exports import export_pdf, export_excel
from ui_components import page_header


def render(rec_df, svc_df):
    office      = st.session_state.assigned_office
    active_svcs = svc_df[svc_df["is_active"] == 1]["name"].tolist()

    page_header(
        "📋", "Service Records",
        f"Office: {office}" if office else "All offices · View, filter, edit and export records",
    )

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🔍 Filter Records", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        sd = c1.date_input("From Date", value=date.today() - timedelta(days=30), key="rec_sd")
        ed = c2.date_input("To Date",   value=date.today(),                       key="rec_ed")

        if office:
            svc_sel = office
            c3.text_input("Service Type", value=office, disabled=True, key="rec_svc_locked")
        else:
            svc_sel = c3.selectbox("Service Type", ["All Services"] + active_svcs, key="rec_svc")

        dept_sel = c4.selectbox("Department", ["All Departments"] + DEPARTMENTS, key="rec_dept")

    svc_arg  = None if (not svc_sel or svc_sel == "All Services")      else svc_sel
    dept_arg = None if (not dept_sel or dept_sel == "All Departments") else dept_sel

    df = filter_df(rec_df, start=sd, end=ed, service=svc_arg, dept=dept_arg, office_lock=office)

    # ── Summary KPIs ──────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f'<div class="kpi-card"><div class="kpi-label">Records Found</div>'
        f'<div class="kpi-value">{len(df):,}</div></div>',
        unsafe_allow_html=True,
    )
    if not df.empty:
        c2.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Unique Students</div>'
            f'<div class="kpi-value">{df["student_id"].nunique():,}</div></div>',
            unsafe_allow_html=True,
        )
        top = df["service_name"].value_counts().idxmax()
        c3.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Top Service</div>'
            f'<div class="kpi-value-sm">{top}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    if df.empty:
        st.info("📭 No records found for the selected filters.")
        return

    # ── Export buttons ────────────────────────────────────────────────────────
    ec1, ec2, _, _ = st.columns(4)
    with ec1:
        st.download_button(
            "⬇️ Export PDF",
            data=export_pdf(df),
            file_name="records.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with ec2:
        st.download_button(
            "⬇️ Export Excel",
            data=export_excel(df),
            file_name="records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── Data table ────────────────────────────────────────────────────────────
    display_df = df[["id", "student_id", "student_name", "department",
                      "service_name", "service_date", "service_hour", "remarks"]].copy()
    display_df["service_date"] = display_df["service_date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "id":           st.column_config.NumberColumn("ID",    width="small"),
            "student_id":   st.column_config.TextColumn("Student ID"),
            "student_name": st.column_config.TextColumn("Name"),
            "department":   st.column_config.TextColumn("Dept",   width="small"),
            "service_name": st.column_config.TextColumn("Service"),
            "service_date": st.column_config.TextColumn("Date"),
            "service_hour": st.column_config.NumberColumn("Hour", width="small"),
            "remarks":      st.column_config.TextColumn("Remarks"),
        },
    )

    # ── Record actions ────────────────────────────────────────────────────────
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("**⚙️ Record Actions**")

    id_list = df["id"].tolist()
    col_sel, col_edit, col_del = st.columns([3, 1, 1])
    selected_id = col_sel.selectbox("Select Record ID", id_list, label_visibility="collapsed",
                                    key="rec_sel_id")

    if col_edit.button("✏️ Edit", use_container_width=True, key="rec_edit_btn"):
        st.session_state.edit_mode = True
        st.session_state.edit_id   = selected_id

    if col_del.button("🗑️ Delete", use_container_width=True, key="rec_del_btn"):
        delete_record(int(selected_id))
        st.success("✅ Record deleted successfully.")
        st.rerun()

    # ── Edit modal ────────────────────────────────────────────────────────────
    if st.session_state.get("edit_mode") and st.session_state.get("edit_id"):
        st.markdown('<div class="modal-card">', unsafe_allow_html=True)
        st.markdown("### ✏️ Edit Service Record")

        all_df  = load_records()
        matched = all_df[all_df["id"] == st.session_state.edit_id]

        if matched.empty:
            st.error("Record not found.")
            st.session_state.edit_mode = False
        else:
            row = matched.iloc[0]
            with st.form("edit_record_form"):
                ec1, ec2 = st.columns(2)
                new_sid  = ec1.text_input("Student ID",   value=str(row["student_id"]))
                new_name = ec2.text_input("Student Name", value=str(row["student_name"]))
                svc_options = active_svcs if active_svcs else OFFICES
                new_svc  = ec1.selectbox(
                    "Service", svc_options,
                    index=svc_options.index(row["service_name"]) if row["service_name"] in svc_options else 0,
                )
                new_dept = ec2.selectbox(
                    "Department", DEPARTMENTS,
                    index=DEPARTMENTS.index(row["department"]) if row["department"] in DEPARTMENTS else 0,
                )
                new_date = ec1.date_input("Date", pd.to_datetime(row["service_date"]))
                new_hour = ec2.number_input("Hour (8–17)", 8, 17, int(row["service_hour"]))
                new_rem  = st.text_area("Remarks", value=str(row.get("remarks", "") or ""))

                sc1, sc2  = st.columns(2)
                save_btn  = sc1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                close_btn = sc2.form_submit_button("❌ Cancel", use_container_width=True)

            if save_btn:
                update_record(int(st.session_state.edit_id), {
                    "student_id":   new_sid,
                    "student_name": new_name,
                    "service_name": new_svc,
                    "department":   new_dept,
                    "service_date": str(new_date),
                    "service_hour": new_hour,
                    "remarks":      new_rem,
                })
                st.success("✅ Record updated!")
                st.session_state.edit_mode = False
                st.rerun()

            if close_btn:
                st.session_state.edit_mode = False
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
