import streamlit as st
import time
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents import EnterpriseAgentCrew
from src.benchmarking import LatencyCostBenchmarker

st.set_page_config(
    page_title="Enterprise Agent Crew | Multi-Agent LLM System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Enterprise Software Crew & Latency Profiler")
st.caption("Autonomous multi-agent swarms (LangChain / CrewAI / Groq) for automated security auditing, QA test suite generation, and real-time inference telemetry benchmarking.")

st.sidebar.header("⚙️ Agent Swarm Settings")
st.sidebar.markdown("**Master LLM:** Groq Llama-3-70B")
st.sidebar.markdown("**Agent Framework:** LangChain / CrewAI Sequential Swarm")
st.sidebar.markdown("**Validation:** Strict Pydantic v2 Schema")

groq_key = st.sidebar.text_input("Groq Cloud API Key (Optional)", type="password", help="Leave blank to run instant simulation / benchmark mode")
if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key
    st.sidebar.success("✓ Custom Groq API Key Activated")

crew = EnterpriseAgentCrew()
benchmarker = LatencyCostBenchmarker()

tab1, tab2, tab3 = st.tabs(["🚀 Execute Swarm Audit", "⚡ Telemetry & Token Benchmark", "📊 Live Architecture"])

SAMPLE_SNIPPETS = {
    "FastAPI Vector DB Authentication": """from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import psycopg2

app = FastAPI()
API_KEY = "sk_live_enterprise_secret_9981"
api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/query-vector")
async def query_vector(query: str, key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid Key")
    conn = psycopg2.connect("postgresql://user:password@localhost:5432/mydb")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM embeddings WHERE text LIKE '%{query}%'")
    return cur.fetchall()
""",
    "AsyncIO Supabase Ingestion Pipeline": """import asyncio
import aiohttp

async def fetch_batch(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(u) for u in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return [await r.text() for r in responses if hasattr(r, 'text')]
""",
    "XGBoost ONNX Model Exporter": """import xgboost as xgb
import onnxmltools

def export_model(bst, num_features):
    initial_type = [('float_input', onnxmltools.convert.common.data_types.FloatTensorType([None, num_features]))]
    onnx_model = onnxmltools.convert_xgboost(bst, initial_types=initial_type)
    onnxmltools.utils.save_model(onnx_model, 'model.onnx')
"""
}

with tab1:
    st.subheader("Autonomous Code Analysis & QA Generation")
    
    preset = st.selectbox("Select Enterprise Code Sample:", list(SAMPLE_SNIPPETS.keys()))
    code_input = st.text_area("Target Python Code to Audit:", value=SAMPLE_SNIPPETS[preset], height=200)
    
    if st.button("▶ Run Multi-Agent Crew Workflow", type="primary"):
        with st.status("Executing Multi-Agent Swarm...", expanded=True) as status:
            st.write("1. 🛡️ **Security Auditor Agent:** Scanning AST tree for secrets & SQL injection risks...")
            time.sleep(0.3)
            st.write("2. 🧪 **QA Architect Agent:** Formulating boundary conditions & pytest suite...")
            time.sleep(0.3)
            st.write("3. 📝 **Lead Documenter Agent:** Validating strict Pydantic v2 data contract...")
            time.sleep(0.3)
            
            result = crew.run_audit(code_input)
            status.update(label="✅ Swarm Execution Complete!", state="complete")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Security Status", "PASSED" if result.get("security_passed") else "VULNERABILITIES DETECTED", delta="High Risk" if not result.get("security_passed") else "Safe")
        c2.metric("Vulnerabilities Found", len(result.get("vulnerabilities", [])))
        c3.metric("Generated Test Cases", len(result.get("test_cases", [])))
        c4.metric("Inference Latency", f"{result.get('latency_ms', 42.5):.1f} ms")
        
        st.subheader("🛡️ Identified Security Findings")
        for v in result.get("vulnerabilities", []):
            st.warning(f"**[{v.get('severity', 'HIGH')}] Line {v.get('line', 'N/A')}:** {v.get('description', '')} — *Fix:* `{v.get('fix_suggestion', '')}`")
        
        st.subheader("🧪 Synthesized PyTest Blueprint")
        st.code(result.get("test_code", "# No tests generated"), language="python")

with tab2:
    st.subheader("Inference Latency, Throughput & Token Cost Profiler")
    
    concurrency = st.slider("Simulated Concurrency Level (Threads)", 1, 20, 5)
    
    if st.button("⚡ Execute Concurrency Benchmark"):
        with st.spinner("Benchmarking Groq Llama-3 cluster under load..."):
            summary = benchmarker.run_benchmark(concurrency=concurrency, iterations=10)
            
            b1, b2, b3, b4 = st.columns(4)
            b1.metric("P95 Latency", f"{summary['p95_latency_ms']} ms")
            b2.metric("Mean Throughput", f"{summary['throughput_rps']} req/s")
            b3.metric("Tokens Processed", summary['total_tokens'])
            b4.metric("Est. Total USD Cost", f"${summary['total_cost_usd']:.6f}")
            
            st.subheader("Latency Distribution (ms)")
            lat_df = pd.DataFrame(summary['latencies_ms'], columns=["Latency (ms)"])
            st.line_chart(lat_df)

with tab3:
    st.subheader("FastAPI Microservice Architecture")
    st.markdown("""
    ```mermaid
    sequenceDiagram
        Client->>FastAPI Microservice (api.py): POST /api/v1/audit/execute
        FastAPI Microservice (api.py)->>Security Auditor Agent: AST Tree & Pattern Scan
        Security Auditor Agent-->>FastAPI Microservice (api.py): Security Findings
        FastAPI Microservice (api.py)->>QA Architect Agent: Generate PyTest Suite
        QA Architect Agent-->>FastAPI Microservice (api.py): PyTest Code
        FastAPI Microservice (api.py)->>Telemetry Engine: Measure Latency & Tokens
        FastAPI Microservice (api.py)-->>Client: Pydantic v2 Validated JSON
    ```
    """)
