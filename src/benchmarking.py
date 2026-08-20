import time
from typing import Dict, Any, List
from pydantic import BaseModel

class TelemetryMetrics(BaseModel):
    latency_ms: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    throughput_tokens_per_sec: float
    model_name: str

class AgentBenchmarker:
    """
    Tracks inference latency, token overhead, and financial compute cost
    across Groq Llama-3-70B/8B clusters.
    """
    def __init__(self, model_name: str = "llama3-70b-8192"):
        self.model_name = model_name
        # Groq pricing per 1K tokens
        self.cost_per_1k_input = 0.00059 if "70b" in model_name else 0.00005
        self.cost_per_1k_output = 0.00079 if "70b" in model_name else 0.00008

    def calculate_metrics(self, prompt_text: str, response_text: str, duration_sec: float) -> TelemetryMetrics:
        # Approximate tokens (standard ~4 chars per token for English/code)
        input_tokens = max(1, len(prompt_text) // 4)
        output_tokens = max(1, len(response_text) // 4)
        total_tokens = input_tokens + output_tokens

        cost = (
            (input_tokens / 1000.0) * self.cost_per_1k_input +
            (output_tokens / 1000.0) * self.cost_per_1k_output
        )

        tokens_per_sec = round(output_tokens / duration_sec, 2) if duration_sec > 0 else 0.0

        return TelemetryMetrics(
            latency_ms=round(duration_sec * 1000, 2),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=round(cost, 6),
            throughput_tokens_per_sec=tokens_per_sec,
            model_name=self.model_name
        )
