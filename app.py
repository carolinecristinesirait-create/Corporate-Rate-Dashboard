# =============================================================
# Dashboard Corporate Rate Hotel Pertamina 2026
# PURE GOOGLE SHEETS VERSION
# =============================================================

from __future__ import annotations

import math
import re
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =============================================================
# 1. CONFIGURATION
# =============================================================

# Link Google Sheets yang kamu kirim.
GOOGLE_SHEET_SHARE_URL = "https://docs.google.com/spreadsheets/d/1aydlmGDgVhGDFgxgLeciUDBvbgCA3Z-dBSOYu6pQ8aU/edit?usp=sharing"

# ID dan GID dipakai untuk membaca data sebagai CSV oleh Streamlit.
GOOGLE_SHEET_ID = "1aydlmGDgVhGDFgxgLeciUDBvbgCA3Z-dBSOYu6pQ8aU"
GOOGLE_SHEET_GID = "0"
GOOGLE_SHEET_URL = GOOGLE_SHEET_SHARE_URL
GOOGLE_SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={GOOGLE_SHEET_GID}"
DATA_REFRESH_TTL_SECONDS = 300

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
    "red": "#E31E24",
    "green": "#008E5A",
    "green_2": "#00A859",
    "yellow": "#FDB913",
    "orange": "#F59E0B",
    "teal": "#007C7A",
    "white": "#FFFFFF",
    "ink": "#0B1F3A",
    "muted": "#64748B",
    "canvas": "#EAF3FB",
    "soft": "#F8FBFF",
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

CHART_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}


# =============================================================
# 2. STREAMLIT SETUP & CSS
# =============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {{
            --navy: {COLORS['navy']};
            --blue: {COLORS['blue']};
            --green: {COLORS['green']};
            --red: {COLORS['red']};
            --yellow: {COLORS['yellow']};
            --ink: {COLORS['ink']};
            --muted: {COLORS['muted']};
            --card-border: rgba(255,255,255,.22);
            --glass: rgba(255,255,255,.08);
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', Arial, sans-serif !important;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 15% 10%, rgba(0,102,179,.28), transparent 28%),
                radial-gradient(circle at 88% 18%, rgba(0,142,90,.25), transparent 30%),
                linear-gradient(135deg, #002B5B 0%, #004D7A 45%, #007C7A 100%) !important;
        }}

        .main .block-container {{
            max-width: 1540px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #002B5B 0%, #03234B 55%, #061A36 100%) !important;
            border-right: 1px solid rgba(255,255,255,.13);
        }}

        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] .stRadio label {{
            padding: .42rem .62rem;
            border-radius: 999px;
            font-weight: 800;
        }}

        div[role="radiogroup"] label:has(input:checked) {{
            background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['green']}) !important;
        }}

        .brand-box {{
            padding: 1.25rem 1rem 1.1rem 1rem;
            border-radius: 24px;
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.16);
            margin-bottom: 1rem;
        }}

        .brand-row {{
            display: flex;
            gap: .78rem;
            align-items: center;
        }}

        .brand-logo {{
            display:flex;
            gap:.28rem;
            align-items:flex-end;
            height:46px;
        }}
        .brand-bar {{ width:14px; border-radius:8px 8px 4px 4px; }}
        .brand-blue {{ background:{COLORS['blue']}; height:28px; }}
        .brand-green {{ background:{COLORS['green_2']}; height:44px; }}
        .brand-red {{ background:{COLORS['red']}; height:35px; }}

        .brand-title {{
            font-size: 1.08rem;
            line-height: 1.08;
            font-weight: 900;
            color: #FFFFFF !important;
            margin-bottom: .22rem;
        }}
        .brand-subtitle {{
            font-size: .75rem;
            font-weight: 700;
            color: rgba(255,255,255,.72) !important;
        }}

        .hero {{
            padding: 1.4rem 1.45rem;
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(0,43,91,.95), rgba(0,102,179,.88) 48%, rgba(0,142,90,.86)),
                radial-gradient(circle at top right, rgba(253,185,19,.35), transparent 24%);
            border: 1px solid rgba(255,255,255,.25);
            box-shadow: 0 24px 70px rgba(0,0,0,.18);
            margin-bottom: 1.15rem;
        }}
        .hero h1 {{
            color: #FFFFFF !important;
            margin: 0;
            font-size: clamp(1.75rem, 3.5vw, 3.15rem);
            letter-spacing: -0.05em;
            font-weight: 950;
            line-height: 1.02;
        }}
        .hero p {{
            color: rgba(255,255,255,.86) !important;
            margin: .55rem 0 0 0;
            font-size: 1rem;
            font-weight: 600;
        }}

        .kpi-card {{
            min-height: 122px;
            padding: 1rem 1.05rem;
            border-radius: 24px;
            background: linear-gradient(160deg, rgba(255,255,255,.96), rgba(235,245,255,.94));
            border: 1px solid rgba(255,255,255,.75);
            box-shadow: 0 18px 48px rgba(0,43,91,.16);
            position: relative;
            overflow: hidden;
        }}
        .kpi-card::before {{
            content:"";
            position:absolute;
            inset:0 auto 0 0;
            width:8px;
            background: linear-gradient(180deg, {COLORS['blue']}, {COLORS['green']});
        }}
        .kpi-icon {{
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display:flex;
            align-items:center;
            justify-content:center;
            background: rgba(0,102,179,.11);
            font-size: 1.15rem;
            margin-bottom: .42rem;
        }}
        .kpi-label {{
            color: {COLORS['muted']} !important;
            font-weight: 800;
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: .06em;
        }}
        .kpi-value {{
            color: {COLORS['ink']} !important;
            font-weight: 950;
            font-size: clamp(1.25rem, 2.2vw, 2rem);
            line-height: 1.02;
            margin-top: .24rem;
        }}
        .kpi-note {{
            color: {COLORS['muted']} !important;
            font-weight: 700;
            font-size: .78rem;
            margin-top: .38rem;
        }}

        .chart-card {{
            background: linear-gradient(145deg, rgba(0,43,91,.62), rgba(0,102,179,.36) 52%, rgba(0,142,90,.22));
            border: 1px solid rgba(255,255,255,.20);
            border-radius: 26px;
            padding: 1rem 1rem 1.15rem 1rem;
            box-shadow: 0 20px 50px rgba(0,0,0,.14);
            margin-bottom: 1rem;
            overflow: hidden;
        }}

        .chart-heading {{
            display:flex;
            align-items:center;
            gap:.58rem;
            margin: .05rem 0 .82rem 0;
            color: #FFFFFF !important;
            font-size: clamp(1rem, 1.6vw, 1.38rem);
            font-weight: 950;
            letter-spacing: -0.035em;
            line-height:1.2;
            text-shadow: 0 2px 12px rgba(0,0,0,.28);
        }}
        .chart-heading * {{ color: #FFFFFF !important; }}
        .chart-heading .dot {{
            flex: 0 0 auto;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: conic-gradient(from 45deg, {COLORS['green']}, {COLORS['yellow']}, {COLORS['red']}, {COLORS['blue']}, {COLORS['green']});
            box-shadow: 0 0 0 9px rgba(0,142,90,.13);
        }}
        .chart-heading .icon {{
            color:#FFFFFF !important;
            filter: drop-shadow(0 2px 7px rgba(0,0,0,.25));
        }}

        .note-card {{
            background: rgba(255,255,255,.94);
            border: 1px solid rgba(255,255,255,.75);
            border-radius: 22px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            color: {COLORS['ink']} !important;
            box-shadow: 0 16px 40px rgba(0,43,91,.12);
        }}
        .note-card h3 {{
            color:{COLORS['ink']} !important;
            font-weight: 900;
            margin:0 0 .45rem 0;
        }}
        .note-card p, .note-card li {{
            color:{COLORS['ink']} !important;
            font-weight: 650;
        }}

        .dataframe th {{
            background: {COLORS['navy']} !important;
            color: #FFFFFF !important;
            font-weight: 900 !important;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 18px;
        }}
        div[data-testid="stButton"] button {{
            border-radius: 999px;
            font-weight: 900;
            border: 1px solid rgba(255,255,255,.55);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================
# 3. DATA LOADING & CLEANING
# =============================================================

@st.cache_data(ttl=DATA_REFRESH_TTL_SECONDS, show_spinner=False)
def load_google_sheet(url: str) -> pd.DataFrame:
    """Read public Google Sheets CSV export."""
    return pd.read_csv(url, dtype=str, keep_default_na=False)


def normalize_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).replace("\u00a0", " ").strip()


def parse_money(value: object) -> float:
    """Convert currency-like strings to numeric values."""
    if value is None or pd.isna(value):
        return 0.0
    text = str(value).strip()
    if text == "":
        return 0.0

    text = text.replace("\u00a0", " ")
    text = text.replace("Rp", "").replace("IDR", "")
    text = text.replace(" ", "")
    text = text.replace("−", "-")

    is_negative = False
    if text.startswith("(") and text.endswith(")"):
        is_negative = True
        text = text[1:-1]

    text = re.sub(r"[^0-9,.-]", "", text)
    if text.count(",") > 0 and text.count(".") > 0:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif text.count(",") > 0:
        parts = text.split(",")
        if len(parts[-1]) in (1, 2):
            text = text.replace(",", ".")
        else:
            text = text.replace(",", "")
    elif text.count(".") > 0:
        parts = text.split(".")
        if len(parts[-1]) == 3 and len(parts) > 1:
            text = text.replace(".", "")

    try:
        number = float(text)
        return -number if is_negative else number
    except Exception:
        return 0.0


def normalize_result(value: object, selisih: float = 0.0) -> str:
    text = normalize_text(value).lower()
    if "revise" in text or "revisi" in text:
        return "Revise"
    if "recommend" in text or "rekom" in text:
        return "Recommend"
    if "same" in text or "sama" in text or "equal" in text:
        return "Sama"
    if text == "":
        if selisih > 0:
            return "Recommend"
        if selisih < 0:
            return "Revise"
        return "Sama"
    return text.title()


def prepare_data(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [normalize_text(c) for c in df.columns]

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[REQUIRED_COLUMNS].copy()
    df = df.replace({"": np.nan})
    df = df.dropna(how="all")
    df = df.fillna("")

    for col in [
        "Group/ Non Group",
        "Nama Group/ Non Group",
        "City",
        "Nama Hotel",
        "Email",
        "Result",
        "Next Action",
        "Checking Remarks",
        "Status",
    ]:
        df[col] = df[col].map(normalize_text)

    df["Publish Rate Num"] = df["Publish Rate"].map(parse_money)
    df["Offering Rate Num"] = df["Offering Corporate Rate 2026"].map(parse_money)
    df["Nilai Selisih Num"] = df["Nilai Selisih"].map(parse_money)

    missing_gap = df["Nilai Selisih Num"].eq(0) & df["Publish Rate Num"].ne(0) & df["Offering Rate Num"].ne(0)
    df.loc[missing_gap, "Nilai Selisih Num"] = df.loc[missing_gap, "Publish Rate Num"] - df.loc[missing_gap, "Offering Rate Num"]

    df["Result"] = [normalize_result(r, s) for r, s in zip(df["Result"], df["Nilai Selisih Num"])]
    df["Group/ Non Group"] = df["Group/ Non Group"].replace("", "Tidak Terisi")
    df["Nama Group/ Non Group"] = df["Nama Group/ Non Group"].replace("", "Tidak Terisi")
    df["City"] = df["City"].replace("", "Tidak Terisi")
    df["Nama Hotel"] = df["Nama Hotel"].replace("", "Tidak Terisi")
    df["Next Action"] = df["Next Action"].replace("", "Belum Terisi")
    df["Status"] = df["Status"].replace("", "Belum Terisi")
    df["Checking Remarks"] = df["Checking Remarks"].replace("", "Belum Terisi")

    df["Has Email"] = df["Email"].str.contains("@", na=False)
    df["Gap Abs"] = df["Nilai Selisih Num"].abs()
    df["Gap Band"] = pd.cut(
        df["Nilai Selisih Num"],
        bins=[-np.inf, -1, 0, 1_000_000, 3_000_000, 5_000_000, np.inf],
        labels=["Negatif", "Sama", "0-1M", "1-3M", "3-5M", ">5M"],
        include_lowest=True,
    ).astype(str)

    return df.reset_index(drop=True)


# =============================================================
# 4. FORMATTERS & UI HELPERS
# =============================================================

def format_rp(value: float, compact: bool = True) -> str:
    if value is None or pd.isna(value):
        value = 0
    sign = "-" if value < 0 else ""
    value = abs(float(value))
    if compact:
        if value >= 1_000_000_000:
            return f"{sign}Rp{value / 1_000_000_000:.1f}B"
        if value >= 1_000_000:
            return f"{sign}Rp{value / 1_000_000:.1f}M"
        if value >= 1_000:
            return f"{sign}Rp{value / 1_000:.1f}K"
    return f"{sign}Rp{value:,.0f}".replace(",", ".")


def shorten_label(text: object, max_len: int = 30) -> str:
    text = normalize_text(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def kpi_card(label: str, value: str, note: str = "", icon: str = "📌") -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str = "") -> None:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            {sub}
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card(title: str, fig: go.Figure, icon: str = "") -> None:
    icon_html = f"<span class='icon'>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-heading"><span class="dot"></span>{icon_html}<span>{title}</span></div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
    st.markdown("</div>", unsafe_allow_html=True)


def note_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="note-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_plot_theme(fig: go.Figure, height: int = 420, show_legend: bool = True) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=110, r=95, t=28, b=70),
        font=dict(family="Inter, Arial, sans-serif", color=COLORS["ink"], size=12),
        paper_bgcolor="#F8FBFF",
        plot_bgcolor="#F8FBFF",
        colorway=[COLORS["navy"], COLORS["green"], COLORS["yellow"], COLORS["blue"], COLORS["red"], COLORS["teal"]],
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.23,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0)",
            font=dict(color=COLORS["ink"], size=12),
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#D7E0EA",
            font=dict(color=COLORS["ink"], family="Inter, Arial, sans-serif", size=12),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(100,116,139,.22)",
        zerolinecolor="rgba(100,116,139,.25)",
        linecolor="rgba(15,23,42,.20)",
        tickfont=dict(color=COLORS["ink"], size=12),
        title_font=dict(color=COLORS["ink"], size=13),
    )
    fig.update_yaxes(
        gridcolor="rgba(100,116,139,.12)",
        zerolinecolor="rgba(100,116,139,.25)",
        linecolor="rgba(15,23,42,.20)",
        tickfont=dict(color=COLORS["ink"], size=12),
        title_font=dict(color=COLORS["ink"], size=13),
    )
    return fig


# =============================================================
# 5. CHART FUNCTIONS
# =============================================================

def result_donut(data: pd.DataFrame) -> go.Figure:
    """Donut Komposisi Result: label inside slice like the requested sample."""
    order = ["Recommend", "Revise"]
    counts = data["Result"].value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["Result", "Jumlah"]
    counts = counts[counts["Jumlah"] > 0]

    if counts.empty:
        fig = go.Figure()
        fig.add_annotation(text="Tidak ada data", x=.5, y=.5, showarrow=False, font=dict(size=18, color=COLORS["ink"]))
        fig.update_layout(height=420, paper_bgcolor=COLORS["canvas"], plot_bgcolor=COLORS["canvas"])
        return fig

    color_map = {"Recommend": COLORS["green"], "Revise": COLORS["yellow"]}
    text_colors = ["#FFFFFF" if x == "Recommend" else COLORS["ink"] for x in counts["Result"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts["Result"],
                values=counts["Jumlah"],
                hole=0.52,
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
                    colors=[color_map.get(x, COLORS["blue"]) for x in counts["Result"]],
                    line=dict(color=COLORS["canvas"], width=5),
                ),
                hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,.0f} hotel<br>Persentase: %{percent}<extra></extra>",
                showlegend=False,
            )
        ]
    )

    fig.update_layout(
        template="plotly_white",
        height=460,
        margin=dict(l=30, r=30, t=8, b=8),
        paper_bgcolor=COLORS["canvas"],
        plot_bgcolor=COLORS["canvas"],
        font=dict(family="Inter, Arial, sans-serif", color=COLORS["ink"], size=13),
        uniformtext_minsize=13,
        uniformtext_mode="show",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#D7E0EA",
            font=dict(color=COLORS["ink"], family="Inter, Arial, sans-serif", size=12),
        ),
    )
    return fig


def horizontal_bar(
    data: pd.DataFrame,
    group_col: str,
    value_col: str = "Nilai Selisih Num",
    top_n: int = 10,
    color: str = COLORS["navy"],
    value_format: str = "rp",
    height: Optional[int] = None,
) -> go.Figure:
    summary = (
        data.groupby(group_col, dropna=False)[value_col]
        .sum()
        .reset_index()
        .sort_values(value_col, ascending=False)
        .head(top_n)
    )
    summary["Label"] = summary[group_col].map(lambda x: shorten_label(x, 34))
    summary["Text"] = summary[value_col].map(format_rp if value_format == "rp" else lambda x: f"{x:,.0f}")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=summary[value_col],
            y=summary["Label"],
            orientation="h",
            marker=dict(color=color, line=dict(color="rgba(255,255,255,.85)", width=1.2)),
            text=summary["Text"],
            textposition="outside",
            textfont=dict(color=COLORS["ink"], size=13, family="Inter, Arial, sans-serif"),
            customdata=np.stack([summary[group_col].astype(str), summary[value_col]], axis=-1) if not summary.empty else None,
            hovertemplate="<b>%{customdata[0]}</b><br>Nilai: %{text}<extra></extra>",
            cliponaxis=False,
        )
    )

    max_val = summary[value_col].max() if not summary.empty else 1
    min_val = summary[value_col].min() if not summary.empty else 0
    padding = max(abs(max_val), abs(min_val), 1) * 0.25
    fig.update_xaxes(range=[min(0, min_val) - padding * .2, max(0, max_val) + padding])
    fig.update_yaxes(autorange="reversed")
    return apply_plot_theme(fig, height=height or max(390, 58 * len(summary) + 120), show_legend=False)


def count_bar(data: pd.DataFrame, group_col: str, top_n: int = 10, color: str = COLORS["green"], height: Optional[int] = None) -> go.Figure:
    summary = data[group_col].value_counts().head(top_n).reset_index()
    summary.columns = [group_col, "Jumlah"]
    summary["Label"] = summary[group_col].map(lambda x: shorten_label(x, 34))

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=summary["Jumlah"],
            y=summary["Label"],
            orientation="h",
            marker=dict(color=color, line=dict(color="rgba(255,255,255,.85)", width=1.2)),
            text=summary["Jumlah"],
            textposition="outside",
            textfont=dict(color=COLORS["ink"], size=13, family="Inter, Arial, sans-serif"),
            customdata=summary[group_col],
            hovertemplate="<b>%{customdata}</b><br>Jumlah: %{x:,.0f} hotel<extra></extra>",
            cliponaxis=False,
        )
    )
    fig.update_xaxes(range=[0, max(summary["Jumlah"].max() * 1.22, 1)])
    fig.update_yaxes(autorange="reversed")
    return apply_plot_theme(fig, height=height or max(390, 54 * len(summary) + 115), show_legend=False)


def stacked_result_by_group(data: pd.DataFrame, group_col: str, top_n: int = 8) -> go.Figure:
    top_groups = data[group_col].value_counts().head(top_n).index.tolist()
    subset = data[data[group_col].isin(top_groups)].copy()
    pivot = (
        subset.groupby([group_col, "Result"], dropna=False)
        .size()
        .reset_index(name="Jumlah")
    )
    result_order = ["Recommend", "Revise", "Sama"]
    color_map = {"Recommend": COLORS["green"], "Revise": COLORS["yellow"], "Sama": COLORS["blue"]}
    fig = go.Figure()

    for result in result_order:
        part = pivot[pivot["Result"] == result].set_index(group_col).reindex(top_groups, fill_value=0).reset_index()
        labels = [shorten_label(x, 26) for x in part[group_col]]
        fig.add_trace(
            go.Bar(
                x=part["Jumlah"],
                y=labels,
                orientation="h",
                name=result,
                marker=dict(color=color_map[result], line=dict(color="#FFFFFF", width=1)),
                text=[str(int(x)) if x > 0 else "" for x in part["Jumlah"]],
                textposition="inside",
                textfont=dict(color=COLORS["ink"] if result == "Revise" else "#FFFFFF", size=12),
                customdata=np.stack([part[group_col].astype(str), part["Jumlah"]], axis=-1),
                hovertemplate="<b>%{customdata[0]}</b><br>Result: " + result + "<br>Jumlah: %{customdata[1]:,.0f}<extra></extra>",
            )
        )

    fig.update_layout(barmode="stack")
    fig.update_yaxes(autorange="reversed")
    return apply_plot_theme(fig, height=max(420, 58 * len(top_groups) + 130), show_legend=True)


def result_by_group_type(data: pd.DataFrame) -> go.Figure:
    summary = (
        data.groupby(["Group/ Non Group", "Result"], dropna=False)
        .size()
        .reset_index(name="Jumlah")
    )
    color_map = {"Recommend": COLORS["green"], "Revise": COLORS["yellow"], "Sama": COLORS["blue"]}
    fig = px.bar(
        summary,
        x="Jumlah",
        y="Group/ Non Group",
        color="Result",
        orientation="h",
        text="Jumlah",
        color_discrete_map=color_map,
    )
    fig.update_traces(textposition="inside", marker_line_color="#FFFFFF", marker_line_width=1)
    fig.update_yaxes(autorange="reversed")
    return apply_plot_theme(fig, height=420, show_legend=True)


def scatter_gap(data: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        data,
        x="Publish Rate Num",
        y="Offering Rate Num",
        size="Gap Abs",
        color="Result",
        color_discrete_map={"Recommend": COLORS["green"], "Revise": COLORS["red"], "Sama": COLORS["blue"]},
        hover_name="Nama Hotel",
        hover_data={"City": True, "Nama Group/ Non Group": True, "Nilai Selisih Num": ":,.0f"},
    )
    max_axis = max(data["Publish Rate Num"].max(), data["Offering Rate Num"].max(), 1)
    fig.add_trace(
        go.Scatter(
            x=[0, max_axis],
            y=[0, max_axis],
            mode="lines",
            line=dict(color=COLORS["muted"], width=2, dash="dash"),
            name="Publish = Offering",
            hoverinfo="skip",
        )
    )
    return apply_plot_theme(fig, height=520, show_legend=True)


def gap_histogram(data: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        data,
        x="Nilai Selisih Num",
        nbins=30,
        color="Result",
        color_discrete_map={"Recommend": COLORS["green"], "Revise": COLORS["yellow"], "Sama": COLORS["blue"]},
    )
    fig.update_layout(bargap=.08)
    return apply_plot_theme(fig, height=430, show_legend=True)


def gap_band_bar(data: pd.DataFrame) -> go.Figure:
    order = ["Negatif", "Sama", "0-1M", "1-3M", "3-5M", ">5M"]
    summary = data["Gap Band"].value_counts().reindex(order, fill_value=0).reset_index()
    summary.columns = ["Gap Band", "Jumlah"]
    fig = px.bar(
        summary,
        x="Gap Band",
        y="Jumlah",
        text="Jumlah",
        color="Gap Band",
        color_discrete_map={"Negatif": COLORS["red"], "Sama": COLORS["blue"], "0-1M": COLORS["teal"], "1-3M": COLORS["green"], "3-5M": COLORS["yellow"], ">5M": COLORS["navy"]},
    )
    fig.update_traces(textposition="outside", marker_line_color="#FFFFFF", marker_line_width=1.2)
    return apply_plot_theme(fig, height=430, show_legend=False)


def missing_chart(data: pd.DataFrame) -> go.Figure:
    checks = {
        "Email": data["Email"].eq("").sum(),
        "Next Action": data["Next Action"].eq("Belum Terisi").sum(),
        "Checking Remarks": data["Checking Remarks"].eq("Belum Terisi").sum(),
        "Status": data["Status"].eq("Belum Terisi").sum(),
        "City": data["City"].eq("Tidak Terisi").sum(),
    }
    summary = pd.DataFrame({"Kolom": list(checks.keys()), "Missing": list(checks.values())}).sort_values("Missing", ascending=False)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=summary["Missing"],
            y=summary["Kolom"],
            orientation="h",
            marker=dict(color=COLORS["red"], line=dict(color="#FFFFFF", width=1.2)),
            text=summary["Missing"],
            textposition="outside",
            cliponaxis=False,
        )
    )
    fig.update_xaxes(range=[0, max(summary["Missing"].max() * 1.25, 1)])
    fig.update_yaxes(autorange="reversed")
    return apply_plot_theme(fig, height=420, show_legend=False)


# =============================================================
# 6. FILTERS
# =============================================================

def sidebar_brand() -> None:
    st.sidebar.markdown(
        f"""
        <div class="brand-box">
            <div class="brand-row">
                <div class="brand-logo">
                    <div class="brand-bar brand-blue"></div>
                    <div class="brand-bar brand-green"></div>
                    <div class="brand-bar brand-red"></div>
                </div>
                <div>
                    <div class="brand-title">Corporate Rate<br>Hotel Pertamina 2026</div>
                    <div class="brand-subtitle">Live Google Sheets Dashboard</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("### 🎛️ Filter Dashboard")
    cities = sorted(data["City"].dropna().unique().tolist())
    results = sorted(data["Result"].dropna().unique().tolist())
    group_types = sorted(data["Group/ Non Group"].dropna().unique().tolist())

    selected_city = st.sidebar.multiselect("City", cities, default=[])
    selected_result = st.sidebar.multiselect("Result", results, default=[])
    selected_group_type = st.sidebar.multiselect("Group / Non Group", group_types, default=[])
    keyword = st.sidebar.text_input("Cari nama hotel / group")

    filtered = data.copy()
    if selected_city:
        filtered = filtered[filtered["City"].isin(selected_city)]
    if selected_result:
        filtered = filtered[filtered["Result"].isin(selected_result)]
    if selected_group_type:
        filtered = filtered[filtered["Group/ Non Group"].isin(selected_group_type)]
    if keyword.strip():
        key = keyword.strip().lower()
        filtered = filtered[
            filtered["Nama Hotel"].str.lower().str.contains(key, na=False)
            | filtered["Nama Group/ Non Group"].str.lower().str.contains(key, na=False)
            | filtered["City"].str.lower().str.contains(key, na=False)
        ]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Data Source")
    st.sidebar.markdown(f"[Buka Google Sheets]({GOOGLE_SHEET_URL})")
    if st.sidebar.button("Refresh data sekarang"):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Quick Stats")
    st.sidebar.write(f"Hotel aktif: **{len(filtered):,.0f}**")
    st.sidebar.write(f"Kota/region: **{filtered['City'].nunique():,.0f}**")
    st.sidebar.write(f"Group: **{filtered['Nama Group/ Non Group'].nunique():,.0f}**")
    return filtered


# =============================================================
# 7. PAGES
# =============================================================

def page_executive(data: pd.DataFrame) -> None:
    section_title("Executive Overview", "Ringkasan performa corporate rate hotel berdasarkan data live Google Sheets.")
    total = len(data)
    recommend = int((data["Result"] == "Recommend").sum())
    revise = int((data["Result"] == "Revise").sum())
    total_gap = data["Nilai Selisih Num"].sum()
    avg_gap = data["Nilai Selisih Num"].mean() if total else 0
    complete_email = data["Has Email"].mean() * 100 if total else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Total Hotel", f"{total:,.0f}", "baris data aktif", "🏨")
    with c2: kpi_card("Recommend", f"{recommend:,.0f}", f"{recommend / max(total,1):.1%} dari data", "✅")
    with c3: kpi_card("Revise", f"{revise:,.0f}", f"{revise / max(total,1):.1%} dari data", "🟡")
    with c4: kpi_card("Total Selisih", format_rp(total_gap), "akumulasi peluang", "💰")
    with c5: kpi_card("Email Valid", f"{complete_email:.1f}%", "kontak terisi", "✉️")

    left, right = st.columns([1, 1.45])
    with left:
        chart_card("Komposisi Result", result_donut(data), "🎯")
    with right:
        chart_card("Top 5 City berdasarkan Total Selisih", horizontal_bar(data, "City", top_n=5, height=460), "📍")

    c1, c2 = st.columns(2)
    with c1:
        chart_card("Top 5 Group berdasarkan Total Selisih", horizontal_bar(data, "Nama Group/ Non Group", top_n=5, color=COLORS["green"], height=440), "👥")
    with c2:
        chart_card("Komposisi Group vs Non Group", result_by_group_type(data), "🏷️")


def page_regional(data: pd.DataFrame) -> None:
    section_title("Regional Analysis", "Analisis distribusi hotel dan peluang nilai selisih per city/region.")
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Jumlah City", f"{data['City'].nunique():,.0f}", "cakupan region", "🌏")
    with c2: kpi_card("City Terbesar", data["City"].value_counts().index[0] if len(data) else "-", "berdasarkan jumlah hotel", "📍")
    with c3: kpi_card("Avg Selisih", format_rp(data["Nilai Selisih Num"].mean()), "rata-rata per hotel", "📊")

    c1, c2 = st.columns(2)
    with c1:
        chart_card("Top 10 City berdasarkan Jumlah Hotel", count_bar(data, "City", top_n=10, color=COLORS["blue"]), "🏨")
    with c2:
        chart_card("Top 10 City berdasarkan Total Selisih", horizontal_bar(data, "City", top_n=10, color=COLORS["navy"]), "💰")

    summary = data.groupby("City", dropna=False).agg(
        Jumlah_Hotel=("Nama Hotel", "count"),
        Recommend=("Result", lambda s: (s == "Recommend").sum()),
        Revise=("Result", lambda s: (s == "Revise").sum()),
        Total_Selisih=("Nilai Selisih Num", "sum"),
        Avg_Selisih=("Nilai Selisih Num", "mean"),
    ).reset_index().sort_values("Total_Selisih", ascending=False)
    st.dataframe(summary, use_container_width=True, hide_index=True)


def page_group(data: pd.DataFrame) -> None:
    section_title("Group Performance", "Perbandingan performa group hotel, non group, dan portofolio brand.")
    c1, c2 = st.columns(2)
    with c1:
        chart_card("Top 10 Group berdasarkan Jumlah Hotel", count_bar(data, "Nama Group/ Non Group", top_n=10, color=COLORS["blue"]), "👥")
    with c2:
        chart_card("Top 10 Group berdasarkan Total Selisih", horizontal_bar(data, "Nama Group/ Non Group", top_n=10, color=COLORS["green"]), "💰")

    chart_card("Komposisi Result per Group", stacked_result_by_group(data, "Nama Group/ Non Group", top_n=10), "📊")


def page_opportunity(data: pd.DataFrame) -> None:
    section_title("Top Opportunity Hotels", "Hotel dengan nilai selisih tertinggi sebagai prioritas negosiasi dan follow-up.")
    positive = data[data["Nilai Selisih Num"] > 0].copy().sort_values("Nilai Selisih Num", ascending=False)
    negative = data[data["Nilai Selisih Num"] < 0].copy().sort_values("Nilai Selisih Num", ascending=True)

    c1, c2 = st.columns(2)
    with c1:
        chart_card("Top 10 Hotel dengan Nilai Selisih Tertinggi", horizontal_bar(positive, "Nama Hotel", top_n=10, color=COLORS["navy"]), "⭐")
    with c2:
        chart_card("Top 10 Hotel dengan Selisih Negatif", horizontal_bar(negative, "Nama Hotel", top_n=10, color=COLORS["red"]), "⚠️")

    display = positive[["City", "Nama Group/ Non Group", "Nama Hotel", "Publish Rate", "Offering Corporate Rate 2026", "Nilai Selisih Num", "Result", "Next Action"]].head(25).copy()
    display["Nilai Selisih"] = display["Nilai Selisih Num"].map(lambda x: format_rp(x, compact=False))
    display = display.drop(columns=["Nilai Selisih Num"])
    st.dataframe(display, use_container_width=True, hide_index=True)


def page_price_gap(data: pd.DataFrame) -> None:
    section_title("Price Gap Analytics", "Analisis pola publish rate, corporate offering, dan distribusi nilai selisih.")
    c1, c2 = st.columns(2)
    with c1:
        chart_card("Distribusi Nilai Selisih", gap_histogram(data), "📊")
    with c2:
        chart_card("Band Nilai Selisih", gap_band_bar(data), "🏷️")
    chart_card("Publish Rate vs Offering Corporate Rate", scatter_gap(data), "🔎")


def page_revise(data: pd.DataFrame) -> None:
    section_title("Revise Priority", "Daftar prioritas hotel yang membutuhkan revisi atau tindak lanjut harga.")
    revise = data[data["Result"] == "Revise"].copy()
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total Revise", f"{len(revise):,.0f}", "perlu follow-up", "🎯")
    with c2: kpi_card("Revise City", f"{revise['City'].nunique():,.0f}", "region terdampak", "📍")
    with c3: kpi_card("Avg Gap Revise", format_rp(revise["Nilai Selisih Num"].mean() if len(revise) else 0), "rata-rata selisih", "💬")

    c1, c2 = st.columns(2)
    with c1:
        chart_card("Revise per City", count_bar(revise, "City", top_n=10, color=COLORS["yellow"]), "📍")
    with c2:
        chart_card("Revise per Group", count_bar(revise, "Nama Group/ Non Group", top_n=10, color=COLORS["red"]), "👥")

    show = revise[["City", "Nama Group/ Non Group", "Nama Hotel", "Email", "Nilai Selisih Num", "Next Action", "Checking Remarks", "Status"]].copy()
    show["Nilai Selisih"] = show["Nilai Selisih Num"].map(lambda x: format_rp(x, compact=False))
    show = show.drop(columns=["Nilai Selisih Num"])
    st.dataframe(show, use_container_width=True, hide_index=True)


def page_action(data: pd.DataFrame) -> None:
    section_title("Action Tracker", "Monitoring status, next action, dan progres tindak lanjut setiap hotel.")
    c1, c2 = st.columns(2)
    with c1:
        chart_card("Status Follow-up", count_bar(data, "Status", top_n=10, color=COLORS["green"]), "✅")
    with c2:
        chart_card("Next Action Terbanyak", count_bar(data, "Next Action", top_n=10, color=COLORS["blue"]), "🗂️")

    tracker = data[["City", "Nama Group/ Non Group", "Nama Hotel", "Result", "Next Action", "Checking Remarks", "Status", "Email"]].copy()
    st.dataframe(tracker, use_container_width=True, hide_index=True)


def page_explorer(data: pd.DataFrame) -> None:
    section_title("Hotel Explorer", "Tabel eksplorasi detail seluruh hotel sesuai filter aktif.")
    search = st.text_input("Cari detail hotel", "")
    view = data.copy()
    if search.strip():
        key = search.strip().lower()
        view = view[
            view["Nama Hotel"].str.lower().str.contains(key, na=False)
            | view["Nama Group/ Non Group"].str.lower().str.contains(key, na=False)
            | view["City"].str.lower().str.contains(key, na=False)
            | view["Email"].str.lower().str.contains(key, na=False)
        ]

    show = view[["No", "Group/ Non Group", "Nama Group/ Non Group", "City", "Nama Hotel", "Email", "Publish Rate", "Offering Corporate Rate 2026", "Nilai Selisih Num", "Result", "Next Action", "Checking Remarks", "Status"]].copy()
    show["Nilai Selisih"] = show["Nilai Selisih Num"].map(lambda x: format_rp(x, compact=False))
    show = show.drop(columns=["Nilai Selisih Num"])
    st.dataframe(show, use_container_width=True, hide_index=True)


def page_quality(data: pd.DataFrame) -> None:
    section_title("Data Quality", "Pemeriksaan kelengkapan field penting untuk menjaga dashboard tetap valid.")
    total = len(data)
    email_rate = data["Has Email"].mean() * 100 if total else 0
    status_rate = (data["Status"] != "Belum Terisi").mean() * 100 if total else 0
    action_rate = (data["Next Action"] != "Belum Terisi").mean() * 100 if total else 0
    duplicate_hotels = data.duplicated(subset=["Nama Hotel", "City"], keep=False).sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Email Valid", f"{email_rate:.1f}%", "field kontak", "✉️")
    with c2: kpi_card("Status Terisi", f"{status_rate:.1f}%", "progress follow-up", "✅")
    with c3: kpi_card("Action Terisi", f"{action_rate:.1f}%", "rencana tindakan", "🗂️")
    with c4: kpi_card("Potensi Duplikat", f"{duplicate_hotels:,.0f}", "nama hotel + city", "🧱")

    c1, c2 = st.columns(2)
    with c1:
        chart_card("Missing Field Penting", missing_chart(data), "⚠️")
    with c2:
        chart_card("Komposisi Group vs Non Group", result_by_group_type(data), "👥")


def page_recommendations(data: pd.DataFrame) -> None:
    section_title("Executive Recommendations", "Rekomendasi otomatis berdasarkan pola nilai selisih, result, dan kelengkapan data.")
    total = len(data)
    recommend_rate = (data["Result"].eq("Recommend").mean() * 100) if total else 0
    revise_rate = (data["Result"].eq("Revise").mean() * 100) if total else 0
    top_city = data.groupby("City")["Nilai Selisih Num"].sum().idxmax() if total else "-"
    top_group = data.groupby("Nama Group/ Non Group")["Nilai Selisih Num"].sum().idxmax() if total else "-"
    missing_email = int((~data["Has Email"]).sum())

    note_card("1. Prioritaskan peluang terbesar", f"Fokuskan negosiasi awal pada city {top_city} dan group {top_group}, karena keduanya memberi kontribusi nilai selisih tertinggi pada data aktif.")
    note_card("2. Kelola kategori Revise", f"Proporsi Revise saat ini sekitar {revise_rate:.1f}%. Hotel pada kategori ini perlu diperiksa ulang agar offering rate lebih kompetitif dan keputusan kontrak lebih aman.")
    note_card("3. Perkuat kelengkapan kontak", f"Masih ada {missing_email:,.0f} baris tanpa email valid. Lengkapi field kontak agar follow-up tidak terhambat.")
    note_card("4. Gunakan dashboard sebagai live monitoring", f"Karena sumber data sudah tersambung ke Google Sheets, update pada spreadsheet bisa langsung dipantau di dashboard setelah cache refresh.")

    c1, c2 = st.columns(2)
    with c1:
        chart_card("Result Portfolio", result_donut(data), "🎯")
    with c2:
        chart_card("Top Opportunity Group", horizontal_bar(data, "Nama Group/ Non Group", top_n=8, color=COLORS["green"]), "💡")


# =============================================================
# 8. MAIN APP
# =============================================================

def main() -> None:
    inject_css()
    sidebar_brand()

    try:
        raw = load_google_sheet(GOOGLE_SHEET_CSV_URL)
        data = prepare_data(raw)
    except Exception as exc:
        st.error("Google Sheets belum bisa dibaca. Pastikan akses spreadsheet diset 'Anyone with the link → Viewer', lalu reboot app.")
        with st.expander("Detail teknis"):
            st.write(str(exc))
        st.stop()

    if data.empty:
        st.error("Data dari Google Sheets kosong. Pastikan baris header dan isi data sudah tersedia.")
        st.stop()

    page = st.sidebar.radio(
        "Menu",
        PAGE_OPTIONS,
        format_func=lambda x: f"{PAGE_ICONS.get(x, '')} {x}",
        label_visibility="collapsed",
    )

    filtered = apply_filters(data)

    if filtered.empty:
        st.warning("Tidak ada data sesuai filter aktif.")
        st.stop()

    if page == "01 Executive Overview":
        page_executive(filtered)
    elif page == "02 Regional Analysis":
        page_regional(filtered)
    elif page == "03 Group Performance":
        page_group(filtered)
    elif page == "04 Top Opportunity Hotels":
        page_opportunity(filtered)
    elif page == "05 Price Gap Analytics":
        page_price_gap(filtered)
    elif page == "06 Revise Priority":
        page_revise(filtered)
    elif page == "07 Action Tracker":
        page_action(filtered)
    elif page == "08 Hotel Explorer":
        page_explorer(filtered)
    elif page == "09 Data Quality":
        page_quality(filtered)
    elif page == "10 Executive Recommendations":
        page_recommendations(filtered)


if __name__ == "__main__":
    main()
