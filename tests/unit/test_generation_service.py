from app.services.generation_service import GenerationService


class FakeRuntime:
    def __init__(self) -> None:
        self.call = None

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_k: int | None,
    ) -> str:
        self.call = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
        }
        return "generated text"


def test_generate_delegates_to_runtime() -> None:
    runtime = FakeRuntime()
    service = GenerationService(runtime=runtime)

    result = service.generate(
        prompt="Once",
        max_tokens=20,
        temperature=0.8,
        top_k=10,
    )

    assert result == "generated text"
    assert runtime.call == {
        "prompt": "Once",
        "max_tokens": 20,
        "temperature": 0.8,
        "top_k": 10,
    }
