import json
from pathlib import Path

import torch

from app.model.gpt import GPT
from app.model.runtime import GPTInferenceRuntime
from app.model.tokenizer import CharTokenizer


def _load_tokenizer(path: Path) -> CharTokenizer:
    data = json.loads(path.read_text(encoding="utf-8"))

    if "characters" in data:
        characters = data["characters"]
        stoi = {
            character: token_id
            for token_id, character in enumerate(characters)
        }
        itos = {
            token_id: character
            for character, token_id in stoi.items()
        }
    else:
        stoi = data["stoi"]
        itos = {
            int(token_id): character
            for token_id, character in data["itos"].items()
        }

    return CharTokenizer(stoi=stoi, itos=itos)


def load_runtime(artifact_path: str | Path) -> GPTInferenceRuntime:
    artifact_path = Path(artifact_path)

    config = json.loads(
        (artifact_path / "config.json").read_text(encoding="utf-8")
    )
    model_config = config.get("model", config)

    model = GPT(
        vocab_size=model_config["vocab_size"],
        block_size=model_config["block_size"],
        embedding_dim=model_config["embedding_dim"],
        num_layers=model_config["num_layers"],
        num_heads=model_config["num_heads"],
        dropout=model_config["dropout"],
    )

    state_dict = torch.load(
        artifact_path / "model.pt",
        map_location="cpu",
        weights_only=True,
    )
    if "model_state_dict" in state_dict:
        state_dict = state_dict["model_state_dict"]
    model.load_state_dict(state_dict)

    tokenizer = _load_tokenizer(artifact_path / "tokenizer.json")
    if len(tokenizer.stoi) != model_config["vocab_size"]:
        raise ValueError("Tokenizer vocabulary does not match model config")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    return GPTInferenceRuntime(
        model=model,
        tokenizer=tokenizer,
        device=device,
    )
