import streamlit as st
import os
import tensorflow as tf
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide"
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Page background */
.stApp {
    background-color: #0B1120;
    color: #E2E8F0;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #141E30;
    border: 0.5px solid #1E2D45;
    border-radius: 10px;
    padding: 18px 20px !important;
}
[data-testid="metric-container"] label {
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #475569 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 20px !important;
    color: #0EA5E9 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 11px !important;
    color: #475569 !important;
}

/* ── Inputs ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size: 12px !important;
    color: #64748B !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.stSelectbox select,
[data-testid="stNumberInput"] input {
    background-color: #141E30 !important;
    border: 0.5px solid #1E2D45 !important;
    color: #E2E8F0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 6px !important;
}
[data-baseweb="select"] > div {
    background-color: #141E30 !important;
    border: 0.5px solid #1E2D45 !important;
    color: #E2E8F0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

/* ── Dividers ── */
hr {
    border-color: #1E2D45 !important;
    margin: 20px 0 !important;
}

/* ── Primary button styling tweak ── */
div.stButton > button {
    width: 100% !important;
    background-color: #0EA5E9 !important;
    color: #0B1120 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 0 !important;
    letter-spacing: 0.02em;
    transition: background 0.15s;
}
div.stButton > button:hover {
    background-color: #38BDF8 !important;
    color: #0B1120 !important;
    border: none !important;
}

/* ── Section label ── */
.section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #475569;
    margin: 8px 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 0.5px;
    background: #1E2D45;
}

/* ── Result boxes ── */
.result-safe {
    background: #0D2218;
    border: 0.5px solid #166534;
    border-radius: 10px;
    padding: 18px 20px;
    margin-top: 8px;
}
.result-fraud {
    background: #200D0D;
    border: 0.5px solid #991B1B;
    border-radius: 10px;
    padding: 18px 20px;
    margin-top: 8px;
}
.result-placeholder {
    background: #141E30;
    border: 0.5px dashed #1E2D45;
    border-radius: 10px;
    padding: 22px;
    text-align: center;
    color: #334155;
    font-size: 13px;
    margin-top: 8px;
}
.badge-safe {
    display: inline-block;
    background: #14532D;
    color: #4ADE80;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 4px;
    margin-bottom: 6px;
}
.badge-fraud {
    display: inline-block;
    background: #450A0A;
    color: #F87171;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 4px;
    margin-bottom: 6px;
}
.result-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}
.result-title-safe  { font-size: 15px; font-weight: 500; color: #86EFAC; margin: 0 0 6px; }
.result-title-fraud { font-size: 15px; font-weight: 500; color: #FCA5A5; margin: 0 0 6px; }
.result-desc  { font-size: 13px; color: #64748B; line-height: 1.5; }
.result-conf-safe  { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 500; color: #4ADE80; }
.result-conf-fraud { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 500; color: #F87171; }

/* ── Footer info grid ── */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 28px;
    margin-top: 4px;
}
.info-item { font-size: 12px; color: #475569; line-height: 1.6; }
.info-item strong { color: #64748B; font-weight: 500; }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 8px 0 24px;">
    <div style="display:inline-flex; align-items:center; gap:12px; margin-bottom:8px;">
        <div style="width:38px;height:38px;border-radius:8px;background:#0EA5E9;
                    display:flex;align-items:center;justify-content:center;font-size:20px;">🛡️</div>
        <span style="font-size:24px;font-weight:600;color:#F8FAFC;">Fraud Detection System</span>
    </div>
    <p style="font-size:14px;color:#64748B;margin:0;">
        Deep Learning · Financial Transaction Analysis
    </p>
</div>
""", unsafe_allow_html=True)


# ── Metrics ────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Dataset size", "6.36M", "transactions")
with c2:
    st.metric("Model", "DNN", "Deep Neural Network")
with c3:
    st.metric("Stack", "TF / Spark", "TensorFlow + PySpark")

st.markdown("<hr>", unsafe_allow_html=True)


# ── Transaction form ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Transaction details</div>', unsafe_allow_html=True)

transaction_type = st.selectbox(
    "Transaction type",
    ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"],
    index=4
)

col_left, col_right = st.columns(2)

with col_left:
    amount          = st.number_input("Amount ($)", min_value=0.0, format="%.2f", key="amt")
    oldbalanceOrg   = st.number_input("Sender balance before ($)", min_value=0.0, format="%.2f", key="ob_org")
    oldbalanceDest  = st.number_input("Receiver balance before ($)", min_value=0.0, format="%.2f", key="ob_dest")

with col_right:
    newbalanceOrig  = st.number_input("Sender balance after ($)", min_value=0.0, format="%.2f", key="nb_orig")
    newbalanceDest  = st.number_input("Receiver balance after ($)", min_value=0.0, format="%.2f", key="nb_dest")

st.markdown("<br>", unsafe_allow_html=True)

# Fixed: Streamlit columns need explicit indexing unpacked cleanly
b_left, b_center, b_right = st.columns([1, 2, 1])
with b_center:
    # Changed to track logic through state cleanly or simple click action
    analyze = st.button("🔍  Analyze transaction", use_container_width=True)


# ── Result panel ───────────────────────────────────────────────────────────────
if not analyze:
    st.markdown(
        '<div class="result-placeholder">Model prediction will appear here once the trained model is connected.</div>',
        unsafe_allow_html=True
    )
else:
    # ── Placeholder heuristic — replace with your model.predict() call ──
    balance_drain = oldbalanceOrg - newbalanceOrig
    is_fraud = (
        transaction_type in ("TRANSFER", "CASH_OUT")
        and amount > 0
        and abs(balance_drain - amount) < 1.0
    )
    confidence = "87.3%" if is_fraud else "96.1%"

    if is_fraud:
        st.markdown(f"""
        <div class="result-fraud">
            <div class="result-row">
                <div>
                    <span class="badge-fraud">High risk</span>
                    <p class="result-title-fraud">Possible fraudulent transaction</p>
                    <p class="result-desc">
                        Pattern matches known fraud signals: full balance drain on
                        {transaction_type} type. Flagged for manual review.
                    </p>
                </div>
                <div class="result-conf-fraud">{confidence}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-safe">
            <div class="result-row">
                <div>
                    <span class="badge-safe">Low risk</span>
                    <p class="result-title-safe">Transaction appears legitimate</p>
                    <p class="result-desc">
                        No anomalous patterns detected. Balance changes are consistent
                        with a legitimate {transaction_type} transaction.
                    </p>
                </div>
                <div class="result-conf-safe">{confidence}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="info-grid">
    <div class="info-item"><strong>Dataset</strong><br>PaySim Financial Transactions</div>
    <div class="info-item"><strong>Records</strong><br>6,362,604 transactions</div>
    <div class="info-item"><strong>Processing</strong><br>Distributed via PySpark</div>
    <div class="info-item"><strong>Project</strong><br>Distributed Computing &amp; Deep Learning</div>
</div>
<p style="font-size:11px;color:#334155;text-align:center;margin-top:20px;">
    Developed as a Final Project for Distributed Computing and Deep Learning
</p>
""", unsafe_allow_html=True)