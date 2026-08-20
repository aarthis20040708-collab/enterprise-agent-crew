from pydantic import BaseModel, Field
from typing import List, Optional

class VulnerabilityItem(BaseModel):
    category: str = Field(description="e.g., Security, Performance, SQL Injection, Concurrency")
    severity: str = Field(description="CRITICAL, HIGH, MEDIUM, or LOW")
    line_or_location: str = Field(description="Function or code line identified")
    description: str = Field(description="Concise description of the vulnerability or bug")
    remediation_suggestion: str = Field(description="Actionable fix or refactored code pattern")

class TestCasePlan(BaseModel):
    test_name: str = Field(description="Descriptive pytest function name (e.g., test_fastapi_rate_limiting)")
    test_type: str = Field(description="Unit, Integration, Concurrency, or Edge-case")
    code_snippet: str = Field(description="Executable Python pytest snippet")

class EnterpriseAuditReport(BaseModel):
    project_summary: str = Field(description="Executive technical summary of the evaluated codebase")
    overall_health_score: int = Field(description="Score out of 100", ge=0, le=100)
    vulnerabilities: List[VulnerabilityItem] = Field(default_factory=list)
    qa_test_blueprints: List[TestCasePlan] = Field(default_factory=list)
    architectural_recommendations: List[str] = Field(default_factory=list)
