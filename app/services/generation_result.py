from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationResult:
    text: str
    generated_tokens: int
    latency_ms: float
