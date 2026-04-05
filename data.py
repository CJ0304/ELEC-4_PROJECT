"""
data.py — Data loaders, savers, and helpers for ServiSense (PostgreSQL)

All storage goes through the database via db.py.
"""

import hashlib
from datetime import datetime

import pandas as pd
import streamlit as st
from sqlalchemy import text

from db import engine


# ── Password hashing ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """SHA-256 hash for password storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Check a plain-text password against a stored hash."""
    return hash_password(password) == hashed


# ── Record loaders ───────────────────────────────────────────────────────────

@st.cache_data(ttl=5)
def load_records():
    df = pd.read_sql("SELECT * FROM service_records ORDER BY id", engine())
    if not df.empty:
        df["service_date"] = pd.to_datetime(df["service_date"])
    else:
        # Ensure column exists with correct dtype even when empty
        for col in ["id", "student_id", "student_name", "department",
                     "service_name", "service_date", "service_hour",
                     "remarks", "created_by", "created_at"]:
            if col not in df.columns:
                df[col] = pd.Series(dtype="object")
        df["service_date"] = pd.Series(dtype="datetime64[ns]")
    return df


@st.cache_data(ttl=5)
def load_services():
    return pd.read_sql("SELECT * FROM services ORDER BY id", engine())


def load_users():
    """Return users as a dict keyed by username (matches old JSON format)."""
    df = pd.read_sql("SELECT * FROM users", engine())
    users = {}
    for _, row in df.iterrows():
        users[row["username"]] = {
            "password": row["password"],
            "role":     row["role"],
            "name":     row["name"],
            "office":   row["office"],
            "status":   row["status"],
        }
    return users


# ── Record writers ───────────────────────────────────────────────────────────

def add_record(row_dict: dict) -> int:
    """INSERT a single record and return its new id."""
    with engine().begin() as conn:
        result = conn.execute(text(
            "INSERT INTO service_records "
            "(student_id, student_name, department, service_name, "
            " service_date, service_hour, remarks, created_by, created_at) "
            "VALUES (:student_id, :student_name, :department, :service_name, "
            " :service_date, :service_hour, :remarks, :created_by, :created_at)"
        ), row_dict)
        # .lastrowid works on both PostgreSQL (via psycopg2) and SQLite
        new_id = result.lastrowid
        if new_id is None or new_id == 0:
            # Fallback: query the max id
            new_id = conn.execute(text(
                "SELECT MAX(id) FROM service_records"
            )).scalar()
    load_records.clear()
    return new_id


def add_records(df: pd.DataFrame):
    """Bulk-insert a DataFrame of records."""
    cols = ["student_id", "student_name", "department", "service_name",
            "service_date", "service_hour", "remarks", "created_by", "created_at"]
    insert_df = df[cols].copy()
    insert_df.to_sql("service_records", engine(), if_exists="append", index=False)
    load_records.clear()


def update_record(record_id: int, updates: dict):
    """UPDATE a single record by id."""
    sets = ", ".join(f"{k} = :{k}" for k in updates)
    updates["rid"] = record_id
    with engine().begin() as conn:
        conn.execute(text(f"UPDATE service_records SET {sets} WHERE id = :rid"), updates)
    load_records.clear()


def delete_record(record_id: int):
    """DELETE a single record by id."""
    with engine().begin() as conn:
        conn.execute(text("DELETE FROM service_records WHERE id = :rid"), {"rid": record_id})
    load_records.clear()


def save_records(df: pd.DataFrame):
    """Full-replace: truncate table and bulk-insert from DataFrame."""
    with engine().begin() as conn:
        conn.execute(text("DELETE FROM service_records"))
    df.to_sql("service_records", engine(), if_exists="append", index=False)
    load_records.clear()


# ── Service writers ──────────────────────────────────────────────────────────

def save_services(df: pd.DataFrame):
    """Full-replace: truncate and re-insert all services."""
    with engine().begin() as conn:
        conn.execute(text("DELETE FROM services"))
    df.to_sql("services", engine(), if_exists="append", index=False)
    load_services.clear()


# ── User writers ─────────────────────────────────────────────────────────────

def save_users(users: dict):
    """Full-replace all users from a dict keyed by username."""
    with engine().begin() as conn:
        conn.execute(text("DELETE FROM users"))
        for username, u in users.items():
            conn.execute(text(
                "INSERT INTO users (username, password, role, name, office, status) "
                "VALUES (:username, :password, :role, :name, :office, :status)"
            ), {
                "username": username,
                "password": u["password"],
                "role":     u["role"],
                "name":     u["name"],
                "office":   u.get("office"),
                "status":   u.get("status", "Active"),
            })


# ── Uploaded-file helpers ────────────────────────────────────────────────────

def save_uploaded_file(filename: str, file_data: bytes, office: str | None, uploaded_by: str):
    """Store an uploaded file in the database."""
    with engine().begin() as conn:
        conn.execute(text(
            "INSERT INTO uploaded_files (filename, file_data, file_size, office, uploaded_by) "
            "VALUES (:fn, :fd, :fs, :off, :ub)"
        ), {"fn": filename, "fd": file_data, "fs": len(file_data),
            "off": office, "ub": uploaded_by})


def list_uploaded_files(office: str | None = None) -> pd.DataFrame:
    """List uploaded files (without the binary data)."""
    with engine().connect() as conn:
        if office:
            result = conn.execute(text(
                "SELECT id, filename, file_size, office, uploaded_by, uploaded_at "
                "FROM uploaded_files WHERE office = :off ORDER BY uploaded_at DESC"
            ), {"off": office})
        else:
            result = conn.execute(text(
                "SELECT id, filename, file_size, office, uploaded_by, uploaded_at "
                "FROM uploaded_files ORDER BY uploaded_at DESC"
            ))
        rows = result.fetchall()
        cols = ["id", "filename", "file_size", "office", "uploaded_by", "uploaded_at"]
        return pd.DataFrame(rows, columns=cols)


def get_uploaded_file(file_id: int) -> tuple[str, bytes]:
    """Return (filename, file_data) for a specific upload."""
    with engine().connect() as conn:
        row = conn.execute(
            text("SELECT filename, file_data FROM uploaded_files WHERE id = :fid"),
            {"fid": file_id},
        ).fetchone()
    if row is None:
        raise FileNotFoundError(f"Uploaded file {file_id} not found")
    return row[0], bytes(row[1])


# ── Filter helper ────────────────────────────────────────────────────────────

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
