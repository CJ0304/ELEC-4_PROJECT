"""
upload_records.py — Upload Records page for ServiSense
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from data import add_records, save_uploaded_file, list_uploaded_files, get_uploaded_file
from ui_components import page_header


def render(rec_df, svc_df):
    office = st.session_state.assigned_office
    role   = st.session_state.user_role

    page_header(
        "📤", "Upload Records",
        f"Office: {office}" if office else "Admin — Import records for any office",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
**Upload a CSV or Excel file** with service records. Required columns:

| Column | Required | Example |
|--------|----------|---------|
| `student_id` | ✅ | 2024-01001 |
| `student_name` | ✅ | Juan Dela Cruz |
| `department` | ✅ | BSIT |
| `service_name` | ⚠️ Auto-filled for staff | Guidance Counseling |
| `service_date` | ✅ | 2024-03-15 |
| `service_hour` | Optional | 10 |
| `remarks` | Optional | Walk-in |
""")
    st.markdown('</div>', unsafe_allow_html=True)

    if role == "Admin":
        active_svcs = svc_df[svc_df["is_active"] == 1]["name"].tolist()
        upload_office = st.selectbox(
            "Target Office",
            ["(Apply service_name from file)"] + active_svcs,
            key="upload_target_office",
        )
    else:
        upload_office = office

    uploaded = st.file_uploader(
        "📂 Choose CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=False,
        key="upload_file",
    )

    if uploaded:
        try:
            new_df = (
                pd.read_csv(uploaded)
                if uploaded.name.endswith(".csv")
                else pd.read_excel(uploaded)
            )
            st.subheader("👁️ Preview (first 10 rows)")
            st.dataframe(new_df.head(10), use_container_width=True)
            st.markdown(f"**{len(new_df)} rows detected**")

            required = {"student_id", "student_name", "department", "service_date"}
            missing  = required - set(new_df.columns.str.lower())
            if missing:
                st.error(f"❌ Missing required columns: {', '.join(missing)}")
                return

            new_df.columns = new_df.columns.str.lower().str.strip()

            if office:
                new_df["service_name"] = office
            elif upload_office != "(Apply service_name from file)":
                new_df["service_name"] = upload_office

            if "service_name" not in new_df.columns:
                st.error("❌ `service_name` column required.")
                return

            if "service_hour" not in new_df.columns:
                new_df["service_hour"] = 8
            if "remarks" not in new_df.columns:
                new_df["remarks"] = ""

            new_df["created_by"] = st.session_state.user_name
            new_df["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_df["service_date"] = (
                pd.to_datetime(new_df["service_date"], errors="coerce")
                .dt.strftime("%Y-%m-%d")
            )

            bad = new_df["service_date"].isna().sum()
            if bad:
                st.warning(f"⚠️ {bad} row(s) with unparseable dates will be skipped.")
                new_df = new_df.dropna(subset=["service_date"])

            if st.button("✅ Import Records into System", type="primary", key="do_import_btn"):
                add_records(new_df)

                # Archive the uploaded file in the database
                safe_name = (office or "admin").replace(" ", "_").replace("/", "")
                ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename  = f"{safe_name}_{ts}_{uploaded.name}"
                save_uploaded_file(
                    filename=filename,
                    file_data=uploaded.getvalue(),
                    office=office,
                    uploaded_by=st.session_state.user_name,
                )

                st.success(f"✅ {len(new_df)} records imported!")
                st.balloons()
                st.rerun()

        except Exception as exc:
            st.error(f"❌ Error reading file: {exc}")

    # ── Previously uploaded files ─────────────────────────────────────────────
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("📁 Previously Uploaded Files")

    uploads_df = list_uploaded_files(office=office)

    if not uploads_df.empty:
        for _, row in uploads_df.iterrows():
            uc1, uc2 = st.columns([4, 1])
            uc1.markdown(f"📄 `{row['filename']}` — {row['file_size'] / 1024:.1f} KB")
            try:
                _, fdata = get_uploaded_file(int(row["id"]))
                uc2.download_button("⬇️", fdata, file_name=row["filename"],
                                    key=f"dl_{row['id']}")
            except FileNotFoundError:
                uc2.write("—")
    else:
        st.info("No uploaded files yet for this office.")
