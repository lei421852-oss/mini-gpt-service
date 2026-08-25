import json

import torch

from app.model.gpt import GPT
from app.model.loader import load_runtime
from app.model.runtime import GPTInferenceRuntime

MODEL_CONFIG = {
    "vocab_size": 3,
    "block_size": 4,
    "embedding_dim": 8,
    "num_layers": 1,
    "num_heads": 2,
    "dropout": 0.0,
}


def create_artifact(tmp_path):
    artifact_path = tmp_path / "char-gpt-v1"
    artifact_path.mkdir()

    model = GPT(**MODEL_CONFIG)
    torch.save(model.state_dict(), artifact_path / "model.pt")
    (artifact_path / "config.json").write_text(
        json.dumps(MODEL_CONFIG),
        encoding="utf-8",
    )
    (artifact_path / "tokenizer.json").write_text(
        json.dumps(
            {
                "format_version": 1,
                "type": "character",
                "characters": ["\n", "a", "b"],
            }
        ),
        encoding="utf-8",
    )

    return artifact_path, model


def test_load_runtime_loads_artifact(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    artifact_path, expected_model = create_artifact(tmp_path)

    runtime = load_runtime(artifact_path)

    assert isinstance(runtime, GPTInferenceRuntime)
    assert not runtime.model.training
    assert runtime.device.type == "cpu"
    assert runtime.tokenizer.stoi == {"\n": 0, "a": 1, "b": 2}
    for name, parameter in runtime.model.state_dict().items():
        assert torch.equal(parameter.cpu(), expected_model.state_dict()[name])


def test_loaded_runtime_can_generate(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    artifact_path, _ = create_artifact(tmp_path)
    runtime = load_runtime(artifact_path)

    generated = runtime.generate(
        prompt="a",
        max_new_tokens=2,
        temperature=0,
    )

    assert generated.startswith("a")
    assert len(generated) == 3
