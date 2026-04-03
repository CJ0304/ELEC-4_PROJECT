"""
data.py — Data initialisation, loaders, and save helpers for ServiSense

No seed / demo data. On first run the system starts completely empty.
Only a single default admin account is created so someone can log in.
"""

import os
import json
from datetime import datetime

import pandas as pd
import streamlit as st

from constants import (
    RECORDS_FILE, SERVICES_FILE, USERS_FILE,
    UPLOADS_DIR,
)

# ── Column schemas ────────────────────────────────────────────────────────────
_RECORDS_COLS = [
    "id", "student_id", "student_name", "department", "service_name",
    "service_date", "service_hour", "remarks", "created_by", "created_at",
]
_SERVICES_COLS = ["id", "name", "category", "description", "is_active"]


# ── Init ──────────────────────────────────────────────────────────────────────

def _create_admin():
    users = {
        "admin": {
            "password": "admin123",
            "role":     "Admin",
            "name":     "System Administrator",
            "office":   None,
            "status":   "Active",
        }
    }
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    return users


def init_data():
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    # Empty CSVs with correct headers — no demo rows
    if not os.path.exists(RECORDS_FILE):
        pd.DataFrame(columns=_RECORDS_COLS).to_csv(RECORDS_FILE, index=False)

    if not os.path.exists(SERVICES_FILE):
        pd.DataFrame(columns=_SERVICES_COLS).to_csv(SERVICES_FILE, index=False)

    # One admin account so the system isn't locked out on first run
    if not os.path.exists(USERS_FILE):
        _create_admin()


# ── Loaders ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=5)
def load_records():
    df = pd.read_csv(RECORDS_FILE)
    if not df.empty:
        df["service_date"] = pd.to_datetime(df["service_date"])
    else:
        df["service_date"] = pd.Series(dtype="datetime64[ns]")
    return df


@st.cache_data(ttl=5)
def load_services():
    return pd.read_csv(SERVICES_FILE)


def load_users():
    if not os.path.exists(USERS_FILE):
        return _create_admin()
    with open(USERS_FILE) as f:
        return json.load(f)


# ── Savers ────────────────────────────────────────────────────────────────────

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def save_records(df):
    df.to_csv(RECORDS_FILE, index=False)
    load_records.clear()


def save_services(df):
    df.to_csv(SERVICES_FILE, index=False)
    load_services.clear()


# ── Filter helper ─────────────────────────────────────────────────────────────

def filter_df(df, start=None, end=None, service=None, dept=None, office_lock=None):
    """
    Filter a records DataFrame.

    Parameters
    ----------
    df          : source DataFrame (service_date must already be datetime)
    start / end : Python date or None
    service     : service name string, "All Services", or None
    dept        : department string, "All Departments", or None
    office_lock : if set, restrict to this office (overrides service filter)
    """
    d = df.copy()
    if office_lock:
        d = d[d["service_name"] == office_lock]
    if start is not None:
        d = d[d["service_date"] >= pd.Timestamp(start)]
    if end is not None:
        d = d[d["service_date"] <= pd.Timestamp(end)]
    if service and service not in ("All Services", None):
        d = d[d["service_name"] == service]
    if dept and dept not in ("All Departments", None):
        d = d[d["department"] == dept]
    return d