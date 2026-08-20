from typing import List, Optional, Dict, Any

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
        def model_dump(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        def dict(self):
            return self.model_dump()
    def Field(default=None, **kwargs):
        return default

class VulnerabilityItem(BaseModel):
    id: str = Field(default="vuln_01")
    severity: str = Field(default="HIGH")
    line: Optional[int] = Field(default=1)
    description: str = Field(default="")
    fix_suggestion: str = Field(default="")

class TestCasePlan(BaseModel):
    name: str = Field(default="test_boundary")
    description: str = Field(default="")
    expected_output: str = Field(default="")

class EnterpriseAuditReport(BaseModel):
    task_id: str = Field(default="task_001")
    security_passed: bool = Field(default=True)
    vulnerabilities: List[Any] = Field(default_factory=list)
    test_cases: List[Any] = Field(default_factory=list)
    test_code: str = Field(default="")
    latency_ms: float = Field(default=42.0)
    tokens_consumed: int = Field(default=350)
    estimated_cost_usd: float = Field(default=0.00025)
