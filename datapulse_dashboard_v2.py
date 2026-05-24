import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataPulse | Enterprise Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg-primary: #080c14;
    --bg-secondary: #0d1220;
    --bg-card: rgba(255,255,255,0.03);
    --border: rgba(255,255,255,0.07);
    --border-accent: rgba(0,230,180,0.3);
    --accent: #00e6b4;
    --accent2: #4f8eff;
    --accent3: #ff5f87;
    --accent4: #ffb84d;
    --accent5: #a78bfa;
    --text-primary: #e8edf5;
    --text-secondary: #7a8599;
    --text-muted: #4a5568;
    --glass: rgba(255,255,255,0.04);
    --glass-border: rgba(255,255,255,0.08);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background: var(--bg-primary);
    background-image:
        radial-gradient(ellipse at 15% 10%, rgba(0,230,180,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(79,142,255,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(167,139,250,0.02) 0%, transparent 70%);
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, #00b894 100%) !important;
    color: #080c14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(0,230,180,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,230,180,0.4) !important;
}

[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-accent) !important;
    border-radius: 12px !important;
}

[data-testid="stMetric"] {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(0,230,180,0.25) !important;
    background: rgba(0,230,180,0.04) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    color: var(--accent) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #080c14 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Syne', sans-serif !important;
}

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

.stSuccess { background: rgba(0,230,180,0.08) !important; border-color: var(--accent) !important; }
.stWarning { background: rgba(255,184,77,0.08) !important; border-color: var(--accent4) !important; }
.stError   { background: rgba(255,95,135,0.08) !important; border-color: var(--accent3) !important; }
.stInfo    { background: rgba(79,142,255,0.08) !important; border-color: var(--accent2) !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }

/* Pulse animation for loading */
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
@keyframes slideIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }

.kpi-card {
    animation: slideIn 0.4s ease forwards;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
for key, val in {
    "df_raw": None, "df_clean": None,
    "cleaning_log": [], "active_section": "overview",
    "anomaly_scores": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Cached Helpers ────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def compute_kpis(df_hash, df):
    missing     = int(df.isnull().sum().sum())
    duplicates  = int(df.duplicated().sum())
    total_cells = df.shape[0] * df.shape[1]
    cleanliness = round((1 - missing / max(total_cells, 1)) * 100, 1)
    mem_bytes   = df.memory_usage(deep=True).sum()
    file_size   = mem_bytes
    return {
        "rows": df.shape[0], "cols": df.shape[1],
        "missing": missing, "duplicates": duplicates,
        "cleanliness": cleanliness,
        "memory_mb": round(mem_bytes / 1024 / 1024, 3),
        "file_size_kb": round(file_size / 1024, 1),
    }

@st.cache_data(show_spinner=False)
def compute_profile(df_hash, df):
    rows = []
    for col in df.columns:
        null_pct    = round(df[col].isnull().mean() * 100, 2)
        unique_pct  = round(df[col].nunique() / max(len(df), 1) * 100, 2)
        dtype       = str(df[col].dtype)
        n_unique    = df[col].nunique()
        high_card   = n_unique > 0.5 * len(df) and df[col].dtype == object
        # Dtype mismatch: object col that looks numeric
        mismatch = False
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors='coerce')
            mismatch = converted.notna().mean() > 0.7
        sample_vals = ", ".join(str(v) for v in df[col].dropna().unique()[:3])
        rows.append({
            "Column": col, "Type": dtype,
            "Null %": null_pct, "Unique %": unique_pct,
            "# Unique": n_unique,
            "High Cardinality": "⚠️ Yes" if high_card else "✓ No",
            "Type Mismatch": "⚠️ Yes" if mismatch else "✓ No",
            "Sample Values": sample_vals,
        })
    return pd.DataFrame(rows)

@st.cache_data(show_spinner=False)
def detect_outliers_iqr(series_hash, series):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return int(((series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)).sum())

@st.cache_data(show_spinner=False)
def compute_anomaly_scores(df_hash, df):
    """Z-score based anomaly scoring per row across numeric columns."""
    num = df.select_dtypes(include=[np.number])
    if num.empty or len(num.columns) < 2:
        return None
    filled = num.fillna(num.median())
    z = ((filled - filled.mean()) / (filled.std() + 1e-9)).abs()
    row_score = z.mean(axis=1).round(4)
    return row_score

def plotly_theme():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#7a8599", size=11),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.04)"),
        margin=dict(l=45, r=20, t=45, b=40),
        colorway=["#00e6b4","#4f8eff","#ff5f87","#ffb84d","#a78bfa","#34d399","#f87171","#38bdf8"],
    )

PALETTE = ["#00e6b4","#4f8eff","#ff5f87","#ffb84d","#a78bfa","#34d399","#f87171","#38bdf8"]

def card(icon, color, title, desc):
    return f"""
    <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
        border-left:3px solid {color};border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.75rem;
        animation:slideIn 0.3s ease;">
        <p style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.9rem;
            color:{color};margin:0 0 5px;">{icon} {title}</p>
        <p style="color:#7a8599;font-size:0.8rem;margin:0;line-height:1.5;">{desc}</p>
    </div>"""

def df_hash(df):
    return str(df.shape) + str(df.columns.tolist()) + str(len(df))

# ─── PDF Generation ────────────────────────────────────────────────────────────
def generate_pdf_report(df, kpis, cleaning_log, is_cleaned):
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Header
        pdf.set_fill_color(8, 12, 20)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(0, 230, 180)
        pdf.cell(0, 20, "", ln=True)
        pdf.cell(0, 12, "DataPulse Analytics Report", ln=True, align="C")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(120, 130, 150)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  Status: {'Cleaned' if is_cleaned else 'Raw'}", ln=True, align="C")

        pdf.ln(10)
        pdf.set_text_color(232, 237, 245)

        # KPI Section
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(0, 200, 160)
        pdf.cell(0, 8, "Executive Summary", ln=True)
        pdf.set_draw_color(0, 200, 160)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        kpi_data = [
            ("Total Rows", f"{kpis['rows']:,}"),
            ("Total Columns", str(kpis['cols'])),
            ("Missing Values", f"{kpis['missing']:,}"),
            ("Duplicate Rows", f"{kpis['duplicates']:,}"),
            ("Cleanliness Score", f"{kpis['cleanliness']}%"),
            ("Memory Usage", f"{kpis['memory_mb']} MB"),
        ]
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(200, 210, 225)
        for label, value in kpi_data:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(120, 150, 180)
            pdf.cell(70, 7, label + ":", ln=False)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(232, 237, 245)
            pdf.cell(0, 7, value, ln=True)

        pdf.ln(6)

        # Column Details
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(0, 200, 160)
        pdf.cell(0, 8, "Column Details", ln=True)
        pdf.set_draw_color(0, 200, 160)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(13, 18, 32)
        pdf.set_text_color(0, 200, 160)
        for h, w in [("Column", 50), ("Type", 30), ("Null%", 20), ("Unique", 20), ("Sample", 70)]:
            pdf.cell(w, 7, h, border=0, fill=True)
        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        for col in df.columns:
            null_p = f"{df[col].isnull().mean()*100:.1f}%"
            uniq   = str(df[col].nunique())
            sample = str(df[col].dropna().iloc[0])[:25] if not df[col].dropna().empty else "—"
            pdf.set_text_color(200, 210, 225)
            pdf.cell(50, 6, col[:28], border=0)
            pdf.set_text_color(120, 150, 180)
            pdf.cell(30, 6, str(df[col].dtype)[:15], border=0)
            color = (255, 95, 135) if float(null_p[:-1]) > 10 else (0, 230, 180)
            pdf.set_text_color(*color)
            pdf.cell(20, 6, null_p, border=0)
            pdf.set_text_color(200, 210, 225)
            pdf.cell(20, 6, uniq, border=0)
            pdf.set_text_color(120, 150, 180)
            pdf.cell(70, 6, sample, border=0)
            pdf.ln()

        pdf.ln(6)

        # Cleaning Log
        if cleaning_log:
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(0, 200, 160)
            pdf.cell(0, 8, "Cleaning Operations Applied", ln=True)
            pdf.set_draw_color(0, 200, 160)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
            pdf.set_font("Helvetica", "", 9)
            for i, entry in enumerate(cleaning_log):
                clean_entry = entry.replace("✓", "[OK]").replace("⚡", "[>>]").replace("⚠", "[!]")
                pdf.set_text_color(0, 200, 160) if "[OK]" in clean_entry else pdf.set_text_color(79, 142, 255)
                pdf.cell(8, 6, f"{i+1}.", ln=False)
                pdf.set_text_color(200, 210, 225)
                pdf.cell(0, 6, clean_entry[:90], ln=True)

        # Footer
        pdf.ln(10)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(74, 85, 104)
        pdf.cell(0, 6, "DataPulse Enterprise v2.1  |  Powered by Python + Streamlit", align="C", ln=True)

        return bytes(pdf.output())
    except Exception as e:
        return None

# ─── Cleaning Pipeline ─────────────────────────────────────────────────────────
def clean_dataframe(df, options):
    df_c = df.copy()
    log  = []

    if options.get("drop_duplicates"):
        before = len(df_c)
        df_c = df_c.drop_duplicates()
        log.append(f"✓ Removed {before - len(df_c)} duplicate rows")

    if options.get("handle_missing"):
        for col in df_c.columns:
            n_miss = df_c[col].isnull().sum()
            if n_miss == 0:
                continue
            if pd.api.types.is_numeric_dtype(df_c[col]):
                strat    = options.get("num_strategy", "median")
                fill_val = df_c[col].median() if strat == "median" else df_c[col].mean()
                df_c[col] = df_c[col].fillna(round(fill_val, 4))
                log.append(f"✓ Filled {n_miss} missing in '{col}' → {strat} ({fill_val:.2f})")
            else:
                mode = df_c[col].mode()
                fill_val = mode[0] if not mode.empty else "Unknown"
                df_c[col] = df_c[col].fillna(fill_val)
                log.append(f"✓ Filled {n_miss} missing in '{col}' → mode ('{fill_val}')")

    if options.get("fix_dtypes"):
        for col in df_c.select_dtypes(include="object").columns:
            converted = pd.to_numeric(df_c[col], errors='coerce')
            # Only convert if >80% of non-null values parse cleanly
            if converted.notna().mean() > 0.80:
                df_c[col] = converted
                log.append(f"✓ Converted '{col}' to numeric (safe threshold met)")

    if options.get("normalize_text"):
        for col in df_c.select_dtypes(include="object").columns:
            df_c[col] = df_c[col].astype(str).str.strip().str.lower()
            log.append(f"✓ Normalized text in '{col}'")

    if options.get("remove_outliers"):
        # Improved: flag outlier mask across ALL numeric cols, remove once
        num_cols = df_c.select_dtypes(include=[np.number]).columns
        outlier_mask = pd.Series(False, index=df_c.index)
        for col in num_cols:
            q1, q3 = df_c[col].quantile(0.25), df_c[col].quantile(0.75)
            iqr = q3 - q1
            if iqr == 0:
                continue
            col_mask = (df_c[col] < q1 - 1.5 * iqr) | (df_c[col] > q3 + 1.5 * iqr)
            outlier_mask = outlier_mask | col_mask
        n_removed = outlier_mask.sum()
        df_c = df_c[~outlier_mask]
        log.append(f"✓ Removed {n_removed} outlier rows (unified IQR across {len(num_cols)} columns)")

    log.append(f"⚡ Pipeline completed at {datetime.now().strftime('%H:%M:%S')} — {len(df_c):,} rows remaining")
    return df_c, log

# ─── AI-Style Insight Summaries ────────────────────────────────────────────────
def generate_ai_insights(df):
    insights = []
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    # Missing
    miss = df.isnull().sum()
    if miss.sum() == 0:
        insights.append(("✅", "#00e6b4", "Complete Dataset", "No missing values detected — dataset is fully populated and ready for modeling."))
    else:
        worst = miss.idxmax()
        insights.append(("⚠️", "#ffb84d", "Missing Data Pattern",
            f"'{worst}' has {miss[worst]} missing values ({miss[worst]/len(df)*100:.1f}%). "
            f"Consider imputation before modeling to avoid biased estimates."))

    # Duplicates
    dups = df.duplicated().sum()
    if dups > 0:
        insights.append(("🔁", "#ff5f87", "Duplicate Records Present",
            f"{dups} duplicate rows found ({dups/len(df)*100:.1f}%). "
            f"Duplicates can inflate model performance metrics — remove before training."))

    # Skewness & distribution
    for col in num_cols[:6]:
        sk = df[col].dropna().skew()
        if sk > 2:
            insights.append(("📊", "#ffb84d", f"Heavy Right Skew — '{col}'",
                f"{col} distribution is heavily right-skewed (skew={sk:.2f}). "
                f"Log or Box-Cox transform recommended before regression modeling."))
        elif sk < -2:
            insights.append(("📊", "#4f8eff", f"Heavy Left Skew — '{col}'",
                f"{col} is left-skewed (skew={sk:.2f}). "
                f"Square or cube-root transformation may normalize the distribution."))

    # Outlier density
    for col in num_cols[:6]:
        n_out = detect_outliers_iqr(col, df[col].dropna())
        pct = n_out / len(df) * 100
        if pct > 5:
            insights.append(("📍", "#4f8eff", f"High Outlier Density — '{col}'",
                f"{n_out} outliers ({pct:.1f}%) detected in '{col}'. "
                f"If these are data errors, removal is advised. If genuine, use robust scalers."))

    # High correlation
    if len(num_cols) >= 2:
        corr = df[num_cols].corr().abs()
        corr_arr = corr.values.copy()
        np.fill_diagonal(corr_arr, 0)
        corr_zeroed = pd.DataFrame(corr_arr, index=corr.index, columns=corr.columns)
        max_val = corr_zeroed.max().max()
        if max_val > 0.85:
            idx = corr_zeroed.stack().idxmax()
            insights.append(("🔗", "#a78bfa", "Multicollinearity Risk",
                f"'{idx[0]}' and '{idx[1]}' are {max_val:.2f} correlated. "
                f"High multicollinearity can destabilize regression coefficients — consider dropping one or using PCA."))

    # Dominant category
    for col in cat_cols[:3]:
        vc = df[col].value_counts(normalize=True)
        if not vc.empty and vc.iloc[0] > 0.65:
            insights.append(("🏷", "#4f8eff", f"Class Imbalance — '{col}'",
                f"'{vc.index[0]}' dominates at {vc.iloc[0]*100:.1f}% of values. "
                f"Class imbalance can bias classification models — consider SMOTE or stratified sampling."))

    # High cardinality
    for col in cat_cols:
        if df[col].nunique() > 0.5 * len(df):
            insights.append(("🗂", "#ff5f87", f"High Cardinality — '{col}'",
                f"'{col}' has {df[col].nunique()} unique values ({df[col].nunique()/len(df)*100:.1f}% of rows). "
                f"High-cardinality features may need hashing, embedding, or removal."))

    # Low variance
    for col in num_cols[:6]:
        mean = df[col].mean()
        if abs(mean) > 1e-6:
            cv = df[col].std() / abs(mean)
            if cv < 0.01:
                insights.append(("📉", "#7a8599", f"Near-Zero Variance — '{col}'",
                    f"'{col}' has coefficient of variation ≈ {cv:.4f}. "
                    f"Near-constant features rarely add predictive value and may be safely dropped."))

    # Dataset size insight
    if len(df) < 500:
        insights.append(("⚡", "#ffb84d", "Small Dataset Warning",
            f"Only {len(df)} rows detected. Small datasets risk overfitting — "
            f"consider data augmentation or cross-validation with k≥10 folds."))
    elif len(df) > 50000:
        insights.append(("🚀", "#00e6b4", "Large Dataset Detected",
            f"{len(df):,} rows present. Consider chunked processing or sampling for exploratory analysis. "
            f"Gradient boosting or neural models will perform well at this scale."))

    return insights

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.5rem 1.2rem 0.8rem;border-bottom:1px solid rgba(255,255,255,0.07);">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#00e6b4,#4f8eff);
                border-radius:9px;display:flex;align-items:center;justify-content:center;
                font-size:17px;font-weight:900;color:#080c14;box-shadow:0 4px 15px rgba(0,230,180,0.3);">⚡</div>
            <span style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
                color:#e8edf5;letter-spacing:-0.02em;">DataPulse</span>
        </div>
        <p style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#4a5568;
            text-transform:uppercase;letter-spacing:0.12em;margin:0;">Enterprise Analytics v2.1</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    sections = {
        "overview":  ("📊", "Overview"),
        "profile":   ("🔬", "Data Profiling"),
        "raw_data":  ("📋", "Raw Data"),
        "clean":     ("🧹", "Data Cleaning"),
        "anomaly":   ("🎯", "Anomaly Detection"),
        "visualize": ("📈", "Visualizations"),
        "insights":  ("💡", "AI Insights"),
        "report":    ("📄", "Report & Export"),
        "history":   ("🕐", "Cleaning History"),
    }

    for key, (icon, label) in sections.items():
        is_active = st.session_state.active_section == key
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.active_section = key
            st.rerun()

    st.markdown("---")
    if st.session_state.df_raw is not None:
        df_sb = st.session_state.df_raw
        kpis_sb = compute_kpis(df_hash(df_sb), df_sb)
        st.markdown(f"""
        <div style="padding:1rem;background:rgba(0,230,180,0.04);
            border:1px solid rgba(0,230,180,0.12);border-radius:10px;margin:0 0.5rem 1rem;">
            <p style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#00e6b4;
                text-transform:uppercase;letter-spacing:0.1em;margin:0 0 6px;">Active Dataset</p>
            <p style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;
                color:#e8edf5;margin:0 0 2px;">{df_sb.shape[0]:,} rows × {df_sb.shape[1]} cols</p>
            <p style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#4a5568;margin:0 0 8px;">
                {kpis_sb['memory_mb']} MB in memory</p>
            <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:5px;">
                <div style="background:linear-gradient(90deg,#00e6b4,#4f8eff);
                    border-radius:4px;height:5px;width:{kpis_sb['cleanliness']}%;
                    transition:width 0.5s ease;"></div>
            </div>
            <p style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#4a5568;margin:4px 0 0;">
                {kpis_sb['cleanliness']}% cleanliness score</p>
        </div>
        """, unsafe_allow_html=True)

# ─── MAIN SECTIONS ─────────────────────────────────────────────────────────────
section = st.session_state.active_section

# ══════════════════ OVERVIEW ══════════════════
if section == "overview":
    st.markdown("""
    <div style="padding:1.5rem 0 1rem;">
        <h1 style="font-family:'Syne',sans-serif;font-size:2.3rem;font-weight:800;
            background:linear-gradient(135deg,#00e6b4 0%,#4f8eff 60%,#a78bfa 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            margin:0;letter-spacing:-0.03em;">Data Cleaning & Analytics</h1>
        <p style="color:#7a8599;font-size:0.95rem;margin:0.4rem 0 0;font-weight:300;">
            Enterprise-grade data pipeline automation · profiling · anomaly detection · reporting
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop CSV or Excel file", type=["csv","xlsx","xls"], label_visibility="collapsed")
    if uploaded:
        with st.spinner("⚡ Parsing dataset…"):
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)
                st.session_state.df_raw = df
                st.session_state.df_clean = None
                st.session_state.cleaning_log = []
                st.session_state.anomaly_scores = None
                st.success(f"✓ Loaded **{uploaded.name}** — {df.shape[0]:,} rows × {df.shape[1]} columns")
            except Exception as e:
                st.error(f"Error loading file: {e}")

    col_a, col_b = st.columns([2,6])
    with col_a:
        if st.button("⚡ Load Sample Dataset", use_container_width=True):
            with st.spinner("Generating sample dataset…"):
                np.random.seed(42)
                n = 800
                df_demo = pd.DataFrame({
                    "customer_id":      range(1, n+1),
                    "age":              np.random.randint(18,75,n).astype(float),
                    "income":           np.random.normal(55000,18000,n).round(2),
                    "spend":            np.random.exponential(800,n).round(2),
                    "region":           np.random.choice(["North","South","East","West","  north "],n),
                    "segment":          np.random.choice(["Premium","Standard","Budget",None],n,p=[0.3,0.4,0.25,0.05]),
                    "churn":            np.random.choice([0,1],n,p=[0.8,0.2]),
                    "tenure_months":    np.random.randint(1,72,n).astype(float),
                    "satisfaction":     np.random.randint(1,6,n).astype(float),
                    "last_purchase_days":np.random.exponential(45,n).round(1),
                })
                for col in ["age","income","segment","tenure_months"]:
                    idx = np.random.choice(n, size=int(n*0.06), replace=False)
                    df_demo.loc[idx, col] = np.nan
                df_demo = pd.concat([df_demo, df_demo.sample(20, random_state=1)], ignore_index=True)
                df_demo.loc[np.random.choice(len(df_demo),10), "income"] = np.random.uniform(300000,500000,10)
                st.session_state.df_raw = df_demo
                st.session_state.df_clean = None
                st.session_state.cleaning_log = []
                st.session_state.anomaly_scores = None
            st.success(f"✓ Sample dataset ready — {len(df_demo):,} rows × {df_demo.shape[1]} columns")
            st.rerun()

    if st.session_state.df_raw is not None:
        df = st.session_state.df_raw
        kpis = compute_kpis(df_hash(df), df)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Dataset KPIs")

        c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
        c1.metric("Total Rows",     f"{kpis['rows']:,}")
        c2.metric("Total Columns",  f"{kpis['cols']}")
        c3.metric("Missing Values", f"{kpis['missing']:,}")
        c4.metric("Duplicates",     f"{kpis['duplicates']:,}")
        c5.metric("Cleanliness",    f"{kpis['cleanliness']}%")
        c6.metric("Memory",         f"{kpis['memory_mb']} MB")
        c7.metric("Est. File Size", f"{kpis['file_size_kb']} KB")

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            with st.spinner("Rendering dtype chart…"):
                st.markdown("#### Data Type Distribution")
                dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
                dtype_counts.columns = ["Type","Count"]
                fig_dt = px.pie(dtype_counts, names="Type", values="Count",
                                color_discrete_sequence=PALETTE, hole=0.55)
                fig_dt.update_layout(**plotly_theme(), height=270, showlegend=True,
                                     legend=dict(orientation="h",yanchor="bottom",y=-0.25))
                fig_dt.update_traces(textinfo="percent+label", textfont_size=10)
                st.plotly_chart(fig_dt, use_container_width=True)

        with col_r:
            with st.spinner("Rendering missing values chart…"):
                st.markdown("#### Missing Values per Column")
                miss = df.isnull().sum()
                miss = miss[miss > 0].sort_values(ascending=False)
                if not miss.empty:
                    fig_miss = px.bar(x=miss.values, y=miss.index, orientation="h",
                                      color=miss.values,
                                      color_continuous_scale=["#4f8eff","#ff5f87"])
                    fig_miss.update_layout(**plotly_theme(), height=270,
                                           coloraxis_showscale=False,
                                           yaxis_title="", xaxis_title="Missing Count")
                    st.plotly_chart(fig_miss, use_container_width=True)
                else:
                    st.success("🎉 No missing values detected in this dataset!")

# ══════════════════ DATA PROFILING ══════════════════
elif section == "profile":
    st.markdown("## 🔬 Data Profiling")
    if st.session_state.df_raw is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        df = st.session_state.df_raw
        with st.spinner("Building data profile…"):
            time.sleep(0.3)
            profile = compute_profile(df_hash(df), df)

        st.markdown("#### Column-level Profile")
        # Highlight warnings
        def highlight_profile(row):
            styles = [""] * len(row)
            if row["Null %"] > 20:
                styles[2] = "color: #ff5f87; font-weight: bold"
            if row["High Cardinality"] == "⚠️ Yes":
                styles[5] = "color: #ffb84d; font-weight: bold"
            if row["Type Mismatch"] == "⚠️ Yes":
                styles[6] = "color: #ffb84d; font-weight: bold"
            return styles

        st.dataframe(profile.style.apply(highlight_profile, axis=1),
                     use_container_width=True, height=400)

        st.markdown("<br>", unsafe_allow_html=True)
        pc1, pc2, pc3 = st.columns(3)

        with pc1:
            with st.spinner("Rendering null chart…"):
                st.markdown("#### Null % per Column")
                fig_null = px.bar(profile, x="Column", y="Null %",
                                  color="Null %", color_continuous_scale=["#00e6b4","#ff5f87"])
                fig_null.update_layout(**plotly_theme(), height=280, coloraxis_showscale=False,
                                       xaxis_tickangle=-35)
                st.plotly_chart(fig_null, use_container_width=True)

        with pc2:
            with st.spinner("Rendering unique% chart…"):
                st.markdown("#### Unique % per Column")
                fig_uniq = px.bar(profile, x="Column", y="Unique %",
                                  color="Unique %", color_continuous_scale=["#4f8eff","#a78bfa"])
                fig_uniq.update_layout(**plotly_theme(), height=280, coloraxis_showscale=False,
                                       xaxis_tickangle=-35)
                st.plotly_chart(fig_uniq, use_container_width=True)

        with pc3:
            st.markdown("#### Profile Summary")
            total = len(profile)
            high_null    = (profile["Null %"] > 20).sum()
            high_card    = (profile["High Cardinality"] == "⚠️ Yes").sum()
            type_mismatch= (profile["Type Mismatch"] == "⚠️ Yes").sum()
            st.markdown(card("🔴","#ff5f87","High Null Columns (>20%)",
                             f"{high_null} of {total} columns exceed 20% null threshold"))
            st.markdown(card("🟡","#ffb84d","High Cardinality Columns",
                             f"{high_card} object column(s) with >50% unique values — may need encoding strategy"))
            st.markdown(card("🔵","#4f8eff","Type Mismatch Detected",
                             f"{type_mismatch} column(s) stored as text but contain numeric data"),
                        unsafe_allow_html=True)

# ══════════════════ RAW DATA ══════════════════
elif section == "raw_data":
    st.markdown("## 📋 Raw Data Preview")
    if st.session_state.df_raw is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        df = st.session_state.df_raw
        c1, c2, c3 = st.columns([2,2,3])
        with c1:
            search_col = st.selectbox("Filter Column", ["— All —"] + list(df.columns))
        with c2:
            search_val = st.text_input("Search Value", placeholder="Type to filter…")
        with c3:
            n_rows = st.slider("Preview Rows", 10, min(500,len(df)), 100)

        df_view = df.copy()
        if search_col != "— All —" and search_val:
            df_view = df_view[df_view[search_col].astype(str).str.contains(search_val, case=False, na=False)]
        elif search_val:
            mask = df_view.apply(lambda c: c.astype(str).str.contains(search_val, case=False, na=False)).any(axis=1)
            df_view = df_view[mask]

        st.markdown(f"<p style='color:#7a8599;font-size:0.8rem;'>{len(df_view):,} matching rows</p>", unsafe_allow_html=True)
        st.dataframe(df_view.head(n_rows), use_container_width=True, height=420)

        st.markdown("#### Column Summary")
        summary = []
        for col in df.columns:
            summary.append({
                "Column": col, "Type": str(df[col].dtype),
                "Missing": int(df[col].isnull().sum()),
                "Missing %": f"{df[col].isnull().mean()*100:.1f}%",
                "Unique": int(df[col].nunique()),
                "Sample": str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "—",
            })
        st.dataframe(pd.DataFrame(summary), use_container_width=True)

# ══════════════════ CLEANING ══════════════════
elif section == "clean":
    st.markdown("## 🧹 Automated Data Cleaning")
    if st.session_state.df_raw is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        df = st.session_state.df_raw
        col_opts, col_preview = st.columns([1,2])

        with col_opts:
            st.markdown("#### Cleaning Pipeline Options")
            opt_dup     = st.checkbox("Remove Duplicates", value=True)
            opt_miss    = st.checkbox("Handle Missing Values", value=True)
            num_strat   = st.selectbox("Numeric Strategy", ["median","mean"], disabled=not opt_miss)
            opt_dtype   = st.checkbox("Fix Data Types (safe threshold)", value=True)
            opt_text    = st.checkbox("Normalize Text", value=True)
            opt_outlier = st.checkbox("Remove Outliers (unified IQR)", value=False)
            st.markdown("<br>", unsafe_allow_html=True)
            run_btn = st.button("⚡ Run Cleaning Pipeline", use_container_width=True)

        with col_preview:
            st.markdown("#### Before / After Comparison")
            kpis_raw = compute_kpis(df_hash(df), df)
            if st.session_state.df_clean is not None:
                with st.spinner("Rendering comparison chart…"):
                    kpis_cl = compute_kpis(df_hash(st.session_state.df_clean), st.session_state.df_clean)
                    cmp = pd.DataFrame({
                        "Metric": ["Rows","Missing","Duplicates","Cleanliness %"],
                        "Before": [kpis_raw["rows"], kpis_raw["missing"], kpis_raw["duplicates"], kpis_raw["cleanliness"]],
                        "After":  [kpis_cl["rows"],  kpis_cl["missing"],  kpis_cl["duplicates"],  kpis_cl["cleanliness"]],
                    })
                    fig_cmp = go.Figure()
                    fig_cmp.add_trace(go.Bar(name="Before", x=cmp["Metric"], y=cmp["Before"], marker_color="#ff5f87"))
                    fig_cmp.add_trace(go.Bar(name="After",  x=cmp["Metric"], y=cmp["After"],  marker_color="#00e6b4"))
                    fig_cmp.update_layout(**plotly_theme(), height=280, barmode="group",
                                           legend=dict(orientation="h",yanchor="bottom",y=1.02))
                    st.plotly_chart(fig_cmp, use_container_width=True)
            else:
                st.markdown("""<div style="height:280px;display:flex;align-items:center;
                    justify-content:center;border:1px dashed rgba(255,255,255,0.07);
                    border-radius:12px;color:#4a5568;font-family:'Space Mono',monospace;font-size:0.75rem;">
                    Run pipeline to see comparison</div>""", unsafe_allow_html=True)

        if run_btn:
            with st.spinner("⚡ Running cleaning pipeline — please wait…"):
                options = {"drop_duplicates":opt_dup,"handle_missing":opt_miss,
                           "num_strategy":num_strat,"fix_dtypes":opt_dtype,
                           "normalize_text":opt_text,"remove_outliers":opt_outlier}
                time.sleep(0.4)
                df_clean, log = clean_dataframe(df, options)
            st.session_state.df_clean = df_clean
            st.session_state.cleaning_log = log
            st.session_state.anomaly_scores = None
            st.success(f"✓ Cleaning complete — {len(log)-1} operations applied, {len(df_clean):,} rows remaining")
            st.rerun()

        if st.session_state.df_clean is not None:
            st.markdown("#### Cleaning Log")
            for entry in st.session_state.cleaning_log:
                color = "#00e6b4" if "✓" in entry else "#4f8eff"
                st.markdown(f"<p style='color:{color};font-family:Space Mono,monospace;font-size:0.78rem;margin:2px 0;'>{entry}</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Cleaned Dataset Preview")
            st.dataframe(st.session_state.df_clean.head(100), use_container_width=True, height=320)
            csv = st.session_state.df_clean.to_csv(index=False).encode()
            st.download_button("⬇ Download Cleaned CSV", csv, "cleaned_data.csv", "text/csv")

# ══════════════════ ANOMALY DETECTION ══════════════════
elif section == "anomaly":
    st.markdown("## 🎯 Anomaly Detection")
    df_use = st.session_state.df_clean if st.session_state.df_clean is not None else st.session_state.df_raw
    if df_use is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        num_cols = df_use.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns for anomaly detection.")
        else:
            st.markdown("""
            <div style="background:rgba(79,142,255,0.06);border:1px solid rgba(79,142,255,0.2);
                border-radius:10px;padding:1rem 1.2rem;margin-bottom:1.2rem;">
                <p style="font-family:'Syne',sans-serif;font-weight:700;color:#4f8eff;margin:0 0 4px;">
                    ⚡ Z-Score Anomaly Scoring</p>
                <p style="color:#7a8599;font-size:0.82rem;margin:0;">
                    Each row is scored by averaging absolute Z-scores across all numeric columns.
                    Scores > 2.5 are flagged as anomalies. Higher score = more anomalous.
                </p>
            </div>""", unsafe_allow_html=True)

            threshold = st.slider("Anomaly Threshold (Z-score)", 1.5, 4.0, 2.5, 0.1)

            if st.button("🎯 Run Anomaly Detection", use_container_width=False):
                with st.spinner("Computing anomaly scores across all numeric features…"):
                    time.sleep(0.5)
                    scores = compute_anomaly_scores(df_hash(df_use), df_use)
                    st.session_state.anomaly_scores = scores
                st.success("✓ Anomaly scoring complete!")

            if st.session_state.anomaly_scores is not None:
                scores = st.session_state.anomaly_scores
                anomalies = scores[scores > threshold]
                pct = len(anomalies)/len(scores)*100

                a1,a2,a3,a4 = st.columns(4)
                a1.metric("Total Rows Scored",    f"{len(scores):,}")
                a2.metric("Anomalies Detected",   f"{len(anomalies):,}")
                a3.metric("Anomaly Rate",          f"{pct:.2f}%")
                a4.metric("Max Anomaly Score",     f"{scores.max():.3f}")

                st.markdown("<br>", unsafe_allow_html=True)
                ac1, ac2 = st.columns(2)

                with ac1:
                    with st.spinner("Rendering score distribution…"):
                        st.markdown("#### Anomaly Score Distribution")
                        fig_hist = px.histogram(x=scores, nbins=60,
                                                color_discrete_sequence=["#4f8eff"])
                        fig_hist.add_vline(x=threshold, line_dash="dash",
                                           line_color="#ff5f87",
                                           annotation_text=f"Threshold ({threshold})",
                                           annotation_font_color="#ff5f87")
                        fig_hist.update_layout(**plotly_theme(), height=300,
                                               xaxis_title="Anomaly Score",
                                               yaxis_title="Count")
                        st.plotly_chart(fig_hist, use_container_width=True)

                with ac2:
                    with st.spinner("Rendering scatter plot…"):
                        st.markdown("#### Score vs Row Index")
                        colors = ["#ff5f87" if s > threshold else "#00e6b4" for s in scores]
                        fig_sc = go.Figure()
                        normal_mask = scores <= threshold
                        anomaly_mask = scores > threshold
                        fig_sc.add_trace(go.Scatter(
                            x=scores.index[normal_mask], y=scores[normal_mask],
                            mode="markers", name="Normal",
                            marker=dict(color="#00e6b4", size=3, opacity=0.6)))
                        fig_sc.add_trace(go.Scatter(
                            x=scores.index[anomaly_mask], y=scores[anomaly_mask],
                            mode="markers", name="Anomaly",
                            marker=dict(color="#ff5f87", size=5, opacity=0.9)))
                        fig_sc.add_hline(y=threshold, line_dash="dash", line_color="#ffb84d")
                        fig_sc.update_layout(**plotly_theme(), height=300,
                                             xaxis_title="Row Index", yaxis_title="Anomaly Score")
                        st.plotly_chart(fig_sc, use_container_width=True)

                # Top anomalies table
                st.markdown("#### Top 20 Most Anomalous Rows")
                top_idx = scores.nlargest(20).index
                anomaly_df = df_use.loc[top_idx].copy()
                anomaly_df.insert(0, "Anomaly Score", scores[top_idx].round(4))
                st.dataframe(anomaly_df, use_container_width=True, height=320)

                anom_csv = anomaly_df.to_csv(index=True).encode()
                st.download_button("⬇ Download Anomaly Report CSV", anom_csv,
                                   "anomalies.csv", "text/csv")

# ══════════════════ VISUALIZATIONS ══════════════════
elif section == "visualize":
    st.markdown("## 📈 Visualization Analytics")
    df_use = st.session_state.df_clean if st.session_state.df_clean is not None else st.session_state.df_raw
    if df_use is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        num_cols = df_use.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df_use.select_dtypes(include="object").columns.tolist()
        tabs = st.tabs(["Distribution","Correlation","Scatter","Categorical","Trend","Heatmap"])

        with tabs[0]:
            if num_cols:
                col_sel = st.selectbox("Column", num_cols, key="dist_col")
                nbins   = st.slider("Bins", 10, 100, 30)
                with st.spinner(f"Rendering distribution of {col_sel}…"):
                    fig = px.histogram(df_use, x=col_sel, nbins=nbins,
                                       color_discrete_sequence=["#00e6b4"], marginal="box")
                    fig.update_layout(**plotly_theme(), height=380, bargap=0.05,
                                      title=f"Distribution — {col_sel}")
                    st.plotly_chart(fig, use_container_width=True)
                s = df_use[col_sel].describe()
                d1,d2,d3,d4 = st.columns(4)
                d1.metric("Mean",   f"{s['mean']:.3f}")
                d2.metric("Median", f"{df_use[col_sel].median():.3f}")
                d3.metric("Std Dev",f"{s['std']:.3f}")
                d4.metric("Skewness",f"{df_use[col_sel].skew():.3f}")

        with tabs[1]:
            if len(num_cols) >= 2:
                sel_cols = st.multiselect("Columns", num_cols,
                    default=num_cols[:min(8,len(num_cols))], key="corr_cols")
                if len(sel_cols) >= 2:
                    with st.spinner("Computing correlation matrix…"):
                        corr = df_use[sel_cols].corr()
                        fig = px.imshow(corr,
                            color_continuous_scale=["#ff5f87","#0d1220","#00e6b4"],
                            zmin=-1, zmax=1, text_auto=".2f", aspect="auto")
                        fig.update_layout(**plotly_theme(), height=440,
                                          title="Pearson Correlation Matrix")
                        st.plotly_chart(fig, use_container_width=True)

        with tabs[2]:
            if len(num_cols) >= 2:
                sc1,sc2,sc3 = st.columns(3)
                x_col = sc1.selectbox("X Axis", num_cols, index=0, key="sc_x")
                y_col = sc2.selectbox("Y Axis", num_cols, index=min(1,len(num_cols)-1), key="sc_y")
                color_col = sc3.selectbox("Color By", ["—"]+cat_cols+num_cols, key="sc_color")
                with st.spinner("Rendering scatter plot…"):
                    kwargs = dict(x=x_col, y=y_col, opacity=0.6,
                                  color_discrete_sequence=PALETTE)
                    if color_col != "—":
                        kwargs["color"] = color_col
                    fig = px.scatter(df_use, **kwargs)
                    fig.update_layout(**plotly_theme(), height=420, title=f"{x_col} vs {y_col}")
                    fig.update_traces(marker=dict(size=4))
                    st.plotly_chart(fig, use_container_width=True)

        with tabs[3]:
            if cat_cols:
                cc1,cc2 = st.columns(2)
                cat_sel   = cc1.selectbox("Category", cat_cols, key="cat_sel")
                chart_type= cc2.selectbox("Chart Type", ["Bar","Pie","Treemap"])
                top_n = st.slider("Top N", 3, 20, 8)
                with st.spinner(f"Rendering {chart_type} chart…"):
                    vc = df_use[cat_sel].value_counts().head(top_n).reset_index()
                    vc.columns = [cat_sel, "count"]
                    if chart_type == "Bar":
                        fig = px.bar(vc, x=cat_sel, y="count", color="count",
                                     color_continuous_scale=["#4f8eff","#00e6b4"])
                        fig.update_layout(**plotly_theme(), height=360, coloraxis_showscale=False)
                    elif chart_type == "Pie":
                        fig = px.pie(vc, names=cat_sel, values="count",
                                     color_discrete_sequence=PALETTE, hole=0.45)
                        fig.update_layout(**plotly_theme(), height=360)
                    else:
                        fig = px.treemap(vc, path=[cat_sel], values="count",
                                         color="count", color_continuous_scale=["#4f8eff","#00e6b4"])
                        fig.update_layout(**plotly_theme(), height=360)
                    st.plotly_chart(fig, use_container_width=True)

        with tabs[4]:
            if num_cols:
                t_cols = st.multiselect("Columns", num_cols,
                    default=num_cols[:min(3,len(num_cols))], key="trend_cols")
                smooth = st.slider("Rolling Avg Window", 1, 50, 1)
                if t_cols:
                    with st.spinner("Rendering trend analysis…"):
                        fig = go.Figure()
                        for i, col in enumerate(t_cols):
                            y = df_use[col].rolling(smooth).mean() if smooth > 1 else df_use[col]
                            fig.add_trace(go.Scatter(x=df_use.index, y=y, name=col, mode="lines",
                                line=dict(color=PALETTE[i % len(PALETTE)], width=2)))
                        fig.update_layout(**plotly_theme(), height=380, title="Trend Analysis")
                        st.plotly_chart(fig, use_container_width=True)

        with tabs[5]:
            if num_cols:
                sample_rows = st.slider("Sample Rows", 20, min(300,len(df_use)), 60)
                sel_heat = st.multiselect("Columns", num_cols,
                    default=num_cols[:min(7,len(num_cols))], key="heat_cols")
                if sel_heat:
                    with st.spinner("Rendering heatmap…"):
                        sample = df_use[sel_heat].dropna().head(sample_rows)
                        fig = px.imshow(sample.T,
                            color_continuous_scale=["#080c14","#4f8eff","#00e6b4"],
                            aspect="auto")
                        fig.update_layout(**plotly_theme(), height=400,
                            title=f"Data Heatmap — {sample_rows} rows × {len(sel_heat)} columns")
                        st.plotly_chart(fig, use_container_width=True)

# ══════════════════ AI INSIGHTS ══════════════════
elif section == "insights":
    st.markdown("## 💡 AI-Style Automated Insights")
    df_use = st.session_state.df_clean if st.session_state.df_clean is not None else st.session_state.df_raw
    if df_use is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        with st.spinner("Analyzing dataset patterns and generating insights…"):
            time.sleep(0.4)
            insights = generate_ai_insights(df_use)

        st.markdown(f"<p style='color:#7a8599;font-size:0.82rem;margin-bottom:1rem;'>"
                    f"⚡ {len(insights)} insights generated from {df_use.shape[0]:,} rows × {df_use.shape[1]} columns</p>",
                    unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        for i, (icon, color, title, desc) in enumerate(insights):
            target = c1 if i % 2 == 0 else c2
            with target:
                st.markdown(card(icon, color, title, desc), unsafe_allow_html=True)

        # Stats table
        num_cols = df_use.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            st.markdown("#### 📊 Extended Descriptive Statistics")
            with st.spinner("Computing statistics…"):
                desc = df_use[num_cols].describe().T.round(3)
                desc["skewness"] = df_use[num_cols].skew().round(3)
                desc["kurtosis"] = df_use[num_cols].kurtosis().round(3)
                desc["outliers"] = [detect_outliers_iqr(col, df_use[col].dropna()) for col in num_cols]
                desc["null_%"]   = [round(df_use[col].isnull().mean()*100,2) for col in num_cols]
            st.dataframe(desc, use_container_width=True)

# ══════════════════ REPORT & EXPORT ══════════════════
elif section == "report":
    st.markdown("## 📄 Report Generation & Export")
    df_use = st.session_state.df_clean if st.session_state.df_clean is not None else st.session_state.df_raw
    if df_use is None:
        st.info("Upload a dataset from the Overview section first.")
    else:
        kpis = compute_kpis(df_hash(df_use), df_use)
        is_cleaned = st.session_state.df_clean is not None
        timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        num_cols   = df_use.select_dtypes(include=[np.number]).columns.tolist()

        # Export buttons
        ec1, ec2, ec3 = st.columns(3)

        with ec1:
            st.markdown("#### 📋 Markdown Report")
            if st.button("Generate Markdown", use_container_width=True):
                with st.spinner("Building markdown report…"):
                    time.sleep(0.3)
                    md = f"# DataPulse Analytics Report\nGenerated: {timestamp}\nStatus: {'Cleaned' if is_cleaned else 'Raw'}\n\n"
                    md += f"## KPIs\n- Rows: {kpis['rows']:,}\n- Columns: {kpis['cols']}\n"
                    md += f"- Missing: {kpis['missing']:,}\n- Duplicates: {kpis['duplicates']:,}\n"
                    md += f"- Cleanliness: {kpis['cleanliness']}%\n- Memory: {kpis['memory_mb']} MB\n\n"
                    md += "## Columns\n"
                    for col in df_use.columns:
                        md += f"- **{col}** ({df_use[col].dtype}): {df_use[col].nunique()} unique, {df_use[col].isnull().sum()} missing\n"
                    if num_cols:
                        md += "\n## Statistics\n```\n"
                        md += df_use[num_cols].describe().round(3).to_string()
                        md += "\n```\n"
                    if st.session_state.cleaning_log:
                        md += "\n## Cleaning Log\n"
                        for e in st.session_state.cleaning_log:
                            md += f"- {e}\n"
                    md += "\n---\n*DataPulse Enterprise v2.1*"
                st.download_button("⬇ Download .md", md.encode(), "datapulse_report.md", "text/markdown", use_container_width=True)

        with ec2:
            st.markdown("#### 📊 CSV Statistics")
            if st.button("Generate CSV", use_container_width=True):
                with st.spinner("Compiling statistics CSV…"):
                    time.sleep(0.2)
                    if num_cols:
                        stats_csv = df_use[num_cols].describe().round(3).to_csv().encode()
                        st.download_button("⬇ Download Stats CSV", stats_csv, "statistics.csv", "text/csv", use_container_width=True)
                    else:
                        st.warning("No numeric columns for statistics CSV.")

        with ec3:
            st.markdown("#### 📄 PDF Report")
            if st.button("Generate PDF", use_container_width=True):
                with st.spinner("Building professional PDF report…"):
                    time.sleep(0.5)
                    pdf_bytes = generate_pdf_report(df_use, kpis, st.session_state.cleaning_log, is_cleaned)
                if pdf_bytes:
                    st.download_button("⬇ Download PDF", pdf_bytes, "datapulse_report.pdf", "application/pdf", use_container_width=True)
                else:
                    st.error("PDF generation failed. Run: pip install fpdf2")

        # Preview
        st.markdown("---")
        st.markdown("#### Report Preview")
        p1,p2,p3,p4,p5,p6 = st.columns(6)
        p1.metric("Rows", f"{kpis['rows']:,}")
        p2.metric("Columns", kpis['cols'])
        p3.metric("Missing", f"{kpis['missing']:,}")
        p4.metric("Duplicates", f"{kpis['duplicates']:,}")
        p5.metric("Cleanliness", f"{kpis['cleanliness']}%")
        p6.metric("Memory", f"{kpis['memory_mb']} MB")

        if num_cols:
            with st.spinner("Rendering statistics preview…"):
                st.markdown("#### Numeric Statistics Preview")
                desc = df_use[num_cols].describe().round(3).T
                st.dataframe(desc, use_container_width=True)

# ══════════════════ HISTORY ══════════════════
elif section == "history":
    st.markdown("## 🕐 Cleaning Log & Pipeline History")
    if not st.session_state.cleaning_log:
        st.info("No cleaning operations recorded. Run the pipeline from Data Cleaning.")
    else:
        kpis_raw = compute_kpis(df_hash(st.session_state.df_raw), st.session_state.df_raw) if st.session_state.df_raw is not None else {}
        kpis_cl  = compute_kpis(df_hash(st.session_state.df_clean), st.session_state.df_clean) if st.session_state.df_clean is not None else {}

        st.markdown(f"""
        <div style="background:rgba(0,230,180,0.04);border:1px solid rgba(0,230,180,0.15);
            border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;">
            <p style="font-family:'Space Mono',monospace;font-size:0.62rem;color:#00e6b4;
                text-transform:uppercase;letter-spacing:0.1em;margin:0 0 6px;">Pipeline Summary</p>
            <p style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#e8edf5;margin:0;">
                {len(st.session_state.cleaning_log)} operations applied</p>
            {"<p style='color:#7a8599;font-size:0.82rem;margin:4px 0 0;'>Rows: " + str(kpis_raw.get('rows','—')) + " → " + str(kpis_cl.get('rows','—')) + "  |  Cleanliness: " + str(kpis_raw.get('cleanliness','—')) + "% → " + str(kpis_cl.get('cleanliness','—')) + "%</p>" if kpis_cl else ""}
        </div>
        """, unsafe_allow_html=True)

        for i, entry in enumerate(st.session_state.cleaning_log):
            color = "#00e6b4" if "✓" in entry else "#4f8eff"
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;
                border-bottom:1px solid rgba(255,255,255,0.04);">
                <div style="width:22px;height:22px;border-radius:50%;
                    background:rgba(0,230,180,0.08);border:1px solid rgba(0,230,180,0.25);
                    display:flex;align-items:center;justify-content:center;
                    font-family:'Space Mono',monospace;font-size:0.58rem;color:#00e6b4;flex-shrink:0;">{i+1}</div>
                <p style="font-family:'Space Mono',monospace;font-size:0.76rem;
                    color:{color};margin:3px 0 0;line-height:1.4;">{entry}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑 Clear History"):
            st.session_state.cleaning_log = []
            st.rerun()
