import torch

from app.model.gpt import GPT
from app.model.tokenizer import CharTokenizer


class GPTInferenceRuntime:
    def __init__(
        self,
        model: GPT,
        tokenizer: CharTokenizer,
        device: torch.device,
    ) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float = 1.0,
        top_k: int | None = None,
    ) -> str:
        input_ids = torch.tensor(
            [self.tokenizer.encode(prompt)],
            dtype=torch.long,
        ).to(self.device)
        output_ids = self.model.generate(
            input_ids,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
        )
        return self.tokenizer.decode(output_ids[0].tolist())
