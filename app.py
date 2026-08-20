import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents import MultiAgentCodeReviewSwarm

st.set_page_config(
    page_title="Multi-Agent Enterprise Software Crew",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .metric-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }
    .badge-critical { background-color: #b62324; color: white; padding: 2px 8px; border-radius: 10px; }
    .badge-medium { background-color: #d29922; color: black; padding: 2px 8px; border-radius: 10px; }
    .badge-low { background-color: #388bfd; color: white; padding: 2px 8px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_swarm():
    return MultiAgentCodeReviewSwarm()

swarm = get_swarm()

st.title("🤖 Multi-Agent Enterprise Software Crew & Latency Profiler")
st.caption("Autonomous code auditing, automated pytest blueprinting, and LLM latency & token cost benchmarking powered by LangChain and Groq Llama-3-70B.")

DEFAULT_CODE = """# Sample FastAPI endpoint with potential issues
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

@app.get("/user/{user_id}")
async def get_user_data(user_id: str):
    # Potential SQL Injection & synchronous blocking in async endpoint
    conn = psycopg2.connect("dbname=users user=postgres password=secret")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM accounts WHERE id = '{user_id}'")
    user = cursor.fetchone()
    return {"user": user}
"""

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("📝 Source Code Input")
    source_code = st.text_area("Paste Python / FastAPI Code to Audit:", value=DEFAULT_CODE, height=320)
    audit_btn = st.button("🚀 Run Multi-Agent Audit Swarm", type="primary")

if audit_btn and source_code:
    with st.spinner("Orchestrating Security Auditor, QA Architect, and Lead Documenter agents..."):
        report, metrics = swarm.run_audit(source_code)
        
        with col_right:
            st.subheader("⚡ Inference & Cost Telemetry")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Latency", f"{metrics.latency_ms} ms")
            m2.metric("Tokens", f"{metrics.total_tokens}")
            m3.metric("Throughput", f"{metrics.throughput_tokens_per_sec} t/s")
            m4.metric("Est. Cost", f"${metrics.estimated_cost_usd:.5f}")

            st.metric("Overall Architecture Health Score", f"{report.overall_health_score} / 100")

        st.divider()

        tab1, tab2, tab3 = st.tabs(["🛡️ Security & Concurrency Audit", "🧪 QA Pytest Blueprints", "📋 Executive Architecture Plan"])
        
        with tab1:
            st.subheader("Vulnerabilities & Bottlenecks Detected")
            for v in report.vulnerabilities:
                badge_class = "badge-critical" if v.severity == "CRITICAL" else "badge-medium" if v.severity == "MEDIUM" else "badge-low"
                st.markdown(f"""
                <div style="border-left: 4px solid #f85149; padding-left: 12px; margin-bottom: 16px; background-color: #0d1117; padding-top: 8px; padding-bottom: 8px;">
                    <h4>{v.category} — <span class="{badge_class}">{v.severity}</span></h4>
                    <p><b>Location:</b> <code>{v.line_or_location}</code></p>
                    <p>{v.description}</p>
                    <p style="color: #58a6ff;"><b>Remediation:</b> {v.remediation_suggestion}</p>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.subheader("Automated Pytest Blueprints")
            for test in report.qa_test_blueprints:
                st.write(f"**Test Name:** `{test.test_name}` ({test.test_type})")
                st.code(test.code_snippet, language="python")

        with tab3:
            st.subheader("Executive Architecture Summary")
            st.write(report.project_summary)
            st.subheader("Key Recommendations")
            for r in report.architectural_recommendations:
                st.markdown(f"- {r}")
