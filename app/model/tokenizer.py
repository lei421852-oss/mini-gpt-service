class CharTokenizer:
    def __init__(
        self,
        stoi: dict[str, int],
        itos: dict[int, str],
    ) -> None:
        self.stoi = stoi
        self.itos = itos

    def encode(self, text: str) -> list[int]:
        return [self.stoi[character] for character in text]

    def decode(self, ids: list[int]) -> str:
        return "".join(self.itos[token_id] for token_id in ids)
