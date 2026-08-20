import time
import random
from typing import List, Dict, Any

class LatencyCostBenchmarker:
    """
    Simulates high-throughput LLM concurrent workloads, token calculation,
    and P95/P99 latency profiling.
    """
    def __init__(self, model_name: str = "llama3-70b-8192"):
        self.model_name = model_name
        self.cost_per_million_input = 0.59
        self.cost_per_million_output = 0.79

    def run_benchmark(self, concurrency: int = 5, iterations: int = 10) -> Dict[str, Any]:
        latencies = []
        total_tokens = 0

        for _ in range(iterations):
            # Base latency around 35ms - 55ms
            base = random.uniform(32.0, 52.0)
            jitter = (concurrency * 1.8) + random.uniform(0.5, 4.0)
            lat = round(base + jitter, 2)
            latencies.append(lat)
            total_tokens += random.randint(320, 580)

        latencies.sort()
        p95_idx = int(len(latencies) * 0.95)
        p95_lat = latencies[min(p95_idx, len(latencies) - 1)]
        mean_lat = round(sum(latencies) / len(latencies), 2)
        
        # USD cost computation
        est_cost = (total_tokens / 1_000_000.0) * ((self.cost_per_million_input + self.cost_per_million_output) / 2.0)

        return {
            "model": self.model_name,
            "concurrency": concurrency,
            "iterations": iterations,
            "mean_latency_ms": mean_lat,
            "p95_latency_ms": p95_lat,
            "throughput_rps": round(1000.0 / mean_lat * concurrency, 1),
            "total_tokens": total_tokens,
            "total_cost_usd": round(est_cost, 6),
            "latencies_ms": latencies
        }

AgentBenchmarker = LatencyCostBenchmarker
