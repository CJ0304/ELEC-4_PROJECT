"""
ui_components.py — Shared UI helpers: sidebar, page header, login page
"""

import streamlit as st
import streamlit.components.v1 as components

from auth import login, logout
from styles import inject_css_login


# ── Login page ────────────────────────────────────────────────────────────────

def page_login():
    inject_css_login()

    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100%;
    background-image: linear-gradient(rgba(212,175,55,0.025) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(212,175,55,0.025) 1px, transparent 1px);
    background-size: 40px 40px; z-index:0; pointer-events:none;"></div>
    """, unsafe_allow_html=True)

    _, col_c, _ = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("<div style='height:6vh'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="login-card">
            <span class="login-logo-icon">🎓</span>
            <h1 class="login-title">ServiSense</h1>
            <p class="login-subtitle">
                Student Services Utilization &amp;<br>Performance Analytics System
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            username  = st.text_input("Username", placeholder="Enter your username")
            password  = st.text_input("Password", type="password", placeholder="••••••••••")
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

        if submitted:
            with st.spinner("Authenticating..."):
                if login(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password. Please try again.")


# ── Sidebar navigation ────────────────────────────────────────────────────────

def sidebar_nav() -> str:
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:20px 6px 16px;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:14px;'>
                <span style='font-size:1.9rem;'>🎓</span>
                <div>
                    <div style='font-family:"Playfair Display",serif;font-size:1.15rem;
                    font-weight:700;color:#FFFFFF !important;line-height:1.1;'>ServiSense</div>
                    <div style='font-size:0.6rem;color:#D4AF37 !important;letter-spacing:1.5px;
                    text-transform:uppercase;margin-top:2px;font-weight:600;'>Analytics System</div>
                </div>
            </div>
            <div style='background:rgba(255,255,255,0.06);border-radius:10px;
            padding:11px 13px;border-left:3px solid #D4AF37;'>
                <div style='font-size:0.85rem;font-weight:600;color:#FFFFFF !important;'>{st.session_state.user_name}</div>
                <div style='font-size:0.7rem;color:#D4AF37 !important;margin-top:3px;font-weight:500;'>
                    {st.session_state.user_role}
                    {f" · {st.session_state.assigned_office}" if st.session_state.assigned_office else " · All Offices"}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<div style='height:3px;background:linear-gradient(90deg,#D4AF37,transparent);"
            "border-radius:2px;margin:0 0 14px;'></div>",
            unsafe_allow_html=True,
        )

        def nav_btn(label: str):
            active = st.session_state.page == label
            if active:
                st.markdown(f"""
                <div style='background:rgba(212,175,55,0.15);border-radius:8px;
                padding:9px 14px;margin:1px 0;border-left:3px solid #D4AF37;
                font-size:0.875rem;font-weight:600;color:#E8CC6A !important;cursor:default;'>
                {label}
                </div>""", unsafe_allow_html=True)
            else:
                if st.button(label, use_container_width=True, key=f"nav_{label}"):
                    st.session_state.page = label
                    st.rerun()

        st.markdown(
            "<p style='font-size:0.6rem;color:rgba(255,255,255,0.35);text-transform:uppercase;"
            "letter-spacing:1.2px;padding:0 4px;margin-bottom:6px;font-weight:600;'>Main Menu</p>",
            unsafe_allow_html=True,
        )
        nav_btn("📊 Dashboard")
        nav_btn("📋 Service Records")
        nav_btn("➕ Add Record")
        nav_btn("📤 Upload Records")

        if st.session_state.user_role == "Admin":
            st.markdown(
                "<p style='font-size:0.6rem;color:rgba(255,255,255,0.35);text-transform:uppercase;"
                "letter-spacing:1.2px;padding:4px 4px;margin:10px 0 6px;"
                "border-top:1px solid rgba(255,255,255,0.08);font-weight:600;'>Admin Tools</p>",
                unsafe_allow_html=True,
            )
            nav_btn("📈 Analytics")
            nav_btn("⚙️ System Settings")
            nav_btn("👥 User Management")

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if st.button("🚪  Sign Out", use_container_width=True, key="logout_btn"):
            logout()
            st.rerun()

        st.markdown("""
        <div style='padding:14px 4px 6px;margin-top:14px;border-top:1px solid rgba(255,255,255,0.08);'>
            <div style='font-size:0.62rem;color:rgba(255,255,255,0.25);text-align:center;'>
                ServiSense v3.0 &nbsp;·&nbsp; 2024
            </div>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.page


# ── Page header ───────────────────────────────────────────────────────────────

def page_header(icon: str, title: str, subtitle: str = ""):
    # Scroll main panel to top on every page navigation
    components.html(
        "<script>window.parent.document.querySelector('.main').scrollTop = 0;</script>",
        height=0,
    )
    st.markdown(f"""
    <div class="page-header">
        <span class="page-header-icon">{icon}</span>
        <div>
            <div class="page-header-title">{title}</div>
            {f'<div class="page-header-sub">{subtitle}</div>' if subtitle else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
