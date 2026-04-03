"""
pages/about.py — About page for ServiSense
"""

import streamlit as st
from ui_components import page_header


def render():
    page_header("ℹ️", "About ServiSense",
                "Student Services Utilization and Performance Analytics System")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
### System Overview
ServiSense is a comprehensive web-based analytics platform designed to monitor, analyze, and improve the delivery of student services across university offices.

### Key Features
| Feature | Description |
|---------|-------------|
| 📊 Dashboard | KPI metrics, service distribution, peak hours, monthly trends |
| 📋 Service Records | View, filter, edit, delete · Export to PDF and Excel |
| ➕ Add Record | Per-office manual record entry with validation |
| 📤 Upload Records | Batch CSV/Excel import with preview and validation |
| 📈 Analytics | Deep-dive analysis: trends, peak hours, department breakdown |
| ⚙️ System Settings | Admin service catalog management |
| 👥 User Management | Staff accounts, roles, password reset, activate/deactivate |

### User Roles
| Role | Access |
|------|--------|
| **Admin** | Full system access — all offices, analytics, settings |
| **Staff** | Own office only — add records, upload files, view reports |

### Demo Accounts
| Username | Password | Office |
|----------|----------|--------|
| admin | admin123 | All Offices |
| staff | staff123 | Guidance Counseling |
| library | lib123 | Library |
| clinic | clinic123 | Clinic / Medical |
| registrar | reg123 | Registrar |
| osaa | osaa123 | OSAA / Student Affairs |
| cashier | cash123 | Cashier |
| ictmo | ict123 | ICTMO |

### Technology Stack
**Frontend** · Streamlit &nbsp;·&nbsp; **Visualization** · Plotly  
**Data Processing** · Pandas &nbsp;·&nbsp; **Export** · FPDF2, OpenPyXL

### Development Team
Magno, Frederick B. · Malubag, John Paul B. · Meris, Shian Michael S.  
Mosada, Jerome D. · Nerona, Gelo Andrei J. · Odato, C.J. P.
""")
    st.markdown('</div>', unsafe_allow_html=True)
