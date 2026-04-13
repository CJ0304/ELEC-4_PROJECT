"""
styles.py — CSS injection and Plotly layout helpers for ServiSense
"""

import streamlit as st
import plotly.graph_objects as go


# ── Login page CSS ────────────────────────────────────────────────────────────

def inject_css_login():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --gold: #D4AF37;
        --gold-light: #E8CC6A;
        --radius-lg: 18px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'DM Sans', sans-serif !important;
        background: linear-gradient(135deg, #0B1F3A 0%, #162E55 50%, #091829 100%) !important;
        overflow: hidden !important;
        height: 100vh !important;
        height: 100dvh !important;
    }
    .main, [data-testid="stMain"] {
        overflow: hidden !important;
        height: 100vh !important;
        height: 100dvh !important;
    }
    .main .block-container {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        min-height: 100dvh !important;
        overflow: hidden !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none !important; }

    [data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        min-width: 0px !important;
        max-width: 0px !important;
        flex: 0 0 0px !important;
        overflow: hidden !important;
    }
    [data-testid="collapsedControl"] { display: none !important; }

    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        width: 100% !important;
    }

    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    .login-card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border-radius: var(--radius-lg);
        padding: 32px 24px;
        box-shadow: 0 24px 80px rgba(0,0,0,0.6);
        border: 1px solid rgba(212,175,55,0.15);
        width: 100%;
    }
    .login-logo-icon { font-size: 3rem; line-height: 1; display: block; text-align: center; }
    .login-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-align: center;
        margin: 10px 0 0 !important;
    }
    .login-subtitle {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.5);
        text-align: center;
        margin: 6px 0 24px;
        line-height: 1.5;
    }

    [data-testid="stForm"] .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1.5px solid rgba(212,175,55,0.4) !important;
        background: rgba(255,255,255,0.92) !important;
        color: #0B1F3A !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
    }
    [data-testid="stForm"] .stTextInput > div > div > input::placeholder {
        color: #9AA5BB !important;
    }
    [data-testid="stForm"] .stTextInput > div > div > input:focus {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 0 3px rgba(212,175,55,0.2) !important;
        outline: none !important;
    }

    [data-testid="stForm"] label,
    [data-testid="stForm"] .stTextInput label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        color: rgba(212,175,55,0.9) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }

    [data-testid="stForm"] .stButton > button[kind="primary"],
    [data-testid="stForm"] .stFormSubmitButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #E8CC6A 100%) !important;
        color: #0B1F3A !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.4rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: 0.3px;
    }
    [data-testid="stForm"] .stFormSubmitButton > button:hover {
        box-shadow: 0 6px 24px rgba(212,175,55,0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* ── LOGIN RESPONSIVE ── */
    @media (max-width: 768px) {
        .login-card {
            padding: 20px 16px;
            margin: 0 4px;
        }
        .login-title { font-size: 1.4rem !important; }
        .login-subtitle { font-size: 0.7rem; margin-bottom: 14px; }
        .login-logo-icon { font-size: 2.2rem; }
        [data-testid="stForm"] .stTextInput > div > div > input {
            padding: 8px 12px !important;
            font-size: 0.85rem !important;
        }
        [data-testid="stForm"] .stFormSubmitButton > button {
            padding: 0.55rem 1rem !important;
            font-size: 0.88rem !important;
        }
    }
    @media (max-width: 480px) {
        .login-card {
            padding: 16px 12px;
            border-radius: 14px;
            box-shadow: 0 16px 50px rgba(0,0,0,0.5);
        }
        .login-title { font-size: 1.2rem !important; }
        .login-subtitle { font-size: 0.65rem; margin-bottom: 12px; line-height: 1.4; }
        .login-logo-icon { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)


# ── App CSS ───────────────────────────────────────────────────────────────────

def inject_css_app():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --navy:       #0B1F3A;
        --navy-mid:   #1A3460;
        --navy-light: #243E6E;
        --gold:       #D4AF37;
        --gold-light: #E8CC6A;
        --gold-pale:  #FDF6DC;
        --white:      #FFFFFF;
        --off-white:  #F5F7FC;
        --gray-100:   #EEF1F8;
        --gray-200:   #DDE2EF;
        --gray-400:   #9AA5BB;
        --gray-500:   #6B7899;
        --radius-sm:  8px;
        --radius-md:  12px;
        --radius-lg:  18px;
        --shadow-sm:  0 2px 8px rgba(11,31,58,0.07);
        --shadow-md:  0 4px 20px rgba(11,31,58,0.12);
        --shadow-lg:  0 10px 40px rgba(11,31,58,0.18);
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--off-white) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none !important; }

    .main .block-container {
        padding: 0rem 2.5rem 2rem 2.5rem !important;
        max-width: 1440px;
    }

    h1 {
        font-family: 'Playfair Display', serif !important;
        color: var(--navy) !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0 !important;
    }
    h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--navy) !important;
        font-weight: 600 !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, #0B1F3A 0%, #162E55 55%, #0E2548 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 30px rgba(0,0,0,0.2);
    }
    [data-testid="stSidebar"] > div {
        overflow-y: auto !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: rgba(255,255,255,0.85) !important;
        text-align: left !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        align-items: stretch !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stElementContainer"] {
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stButton {
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        text-align: left !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: rgba(255,255,255,0.75) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 9px 14px !important;
        text-align: left !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        margin: 1px 0 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(212,175,55,0.15) !important;
        color: var(--gold-light) !important;
        transform: translateX(3px);
    }

    /* ── KPI CARDS ── */
    .kpi-card {
        background: var(--white) !important;
        border-radius: var(--radius-md);
        padding: 18px 20px 16px;
        box-shadow: var(--shadow-sm);
        border-top: 3px solid var(--gold);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
    .kpi-label {
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        color: var(--gray-400) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 0 8px 0;
    }
    .kpi-value {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        color: var(--navy) !important;
        margin: 0;
        line-height: 1;
    }
    .kpi-sub {
        font-size: 0.7rem !important;
        color: var(--gray-500) !important;
        margin-top: 5px;
        font-weight: 500;
    }
    .kpi-value-sm {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: var(--navy) !important;
        margin: 0;
        line-height: 1.3;
    }

    /* ── CHART CARDS ── */
    .chart-card {
        background: var(--white) !important;
        border-radius: var(--radius-md);
        padding: 22px 22px 16px;
        box-shadow: var(--shadow-sm);
        margin-bottom: 16px;
    }
    .chart-title {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: var(--navy) !important;
        margin: 0 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--gray-100);
    }
    .chart-insight {
        font-size: 0.78rem !important;
        color: var(--gray-500) !important;
        padding: 6px 0 4px;
        font-style: italic;
    }

    /* ── PAGE HEADER ── */
    .page-header {
        background: linear-gradient(130deg, #0B1F3A 0%, #1A3460 100%);
        border-radius: var(--radius-md);
        padding: 16px 26px;
        margin-top: 0px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    .page-header-icon { font-size: 1.9rem; }
    .page-header-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin: 0;
        line-height: 1.2;
    }
    .page-header-sub {
        font-size: 0.78rem !important;
        color: rgba(232,204,106,0.9) !important;
        margin: 3px 0 0 0;
        font-weight: 400;
    }

    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, var(--gold) 0%, var(--gray-100) 60%, transparent 100%);
        margin: 20px 0;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: var(--white) !important;
        color: var(--navy) !important;
        border: 1.5px solid var(--gray-200) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        border-color: var(--gold) !important;
        color: var(--navy-mid) !important;
        box-shadow: 0 2px 10px rgba(212,175,55,0.2) !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--gold) !important;
        color: #1a1a1a !important;
        border: 1px solid transparent !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--gold-light) !important;
        box-shadow: 0 4px 16px rgba(212,175,55,0.35) !important;
        transform: translateY(-1px);
    }
    .stFormSubmitButton > button {
        background: var(--gold) !important;
        color: #1a1a1a !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
        cursor: pointer !important;
    }
    .stFormSubmitButton > button[kind="secondary"] {
        background: var(--white) !important;
        color: var(--navy) !important;
        border: 1.5px solid var(--gray-200) !important;
    }
    .stDownloadButton > button {
        background: var(--gold-pale) !important;
        color: var(--navy) !important;
        border: 1.5px solid rgba(212,175,55,0.5) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: var(--gold) !important;
        border-color: var(--gold) !important;
    }

    /* ── FORM INPUTS ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > textarea {
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--gray-200) !important;
        font-family: 'DM Sans', sans-serif !important;
        color: var(--navy) !important;
        background: var(--white) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(212,175,55,0.12) !important;
        outline: none !important;
    }
    .stSelectbox > div > div {
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--gray-200) !important;
        background: var(--white) !important;
        color: var(--navy) !important;
    }
    .stSelectbox [data-baseweb="select"] > div { background: var(--white) !important; color: var(--navy) !important; }
    .stSelectbox [data-baseweb="select"] span  { color: var(--navy) !important; }

    label,
    .stTextInput label, .stSelectbox label, .stDateInput label,
    .stNumberInput label, .stTextArea label, .stFileUploader label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        color: var(--gray-500) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }


    /* ── DATAFRAME ── */
    [data-testid="stDataFrame"] {
        border-radius: var(--radius-md) !important;
        overflow: hidden;
        border: 1px solid var(--gray-200) !important;
        box-shadow: var(--shadow-sm);
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--gray-100) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: 1px solid var(--gray-200) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        color: var(--navy) !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
        padding: 8px 16px !important;
        cursor: pointer !important;
    }
    .stTabs [data-baseweb="tab"]:hover { background: rgba(11,31,58,0.06) !important; color: var(--navy) !important; }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: var(--gold) !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span { color: var(--gold) !important; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 16px !important; }

    /* ── METRIC ── */
    [data-testid="stMetric"] { background: var(--white); border-radius: var(--radius-md); padding: 14px 18px; border-left: 3px solid var(--gold); box-shadow: var(--shadow-sm); }
    [data-testid="stMetricLabel"] { font-size: 0.7rem !important; color: var(--gray-400) !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.8px; }
    [data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; color: var(--navy) !important; font-size: 1.6rem !important; }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--gray-100); }
    ::-webkit-scrollbar-thumb { background: var(--gray-200); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold); }

    [data-testid="stSpinner"] p { color: var(--navy) !important; }

    /* ── RESPONSIVE: TABLET (≤ 1024px) ── */
    @media (max-width: 1024px) {
        .main .block-container {
            padding: 0rem 1.5rem 2rem !important;
            max-width: 100% !important;
        }
        .kpi-value { font-size: 1.6rem !important; }
        .chart-card { padding: 16px 16px 12px; }
    }

    /* ── RESPONSIVE: MOBILE (≤ 768px) ── */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0rem 0.75rem 1.5rem !important;
            max-width: 100% !important;
        }

        /* Sidebar: hidden by default, slides in when Streamlit opens it */
        [data-testid="stSidebar"] {
            width: 75vw !important;
            min-width: 220px !important;
            max-width: 280px !important;
        }
        [data-testid="stSidebar"] > div {
            width: 100% !important;
            min-width: 0 !important;
            padding-top: 10px !important;
        }
        /* Force left-align everything in sidebar on mobile */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            align-items: stretch !important;
        }
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown div,
        [data-testid="stSidebar"] .stMarkdown p {
            text-align: left !important;
            justify-content: flex-start !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
        }

        /* Main content uses full width when sidebar is collapsed */
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
        }

        /* Page header */
        .page-header {
            padding: 14px 16px;
            margin-top: 0px;
            margin-bottom: 14px;
            gap: 10px;
        }
        .page-header-icon { font-size: 1.5rem; }
        .page-header-title { font-size: 1.15rem !important; }
        .page-header-sub { font-size: 0.7rem !important; }

        /* KPI cards */
        .kpi-card { padding: 14px 16px 12px; }
        .kpi-value { font-size: 1.4rem !important; }
        .kpi-label { font-size: 0.65rem !important; }
        .kpi-sub { font-size: 0.65rem !important; }

        /* Chart cards */
        .chart-card {
            padding: 14px 12px 10px;
            margin-bottom: 10px;
        }
        .chart-title { font-size: 0.85rem !important; margin-bottom: 10px; padding-bottom: 8px; }

        /* Headings */
        h1 { font-size: 1.5rem !important; }

        /* Tabs — horizontally scrollable */
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
            flex-wrap: nowrap !important;
            scrollbar-width: none;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px !important;
            font-size: 0.8rem !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }

        /* Metric */
        [data-testid="stMetric"] { padding: 10px 14px; }
        [data-testid="stMetricValue"] { font-size: 1.3rem !important; }

        /* Section divider */
        .section-divider { margin: 14px 0; }

        /* Make Streamlit columns stack on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* Dataframe — horizontal scroll */
        [data-testid="stDataFrame"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
        }

        /* Buttons */
        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button {
            font-size: 0.85rem !important;
            padding: 8px 14px !important;
        }

        /* Form labels */
        label,
        .stTextInput label, .stSelectbox label, .stDateInput label,
        .stNumberInput label, .stTextArea label, .stFileUploader label {
            font-size: 0.72rem !important;
        }
    }

    /* ── RESPONSIVE: SMALL MOBILE (≤ 480px) ── */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0rem 0.5rem 1rem !important;
        }

        .page-header {
            padding: 12px 14px;
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
        }
        .page-header-title { font-size: 1.05rem !important; }

        h1 { font-size: 1.3rem !important; }

        .kpi-value { font-size: 1.2rem !important; }
        .kpi-card { padding: 12px 14px 10px; }

        .chart-card { padding: 10px 8px 8px; }

        .stTabs [data-baseweb="tab"] {
            padding: 5px 10px !important;
            font-size: 0.75rem !important;
        }

        [data-testid="stMetricValue"] { font-size: 1.1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)


# ── Plotly layout helper ───────────────────────────────────────────────────────

def plotly_layout(fig, height: int = 320):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#0B1F3A", size=12),
        margin=dict(l=10, r=10, t=10, b=30),
        legend=dict(bgcolor="rgba(255,255,255,0.85)", bordercolor="#DDE2EF",
                    borderwidth=1, font=dict(size=11)),
    )
    fig.update_xaxes(gridcolor="#EEF1F8", linecolor="#DDE2EF", tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#EEF1F8", linecolor="#DDE2EF", tickfont=dict(size=11))
    return fig
