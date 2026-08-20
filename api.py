from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
import logging

from src.schemas import EnterpriseAuditReport
from src.benchmarking import TelemetryMetrics
from src.agents import MultiAgentCodeReviewSwarm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EnterpriseCrew.API")

app = FastAPI(
    title="Enterprise Multi-Agent Code Audit & Telemetry Microservice",
    description="Asynchronous microservice orchestrating multi-agent LLM swarms for automated vulnerability analysis, pytest generation, and real-time inference latency benchmarking.",
    version="2.0.0"
)

swarm = MultiAgentCodeReviewSwarm()

class CodeAuditRequest(BaseModel):
    source_code: str = Field(..., min_length=10, example="""@app.get("/users")\ndef get_users(id: str):\n    return db.execute(f"SELECT * FROM users WHERE id = '{id}'")""")
    model_override: str = Field(default="llama3-70b-8192")

class CodeAuditResponse(BaseModel):
    report: EnterpriseAuditReport
    telemetry: TelemetryMetrics

@app.get("/health", tags=["System & Telemetry"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Enterprise-Agent-Crew-API",
        "model_loaded": "Llama-3-70B-Groq"
    }

@app.post("/api/v1/audit/analyze", response_model=CodeAuditResponse, tags=["Multi-Agent Orchestration"])
async def audit_codebase(payload: CodeAuditRequest):
    """
    Executes collaborative multi-agent code analysis pipeline with full latency & token telemetry.
    """
    try:
        report, metrics = swarm.run_audit(payload.source_code)
        return CodeAuditResponse(report=report, telemetry=metrics)
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)
