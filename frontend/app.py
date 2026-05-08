import streamlit as st
import requests

API_URL = "https://7sjfiytdxh.execute-api.ap-southeast-2.amazonaws.com/hello"

st.set_page_config(
    page_title="Multi-Tenant API Console",
    page_icon="🛰️",
    layout="centered"
)

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    /* Global font size bump */
    html, body, [class*="css"] {
        font-size: 16px !important;
    }

    .card {
        background: #1a1d27;
        border: 1px solid #2e3147;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: #7c83a8;
        margin-bottom: 16px;
    }

    .badges-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .badge {
        background: #1e2235;
        border: 1px solid #2e3560;
        border-radius: 999px;
        padding: 7px 18px;
        font-size: 14px;
        color: #818cf8;
        font-weight: 600;
        white-space: nowrap;
    }

    .metric-box {
        background: #1e2235;
        border: 1px solid #2e3560;
        border-radius: 12px;
        padding: 22px 28px;
        text-align: center;
    }
    .metric-label {
        font-size: 13px;
        color: #7c83a8;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #818cf8;
    }

    .progress-track {
        background: #2e3147;
        border-radius: 999px;
        height: 9px;
        margin-top: 12px;
        overflow: hidden;
    }
    .progress-fill {
        height: 9px;
        border-radius: 999px;
        background: linear-gradient(90deg, #6366f1, #818cf8);
    }

    .chip-success {
        background: #0d2b1f; border: 1px solid #16a34a;
        color: #4ade80; border-radius: 8px;
        padding: 8px 18px; font-size: 15px; font-weight: 700;
        display: inline-block;
    }
    .chip-warn {
        background: #2b1d08; border: 1px solid #d97706;
        color: #fbbf24; border-radius: 8px;
        padding: 8px 18px; font-size: 15px; font-weight: 700;
        display: inline-block;
    }
    .chip-error {
        background: #2b0a0a; border: 1px solid #dc2626;
        color: #f87171; border-radius: 8px;
        padding: 8px 18px; font-size: 15px; font-weight: 700;
        display: inline-block;
    }

    label { color: #a0a8c8 !important; font-size: 15px !important; font-weight: 500 !important; }

    .stTextInput input {
        background: #1e2235 !important;
        border: 1px solid #2e3560 !important;
        border-radius: 8px !important;
        color: #e2e5f1 !important;
        font-size: 15px !important;
        padding: 10px 14px !important;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #818cf8);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 14px;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.03em;
        margin-top: 8px;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    .footer {
        text-align: center;
        color: #4a5080;
        font-size: 13px;
        padding-top: 10px;
    }
    .footer span { color: #6366f1; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 36px 0 24px 0;'>
    <div style='font-size:48px;'>🛰️</div>
    <div style='font-size:28px; font-weight:800; color:#e2e5f1; margin:10px 0 6px 0;'>
        Multi-Tenant API Console
    </div>
    <div style='color:#7c83a8; font-size:16px; font-weight:500;'>
        Auth &nbsp;·&nbsp; Rate Limiting &nbsp;·&nbsp; Usage Tracking &nbsp;·&nbsp; Serverless
    </div>
</div>
""", unsafe_allow_html=True)

# ── Feature badges (no stray closing div issue) ───────────────────────────────
st.markdown("""
<div class='card'>
    <div class='section-title'>Platform Capabilities</div>
    <div class='badges-wrap'>
        <span class='badge'>🔐 Token Auth</span>
        <span class='badge'>⚡ Rate Limiting</span>
        <span class='badge'>📊 DynamoDB Tracking</span>
        <span class='badge'>☁️ AWS Lambda</span>
        <span class='badge'>🔗 API Gateway</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Request form ──────────────────────────────────────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Send API Request</div>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    name = st.text_input("Name", placeholder="e.g. Vanshika")
with col_b:
    tenant_id = st.text_input("Tenant ID", value="tenant_1")

send = st.button("Send Request →")
st.markdown("</div>", unsafe_allow_html=True)

# ── Response ──────────────────────────────────────────────────────────────────
if send:
    params  = {"name": name if name else "Guest", "tenantId": tenant_id}
    headers = {"Authorization": "Bearer my-secret-token"}

    try:
        with st.spinner("Reaching endpoint..."):
            resp = requests.get(API_URL, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            data  = resp.json()
            usage = data.get("usage", 0)
            limit = data.get("limit", 1)
            pct   = min(int((usage / limit) * 100), 100) if limit else 0

            st.markdown("<span class='chip-success'>✅ 200 OK — Request Successful</span><br><br>",
                        unsafe_allow_html=True)

            st.markdown(f"""
            <div class='card'>
                <div class='section-title'>Usage Snapshot</div>
                <div style='display:flex; gap:20px;'>
                    <div class='metric-box' style='flex:1;'>
                        <div class='metric-label'>Requests Used</div>
                        <div class='metric-value'>{usage}</div>
                    </div>
                    <div class='metric-box' style='flex:1;'>
                        <div class='metric-label'>Rate Limit</div>
                        <div class='metric-value'>{limit}</div>
                    </div>
                </div>
                <div style='margin-top:18px;'>
                    <div style='display:flex; justify-content:space-between;
                                font-size:13px; color:#7c83a8; margin-bottom:6px;'>
                        <span>Consumption</span><span>{pct}%</span>
                    </div>
                    <div class='progress-track'>
                        <div class='progress-fill' style='width:{pct}%;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📄 Raw Response JSON"):
                st.json(data)

        elif resp.status_code == 429:
            st.markdown("<span class='chip-warn'>⚠️ 429 — Rate Limit Exceeded</span><br><br>",
                        unsafe_allow_html=True)
            with st.expander("📄 Response Details"):
                st.json(resp.json())

        elif resp.status_code == 401:
            st.markdown("<span class='chip-error'>🔐 401 — Unauthorized: Invalid Token</span>",
                        unsafe_allow_html=True)

        else:
            st.markdown(f"<span class='chip-error'>❌ {resp.status_code} — Unexpected Error</span><br><br>",
                        unsafe_allow_html=True)
            with st.expander("📄 Response Details"):
                st.json(resp.json())

    except requests.exceptions.Timeout:
        st.markdown("<span class='chip-error'>⏱️ Request timed out — check your connection</span>",
                    unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"<span class='chip-error'>🚨 Error: {e}</span>",
                    unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class='footer'>
    Powered by <span>AWS Lambda</span> &nbsp;·&nbsp; <span>API Gateway</span>
    &nbsp;·&nbsp; <span>DynamoDB</span> &nbsp;·&nbsp; <span>Streamlit</span>
</div>
""", unsafe_allow_html=True)
