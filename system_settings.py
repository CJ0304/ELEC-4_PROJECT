"""
pages/system_settings.py — System Settings page for ServiSense (Admin only)
"""

import pandas as pd
import streamlit as st

from constants import SERVICE_CATEGORIES
from data import save_services
from ui_components import page_header


def render(svc_df):
    page_header("⚙️", "System Settings", "Admin only — Manage the services catalog")

    # ── Search & table ────────────────────────────────────────────────────────
    search  = st.text_input("🔍 Search Services", placeholder="Type to search...", key="svc_search")
    display = (
        svc_df[svc_df["name"].str.contains(search, case=False, na=False)]
        if search else svc_df
    )

    if display.empty:
        st.info("📭 No services found.")
    else:
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id":          "ID",
                "name":        "Service Name",
                "category":    "Category",
                "description": "Description",
                "is_active":   "Active",
            },
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    tab_add, tab_edit = st.tabs(["➕  Add Service", "✏️  Edit / Toggle Status"])

    # ── Tab: Add Service — form always visible, no toggle needed ──────────────
    with tab_add:
        st.markdown("#### 🛠️ Add New Service")
        with st.form("add_service_form", clear_on_submit=True):
            fc1, fc2  = st.columns(2)
            svc_name  = fc1.text_input("Service Name *", placeholder="e.g. Medical Records")
            category  = fc2.selectbox("Category", SERVICE_CATEGORIES)
            status    = fc1.selectbox("Status", ["Active", "Inactive"])
            desc      = st.text_area("Description", placeholder="Brief description...")
            submitted = st.form_submit_button("💾 Save Service", type="primary", use_container_width=True)

        if submitted:
            if not svc_name.strip():
                st.error("⚠️ Service name is required.")
            elif svc_name.strip() in svc_df["name"].values:
                st.error(f"⚠️ '{svc_name.strip()}' already exists.")
            else:
                new_id  = int(svc_df["id"].max()) + 1 if not svc_df.empty else 1
                new_row = pd.DataFrame([{
                    "id":          new_id,
                    "name":        svc_name.strip(),
                    "category":    category,
                    "description": desc.strip(),
                    "is_active":   1 if status == "Active" else 0,
                }])
                save_services(pd.concat([svc_df, new_row], ignore_index=True))
                st.success(f"✅ Service '{svc_name.strip()}' added!")
                st.rerun()

    # ── Tab: Edit / Toggle ────────────────────────────────────────────────────
    with tab_edit:
        if svc_df.empty:
            st.info("No services available to edit.")
            return

        st.markdown("#### ✏️ Edit / Toggle Service")
        sel_svc = st.selectbox("Select Service to Edit", svc_df["name"].tolist(), key="edit_svc_sel")
        row     = svc_df[svc_df["name"] == sel_svc].iloc[0]

        with st.form("edit_svc_form"):
            ec1, ec2 = st.columns(2)
            en   = ec1.text_input("Service Name", value=str(row["name"]))
            ecat = ec2.selectbox(
                "Category", SERVICE_CATEGORIES,
                index=SERVICE_CATEGORIES.index(row["category"])
                if row["category"] in SERVICE_CATEGORIES else 0,
            )
            es  = ec1.selectbox(
                "Status", ["Active", "Inactive"],
                index=0 if int(row["is_active"]) == 1 else 1,
            )
            ed    = st.text_area("Description", value=str(row.get("description", "") or ""))
            saved = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)

        if saved:
            idx = svc_df.index[svc_df["name"] == sel_svc]
            svc_df.loc[idx, "name"]        = en.strip()
            svc_df.loc[idx, "category"]    = ecat
            svc_df.loc[idx, "description"] = ed.strip()
            svc_df.loc[idx, "is_active"]   = 1 if es == "Active" else 0
            save_services(svc_df)
            st.success("✅ Service updated!")
            st.rerun()