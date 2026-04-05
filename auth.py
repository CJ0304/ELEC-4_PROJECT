"""
auth.py — Authentication and session state for ServiSense
"""

import streamlit as st
from data import load_users, save_users, verify_password


# ── Session initialisation ────────────────────────────────────────────────────

def init_session():
    defaults = {
        "authenticated":    False,
        "user_role":        None,
        "user_name":        None,
        "assigned_office":  None,
        "username":         None,
        "page":             "📊 Dashboard",
        "edit_mode":        False,
        "edit_id":          None,
        "show_add_service": False,
        "show_add_user":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Login / Logout ────────────────────────────────────────────────────────────

def login(username: str, password: str) -> bool:
    users = load_users()
    u = users.get(username)
    if u and verify_password(password, u["password"]) and u.get("status", "Active") == "Active":
        st.session_state.authenticated   = True
        st.session_state.user_role       = u["role"]
        st.session_state.user_name       = u["name"]
        st.session_state.assigned_office = u["office"]
        st.session_state.username        = username
        return True
    return False


def logout():
    for k in ["authenticated", "user_role", "user_name", "assigned_office", "username"]:
        st.session_state[k] = None
    st.session_state.authenticated = False
    st.session_state.page = "📊 Dashboard"
