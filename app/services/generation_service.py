from app.model.runtime import GPTInferenceRuntime


class GenerationService:
    def __init__(self, runtime: GPTInferenceRuntime) -> None:
        self.runtime = runtime

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_k: int | None,
    ) -> str:
        return self.runtime.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
        )
