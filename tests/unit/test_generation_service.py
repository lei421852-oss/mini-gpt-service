import logging

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
        return f"{prompt} generated"


def test_generate_returns_observable_result(caplog) -> None:
    runtime = FakeRuntime()
    service = GenerationService(runtime=runtime)

    with caplog.at_level(
        logging.INFO,
        logger="app.services.generation_service",
    ):
        result = service.generate(
            prompt="Once",
            max_tokens=20,
            temperature=0.8,
            top_k=10,
        )

    assert result.text == "Once generated"
    assert result.generated_tokens == 10
    assert result.latency_ms >= 0
    assert runtime.call == {
        "prompt": "Once",
        "max_tokens": 20,
        "temperature": 0.8,
        "top_k": 10,
    }

    log_message = caplog.records[-1].getMessage()
    assert "prompt_length=4" in log_message
    assert "generated_tokens=10" in log_message
    assert "latency_ms=" in log_message
    assert "Once" not in log_message
    assert "Once generated" not in log_message
