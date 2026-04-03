"""
pages/user_management.py — User Management page for ServiSense (Admin only)
"""

import pandas as pd
import streamlit as st

from constants import OFFICES
from data import load_users, save_users
from ui_components import page_header


def render():
    page_header("👥", "User Management", "Admin only — Manage staff accounts and access")

    users  = load_users()
    search = st.text_input("🔍 Search Users",
                           placeholder="Search by name or username...", key="usr_search")

    rows = [
        {
            "Username": un,
            "Name":     u["name"],
            "Role":     u["role"],
            "Office":   u.get("office") or "All Offices",
            "Status":   u.get("status", "Active"),
        }
        for un, u in users.items()
        if search.lower() in un.lower() or search.lower() in u["name"].lower()
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "➕  Add Staff",
        "✏️  Edit / Reset Password",
        "🔴  Activate / Deactivate",
    ])

    # ── Tab 1: Add Staff — form always visible, no toggle ─────────────────────
    with tab1:
        st.markdown("#### 👤 Create New Staff Account")
        st.markdown('<div class="modal-card">', unsafe_allow_html=True)

        with st.form("add_user_form", clear_on_submit=True):
            uc1, uc2  = st.columns(2)
            username  = uc1.text_input("Username *",  placeholder="e.g. jdelacruz")
            full_name = uc2.text_input("Full Name *", placeholder="e.g. Juan Dela Cruz")
            password  = uc1.text_input("Password *",  value="Staff123")
            role      = uc2.selectbox("Role", ["Staff", "Admin"])
            office    = uc1.selectbox("Assigned Office", ["(None — Admin)"] + OFFICES)
            status    = uc2.selectbox("Status", ["Active", "Inactive"])
            submitted = st.form_submit_button("💾 Create Account", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            fresh_users = load_users()
            if not username.strip() or not full_name.strip():
                st.error("⚠️ Username and Full Name are required.")
            elif username.strip() in fresh_users:
                st.error(f"⚠️ Username '{username.strip()}' already exists.")
            else:
                fresh_users[username.strip()] = {
                    "password": password,
                    "role":     role,
                    "name":     full_name.strip(),
                    "office":   None if office.startswith("(None") else office,
                    "status":   status,
                }
                save_users(fresh_users)
                st.success(f"✅ User '{username.strip()}' created!")
                st.rerun()

    # ── Tab 2: Edit / Reset Password ──────────────────────────────────────────
    with tab2:
        st.markdown("#### ✏️ Edit User / Reset Password")

        if not users:
            st.info("No users found.")
            return

        sel_u = st.selectbox("Select User to Edit", list(users.keys()), key="edit_usr_sel")
        u     = users[sel_u]

        st.markdown('<div class="modal-card">', unsafe_allow_html=True)
        with st.form("edit_user_form"):
            ec1, ec2 = st.columns(2)
            enm  = ec1.text_input("Full Name",                  value=u["name"])
            npw  = ec2.text_input("New Password (blank = keep)", value="")

            all_offices_opts = ["(None — Admin)"] + OFFICES
            cur_off = u.get("office") or "(None — Admin)"
            eoff = ec1.selectbox(
                "Assigned Office", all_offices_opts,
                index=all_offices_opts.index(cur_off) if cur_off in all_offices_opts else 0,
            )
            erol  = ec2.selectbox("Role", ["Staff", "Admin"],
                                  index=0 if u["role"] == "Staff" else 1)
            saved = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if saved:
            users[sel_u]["name"]   = enm.strip()
            users[sel_u]["role"]   = erol
            users[sel_u]["office"] = None if eoff.startswith("(None") else eoff
            if npw.strip():
                users[sel_u]["password"] = npw.strip()
            save_users(users)
            st.success("✅ User updated!")
            st.rerun()

    # ── Tab 3: Activate / Deactivate ─────────────────────────────────────────
    with tab3:
        st.markdown("#### 🔴 Activate / Deactivate Account")
        non_admin = [u for u in users if u != st.session_state.username]
        if not non_admin:
            st.info("No other users to manage.")
            return

        sel_tog  = st.selectbox("Select User", non_admin, key="tog_sel")
        cur_stat = users[sel_tog].get("status", "Active")
        color    = "#2E7D5E" if cur_stat == "Active" else "#C0392B"
        icon     = "✅ Active" if cur_stat == "Active" else "🔴 Inactive"

        st.markdown(f"""
        <div class="kpi-card" style="margin:8px 0;max-width:300px;">
            <div class="kpi-label">Current Status</div>
            <div style="font-size:1.1rem;font-weight:700;color:{color};margin-top:4px;">{icon}</div>
        </div>""", unsafe_allow_html=True)

        ac1, ac2 = st.columns(2)
        if ac1.button("✅ Activate",   disabled=(cur_stat == "Active"),   use_container_width=True, key="act_btn"):
            users[sel_tog]["status"] = "Active"
            save_users(users)
            st.rerun()
        if ac2.button("🔴 Deactivate", disabled=(cur_stat == "Inactive"), use_container_width=True, key="deact_btn"):
            users[sel_tog]["status"] = "Inactive"
            save_users(users)
            st.rerun()