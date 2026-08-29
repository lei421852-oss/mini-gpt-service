import logging
import time

from app.model.runtime import GPTInferenceRuntime
from app.services.generation_result import GenerationResult

logger = logging.getLogger(__name__)


class GenerationService:
    def __init__(self, runtime: GPTInferenceRuntime) -> None:
        self.runtime = runtime

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_k: int | None,
    ) -> GenerationResult:
        started_at = time.perf_counter()
        output_text = self.runtime.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
        )
        latency_ms = (time.perf_counter() - started_at) * 1000

        # This length difference is valid only for the current char-level model.
        generated_tokens = len(output_text) - len(prompt)
        result = GenerationResult(
            text=output_text,
            generated_tokens=generated_tokens,
            latency_ms=latency_ms,
        )

        logger.info(
            "generation_completed prompt_length=%d generated_tokens=%d "
            "latency_ms=%.3f",
            len(prompt),
            result.generated_tokens,
            result.latency_ms,
        )

        return result
