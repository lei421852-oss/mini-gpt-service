import torch

from app.model.runtime import GPTInferenceRuntime
from app.model.tokenizer import CharTokenizer


class StubGPT:
    def generate(
        self,
        input_ids,
        max_new_tokens,
        temperature,
        top_k,
    ):
        assert input_ids.shape == (1, 1)
        assert input_ids.device.type == "cpu"
        assert max_new_tokens == 1
        assert temperature == 0.8
        assert top_k == 2
        return torch.tensor([[0, 1]])


def test_runtime_generate_returns_string() -> None:
    tokenizer = CharTokenizer(
        stoi={"a": 0, "b": 1},
        itos={0: "a", 1: "b"},
    )
    runtime = GPTInferenceRuntime(
        model=StubGPT(),
        tokenizer=tokenizer,
        device=torch.device("cpu"),
    )

    generated = runtime.generate(
        prompt="a",
        max_tokens=1,
        temperature=0.8,
        top_k=2,
    )

    assert isinstance(generated, str)
    assert generated == "ab"
