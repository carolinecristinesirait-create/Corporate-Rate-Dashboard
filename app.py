# =============================================================
# Dashboard Corporate Rate Hotel Pertamina 2026
# Streamlit single-file application
# Author: Generated for user request
# =============================================================

from __future__ import annotations

import io
import math
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =============================================================
# 1. CONFIGURATION
# =============================================================

APP_TITLE = "Dashboard Corporate Rate Hotel Pertamina 2026"
APP_SUBTITLE = "Executive pricing intelligence untuk perpanjangan kontrak hotel"
# Google Sheets data source.
# Spreadsheet must be shared as: Anyone with the link -> Viewer.
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1aydlmGDgVhGDFgxgLeciUDBvbgCA3Z-dBSOYu6pQ8aU/edit?usp=sharing"
GOOGLE_SHEET_ID = "1aydlmGDgVhGDFgxgLeciUDBvbgCA3Z-dBSOYu6pQ8aU"

# Kosongkan dulu supaya aplikasi membaca tab pertama yang aktif.
# Kalau data bukan di tab pertama, isi angka setelah gid= dari URL tab Google Sheets.
# Contoh: .../edit#gid=123456789  ->  GOOGLE_SHEET_GID = "123456789"
GOOGLE_SHEET_GID = ""


def build_google_sheet_csv_urls(sheet_id: str, gid: str = "") -> List[str]:
    """Build several Google Sheets CSV URLs so the app is not stuck on one endpoint."""
    gid = str(gid or "").strip()
    base = f"https://docs.google.com/spreadsheets/d/{sheet_id}"

    urls: List[str] = []

    # Best default: no gid. Google returns the first visible sheet, even when gid=0 is invalid.
    urls.append(f"{base}/export?format=csv")
    urls.append(f"{base}/gviz/tq?tqx=out:csv")

    # If a gid is provided, try gid-specific endpoints too.
    if gid:
        urls.insert(0, f"{base}/export?format=csv&id={sheet_id}&gid={gid}")
        urls.insert(1, f"{base}/export?format=csv&gid={gid}")
        urls.insert(2, f"{base}/gviz/tq?tqx=out:csv&gid={gid}")
        urls.append(f"{base}/pub?gid={gid}&single=true&output=csv")

    # Remove duplicates while preserving order.
    return list(dict.fromkeys(urls))


GOOGLE_SHEETS_CSV_URLS = build_google_sheet_csv_urls(GOOGLE_SHEET_ID, GOOGLE_SHEET_GID)
GOOGLE_SHEETS_CSV_URL = GOOGLE_SHEETS_CSV_URLS[0]


REQUIRED_COLUMNS = [
    "No",
    "Group/ Non Group",
    "Nama Group/ Non Group",
    "City",
    "Nama Hotel",
    "Email",
    "Publish Rate",
    "Offering Corporate Rate 2026",
    "Nilai Selisih",
    "Result",
    "Next Action",
    "Checking Remarks",
    "Status",
]

COLORS = {
    "navy": "#002B5B",
    "navy_2": "#003E7E",
    "blue": "#0066B3",
    "light_blue": "#EAF4FF",
    "red": "#E31E24",
    "light_red": "#FFECEC",
    "green": "#008E5A",
    "green_2": "#00A859",
    "light_green": "#EAFBF3",
    "yellow": "#FDB913",
    "orange": "#F59E0B",
    "light_yellow": "#FFF7E0",
    "teal": "#007C7A",
    "gray": "#65758B",
    "light_gray": "#F5F7FA",
    "white": "#FFFFFF",
    "black": "#0F172A",
}

COLORWAY = [
    COLORS["navy"],
    COLORS["green"],
    COLORS["yellow"],
    COLORS["blue"],
    COLORS["red"],
    COLORS["teal"],
    "#8B5CF6",
    "#64748B",
]

CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "dashboard_corporate_rate_hotel_pertamina_2026",
        "height": 900,
        "width": 1600,
        "scale": 2,
    },
}

PAGE_OPTIONS = [
    "01 Executive Overview",
    "02 Regional Analysis",
    "03 Group Performance",
    "04 Top Opportunity Hotels",
    "05 Price Gap Analytics",
    "06 Revise Priority",
    "07 Action Tracker",
    "08 Hotel Explorer",
    "09 Data Quality",
    "10 Executive Recommendations",
]

PAGE_ICONS = {
    "01 Executive Overview": "🏠",
    "02 Regional Analysis": "🌏",
    "03 Group Performance": "👥",
    "04 Top Opportunity Hotels": "⭐",
    "05 Price Gap Analytics": "📈",
    "06 Revise Priority": "🎯",
    "07 Action Tracker": "🗂️",
    "08 Hotel Explorer": "🔎",
    "09 Data Quality": "🧱",
    "10 Executive Recommendations": "💡",
}

# Coordinate point for province-level map. City in the data behaves like province/region.
PROVINCE_COORDS = {
    "Aceh": (4.6951, 96.7494),
    "Bali": (-8.4095, 115.1889),
    "Banten": (-6.4058, 106.0640),
    "Bengkulu": (-3.7928, 102.2608),
    "DI Yogyakarta": (-7.8754, 110.4262),
    "DKI Jakarta": (-6.2088, 106.8456),
    "Gorontalo": (0.5435, 123.0568),
    "Jambi": (-1.6101, 103.6131),
    "Jawa Barat": (-6.9175, 107.6191),
    "Jawa Tengah": (-7.1509, 110.1403),
    "Jawa Timur": (-7.5361, 112.2384),
    "Kalimantan Barat": (-0.2788, 111.4753),
    "Kalimantan Selatan": (-3.0926, 115.2838),
    "Kalimantan Tengah": (-1.6815, 113.3824),
    "Kalimantan Timur": (0.5387, 116.4194),
    "Kalimantan Utara": (3.0731, 116.0414),
    "Kepulauan Bangka Belitung": (-2.7411, 106.4406),
    "Kepulauan Riau": (3.9457, 108.1429),
    "Lampung": (-4.5586, 105.4068),
    "Maluku": (-3.2385, 130.1453),
    "Nusa Tenggara Barat": (-8.6529, 117.3616),
    "Nusa Tenggara Timur": (-8.6574, 121.0794),
    "Papua": (-4.2699, 138.0804),
    "Papua Barat": (-1.3361, 133.1747),
    "Riau": (0.2933, 101.7068),
    "Sulawesi Selatan": (-3.6688, 119.9741),
    "Sulawesi Tengah": (-1.4300, 121.4456),
    "Sulawesi Tenggara": (-4.1449, 122.1746),
    "Sulawesi Utara": (1.4931, 124.8413),
    "Sumatera Barat": (-0.7399, 100.8000),
    "Sumatera Selatan": (-3.3194, 103.9144),
    "Sumatera Utara": (2.1154, 99.5451),
}


# =============================================================
# 2. PAGE SETUP AND CSS
# =============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    """Inject polished Pertamina-style CSS with a dark blue gradient canvas and clean white cards."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {{
            --pertamina-navy: {COLORS['navy']};
            --pertamina-blue: {COLORS['blue']};
            --pertamina-green: {COLORS['green_2']};
            --pertamina-red: {COLORS['red']};
            --pertamina-yellow: {COLORS['yellow']};
            --ink: #0B1F3A;
            --muted: #64748B;
            --card: rgba(255,255,255,.96);
            --card-border: rgba(226,232,240,.75);
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 8% 6%, rgba(0,168,89,.34) 0, transparent 25%),
                radial-gradient(circle at 94% 9%, rgba(227,30,36,.22) 0, transparent 24%),
                radial-gradient(circle at 70% 90%, rgba(0,102,179,.30) 0, transparent 30%),
                linear-gradient(135deg, #00152F 0%, #003B73 42%, #005F73 78%, #007C59 100%);
            color: var(--ink);
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px),
                linear-gradient(180deg, rgba(255,255,255,.025) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,.65), transparent 70%);
        }}

        .main .block-container {{
            padding-top: 1.1rem;
            padding-left: 1.55rem;
            padding-right: 1.55rem;
            padding-bottom: 2rem;
            max-width: 1600px;
        }}

        h1, h2, h3, h4, h5, h6, p, span, label {{
            letter-spacing: -0.015em;
        }}

        h1, h2, h3 {{
            color: var(--ink);
            font-weight: 900;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background:
                radial-gradient(circle at 20% 15%, rgba(0,168,89,.28), transparent 27%),
                radial-gradient(circle at 90% 2%, rgba(227,30,36,.20), transparent 22%),
                linear-gradient(180deg, #001C43 0%, #002B5B 55%, #001A3D 100%);
            border-right: 1px solid rgba(255,255,255,.12);
            box-shadow: 16px 0 45px rgba(0,0,0,.20);
        }}
        section[data-testid="stSidebar"] * {{
            color: #EAF4FF !important;
        }}
        section[data-testid="stSidebar"] .stRadio label {{
            background: transparent;
            border-radius: 14px;
            padding: 5px 8px;
            transition: all .18s ease;
        }}
        section[data-testid="stSidebar"] .stRadio label:hover {{
            background: rgba(255,255,255,.09);
            transform: translateX(2px);
        }}
        section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
            background: linear-gradient(90deg, rgba(0,102,179,.95), rgba(0,168,89,.70));
            box-shadow: 0 10px 22px rgba(0,0,0,.18);
        }}
        section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
            color: #0F172A !important;
        }}

        .logo-wrap {{
            display:flex;
            gap:13px;
            align-items:center;
            padding: 10px 2px 24px 2px;
            border-bottom: 1px solid rgba(255,255,255,.16);
            margin-bottom: 16px;
        }}
        .logo-bars {{
            width:44px;
            height:44px;
            display:grid;
            grid-template-columns: repeat(3, 1fr);
            gap:5px;
            align-items:end;
        }}
        .logo-bars span {{
            display:block;
            border-radius: 9px 9px 5px 5px;
            box-shadow: 0 12px 24px rgba(0,0,0,.26);
        }}
        .logo-bars span:nth-child(1) {{ height: 24px; background: var(--pertamina-blue); }}
        .logo-bars span:nth-child(2) {{ height: 39px; background: var(--pertamina-green); }}
        .logo-bars span:nth-child(3) {{ height: 31px; background: var(--pertamina-red); }}
        .logo-text-title {{
            font-weight: 900;
            line-height: 1.08;
            color: #FFFFFF !important;
            font-size: 1.03rem;
        }}
        .logo-text-sub {{
            font-weight: 650;
            color: rgba(255,255,255,.78) !important;
            font-size: .72rem;
            margin-top: 4px;
        }}

        /* Header */
        .page-title {{
            background:
                radial-gradient(circle at 84% 8%, rgba(253,185,19,.24), transparent 23%),
                radial-gradient(circle at 7% 10%, rgba(0,168,89,.26), transparent 20%),
                linear-gradient(95deg, rgba(0,27,68,.98) 0%, rgba(0,68,128,.95) 50%, rgba(0,124,89,.92) 100%);
            border: 1px solid rgba(255,255,255,.22);
            border-radius: 26px;
            padding: 24px 28px;
            margin: 0 0 18px 0;
            box-shadow: 0 24px 60px rgba(0,0,0,.20);
            position: relative;
            overflow: hidden;
        }}
        .page-title::after {{
            content:"";
            position:absolute;
            inset:0;
            background: linear-gradient(110deg, transparent 0%, rgba(255,255,255,.12) 45%, transparent 70%);
            transform: translateX(-70%);
        }}
        .page-title h1 {{
            color: #FFFFFF !important;
            margin: 0;
            font-weight: 900;
            font-size: clamp(1.55rem, 2.2vw, 2.25rem);
            line-height: 1.08;
            position: relative;
            z-index: 1;
        }}
        .page-title p {{
            color: rgba(255,255,255,.86) !important;
            margin: 8px 0 0 0;
            font-weight: 650;
            font-size: .95rem;
            position: relative;
            z-index: 1;
        }}

        /* Filter card */
        .filter-card {{
            background: rgba(255,255,255,.90);
            backdrop-filter: blur(18px);
            border: 1px solid rgba(255,255,255,.45);
            box-shadow: 0 18px 40px rgba(0,0,0,.16);
            border-radius: 22px;
            padding: 16px 18px;
            margin-bottom: 18px;
        }}
        div[data-baseweb="select"] > div {{
            border-radius: 13px !important;
            border-color: rgba(0,43,91,.14) !important;
            box-shadow: 0 6px 16px rgba(15,23,42,.05) !important;
        }}

        /* Streamlit border containers: make them look like dashboard cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255,255,255,.96) !important;
            border: 1px solid rgba(226,232,240,.78) !important;
            border-radius: 24px !important;
            box-shadow: 0 20px 48px rgba(0,0,0,.14) !important;
            backdrop-filter: blur(16px);
        }}

        .section-card {{
            background: rgba(255,255,255,.96);
            border: 1px solid rgba(226,232,240,.78);
            border-radius: 24px;
            padding: 18px;
            box-shadow: 0 20px 48px rgba(0,0,0,.14);
            margin-bottom: 18px;
        }}
        .section-heading {{
            color: var(--ink) !important;
            font-weight: 900;
            font-size: 1.04rem;
            margin: 0 0 .65rem 0;
            display:flex;
            align-items:center;
            gap:.62rem;
        }}
        .section-heading .dot {{
            width: 12px;
            height: 12px;
            background: linear-gradient(135deg, var(--pertamina-red), var(--pertamina-green));
            border-radius:50%;
            display:inline-block;
            box-shadow: 0 0 0 4px rgba(0,168,89,.10);
        }}

        /* KPI cards */
        .kpi-card {{
            background:
                linear-gradient(180deg, rgba(255,255,255,.98), rgba(245,249,255,.96));
            border: 1px solid rgba(255,255,255,.65);
            border-radius: 23px;
            padding: 17px 17px 15px 17px;
            min-height: 132px;
            box-shadow: 0 20px 45px rgba(0,0,0,.15);
            position: relative;
            overflow: hidden;
        }}
        .kpi-card::before {{
            content:"";
            position:absolute;
            left:0;
            right:0;
            top:0;
            height:4px;
            background: linear-gradient(90deg, var(--pertamina-blue), var(--pertamina-green), var(--pertamina-red));
        }}
        .kpi-card::after {{
            content:"";
            position:absolute;
            width:165px;
            height:165px;
            right:-96px;
            top:-98px;
            border-radius:50%;
            background: rgba(0,102,179,.10);
        }}
        .kpi-card.kpi-green::after {{ background: rgba(0,168,89,.13); }}
        .kpi-card.kpi-red::after {{ background: rgba(227,30,36,.12); }}
        .kpi-card.kpi-yellow::after {{ background: rgba(253,185,19,.18); }}
        .kpi-card.kpi-navy::after {{ background: rgba(0,43,91,.13); }}
        .kpi-icon {{
            width: 46px;
            height: 46px;
            border-radius: 16px;
            display:flex;
            align-items:center;
            justify-content:center;
            background: linear-gradient(135deg, #001B44 0%, var(--pertamina-blue) 100%);
            color: #fff !important;
            font-size: 1.12rem;
            font-weight: 900;
            box-shadow: 0 12px 24px rgba(0,43,91,.20);
        }}
        .kpi-green .kpi-icon {{ background: linear-gradient(135deg, #007C57, var(--pertamina-green)); }}
        .kpi-red .kpi-icon {{ background: linear-gradient(135deg, #B91C1C, var(--pertamina-red)); }}
        .kpi-yellow .kpi-icon {{ background: linear-gradient(135deg, #D97706, var(--pertamina-yellow)); }}
        .kpi-navy .kpi-icon {{ background: linear-gradient(135deg, #001B44, var(--pertamina-blue)); }}
        .kpi-label {{
            font-size: .72rem;
            color: var(--muted) !important;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: .06em;
            margin-top: 11px;
        }}
        .kpi-value {{
            color: var(--ink) !important;
            font-size: clamp(1.22rem, 1.8vw, 1.72rem);
            font-weight: 900;
            line-height: 1.08;
            margin-top: 4px;
            white-space: nowrap;
        }}
        .kpi-note {{
            color: var(--muted) !important;
            font-size: .76rem;
            font-weight: 650;
            margin-top: 7px;
        }}

        .insight-card {{
            border-radius: 22px;
            padding: 18px;
            background: linear-gradient(135deg, #FFFFFF 0%, #F4FAFF 100%);
            border: 1px solid rgba(226,232,240,.85);
            box-shadow: 0 18px 40px rgba(0,0,0,.12);
            height: 100%;
        }}
        .insight-title {{
            color: var(--ink) !important;
            font-weight: 900;
            font-size: .98rem;
            margin-bottom: 6px;
        }}
        .insight-body {{
            color: #475569 !important;
            font-size: .9rem;
            line-height: 1.5;
        }}
        .pill {{
            display:inline-flex;
            align-items:center;
            gap: 6px;
            border-radius: 999px;
            padding: 5px 10px;
            font-weight: 900;
            font-size: .75rem;
            border: 1px solid rgba(0,43,91,.08);
            background: #EFF6FF;
            color: var(--ink) !important;
        }}
        .pill-green {{ background: {COLORS['light_green']}; color: {COLORS['green']} !important; }}
        .pill-red {{ background: {COLORS['light_red']}; color: {COLORS['red']} !important; }}
        .pill-yellow {{ background: {COLORS['light_yellow']}; color: #B45309 !important; }}

        .footer-band {{
            background: linear-gradient(90deg, #001B44, #0066B3, #007C59);
            color: white !important;
            border-radius: 20px;
            padding: 17px 18px;
            font-weight: 800;
            box-shadow: 0 18px 38px rgba(0,0,0,.18);
            margin-top: 8px;
        }}

        div[data-testid="stMetricValue"] {{ color: #FFFFFF !important; }}
        div[data-testid="stMetricLabel"] {{ color: rgba(255,255,255,.78) !important; }}
        div[data-testid="stMetricDelta"] {{ color: #D1FAE5 !important; }}

        .stCaption, div[data-testid="stCaptionContainer"] p {{
            color: rgba(255,255,255,.82) !important;
            font-weight: 600;
        }}

        .stDataFrame {{
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 10px 24px rgba(15,23,42,.08);
        }}
        .dataframe th {{
            background-color: var(--pertamina-navy) !important;
            color: white !important;
        }}

        div[data-testid="stDownloadButton"] button,
        div[data-testid="stButton"] button {{
            border-radius: 13px;
            border: 1px solid rgba(0,43,91,.14);
            background: linear-gradient(135deg, #001B44 0%, #0066B3 100%);
            color: white !important;
            font-weight: 800;
        }}
        div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stButton"] button:hover {{
            border-color: var(--pertamina-green);
            box-shadow: 0 12px 24px rgba(0,102,179,.22);
        }}

        /* Plotly: force readable labels. This fixes white/washed-out chart text. */
        .js-plotly-plot .plotly text {{
            fill: #0B1F3A !important;
            font-family: 'Inter', Arial, sans-serif !important;
            font-weight: 650 !important;
        }}
        .js-plotly-plot .legendtext {{
            fill: #0B1F3A !important;
            font-size: 12px !important;
        }}
        .js-plotly-plot .gtitle {{
            display: none !important;
        }}

        @media (max-width: 1100px) {{
            .main .block-container {{ padding-left: .85rem; padding-right: .85rem; }}
            .page-title {{ padding: 20px; }}
            .kpi-card {{ min-height: 118px; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================
# 3. DATA LOADING AND PREPROCESSING
# =============================================================


def _download_csv_bytes(csv_url: str) -> bytes:
    """Download CSV with a browser-like header; Google can reject plain urllib requests."""
    request = urllib.request.Request(
        csv_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            "Accept": "text/csv,application/csv,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _looks_like_google_error(content: bytes) -> bool:
    sample = content[:500].decode("utf-8", errors="ignore").lower()
    return any(
        marker in sample
        for marker in [
            "<html",
            "<!doctype html",
            "servicelogin",
            "accounts.google",
            "document is not published",
            "sorry, unable to open",
        ]
    )


@st.cache_data(ttl=300, show_spinner=False)
def cached_read_google_sheets(csv_urls: Tuple[str, ...]) -> pd.DataFrame:
    """Read dashboard data directly from Google Sheets CSV export.

    The loader tries multiple official Google Sheets CSV endpoints because
    /export?format=csv&gid=0 can return HTTP 400 when gid=0 is not the
    actual visible sheet id.
    """
    errors: List[str] = []

    for csv_url in csv_urls:
        try:
            content = _download_csv_bytes(csv_url)
            if not content or _looks_like_google_error(content):
                raise ValueError("Google returned an HTML/error page, not CSV data.")

            frame = pd.read_csv(io.BytesIO(content))
            if frame.empty:
                raise ValueError("CSV berhasil dibuka, tetapi datanya kosong.")
            return frame
        except Exception as exc:
            errors.append(f"{csv_url} -> {type(exc).__name__}: {exc}")

    raise RuntimeError(
        "Semua endpoint Google Sheets gagal dibaca. Detail percobaan:\n"
        + "\n".join(errors)
    )


def clean_text_series(series: pd.Series) -> pd.Series:
    """Clean object columns without accidentally converting missing values to literal 'nan'."""
    return (
        series.astype("string")
        .str.replace("\u00a0", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def normalize_result(value: object) -> str:
    text = str(value).replace("\u00a0", " ").strip().lower()
    if text.startswith("recommend") or text.startswith("rekomend"):
        return "Recommend"
    if text.startswith("revise") or text.startswith("revisi"):
        return "Revise"
    if text in {"same", "sama"}:
        return "Sama"
    return text.title() if text and text != "nan" else "Tidak Ada"


def normalize_action(value: object) -> str:
    text = str(value).replace("\u00a0", " ").strip().lower()
    if "sign" in text or "kontrak" in text:
        return "Sign Kontrak"
    if "review" in text or "revise" in text or "revisi" in text:
        return "Review Rate"
    if "maintain" in text or "done" in text or "selesai" in text:
        return "Done"
    return text.title() if text and text != "nan" else "Belum Ditentukan"


def clean_dataframe(raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Validate, clean, enrich and return dashboard-ready data."""
    data = raw.copy()
    data.columns = [str(c).replace("\u00a0", " ").strip() for c in data.columns]

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing_cols:
        st.error("Kolom wajib tidak ditemukan: " + ", ".join(missing_cols))
        st.stop()

    data = data[REQUIRED_COLUMNS].copy()
    data["Result Raw"] = data["Result"].astype("string")
    data["Next Action Raw"] = data["Next Action"].astype("string")

    # Clean regular text fields. Keep Result Raw and Next Action Raw untouched
    # so Data Quality can detect whitespace/category issues from the original file.
    text_cols = [
        "Group/ Non Group",
        "Nama Group/ Non Group",
        "City",
        "Nama Hotel",
        "Email",
        "Checking Remarks",
        "Status",
    ]
    for col in text_cols:
        data[col] = clean_text_series(data[col])

    for col in ["Publish Rate", "Offering Corporate Rate 2026", "Nilai Selisih"]:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    data["Result"] = data["Result Raw"].apply(normalize_result)
    data["Next Action"] = data["Next Action Raw"].apply(normalize_action)
    data["Group/ Non Group"] = data["Group/ Non Group"].fillna("Tidak Ada").replace("", "Tidak Ada")
    data["Nama Group/ Non Group"] = data["Nama Group/ Non Group"].fillna("Tidak Ada").replace("", "Tidak Ada")
    data["City"] = data["City"].fillna("Tidak Ada").replace("", "Tidak Ada")
    data["Nama Hotel"] = data["Nama Hotel"].fillna("Tidak Ada").replace("", "Tidak Ada")

    email = data["Email"].fillna("").astype(str).str.strip()
    remarks = data["Checking Remarks"].fillna("").astype(str).str.strip()
    data["Email Missing"] = email.isin(["", "-", "nan", "None", "NaN"])
    data["Remarks Missing"] = remarks.isin(["", "-", "nan", "None", "NaN"])

    data["Is Recommend"] = data["Result"].eq("Recommend")
    data["Is Revise"] = data["Result"].eq("Revise")
    data["Is Sign Kontrak"] = data["Next Action"].eq("Sign Kontrak")
    data["Is Positive Gap"] = data["Nilai Selisih"] > 0
    data["Is Negative Gap"] = data["Nilai Selisih"] < 0
    data["Is Same Rate"] = data["Nilai Selisih"].eq(0)

    data["Corporate Status"] = np.select(
        [data["Nilai Selisih"] > 0, data["Nilai Selisih"] < 0, data["Nilai Selisih"].eq(0)],
        ["Corporate Lebih Murah", "Corporate Lebih Mahal", "Sama dengan Publish"],
        default="Tidak Ada",
    )
    data["Gap Band"] = np.select(
        [
            data["Nilai Selisih"] < 0,
            data["Nilai Selisih"].eq(0),
            (data["Nilai Selisih"] > 0) & (data["Nilai Selisih"] <= 100_000),
            (data["Nilai Selisih"] > 100_000) & (data["Nilai Selisih"] <= 300_000),
            (data["Nilai Selisih"] > 300_000) & (data["Nilai Selisih"] <= 500_000),
            data["Nilai Selisih"] > 500_000,
        ],
        ["Negatif", "Sama", "0-100rb", "100-300rb", "300-500rb", ">500rb"],
        default="Tidak Ada",
    )
    data["Discount vs Publish %"] = np.where(
        data["Publish Rate"] > 0,
        data["Nilai Selisih"] / data["Publish Rate"],
        0,
    )
    data["Corporate Rate Ratio"] = np.where(
        data["Publish Rate"] > 0,
        data["Offering Corporate Rate 2026"] / data["Publish Rate"],
        np.nan,
    )
    data["Priority"] = np.select(
        [
            data["Nilai Selisih"] < 0,
            data["Is Revise"] & (data["Nilai Selisih"] >= 0) & (data["Nilai Selisih"] <= 100_000),
            data["Is Sign Kontrak"],
            data["Is Recommend"] & (data["Nilai Selisih"] > 500_000),
            data["Is Recommend"],
        ],
        [
            "P1 - Urgent Negative",
            "P2 - Revise Positive",
            "P3 - Sign Kontrak",
            "Maintain High Opportunity",
            "Maintain Rate",
        ],
        default="Review Manual",
    )

    # SLA is synthetic because the source file has no date. It is used only as a tracking indicator.
    data["SLA Status"] = np.select(
        [data["Priority"].eq("P1 - Urgent Negative"), data["Priority"].eq("P3 - Sign Kontrak")],
        ["Critical", "On Track"],
        default="Completed",
    )

    # Add coordinates for map page.
    data["Latitude"] = data["City"].map(lambda x: PROVINCE_COORDS.get(str(x), (np.nan, np.nan))[0])
    data["Longitude"] = data["City"].map(lambda x: PROVINCE_COORDS.get(str(x), (np.nan, np.nan))[1])

    raw_result_counts = data["Result Raw"].value_counts(dropna=False).to_dict()
    raw_result_string = data["Result Raw"].astype(str).str.replace("\u00a0", " ", regex=False)
    result_whitespace_issue = int((raw_result_string != raw_result_string.str.strip()).sum())

    metadata = {
        "rows": len(data),
        "columns": list(data.columns),
        "raw_result_counts": raw_result_counts,
        "result_whitespace_issue": result_whitespace_issue,
        "missing_email": int(data["Email Missing"].sum()),
        "missing_remarks": int(data["Remarks Missing"].sum()),
    }
    return data, metadata


# =============================================================
# 4. FORMATTERS AND HELPERS
# =============================================================


def format_number(value: float, decimals: int = 0) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:,.{decimals}f}".replace(",", ".")


def format_rupiah(value: float, compact: bool = True, decimals: int = 1) -> str:
    if value is None or pd.isna(value):
        return "Rp-"
    sign = "-" if value < 0 else ""
    abs_value = abs(float(value))
    if compact:
        if abs_value >= 1_000_000_000:
            return f"{sign}Rp{abs_value / 1_000_000_000:.{decimals}f}B"
        if abs_value >= 1_000_000:
            return f"{sign}Rp{abs_value / 1_000_000:.{decimals}f}M"
        if abs_value >= 1_000:
            return f"{sign}Rp{abs_value / 1_000:.{decimals}f}K"
    return f"{sign}Rp{abs_value:,.0f}".replace(",", ".")


def format_pct(value: float, decimals: int = 1) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value * 100:.{decimals}f}%"


def safe_div(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def option_list(series: pd.Series, label_all: str = "Semua") -> List[str]:
    values = sorted([str(x) for x in series.dropna().unique() if str(x).strip()])
    return [label_all] + values


def selected_filter(data: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    if value and value != "Semua":
        return data[data[column].astype(str).eq(str(value))]
    return data


def selected_multi_filter(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    if values:
        return data[data[column].astype(str).isin(values)]
    return data


def sort_table(data: pd.DataFrame, by: str, ascending: bool = False, n: Optional[int] = None) -> pd.DataFrame:
    if data.empty or by not in data.columns:
        return data.head(0)
    out = data.sort_values(by=by, ascending=ascending)
    return out.head(n) if n else out


def aggregate_by(data: pd.DataFrame, group_col: str) -> pd.DataFrame:
    if data.empty:
        return pd.DataFrame(
            columns=[
                group_col,
                "Jumlah Hotel",
                "Total Selisih",
                "Avg Selisih",
                "Avg Publish Rate",
                "Avg Corporate Rate",
                "Recommend",
                "Revise",
                "Negative",
                "Sign Kontrak",
                "Missing Email",
                "Missing Remarks",
                "Revise Rate",
                "Negative Rate",
                "Avg Discount %",
            ]
        )

    agg = (
        data.groupby(group_col, dropna=False)
        .agg(
            **{
                "Jumlah Hotel": ("Nama Hotel", "count"),
                "Total Selisih": ("Nilai Selisih", "sum"),
                "Avg Selisih": ("Nilai Selisih", "mean"),
                "Avg Publish Rate": ("Publish Rate", "mean"),
                "Avg Corporate Rate": ("Offering Corporate Rate 2026", "mean"),
                "Recommend": ("Is Recommend", "sum"),
                "Revise": ("Is Revise", "sum"),
                "Negative": ("Is Negative Gap", "sum"),
                "Sign Kontrak": ("Is Sign Kontrak", "sum"),
                "Missing Email": ("Email Missing", "sum"),
                "Missing Remarks": ("Remarks Missing", "sum"),
            }
        )
        .reset_index()
    )
    agg["Revise Rate"] = agg.apply(lambda r: safe_div(r["Revise"], r["Jumlah Hotel"]), axis=1)
    agg["Negative Rate"] = agg.apply(lambda r: safe_div(r["Negative"], r["Jumlah Hotel"]), axis=1)
    agg["Avg Discount %"] = agg.apply(lambda r: safe_div(r["Avg Selisih"], r["Avg Publish Rate"]), axis=1)
    return agg


def kpi_summary(data: pd.DataFrame) -> Dict[str, float]:
    total = len(data)
    positive_gap = data.loc[data["Nilai Selisih"] > 0, "Nilai Selisih"].sum() if total else 0
    negative_gap = data.loc[data["Nilai Selisih"] < 0, "Nilai Selisih"].sum() if total else 0
    return {
        "total": total,
        "recommend": int(data["Is Recommend"].sum()) if total else 0,
        "revise": int(data["Is Revise"].sum()) if total else 0,
        "positive_count": int((data["Nilai Selisih"] > 0).sum()) if total else 0,
        "negative_count": int((data["Nilai Selisih"] < 0).sum()) if total else 0,
        "same_count": int((data["Nilai Selisih"] == 0).sum()) if total else 0,
        "sign_kontrak": int(data["Is Sign Kontrak"].sum()) if total else 0,
        "total_gap": float(data["Nilai Selisih"].sum()) if total else 0,
        "positive_gap": float(positive_gap),
        "negative_gap": float(negative_gap),
        "avg_gap": float(data["Nilai Selisih"].mean()) if total else 0,
        "avg_publish": float(data["Publish Rate"].mean()) if total else 0,
        "avg_corporate": float(data["Offering Corporate Rate 2026"].mean()) if total else 0,
        "missing_email": int(data["Email Missing"].sum()) if total else 0,
        "missing_remarks": int(data["Remarks Missing"].sum()) if total else 0,
        "group_count": int(data["Nama Group/ Non Group"].nunique()) if total else 0,
        "city_count": int(data["City"].nunique()) if total else 0,
    }


def style_numeric_table(data: pd.DataFrame) -> pd.DataFrame:
    """Return a display copy with readable money and percentage formats.

    Important: columns such as Revise Rate and Negative Rate are percentages,
    while Publish Rate and Corporate Rate are money columns.
    """
    out = data.copy()
    money_cols = []
    pct_cols = []
    for c in out.columns:
        cl = c.lower()
        is_money = (
            "selisih" in cl
            or "publish rate" in cl
            or "corporate rate" in cl
            or "opportunity" in cl
        )
        is_pct = (
            "%" in c
            or "discount" in cl
            or c in {"Revise Rate", "Negative Rate"}
        )
        if is_money:
            money_cols.append(c)
        elif is_pct:
            pct_cols.append(c)

    for col in money_cols:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].map(lambda x: format_rupiah(x, compact=False))
    for col in pct_cols:
        if col in out.columns and pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].map(lambda x: format_pct(x))
    return out


def apply_plot_theme(fig: go.Figure, height: int = 360, show_legend: bool = True) -> go.Figure:
    """Apply a clean, readable corporate chart theme.

    The previous version used transparent plot backgrounds and narrow margins, which made
    axis labels look washed out on light/gradient backgrounds. This version gives every
    chart its own white canvas, darker text, safer margins, and better mobile behavior.
    """
    fig.update_layout(
        template="plotly_white",
        height=height,
        autosize=True,
        margin=dict(l=88, r=92, t=18, b=56),
        font=dict(family="Inter, Arial, sans-serif", color="#0B1F3A", size=12),
        title=None,
        paper_bgcolor="rgba(255,255,255,0.98)",
        plot_bgcolor="rgba(248,251,255,0.98)",
        colorway=COLORWAY,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0)",
            font=dict(color="#0B1F3A", size=11),
        ),
        showlegend=show_legend,
        hoverlabel=dict(
            bgcolor="#0B1F3A",
            bordercolor="rgba(255,255,255,.45)",
            font=dict(color="#FFFFFF", family="Inter, Arial, sans-serif", size=12),
        ),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,.25)",
        zeroline=False,
        linecolor="rgba(15,23,42,.18)",
        tickfont=dict(color="#334155", size=11),
        title_font=dict(color="#334155", size=12),
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=False,
        gridcolor="rgba(148,163,184,.18)",
        zeroline=False,
        linecolor="rgba(15,23,42,.18)",
        tickfont=dict(color="#334155", size=11),
        title_font=dict(color="#334155", size=12),
        automargin=True,
    )
    return fig


def kpi_card(label: str, value: str, note: str = "", icon: str = "📌", color: str = "navy") -> None:
    st.markdown(
        f"""
        <div class="kpi-card kpi-{color}">
            <div class="kpi-top">
                <div>
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-note">{note}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, icon: str = "") -> None:
    icon_text = f"{icon} " if icon else ""
    st.markdown(
        f"<div class='section-heading'><span class='dot'></span>{icon_text}{title}</div>",
        unsafe_allow_html=True,
    )


def insight_card(title: str, body: str, badge: str = "", badge_type: str = "") -> None:
    badge_html = f"<div style='margin-bottom:10px'><span class='pill {badge_type}'>{badge}</span></div>" if badge else ""
    st.markdown(
        f"""
        <div class="insight-card">
            {badge_html}
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card(title: str, fig: go.Figure, icon: str = "") -> None:
    """Render a chart inside a real Streamlit bordered container so the card is not broken."""
    with st.container(border=True):
        section_header(title, icon)
        st.plotly_chart(fig, use_container_width=True, config=CONFIG)


def dataframe_card(title: str, data: pd.DataFrame, icon: str = "📋", height: int = 330) -> None:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_header(title, icon)
    st.dataframe(data, use_container_width=True, hide_index=True, height=height)
    st.markdown("</div>", unsafe_allow_html=True)


def empty_state(message: str = "Tidak ada data pada filter ini.") -> None:
    st.info(message)


def to_excel_bytes(data: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, index=False, sheet_name="Filtered Data")
    return output.getvalue()




def shorten_label(value: object, max_len: int = 24) -> str:
    """Shorten long category labels for narrow chart columns without changing source data."""
    text = str(value)
    return text if len(text) <= max_len else text[: max_len - 1].rstrip() + "…"


def safe_axis_max(values: pd.Series | np.ndarray, pad: float = 1.24) -> float:
    """Return a padded positive axis maximum for value labels outside bars."""
    if values is None or len(values) == 0:
        return 1.0
    max_value = float(np.nanmax(values)) if len(values) else 1.0
    if not np.isfinite(max_value) or max_value <= 0:
        return 1.0
    return max_value * pad


# =============================================================
# 5. CHART BUILDERS
# =============================================================


def result_donut(data: pd.DataFrame) -> go.Figure:
    """Donut Komposisi Result: besar, bersih, label langsung di dalam slice."""

    order = ["Recommend", "Revise", "Sama"]
    counts = (
        data["Result"]
        .astype(str)
        .str.strip()
        .value_counts()
        .reindex(order, fill_value=0)
        .reset_index()
    )
    counts.columns = ["Result", "Jumlah"]
    counts = counts[counts["Jumlah"] > 0].copy()

    if counts.empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#EAF3FB",
            plot_bgcolor="#EAF3FB",
            annotations=[
                dict(
                    text="Tidak ada data",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(color="#0B1F3A", size=15, family="Inter, Arial, sans-serif"),
                )
            ],
        )
        return fig

    color_map = {
        "Recommend": COLORS["green"],
        "Revise": COLORS["yellow"],
        "Sama": COLORS["blue"],
    }

    text_color_map = {
        "Recommend": "#FFFFFF",
        "Revise": "#0B1F3A",
        "Sama": "#FFFFFF",
    }

    labels = counts["Result"].tolist()
    values = counts["Jumlah"].tolist()
    colors = [color_map.get(label, COLORS["blue"]) for label in labels]
    text_colors = [text_color_map.get(label, "#FFFFFF") for label in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.50,
                sort=False,
                direction="clockwise",
                rotation=90,
                textinfo="label+percent",
                textposition="inside",
                insidetextorientation="radial",
                textfont=dict(
                    family="Inter, Arial, sans-serif",
                    size=18,
                    color=text_colors,
                ),
                marker=dict(
                    colors=colors,
                    line=dict(color="#EAF3FB", width=4),
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Jumlah: %{value:,.0f} hotel<br>"
                    "Persentase: %{percent}<extra></extra>"
                ),
                showlegend=False,
            )
        ]
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#EAF3FB",
        plot_bgcolor="#EAF3FB",
        font=dict(family="Inter, Arial, sans-serif", color="#0B1F3A", size=13),
        uniformtext_minsize=13,
        uniformtext_mode="show",
        hoverlabel=dict(
            bgcolor="#0B1F3A",
            bordercolor="rgba(255,255,255,.5)",
            font=dict(color="#FFFFFF", family="Inter, Arial, sans-serif", size=12),
        ),
    )

    return fig


def gap_band_bar(data: pd.DataFrame, orientation: str = "h") -> go.Figure:
    order = ["Negatif", "Sama", "0-100rb", "100-300rb", "300-500rb", ">500rb"]
    colors = [COLORS["red"], COLORS["gray"], COLORS["yellow"], COLORS["teal"], COLORS["blue"], COLORS["navy"]]
    counts = data["Gap Band"].value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["Band Selisih", "Jumlah Hotel"]
    fig = px.bar(
        counts,
        y="Band Selisih" if orientation == "h" else "Jumlah Hotel",
        x="Jumlah Hotel" if orientation == "h" else "Band Selisih",
        orientation=orientation,
        text="Jumlah Hotel",
        color="Band Selisih",
        color_discrete_map=dict(zip(order, colors)),
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(color="#0B1F3A", size=12, family="Inter, Arial, sans-serif"),
        marker_line_color="rgba(255,255,255,.85)",
        marker_line_width=1.2,
        cliponaxis=False,
        hovertemplate="%{y}<br>Jumlah: %{x:,.0f} hotel<extra></extra>" if orientation == "h" else "%{x}<br>Jumlah: %{y:,.0f} hotel<extra></extra>",
    )
    fig.update_layout(xaxis_title="Jumlah Hotel", yaxis_title="")
    if orientation == "h":
        fig.update_xaxes(range=[0, safe_axis_max(counts["Jumlah Hotel"], 1.22)])
        fig.update_layout(margin=dict(l=118, r=76, t=18, b=44))
    return apply_plot_theme(fig, height=350, show_legend=False)


def horizontal_bar(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str = COLORS["navy"],
    height: int = 360,
    text_format: str = "money",
) -> go.Figure:
    if data.empty:
        return apply_plot_theme(go.Figure(), height=height, show_legend=False)

    ordered = data.sort_values(x, ascending=True).copy()
    ordered["_label_short"] = ordered[y].map(lambda v: shorten_label(v, 28))

    if text_format == "money":
        text = ordered[x].map(lambda v: format_rupiah(v, compact=True))
    elif text_format == "pct":
        text = ordered[x].map(lambda v: format_pct(v))
    else:
        text = ordered[x].map(lambda v: format_number(v))

    fig = go.Figure(
        go.Bar(
            x=ordered[x],
            y=ordered["_label_short"],
            orientation="h",
            marker=dict(
                color=color,
                line=dict(color="rgba(255,255,255,.88)", width=1.2),
                cornerradius=7,
            ),
            text=text,
            textposition="outside",
            textfont=dict(color="#0B1F3A", size=12, family="Inter, Arial, sans-serif"),
            customdata=np.stack([ordered[y].astype(str), ordered[x]], axis=-1),
            hovertemplate="%{customdata[0]}<br>" + x + ": %{customdata[1]:,.0f}<extra></extra>",
            cliponaxis=False,
        )
    )
    fig.update_layout(xaxis_title="", yaxis_title="")
    fig.update_xaxes(range=[0, safe_axis_max(ordered[x], 1.30)])
    fig.update_layout(margin=dict(l=178, r=106, t=18, b=46))
    return apply_plot_theme(fig, height=height, show_legend=False)


def stacked_result_by_group(data: pd.DataFrame, group_col: str, top_n: int = 10) -> go.Figure:
    """Stacked bar Komposisi Result per Group.

    Plotly Bar tidak punya properti `textinfo`; properti itu hanya untuk Pie/Donut.
    Karena itu chart ini memakai `text`, `textposition`, dan `textfont` supaya aman
    di Streamlit Cloud.
    """

    if data.empty or group_col not in data.columns or "Result" not in data.columns:
        return apply_plot_theme(go.Figure(), height=460, show_legend=True)

    result_order = ["Recommend", "Revise", "Sama"]
    color_map = {
        "Recommend": COLORS["green"],
        "Revise": COLORS["yellow"],
        "Sama": COLORS["blue"],
    }

    group_rank = (
        data.groupby(group_col, dropna=False)
        .size()
        .reset_index(name="Total")
        .sort_values("Total", ascending=False)
        .head(top_n)
    )

    selected_groups = group_rank[group_col].astype(str).tolist()
    subset = data[data[group_col].astype(str).isin(selected_groups)].copy()
    subset["Result"] = subset["Result"].astype(str).str.strip()

    pivot = (
        subset.groupby([group_col, "Result"], dropna=False)
        .size()
        .reset_index(name="Jumlah")
    )
    pivot[group_col] = pivot[group_col].astype(str)
    pivot = pivot[pivot["Result"].isin(result_order)]

    full_index = pd.MultiIndex.from_product(
        [selected_groups, result_order],
        names=[group_col, "Result"],
    )

    pivot = (
        pivot.set_index([group_col, "Result"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )

    total_per_group = pivot.groupby(group_col)["Jumlah"].sum().replace(0, np.nan)

    pivot["Persen"] = pivot.apply(
        lambda row: (row["Jumlah"] / total_per_group.loc[row[group_col]] * 100)
        if pd.notna(total_per_group.loc[row[group_col]]) else 0,
        axis=1,
    )

    pivot["_Group_Short"] = pivot[group_col].map(lambda x: shorten_label(str(x), 28))

    fig = go.Figure()

    for result in result_order:
        part = pivot[pivot["Result"] == result].copy()
        if part.empty:
            continue

        text_values = part.apply(
            lambda row: f"{int(row['Jumlah'])}" if row["Jumlah"] >= 3 else "",
            axis=1,
        )

        fig.add_trace(
            go.Bar(
                x=part["Jumlah"],
                y=part["_Group_Short"],
                orientation="h",
                name=result,
                marker=dict(
                    color=color_map.get(result, COLORS["blue"]),
                    line=dict(color="#FFFFFF", width=1.4),
                ),
                text=text_values,
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(
                    color="#0B1F3A" if result == "Revise" else "#FFFFFF",
                    size=12,
                    family="Inter, Arial, sans-serif",
                ),
                customdata=np.stack(
                    [
                        part[group_col].astype(str),
                        part["Result"].astype(str),
                        part["Jumlah"],
                        part["Persen"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Result: %{customdata[1]}<br>"
                    "Jumlah: %{customdata[2]:,.0f} hotel<br>"
                    "Persentase: %{customdata[3]:.1f}%"
                    "<extra></extra>"
                ),
                cliponaxis=False,
            )
        )

    max_total = (
        pivot.groupby("_Group_Short")["Jumlah"].sum().max()
        if not pivot.empty else 1
    )
    chart_height = max(460, 56 * len(selected_groups) + 130)
    category_order = list(reversed([shorten_label(str(x), 28) for x in selected_groups]))

    fig.update_layout(
        barmode="stack",
        height=chart_height,
        margin=dict(l=210, r=120, t=25, b=85),
        xaxis_title="Jumlah Hotel",
        yaxis_title="",
        legend_title_text="Result",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.24,
            xanchor="center",
            x=0.5,
        ),
    )

    fig.update_xaxes(range=[0, max(1, max_total) * 1.18])
    fig.update_yaxes(categoryorder="array", categoryarray=category_order)

    return apply_plot_theme(fig, height=chart_height, show_legend=True)


def scatter_price(data: pd.DataFrame) -> go.Figure:
    if data.empty:
        return apply_plot_theme(go.Figure(), height=420)
    fig = px.scatter(
        data,
        x="Publish Rate",
        y="Offering Corporate Rate 2026",
        color="Corporate Status",
        size=np.clip(data["Nilai Selisih"].abs(), 10_000, None),
        hover_name="Nama Hotel",
        hover_data={
            "City": True,
            "Nama Group/ Non Group": True,
            "Nilai Selisih": ":,.0f",
            "Publish Rate": ":,.0f",
            "Offering Corporate Rate 2026": ":,.0f",
            "Corporate Status": True,
        },
        color_discrete_map={
            "Corporate Lebih Murah": COLORS["green"],
            "Corporate Lebih Mahal": COLORS["red"],
            "Sama dengan Publish": COLORS["yellow"],
        },
    )
    min_val = min(data["Publish Rate"].min(), data["Offering Corporate Rate 2026"].min())
    max_val = max(data["Publish Rate"].max(), data["Offering Corporate Rate 2026"].max())
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name="Sama dengan Publish",
            line=dict(color="rgba(0,43,91,.35)", dash="dash", width=2),
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        title="Publish Rate vs Corporate Rate 2026",
        xaxis_title="Publish Rate (Rp)",
        yaxis_title="Offering Corporate Rate 2026 (Rp)",
    )
    return apply_plot_theme(fig, height=455)


def city_boxplot(data: pd.DataFrame, top_n: int = 8) -> go.Figure:
    if data.empty:
        return apply_plot_theme(go.Figure(), height=380)
    top_city = data["City"].value_counts().head(top_n).index
    subset = data[data["City"].isin(top_city)]
    fig = px.box(
        subset,
        x="City",
        y="Nilai Selisih",
        points="outliers",
        color="City",
        color_discrete_sequence=COLORWAY,
    )
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["red"], opacity=.65)
    fig.update_layout(title="Sebaran Nilai Selisih per Wilayah Utama", xaxis_title="", yaxis_title="Nilai Selisih (Rp)")
    return apply_plot_theme(fig, height=395, show_legend=False)


def waterfall_by_band(data: pd.DataFrame) -> go.Figure:
    order = ["Negatif", "Sama", "0-100rb", "100-300rb", "300-500rb", ">500rb"]
    band = data.groupby("Gap Band")["Nilai Selisih"].sum().reindex(order, fill_value=0).reset_index()
    fig = go.Figure(
        go.Waterfall(
            name="Kontribusi",
            orientation="v",
            measure=["relative"] * len(band) + ["total"],
            x=list(band["Gap Band"]) + ["Total"],
            y=list(band["Nilai Selisih"]) + [band["Nilai Selisih"].sum()],
            text=[format_rupiah(v, compact=True) for v in band["Nilai Selisih"]] + [format_rupiah(band["Nilai Selisih"].sum(), compact=True)],
            textposition="outside",
            connector={"line": {"color": "rgba(100,116,139,.45)"}},
            increasing={"marker": {"color": COLORS["green"]}},
            decreasing={"marker": {"color": COLORS["red"]}},
            totals={"marker": {"color": COLORS["navy"]}},
        )
    )
    fig.update_layout(title="Kontribusi Nilai Selisih per Band Harga", yaxis_title="Nilai Selisih (Rp)")
    return apply_plot_theme(fig, height=380, show_legend=False)


def province_map(data: pd.DataFrame) -> go.Figure:
    regional = aggregate_by(data, "City")
    regional["Latitude"] = regional["City"].map(lambda x: PROVINCE_COORDS.get(str(x), (np.nan, np.nan))[0])
    regional["Longitude"] = regional["City"].map(lambda x: PROVINCE_COORDS.get(str(x), (np.nan, np.nan))[1])
    regional = regional.dropna(subset=["Latitude", "Longitude"])

    if regional.empty:
        return apply_plot_theme(go.Figure(), height=495)

    regional["Status"] = np.where(regional["Total Selisih"] >= 0, "Positif", "Negatif")
    fig = px.scatter_mapbox(
        regional,
        lat="Latitude",
        lon="Longitude",
        size="Jumlah Hotel",
        color="Total Selisih",
        hover_name="City",
        hover_data={
            "Jumlah Hotel": True,
            "Total Selisih": ":,.0f",
            "Avg Selisih": ":,.0f",
            "Recommend": True,
            "Revise": True,
            "Latitude": False,
            "Longitude": False,
        },
        color_continuous_scale=[[0, COLORS["red"]], [.35, COLORS["yellow"]], [1, COLORS["green"]]],
        size_max=46,
        zoom=3.25,
        center={"lat": -2.1, "lon": 118.1},
        mapbox_style="open-street-map",
    )
    fig.update_layout(title="Peta Total Nilai Selisih per Wilayah", coloraxis_colorbar=dict(title="Selisih"))
    return apply_plot_theme(fig, height=505)


def group_bubble(data: pd.DataFrame) -> go.Figure:
    group = aggregate_by(data, "Nama Group/ Non Group")
    if group.empty:
        return apply_plot_theme(go.Figure(), height=395)
    group = group[group["Jumlah Hotel"] > 0]
    fig = px.scatter(
        group,
        x="Revise",
        y="Total Selisih",
        size="Jumlah Hotel",
        color="Avg Selisih",
        hover_name="Nama Group/ Non Group",
        hover_data={
            "Jumlah Hotel": True,
            "Recommend": True,
            "Revise": True,
            "Total Selisih": ":,.0f",
            "Avg Selisih": ":,.0f",
        },
        color_continuous_scale=[[0, COLORS["red"]], [.45, COLORS["yellow"]], [1, COLORS["green"]]],
        size_max=50,
    )
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["red"], opacity=.5)
    fig.update_layout(title="Posisi Group: Total Selisih vs Revise", xaxis_title="Jumlah Revise", yaxis_title="Total Selisih (Rp)")
    return apply_plot_theme(fig, height=395)


def action_stacked_bar(data: pd.DataFrame) -> go.Figure:
    pivot = data.groupby(["Next Action", "Result"]).size().reset_index(name="Jumlah")
    fig = px.bar(
        pivot,
        x="Next Action",
        y="Jumlah",
        color="Result",
        barmode="stack",
        text="Jumlah",
        color_discrete_map={"Recommend": COLORS["green"], "Revise": COLORS["yellow"], "Sama": COLORS["blue"]},
    )
    fig.update_layout(title="Action berdasarkan Result", xaxis_title="Next Action", yaxis_title="Jumlah Hotel")
    return apply_plot_theme(fig, height=360)


def impact_effort_chart(data: pd.DataFrame) -> go.Figure:
    summary = kpi_summary(data)
    actions = pd.DataFrame(
        [
            {
                "Action": "Maintain Top Hotel",
                "Impact": 5,
                "Effort": 1.4,
                "Kategori": "Quick Win",
                "Nilai": summary["positive_gap"],
                "Catatan": "Pertahankan rate hotel yang sudah memberi selisih positif.",
            },
            {
                "Action": "Negotiate Negative Rates",
                "Impact": 5,
                "Effort": 3.8,
                "Kategori": "Prioritas Utama",
                "Nilai": abs(summary["negative_gap"]),
                "Catatan": "Fokus pada hotel dengan corporate rate lebih mahal.",
            },
            {
                "Action": "Review High-Volume Groups",
                "Impact": 4,
                "Effort": 2.7,
                "Kategori": "Nilai Potensial",
                "Nilai": summary["total_gap"],
                "Catatan": "Optimalkan group yang volume hotelnya besar.",
            },
            {
                "Action": "Complete Missing Email",
                "Impact": 3,
                "Effort": 1.6,
                "Kategori": "Fondasi Data",
                "Nilai": summary["missing_email"],
                "Catatan": "Percepat follow-up kontrak dengan data kontak lengkap.",
            },
            {
                "Action": "Finalize Contracts",
                "Impact": 4,
                "Effort": 3.2,
                "Kategori": "Penutupan 2026",
                "Nilai": summary["sign_kontrak"],
                "Catatan": "Selesaikan hotel yang masih masuk Sign Kontrak.",
            },
        ]
    )
    fig = px.scatter(
        actions,
        x="Effort",
        y="Impact",
        size=np.clip(actions["Nilai"].abs(), 1, None),
        color="Kategori",
        text="Action",
        hover_data={"Catatan": True, "Nilai": True},
        color_discrete_sequence=[COLORS["green"], COLORS["red"], COLORS["yellow"], COLORS["blue"], COLORS["navy"]],
        size_max=48,
    )
    fig.update_traces(textposition="top center")
    fig.add_shape(type="line", x0=2.5, x1=2.5, y0=.5, y1=5.5, line=dict(color="rgba(100,116,139,.35)", dash="dash"))
    fig.add_shape(type="line", x0=.5, x1=5.5, y0=3.0, y1=3.0, line=dict(color="rgba(100,116,139,.35)", dash="dash"))
    fig.update_layout(
        title="Impact vs Effort Matrix",
        xaxis=dict(title="Usaha / Effort", range=[0.5, 5.5]),
        yaxis=dict(title="Dampak / Impact", range=[0.5, 5.5]),
    )
    return apply_plot_theme(fig, height=430)


# =============================================================
# 6. LAYOUT COMPONENTS
# =============================================================


def sidebar_nav() -> str:
    st.sidebar.markdown(
        """
        <div class="logo-wrap">
            <div class="logo-bars"><span></span><span></span><span></span></div>
            <div>
                <div class="logo-text-title">Corporate Rate<br/>Hotel Pertamina 2026</div>
                <div class="logo-text-sub">Pricing Intelligence Dashboard</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio(
        "Navigasi Dashboard",
        PAGE_OPTIONS,
        format_func=lambda x: f"{PAGE_ICONS.get(x, '')}  {x}",
        label_visibility="collapsed",
    )
    st.sidebar.markdown("---")
    return page


def page_title(page: str, subtitle: str = APP_SUBTITLE) -> None:
    st.markdown(
        f"""
        <div class="page-title">
            <h1>{APP_TITLE}</h1>
            <p>{PAGE_ICONS.get(page, '📊')} {page} · {subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def data_source_selector() -> pd.DataFrame:
    """Load dataset directly from Google Sheets; no Excel file or embedded data needed."""
    st.sidebar.markdown("---")
    st.sidebar.caption("☁️ Dataset aktif: Google Sheets")

    try:
        return cached_read_google_sheets(tuple(GOOGLE_SHEETS_CSV_URLS))
    except Exception as exc:
        st.error(
            "Data Google Sheets gagal dibaca. Pastikan spreadsheet sudah di-share "
            "dengan akses 'Anyone with the link' sebagai Viewer, dan pastikan tab data memakai GID yang benar."
        )
        st.info("URL CSV yang dicoba aplikasi:\n" + "\n".join(GOOGLE_SHEETS_CSV_URLS))
        st.exception(exc)
        st.stop()


def global_filters(data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1.2, 1, 1, 1])
    with c1:
        tahun = st.selectbox("Tahun", ["2026"], index=0)
    with c2:
        city = st.selectbox("City", option_list(data["City"]), index=0)
    with c3:
        group = st.selectbox("Group", option_list(data["Nama Group/ Non Group"]), index=0)
    with c4:
        result = st.selectbox("Result", option_list(data["Result"]), index=0)
    with c5:
        action = st.selectbox("Next Action", option_list(data["Next Action"]), index=0)
    with c6:
        band = st.selectbox("Band Nilai", option_list(data["Gap Band"]), index=0)
    st.markdown("</div>", unsafe_allow_html=True)

    filtered = data.copy()
    for col, val in [
        ("City", city),
        ("Nama Group/ Non Group", group),
        ("Result", result),
        ("Next Action", action),
        ("Gap Band", band),
    ]:
        filtered = selected_filter(filtered, col, val)

    context = {
        "tahun": tahun,
        "city": city,
        "group": group,
        "result": result,
        "action": action,
        "band": band,
    }
    return filtered, context


def sidebar_downloads(data: pd.DataFrame) -> None:
    st.sidebar.markdown("### ⬇️ Export")
    csv = data.to_csv(index=False).encode("utf-8-sig")
    st.sidebar.download_button(
        "Download CSV Filtered",
        data=csv,
        file_name="filtered_corporate_rate_hotel_pertamina_2026.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.sidebar.download_button(
        "Download Excel Filtered",
        data=to_excel_bytes(data),
        file_name="filtered_corporate_rate_hotel_pertamina_2026.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


def overview_kpi_row(data: pd.DataFrame) -> None:
    s = kpi_summary(data)
    cols = st.columns(6)
    with cols[0]:
        kpi_card("Total Hotel", f"{s['total']:,}".replace(",", "."), "jumlah record aktif", "🏨", "navy")
    with cols[1]:
        kpi_card("Recommend", f"{s['recommend']:,}".replace(",", "."), format_pct(safe_div(s["recommend"], s["total"])), "✅", "green")
    with cols[2]:
        kpi_card("Revise", f"{s['revise']:,}".replace(",", "."), format_pct(safe_div(s["revise"], s["total"])), "✏️", "yellow")
    with cols[3]:
        kpi_card("Total Nilai Selisih", format_rupiah(s["total_gap"]), "net opportunity", "Rp", "navy")
    with cols[4]:
        kpi_card("Rata-rata Selisih", format_rupiah(s["avg_gap"]), "per hotel", "📈", "green")
    with cols[5]:
        kpi_card("Selisih Negatif", f"{s['negative_count']:,}".replace(",", "."), "urgent revise", "⬇️", "red")


# =============================================================
# 7. DASHBOARD PAGES
# =============================================================


def page_executive_overview(data: pd.DataFrame, metadata: Dict[str, object]) -> None:
    overview_kpi_row(data)
    st.caption(
        "Catatan cleaning: kategori Result sudah dinormalisasi dari spasi/karakter tersembunyi. "
        f"Terdeteksi {metadata.get('result_whitespace_issue', 0)} record Result dengan whitespace tambahan."
    )

    if data.empty:
        empty_state()
        return

    # Two-by-two chart layout so labels do not collide on laptop screens.
    row1_left, row1_right = st.columns([0.92, 1.38])
    with row1_left:
        chart_card("Komposisi Result", result_donut(data), "🍩")
    with row1_right:
        city_top = aggregate_by(data, "City").sort_values("Total Selisih", ascending=False).head(5)
        chart_card(
            "Top 5 City berdasarkan Total Selisih",
            horizontal_bar(city_top, "Total Selisih", "City", "", COLORS["navy"], 345),
            "📍",
        )

    row2_left, row2_right = st.columns([1.38, 0.92])
    with row2_left:
        group_top = aggregate_by(data, "Nama Group/ Non Group").sort_values("Total Selisih", ascending=False).head(5)
        chart_card(
            "Top 5 Group berdasarkan Total Selisih",
            horizontal_bar(group_top, "Total Selisih", "Nama Group/ Non Group", "", COLORS["green"], 345),
            "👥",
        )
    with row2_right:
        chart_card("Distribusi Nilai Selisih", gap_band_bar(data), "📊")

    left2, right2 = st.columns([1.35, .95])
    with left2:
        top_table = data.sort_values("Nilai Selisih", ascending=False).head(12)[
            [
                "Nama Hotel",
                "City",
                "Nama Group/ Non Group",
                "Publish Rate",
                "Offering Corporate Rate 2026",
                "Nilai Selisih",
                "Result",
                "Next Action",
            ]
        ]
        dataframe_card("Snapshot Hotel dengan Selisih Tertinggi", style_numeric_table(top_table), "🏨", 410)
    with right2:
        top_city = aggregate_by(data, "City").sort_values("Total Selisih", ascending=False).head(3)
        top_city_names = ", ".join(top_city["City"].tolist()) if not top_city.empty else "-"
        insight_card(
            "Area kontribusi terbesar",
            f"Wilayah dengan kontribusi selisih terbesar pada filter ini adalah <b>{top_city_names}</b>. Gunakan halaman Regional Analysis untuk melihat prioritas per provinsi.",
            "Regional Focus",
            "pill-green",
        )

    st.markdown("<div class='footer-band'>🎯 Arah utama: pertahankan rate yang memberikan selisih positif dan prioritaskan negosiasi hotel dengan selisih negatif.</div>", unsafe_allow_html=True)


def page_regional_analysis(data: pd.DataFrame) -> None:
    s = kpi_summary(data)
    regional = aggregate_by(data, "City")
    top_reg = regional.sort_values("Total Selisih", ascending=False).head(1)
    top_rev = regional.sort_values("Revise", ascending=False).head(1)
    second = regional.sort_values("Total Selisih", ascending=False).head(2).tail(1)

    cols = st.columns(5)
    with cols[0]:
        kpi_card("Total Selisih Nasional", format_rupiah(s["total_gap"]), "berdasarkan filter", "Rp", "navy")
    with cols[1]:
        kpi_card("Provinsi Tertinggi", top_reg["City"].iloc[0] if not top_reg.empty else "-", format_rupiah(top_reg["Total Selisih"].iloc[0]) if not top_reg.empty else "-", "🏆", "green")
    with cols[2]:
        kpi_card("Provinsi #2", second["City"].iloc[0] if not second.empty else "-", format_rupiah(second["Total Selisih"].iloc[0]) if not second.empty else "-", "🌴", "green")
    with cols[3]:
        kpi_card("Rata-rata Selisih", format_rupiah(s["avg_gap"]), "per hotel", "📈", "navy")
    with cols[4]:
        kpi_card("Revise Tertinggi", top_rev["City"].iloc[0] if not top_rev.empty else "-", f"{int(top_rev['Revise'].iloc[0])} hotel" if not top_rev.empty else "-", "✏️", "yellow")

    if data.empty:
        empty_state()
        return

    left, right = st.columns([1.35, .9])
    with left:
        chart_card("Peta Total Nilai Selisih per Wilayah", province_map(data), "🗺️")
    with right:
        top10 = regional.sort_values("Total Selisih", ascending=False).head(10)
        chart_card("Top 10 Provinsi berdasarkan Total Selisih", horizontal_bar(top10, "Total Selisih", "City", "", COLORS["navy"], 505), "🏁")

    left2, right2 = st.columns([1.35, .95])
    with left2:
        display = regional.sort_values("Total Selisih", ascending=False).head(15)[
            ["City", "Jumlah Hotel", "Total Selisih", "Avg Selisih", "Recommend", "Revise", "Revise Rate"]
        ]
        dataframe_card("Kinerja Wilayah", style_numeric_table(display), "📋", 420)
    with right2:
        rev = regional.sort_values("Revise", ascending=False).head(7)
        chart_card("Provinsi dengan Revise Terbanyak", horizontal_bar(rev, "Revise", "City", "", COLORS["yellow"], 330, text_format="number"), "✏️")
        top_city = regional.sort_values("Jumlah Hotel", ascending=False).head(1)
        insight_card(
            "Fokus regional",
            f"<b>{top_city['City'].iloc[0] if not top_city.empty else '-'}</b> memiliki volume hotel tertinggi pada filter ini. Area dengan volume tinggi cocok menjadi target optimasi rate dan validasi kontrak.",
            "Volume Focus",
            "pill-green",
        )


def page_group_performance(data: pd.DataFrame) -> None:
    group = aggregate_by(data, "Nama Group/ Non Group")
    s = kpi_summary(data)
    top_group = group.sort_values("Total Selisih", ascending=False).head(1)
    top_volume = group.sort_values("Jumlah Hotel", ascending=False).head(1)
    top_avg = group[group["Jumlah Hotel"] >= 2].sort_values("Avg Selisih", ascending=False).head(1)
    top_revise = group.sort_values("Revise", ascending=False).head(1)
    group_type_counts = data["Group/ Non Group"].value_counts()

    cols = st.columns(6)
    with cols[0]:
        kpi_card("Total Group", f"{s['group_count']}+", "unique group/non-group", "👥", "navy")
    with cols[1]:
        kpi_card("Group Tertinggi", top_group["Nama Group/ Non Group"].iloc[0] if not top_group.empty else "-", format_rupiah(top_group["Total Selisih"].iloc[0]) if not top_group.empty else "-", "🏆", "green")
    with cols[2]:
        kpi_card("Group Volume Tertinggi", top_volume["Nama Group/ Non Group"].iloc[0] if not top_volume.empty else "-", f"{int(top_volume['Jumlah Hotel'].iloc[0])} hotel" if not top_volume.empty else "-", "🏨", "yellow")
    with cols[3]:
        kpi_card("Avg Selisih Tertinggi", top_avg["Nama Group/ Non Group"].iloc[0] if not top_avg.empty else "-", format_rupiah(top_avg["Avg Selisih"].iloc[0]) if not top_avg.empty else "-", "📈", "green")
    with cols[4]:
        kpi_card("Revise Tertinggi", top_revise["Nama Group/ Non Group"].iloc[0] if not top_revise.empty else "-", f"{int(top_revise['Revise'].iloc[0])} hotel" if not top_revise.empty else "-", "⚠️", "red")
    with cols[5]:
        g = int(group_type_counts.get("Group", 0))
        ng = int(group_type_counts.get("Non Group", 0))
        kpi_card("Group vs Non Group", f"{g} vs {ng}", format_pct(safe_div(g, g + ng)), "◔", "navy")

    if data.empty:
        empty_state()
        return

    left, mid, right = st.columns([1, 1, 1])
    with left:
        top = group.sort_values("Total Selisih", ascending=False).head(10)
        chart_card("Top Group berdasarkan Total Selisih", horizontal_bar(top, "Total Selisih", "Nama Group/ Non Group", "", COLORS["navy"], 390), "👥")
    with mid:
        chart_card("Posisi Group: Total Selisih vs Revise", group_bubble(data), "🫧")
    with right:
        chart_card("Komposisi Result per Group", stacked_result_by_group(data, "Nama Group/ Non Group", top_n=8), "📊")

    left2, right2 = st.columns([1.45, .85])
    with left2:
        table = group.sort_values("Total Selisih", ascending=False).head(20)[
            ["Nama Group/ Non Group", "Jumlah Hotel", "Total Selisih", "Avg Selisih", "Recommend", "Revise", "Revise Rate"]
        ]
        dataframe_card("Scorecard Group", style_numeric_table(table), "📋", 430)
    with right2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Benchmark", "🏅")
        if not top_group.empty:
            insight_card("Paling kuat dari sisi total selisih", f"<b>{top_group['Nama Group/ Non Group'].iloc[0]}</b> berkontribusi {format_rupiah(top_group['Total Selisih'].iloc[0])}.", "Total Selisih", "pill-green")
        if not top_volume.empty:
            insight_card("Paling kuat dari sisi volume", f"<b>{top_volume['Nama Group/ Non Group'].iloc[0]}</b> memiliki {int(top_volume['Jumlah Hotel'].iloc[0])} hotel.", "Volume", "pill-yellow")
        if not top_revise.empty:
            insight_card("Perlu perhatian revisi", f"<b>{top_revise['Nama Group/ Non Group'].iloc[0]}</b> punya {int(top_revise['Revise'].iloc[0])} hotel revise.", "Revise", "pill-red")
        st.markdown("</div>", unsafe_allow_html=True)


def page_top_opportunity(data: pd.DataFrame) -> None:
    if data.empty:
        overview_kpi_row(data)
        empty_state()
        return
    top_positive = data[data["Nilai Selisih"] > 0].sort_values("Nilai Selisih", ascending=False)
    top_negative = data[data["Nilai Selisih"] < 0].sort_values("Nilai Selisih", ascending=True)
    top10_total = top_positive.head(10)["Nilai Selisih"].sum()

    cols = st.columns(5)
    with cols[0]:
        kpi_card("Hotel Selisih Tertinggi", top_positive["Nama Hotel"].iloc[0] if not top_positive.empty else "-", format_rupiah(top_positive["Nilai Selisih"].iloc[0]) if not top_positive.empty else "-", "🏆", "green")
    with cols[1]:
        kpi_card("Top 10 Hotel Total", format_rupiah(top10_total), "nilai selisih positif", "📊", "navy")
    with cols[2]:
        kpi_card("Hotel Selisih Negatif", f"{len(top_negative)}", "butuh negosiasi", "⬇️", "red")
    with cols[3]:
        kpi_card("Selisih Terendah", top_negative["Nama Hotel"].iloc[0] if not top_negative.empty else "-", format_rupiah(top_negative["Nilai Selisih"].iloc[0]) if not top_negative.empty else "-", "〽️", "yellow")
    with cols[4]:
        kpi_card("Rata-rata Top 10", format_rupiah(safe_div(top10_total, min(10, len(top_positive)))), "hotel unggulan", "📈", "green")

    left, right = st.columns([1, 1])
    with left:
        top10 = top_positive.head(10).copy()
        chart_card("Top 10 Hotel dengan Nilai Selisih Tertinggi", horizontal_bar(top10, "Nilai Selisih", "Nama Hotel", "", COLORS["navy"], 430), "⭐")
    with right:
        neg10 = top_negative.head(10).copy()
        chart_card("Top 10 Hotel dengan Selisih Negatif", horizontal_bar(neg10, "Nilai Selisih", "Nama Hotel", "", COLORS["red"], 430), "⚠️")

    left2, right2 = st.columns([1.45, .75])
    with left2:
        table = pd.concat([top_positive.head(15), top_negative.head(8)], axis=0).drop_duplicates("Nama Hotel")
        table = table[
            [
                "Nama Hotel",
                "City",
                "Nama Group/ Non Group",
                "Publish Rate",
                "Offering Corporate Rate 2026",
                "Nilai Selisih",
                "Result",
                "Next Action",
            ]
        ]
        dataframe_card("Hotel Opportunity List", style_numeric_table(table), "🏨", 510)
    with right2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Highlight Hotel", "🌟")
        for idx, row in top_positive.head(3).iterrows():
            insight_card(
                row["Nama Hotel"],
                f"{row['City']} · {row['Nama Group/ Non Group']}<br><b>{format_rupiah(row['Nilai Selisih'])}</b>",
                "Opportunity",
                "pill-green",
            )
        if not top_negative.empty:
            row = top_negative.iloc[0]
            insight_card(
                row["Nama Hotel"],
                f"{row['City']} · {row['Nama Group/ Non Group']}<br><b>{format_rupiah(row['Nilai Selisih'])}</b>",
                "Revise Highest",
                "pill-red",
            )
        st.markdown("</div>", unsafe_allow_html=True)


def page_price_gap(data: pd.DataFrame) -> None:
    s = kpi_summary(data)
    avg_discount = safe_div(s["avg_gap"], s["avg_publish"])
    cols = st.columns(6)
    with cols[0]:
        kpi_card("Corporate Lebih Murah", f"{s['positive_count']}", format_pct(safe_div(s["positive_count"], s["total"])), "⬇️", "green")
    with cols[1]:
        kpi_card("Corporate Lebih Mahal", f"{s['negative_count']}", format_pct(safe_div(s["negative_count"], s["total"])), "⬆️", "red")
    with cols[2]:
        kpi_card("Sama dengan Publish", f"{s['same_count']}", format_pct(safe_div(s["same_count"], s["total"])), "=", "yellow")
    with cols[3]:
        kpi_card("Avg Publish Rate", format_rupiah(s["avg_publish"]), "rata-rata", "Rp", "navy")
    with cols[4]:
        kpi_card("Avg Corporate Rate", format_rupiah(s["avg_corporate"]), "rata-rata", "💼", "green")
    with cols[5]:
        kpi_card("Avg Diskon vs Publish", format_pct(avg_discount), "positif = hemat", "%", "yellow")

    if data.empty:
        empty_state()
        return

    left, right = st.columns([1.35, .85])
    with left:
        chart_card("Publish Rate vs Corporate Rate 2026", scatter_price(data), "📉")
    with right:
        chart_card("Kategori Nilai Selisih", gap_band_bar(data, orientation="v"), "🏷️")

    left2, right2 = st.columns([1, 1])
    with left2:
        chart_card("Kontribusi Nilai Selisih per Band Harga", waterfall_by_band(data), "🌊")
    with right2:
        chart_card("Sebaran Nilai Selisih per Wilayah Utama", city_boxplot(data), "📦")

    status = data.groupby("Corporate Status").agg(**{"Jumlah Hotel": ("Nama Hotel", "count"), "Total Selisih": ("Nilai Selisih", "sum")}).reset_index()
    left3, right3 = st.columns([.7, 1.3])
    with left3:
        dataframe_card("Status Harga 2026", style_numeric_table(status), "📋", 260)
    with right3:
        insight_card(
            "Interpretasi cepat",
            "Sebagian besar hotel yang corporate rate-nya lebih murah adalah sumber opportunity. Hotel dengan corporate rate lebih mahal harus dinegosiasikan agar tidak menggerus total nilai selisih portofolio.",
            "Price Gap Insight",
            "pill-green",
        )


def page_revise_priority(data: pd.DataFrame) -> None:
    s = kpi_summary(data)
    p1 = int(data["Priority"].eq("P1 - Urgent Negative").sum()) if not data.empty else 0
    p2 = int(data["Priority"].eq("P2 - Revise Positive").sum()) if not data.empty else 0
    thin = int(data["Gap Band"].eq("0-100rb").sum()) if not data.empty else 0
    safe = int(data["Priority"].eq("Maintain Rate").sum() + data["Priority"].eq("Maintain High Opportunity").sum()) if not data.empty else 0

    cols = st.columns(6)
    with cols[0]:
        kpi_card("Total Revise", f"{s['revise']}", "hotel", "✏️", "yellow")
    with cols[1]:
        kpi_card("Prioritas P1 Negatif", f"{p1}", "urgent", "⬇️", "red")
    with cols[2]:
        kpi_card("Prioritas P2", f"{p2}", "revise positif", "📈", "green")
    with cols[3]:
        kpi_card("Selisih Tipis", f"{thin}", "0-100rb", "≈", "yellow")
    with cols[4]:
        kpi_card("Sign Kontrak", f"{s['sign_kontrak']}", "finalisasi", "🖊️", "navy")
    with cols[5]:
        kpi_card("Hotel Aman", f"{safe}+", "maintain", "🛡️", "green")

    if data.empty:
        empty_state()
        return

    regional = aggregate_by(data, "City")
    group = aggregate_by(data, "Nama Group/ Non Group")
    left, mid, right = st.columns([.9, 1, 1])
    with left:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Prioritas Negosiasi", "🎯")
        insight_card("URGENT NEGATIVE", f"{p1} hotel perlu tindakan segera karena corporate rate lebih mahal.", "P1", "pill-red")
        insight_card("REVISE POSITIVE", f"{p2} hotel masih punya potensi selisih positif tetapi perlu review rate.", "P2", "pill-green")
        insight_card("SELISIH TIPIS", f"{thin} hotel berada pada band 0-100rb; cocok untuk pendekatan selektif.", "Thin Gap", "pill-yellow")
        insight_card("AMAN", f"{safe}+ hotel dapat dipertahankan relasinya dengan maintain rate.", "Maintain", "pill-green")
        st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        rev_city = regional.sort_values("Revise", ascending=False).head(7)
        chart_card("Provinsi dengan Revise Tertinggi", horizontal_bar(rev_city, "Revise", "City", "", COLORS["navy"], 470, text_format="number"), "📍")
    with right:
        rev_group = group.sort_values("Revise", ascending=False).head(7)
        chart_card("Group dengan Revise Tertinggi", horizontal_bar(rev_group, "Revise", "Nama Group/ Non Group", "", COLORS["blue"], 470, text_format="number"), "👥")

    left2, right2 = st.columns([1.5, .7])
    with left2:
        priority = data.sort_values(["Is Negative Gap", "Nilai Selisih"], ascending=[False, True]).head(35)[
            ["Nama Hotel", "City", "Nama Group/ Non Group", "Nilai Selisih", "Result", "Priority", "Next Action", "Checking Remarks"]
        ]
        dataframe_card("Daftar Hotel Prioritas", style_numeric_table(priority), "📋", 510)
    with right2:
        insight_card(
            "Fokus negosiasi awal",
            "Mulai dari hotel berselisih negatif, lalu lanjutkan ke hotel revise di wilayah padat volume. Prioritas ini menjaga nilai portofolio sekaligus mempercepat tindak lanjut kontrak.",
            "Negotiation Focus",
            "pill-red",
        )


def page_action_tracker(data: pd.DataFrame) -> None:
    s = kpi_summary(data)
    done = int(data["Next Action"].eq("Done").sum()) if not data.empty else 0
    sign = s["sign_kontrak"]
    follow_critical = int(data["Priority"].eq("P1 - Urgent Negative").sum()) if not data.empty else 0
    sla_completion = safe_div(done, s["total"])

    cols = st.columns(6)
    with cols[0]:
        kpi_card("Done", f"{done}", "selesai", "✅", "green")
    with cols[1]:
        kpi_card("Sign Kontrak", f"{sign}", "perlu finalisasi", "🖊️", "navy")
    with cols[2]:
        kpi_card("Follow-up Critical", f"{follow_critical}", "negative gap", "⚠️", "red")
    with cols[3]:
        kpi_card("Recommend Siap Maintain", f"{s['recommend']}", "maintain rate", "👥", "green")
    with cols[4]:
        kpi_card("Revise Perlu Review", f"{s['revise']}", "review rate", "✏️", "yellow")
    with cols[5]:
        kpi_card("SLA Completion", format_pct(sla_completion, 0), "done / total", "◔", "green")

    if data.empty:
        empty_state()
        return

    left, right = st.columns([1, 1.5])
    with left:
        action_counts = data["Next Action"].value_counts().reset_index()
        action_counts.columns = ["Next Action", "Jumlah"]
        fig = px.pie(
            action_counts,
            names="Next Action",
            values="Jumlah",
            hole=.62,
            color="Next Action",
            color_discrete_map={"Done": COLORS["green"], "Sign Kontrak": COLORS["navy"], "Review Rate": COLORS["yellow"]},
        )
        fig.update_layout(title="Status Next Action")
        chart_card("Status Next Action", apply_plot_theme(fig, height=385), "🍩")
    with right:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Pipeline Tindak Lanjut", "🚦")
        c1, c2, c3 = st.columns(3)
        pipeline = {
            "Maintain Rate": data[data["Priority"].str.contains("Maintain", na=False)].sort_values("Nilai Selisih", ascending=False).head(5),
            "Review Rate": data[data["Priority"].str.contains("Revise|Negative", regex=True, na=False)].sort_values("Nilai Selisih", ascending=True).head(5),
            "Sign Kontrak": data[data["Next Action"].eq("Sign Kontrak")].head(5),
        }
        for col, (title, subset) in zip([c1, c2, c3], pipeline.items()):
            with col:
                st.markdown(f"<span class='pill {'pill-green' if title=='Maintain Rate' else 'pill-yellow' if title=='Review Rate' else ''}'>{title} · {len(subset)}</span>", unsafe_allow_html=True)
                for _, row in subset.iterrows():
                    st.markdown(f"<div style='padding:9px 0;border-bottom:1px solid #E2E8F0'><b>{row['Nama Hotel']}</b><br><span style='color:#64748B;font-size:.82rem'>{row['City']} · {format_rupiah(row['Nilai Selisih'])}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    left2, right2 = st.columns([1.35, .9])
    with left2:
        need_action = data[data["Next Action"].ne("Done") | data["Priority"].eq("P1 - Urgent Negative")].sort_values("Nilai Selisih").head(50)[
            ["Nama Hotel", "City", "Nama Group/ Non Group", "Next Action", "Result", "Priority", "SLA Status", "Nilai Selisih"]
        ]
        dataframe_card("Hotel yang Masih Memerlukan Action", style_numeric_table(need_action), "📋", 430)
    with right2:
        chart_card("Action berdasarkan Result", action_stacked_bar(data), "📊")
        insight_card("Tahapan negosiasi", "Gunakan halaman ini untuk melihat action yang belum selesai, terutama Sign Kontrak dan hotel berselisih negatif yang membutuhkan review rate.", "Action Tracker", "pill-green")


def page_hotel_explorer(data: pd.DataFrame) -> None:
    if data.empty:
        empty_state()
        return

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_header("Direktori Hotel", "🔎")
    c1, c2, c3, c4, c5 = st.columns([1.2, 1.1, 1.1, 1.1, 1])
    with c1:
        search = st.text_input("Cari hotel / email / remarks", placeholder="Ketik nama hotel, email, atau kata kunci...")
    with c2:
        group_type = st.selectbox("Group / Non Group", option_list(data["Group/ Non Group"]), key="hotel_group_type")
    with c3:
        profile_group = st.selectbox("Nama Group", option_list(data["Nama Group/ Non Group"]), key="hotel_group_name")
    with c4:
        price_status = st.selectbox("Status Harga", option_list(data["Corporate Status"]), key="hotel_price_status")
    with c5:
        sort_mode = st.selectbox("Urutkan", ["Selisih tertinggi", "Selisih terendah", "Publish rate tertinggi", "Nama hotel A-Z"])

    explorer = data.copy()
    explorer = selected_filter(explorer, "Group/ Non Group", group_type)
    explorer = selected_filter(explorer, "Nama Group/ Non Group", profile_group)
    explorer = selected_filter(explorer, "Corporate Status", price_status)
    if search:
        s = search.lower().strip()
        mask = (
            explorer["Nama Hotel"].str.lower().str.contains(s, na=False)
            | explorer["Email"].str.lower().str.contains(s, na=False)
            | explorer["Checking Remarks"].str.lower().str.contains(s, na=False)
            | explorer["City"].str.lower().str.contains(s, na=False)
        )
        explorer = explorer[mask]
    if sort_mode == "Selisih tertinggi":
        explorer = explorer.sort_values("Nilai Selisih", ascending=False)
    elif sort_mode == "Selisih terendah":
        explorer = explorer.sort_values("Nilai Selisih", ascending=True)
    elif sort_mode == "Publish rate tertinggi":
        explorer = explorer.sort_values("Publish Rate", ascending=False)
    else:
        explorer = explorer.sort_values("Nama Hotel")

    table = explorer[
        [
            "Nama Hotel",
            "City",
            "Nama Group/ Non Group",
            "Publish Rate",
            "Offering Corporate Rate 2026",
            "Nilai Selisih",
            "Result",
            "Next Action",
            "Checking Remarks",
            "Email",
        ]
    ].copy()
    st.dataframe(style_numeric_table(table), use_container_width=True, hide_index=True, height=390)
    st.caption(f"Menampilkan {len(explorer):,} dari {len(data):,} hotel pada filter explorer.".replace(",", "."))
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, .8])
    with left:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Bandingkan Hotel Terpilih", "⚖️")
        choices = explorer["Nama Hotel"].dropna().unique().tolist()
        default_choices = choices[:3]
        selected = st.multiselect("Pilih maksimal 5 hotel", choices, default=default_choices, max_selections=5)
        compare = explorer[explorer["Nama Hotel"].isin(selected)].copy()
        if not compare.empty:
            fig = go.Figure()
            for _, row in compare.iterrows():
                fig.add_trace(go.Bar(name=row["Nama Hotel"], x=["Publish Rate", "Corporate Rate", "Nilai Selisih"], y=[row["Publish Rate"], row["Offering Corporate Rate 2026"], row["Nilai Selisih"]]))
            fig.update_layout(title="Perbandingan Rate dan Selisih", barmode="group", yaxis_title="Rp")
            st.plotly_chart(apply_plot_theme(fig, height=390), use_container_width=True, config=CONFIG)
        else:
            empty_state("Pilih hotel untuk dibandingkan.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Hotel Profile", "🏨")
        hotel_choice = st.selectbox("Pilih hotel detail", explorer["Nama Hotel"].tolist() if not explorer.empty else ["Tidak ada data"])
        if hotel_choice != "Tidak ada data":
            row = explorer[explorer["Nama Hotel"].eq(hotel_choice)].iloc[0]
            color = "pill-green" if row["Result"] == "Recommend" else "pill-red" if row["Nilai Selisih"] < 0 else "pill-yellow"
            st.markdown(f"<h3 style='margin-bottom:0'>{row['Nama Hotel']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#64748B'>{row['City']} · {row['Nama Group/ Non Group']}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<span class='pill {color}'>{row['Result']}</span> &nbsp; <span class='pill'>{row['Next Action']}</span>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Publish", format_rupiah(row["Publish Rate"]))
            c2.metric("Corporate", format_rupiah(row["Offering Corporate Rate 2026"]))
            c3.metric("Selisih", format_rupiah(row["Nilai Selisih"]))
            st.markdown("**Email**")
            st.write("Tidak tersedia" if row["Email Missing"] else row["Email"])
            st.markdown("**Checking Remarks**")
            st.write("Tidak tersedia" if row["Remarks Missing"] else row["Checking Remarks"])
        st.markdown("</div>", unsafe_allow_html=True)

    chart_card("Posisi Hotel dalam Band Selisih", scatter_price(explorer), "📍")


def page_data_quality(data: pd.DataFrame, metadata: Dict[str, object]) -> None:
    s = kpi_summary(data)
    email_complete = 1 - safe_div(s["missing_email"], s["total"])
    remarks_complete = 1 - safe_div(s["missing_remarks"], s["total"])
    group_counts = data["Group/ Non Group"].value_counts()
    g = int(group_counts.get("Group", 0))
    ng = int(group_counts.get("Non Group", 0))

    cols = st.columns(6)
    with cols[0]:
        kpi_card("Total Record", f"{s['total']}", "baris data", "🧱", "navy")
    with cols[1]:
        kpi_card("Missing Email", f"{s['missing_email']}", "perlu dilengkapi", "✉️", "red")
    with cols[2]:
        kpi_card("Missing Remarks", f"{s['missing_remarks']}", "perlu dilengkapi", "💬", "yellow")
    with cols[3]:
        kpi_card("Completeness Email", format_pct(email_complete), "validasi kontak", "✅", "green")
    with cols[4]:
        kpi_card("Completeness Remarks", format_pct(remarks_complete), "checking notes", "✅", "green")
    with cols[5]:
        kpi_card("Group vs Non Group", f"{g} vs {ng}", "komposisi", "👥", "navy")

    if data.empty:
        empty_state()
        return

    left, mid, right = st.columns([1, 1, 1])
    with left:
        comp = pd.DataFrame(
            {
                "Field": ["Email", "Checking Remarks"],
                "Lengkap": [s["total"] - s["missing_email"], s["total"] - s["missing_remarks"]],
                "Missing": [s["missing_email"], s["missing_remarks"]],
            }
        )
        comp_melt = comp.melt(id_vars="Field", value_vars=["Lengkap", "Missing"], var_name="Status", value_name="Jumlah")
        fig = px.bar(comp_melt, y="Field", x="Jumlah", color="Status", orientation="h", text="Jumlah", barmode="stack", color_discrete_map={"Lengkap": COLORS["green"], "Missing": COLORS["red"]})
        fig.update_layout(title="Kelengkapan Data", xaxis_title="Jumlah", yaxis_title="")
        chart_card("Kelengkapan Data", apply_plot_theme(fig, height=340), "✅")
    with mid:
        missing_group = aggregate_by(data, "Nama Group/ Non Group").sort_values("Missing Email", ascending=False).head(6)
        chart_card("Missing Email per Group", horizontal_bar(missing_group, "Missing Email", "Nama Group/ Non Group", "", COLORS["navy"], 340, "number"), "✉️")
    with right:
        group_df = group_counts.reset_index()
        group_df.columns = ["Tipe", "Jumlah"]
        fig = px.bar(group_df, x="Jumlah", y="Tipe", color="Tipe", orientation="h", text="Jumlah", color_discrete_map={"Group": COLORS["navy"], "Non Group": COLORS["yellow"]})
        fig.update_layout(title="Komposisi Group vs Non Group", xaxis_title="Jumlah", yaxis_title="")
        chart_card("Komposisi Group vs Non Group", apply_plot_theme(fig, height=340, show_legend=False), "👥")

    left2, right2 = st.columns([1.45, .75])
    with left2:
        dq = data[data["Email Missing"] | data["Remarks Missing"]][
            ["Nama Hotel", "City", "Nama Group/ Non Group", "Email", "Checking Remarks", "Result", "Next Action"]
        ].copy()
        dq["Email"] = np.where(data.loc[dq.index, "Email Missing"], "Missing", dq["Email"])
        dq["Checking Remarks"] = np.where(data.loc[dq.index, "Remarks Missing"], "Missing", dq["Checking Remarks"])
        dataframe_card("Daftar Data yang Perlu Dilengkapi", dq.head(100), "📋", 445)
    with right2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("Quality Checklist", "✅")
        checklist = [
            ("Nama Hotel", True),
            ("City", True),
            ("Publish Rate", True),
            ("Corporate Rate 2026", True),
            ("Nilai Selisih", True),
            ("Result", metadata.get("result_whitespace_issue", 0) == 0),
            ("Next Action", True),
            ("Email", s["missing_email"] == 0),
            ("Checking Remarks", s["missing_remarks"] == 0),
        ]
        for label, ok in checklist:
            badge = "pill-green" if ok else "pill-yellow"
            text = "Lengkap" if ok else "Perlu dicek"
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #E2E8F0'><b>{label}</b><span class='pill {badge}'>{text}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if metadata.get("result_whitespace_issue", 0):
            insight_card(
                "Catatan cleaning kategori",
                f"Ada {metadata.get('result_whitespace_issue', 0)} record dengan spasi tambahan pada kolom Result. Dashboard ini otomatis menormalisasi agar analisis tidak pecah kategori.",
                "Cleaning Applied",
                "pill-yellow",
            )


def page_recommendations(data: pd.DataFrame) -> None:
    s = kpi_summary(data)
    p1 = int(data["Priority"].eq("P1 - Urgent Negative").sum()) if not data.empty else 0
    sign = s["sign_kontrak"]

    cols = st.columns(5)
    with cols[0]:
        kpi_card("Total Opportunity", format_rupiah(s["total_gap"]), "net selisih", "🏨", "navy")
    with cols[1]:
        kpi_card("Recommend", f"{s['recommend']}", "maintain rate", "✅", "green")
    with cols[2]:
        kpi_card("Revise", f"{s['revise']}", "review needed", "✏️", "yellow")
    with cols[3]:
        kpi_card("Priority Negatif", f"{p1}", "urgent", "⬇️", "red")
    with cols[4]:
        kpi_card("Remaining Sign Kontrak", f"{sign}", "finalisasi", "📄", "navy")

    if data.empty:
        empty_state()
        return

    regional = aggregate_by(data, "City").sort_values("Total Selisih", ascending=False)
    groups = aggregate_by(data, "Nama Group/ Non Group").sort_values("Total Selisih", ascending=False)
    top_city = regional.head(3)["City"].tolist()
    top_group = groups.head(2)["Nama Group/ Non Group"].tolist()
    neg_hotels = data[data["Nilai Selisih"] < 0].sort_values("Nilai Selisih").head(3)["Nama Hotel"].tolist()

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_header("Ringkasan Temuan Utama", "💡")
    insight_cols = st.columns(5)
    with insight_cols[0]:
        insight_card("Mayoritas hotel recommend", f"{s['recommend']} hotel dapat dipertahankan dengan maintain rate karena corporate masih kompetitif.", "Maintain", "pill-green")
    with insight_cols[1]:
        insight_card("Kontribusi terbesar wilayah", f"Area utama: <b>{', '.join(top_city)}</b>. Wilayah ini layak menjadi fokus optimasi rate.", "Regional", "pill-green")
    with insight_cols[2]:
        insight_card("Group utama", f"Group dominan: <b>{', '.join(top_group)}</b>. Pendekatan group contract bisa mempercepat follow-up.", "Group", "pill-yellow")
    with insight_cols[3]:
        insight_card("Hotel berselisih negatif", f"Prioritas negosiasi: <b>{', '.join(neg_hotels) if neg_hotels else '-'}</b>.", "Risk", "pill-red")
    with insight_cols[4]:
        insight_card("Kontrak tersisa", f"Ada {sign} hotel pada tahap Sign Kontrak; finalisasi dapat mengunci benefit 2026.", "Contract", "")
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.1, .9])
    with left:
        actions = pd.DataFrame(
            [
                ["Pertahankan Rate Unggul", "Maintain rate hotel recommend dan berkontribusi tinggi", "P1", "Tinggi", "Rendah"],
                ["Negosiasi Ulang Hotel Negatif", "Fokus hotel dengan corporate rate lebih mahal dari publish", "P1", "Tinggi", "Sedang"],
                ["Review Group Revisi Tinggi", "Cek group dengan volume revise tinggi untuk pembaruan rate", "P2", "Sedang", "Sedang"],
                ["Selesaikan Sign Kontrak", "Finalisasi hotel pada tahap Sign Kontrak", "P2", "Tinggi", "Sedang"],
                ["Lengkapi Data", "Prioritaskan email dan remarks missing", "P3", "Sedang", "Rendah"],
            ],
            columns=["Rekomendasi Tindak Lanjut", "Detail", "Prioritas", "Impact", "Effort"],
        )
        dataframe_card("Rekomendasi Tindak Lanjut", actions, "📋", 305)
    with right:
        chart_card("Impact vs Effort", impact_effort_chart(data), "🎯")

    left2, right2 = st.columns([.95, 1.05])
    with left2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_header("30-60-90 Day Plan", "🗓️")
        plan = [
            ("30 Hari", "Fondasi & Quick Win", "Amankan rate hotel recommend berkontribusi tinggi, tindak cepat P1 negatif, lengkapi email missing."),
            ("60 Hari", "Akselerasi & Negosiasi", "Negosiasi hotel negatif dan revise tipis, review group dengan revise tinggi, perbarui rate wilayah prioritas."),
            ("90 Hari", "Finalisasi & Optimasi", "Finalisasi Sign Kontrak, evaluasi hasil negosiasi, susun strategi 2026+ berbasis data."),
        ]
        for label, title, body in plan:
            st.markdown(f"<div style='display:flex;gap:14px;padding:12px 0;border-bottom:1px solid #E2E8F0'><div class='kpi-icon' style='width:48px;height:48px'>{label.split()[0]}</div><div><b>{title}</b><br><span style='color:#475569'>{body}</span></div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right2:
        target = regional.head(7)[["City", "Jumlah Hotel", "Total Selisih", "Recommend", "Revise"]].copy()
        target["Fokus Utama"] = np.where(target["Revise"] > target["Recommend"] * 0.25, "Review & negosiasi rate", "Pertahankan rate unggul")
        target["Potential Impact"] = target["Total Selisih"].rank(method="dense", ascending=False).map(lambda x: "★" * max(1, int(6 - min(x, 5))))
        dataframe_card("Target Focus", style_numeric_table(target[["City", "Fokus Utama", "Total Selisih", "Potential Impact"]]), "🎯", 400)

    st.markdown("<div class='footer-band'>🎯 Arah utama: maksimalkan value dari hotel berkontribusi tinggi sambil menurunkan risiko pada portofolio revise dan selisih negatif.</div>", unsafe_allow_html=True)


# =============================================================
# 8. MAIN APPLICATION
# =============================================================


def main() -> None:
    inject_css()
    page = sidebar_nav()
    raw = data_source_selector()
    data, metadata = clean_dataframe(raw)

    # Sidebar quick portfolio stats.
    s_all = kpi_summary(data)
    st.sidebar.markdown("### 📌 Portfolio Quick Stats")
    st.sidebar.metric("Total Hotel", f"{s_all['total']:,}".replace(",", "."))
    st.sidebar.metric("Total Nilai Selisih", format_rupiah(s_all["total_gap"]))
    st.sidebar.metric("Recommend / Revise", f"{s_all['recommend']} / {s_all['revise']}")
    st.sidebar.caption("Data per: 26 Mei 2026 · Tahun analisis 2026")

    page_title(page)
    filtered, context = global_filters(data)

    st.caption(
        f"Filter aktif: City = {context['city']} · Group = {context['group']} · Result = {context['result']} · "
        f"Next Action = {context['action']} · Band = {context['band']} · Record tampil = {len(filtered):,}".replace(",", ".")
    )

    if page == "01 Executive Overview":
        page_executive_overview(filtered, metadata)
    elif page == "02 Regional Analysis":
        page_regional_analysis(filtered)
    elif page == "03 Group Performance":
        page_group_performance(filtered)
    elif page == "04 Top Opportunity Hotels":
        page_top_opportunity(filtered)
    elif page == "05 Price Gap Analytics":
        page_price_gap(filtered)
    elif page == "06 Revise Priority":
        page_revise_priority(filtered)
    elif page == "07 Action Tracker":
        page_action_tracker(filtered)
    elif page == "08 Hotel Explorer":
        page_hotel_explorer(filtered)
    elif page == "09 Data Quality":
        page_data_quality(filtered, metadata)
    elif page == "10 Executive Recommendations":
        page_recommendations(filtered)

    st.markdown("---")
    st.caption(
        "Dashboard ini dibuat untuk analisis Corporate Rate Hotel Pertamina 2026. "
        "Semua metrik mengikuti filter aktif dan otomatis membaca dataset langsung dari Google Sheets."
    )


if __name__ == "__main__":
    main()
