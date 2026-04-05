"""
db.py — PostgreSQL connection, table creation, and seeding for ServiSense
"""

import os

import streamlit as st
from sqlalchemy import (
    create_engine, text, MetaData, Table, Column,
    Integer, String, Text, Date, LargeBinary, DateTime,
    func,
)


def get_engine():
    """Return a SQLAlchemy engine from DATABASE_URL env var."""
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it to your PostgreSQL connection string."
        )
    # Render uses 'postgres://' but SQLAlchemy 2.x requires 'postgresql://'
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    kwargs = {"pool_pre_ping": True}
    # SQLite doesn't support pool_size
    if not url.startswith("sqlite"):
        kwargs["pool_size"] = 5
    return create_engine(url, **kwargs)


@st.cache_resource
def _cached_engine():
    """Streamlit-cached engine (created once per app lifetime)."""
    return get_engine()


def engine():
    """Public accessor for the cached engine."""
    return _cached_engine()


# ── Schema (dialect-agnostic via SQLAlchemy) ─────────────────────────────────

metadata = MetaData()

service_records_table = Table(
    "service_records", metadata,
    Column("id",            Integer, primary_key=True, autoincrement=True),
    Column("student_id",    String(50),  nullable=False),
    Column("student_name",  String(150), nullable=False),
    Column("department",    String(50),  nullable=False),
    Column("service_name",  String(100), nullable=False),
    Column("service_date",  Date,        nullable=False),
    Column("service_hour",  Integer),
    Column("remarks",       Text,        server_default=""),
    Column("created_by",    String(100)),
    Column("created_at",    DateTime,    server_default=func.now()),
)

services_table = Table(
    "services", metadata,
    Column("id",          Integer, primary_key=True, autoincrement=True),
    Column("name",        String(100), unique=True, nullable=False),
    Column("category",    String(50)),
    Column("description", Text,        server_default=""),
    Column("is_active",   Integer,     server_default="1"),
)

users_table = Table(
    "users", metadata,
    Column("username", String(50),  primary_key=True),
    Column("password", String(64),  nullable=False),
    Column("role",     String(20),  nullable=False),
    Column("name",     String(150), nullable=False),
    Column("office",   String(100)),
    Column("status",   String(20),  server_default="Active"),
)

uploaded_files_table = Table(
    "uploaded_files", metadata,
    Column("id",          Integer, primary_key=True, autoincrement=True),
    Column("filename",    String(255), nullable=False),
    Column("file_data",   LargeBinary, nullable=False),
    Column("file_size",   Integer,     nullable=False),
    Column("office",      String(100)),
    Column("uploaded_by", String(100)),
    Column("uploaded_at", DateTime,    server_default=func.now()),
)


def init_tables():
    """Create all tables if they don't exist (works on any SQL dialect)."""
    metadata.create_all(engine())


# ── Seeding ──────────────────────────────────────────────────────────────────

def seed_defaults():
    """Insert default users and services if tables are empty."""
    from data import hash_password
    from constants import OFFICES

    eng = engine()

    with eng.begin() as conn:
        # Seed users if empty
        count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
        if count == 0:
            demo = [
                ("admin",     hash_password("admin123"),   "Admin", "System Administrator",  None,                     "Active"),
                ("staff",     hash_password("staff123"),   "Staff", "Guidance Staff",         "Guidance Counseling",    "Active"),
                ("library",   hash_password("lib123"),     "Staff", "Library Staff",           "Library",               "Active"),
                ("clinic",    hash_password("clinic123"),  "Staff", "Clinic Staff",            "Clinic / Medical",      "Active"),
                ("registrar", hash_password("reg123"),     "Staff", "Registrar Staff",         "Registrar",             "Active"),
                ("osaa",      hash_password("osaa123"),    "Staff", "OSAA Staff",              "OSAA / Student Affairs","Active"),
                ("cashier",   hash_password("cash123"),    "Staff", "Cashier Staff",           "Cashier",               "Active"),
                ("ictmo",     hash_password("ict123"),     "Staff", "ICTMO Staff",             "ICTMO",                 "Active"),
            ]
            for username, pw, role, name, office, status in demo:
                conn.execute(text(
                    "INSERT INTO users (username, password, role, name, office, status) "
                    "VALUES (:u, :p, :r, :n, :o, :s)"
                ), {"u": username, "p": pw, "r": role, "n": name, "o": office, "s": status})

        # Seed services if empty
        count = conn.execute(text("SELECT COUNT(*) FROM services")).scalar()
        if count == 0:
            categories = ["Academic", "Academic", "Health", "Enrollment",
                          "Student Life", "Enrollment", "Academic"]
            for office, cat in zip(OFFICES, categories):
                conn.execute(text(
                    "INSERT INTO services (name, category, description, is_active) "
                    "VALUES (:n, :c, :d, 1)"
                ), {"n": office, "c": cat, "d": f"Services provided by {office}"})
