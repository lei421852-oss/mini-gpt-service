from app.core.exceptions import UnknownCharacterError


class CharTokenizer:
    def __init__(
        self,
        stoi: dict[str, int],
        itos: dict[int, str],
    ) -> None:
        self.stoi = stoi
        self.itos = itos

    def encode(self, text: str) -> list[int]:
        try:
            return [self.stoi[character] for character in text]
        except KeyError as error:
            raise UnknownCharacterError(error.args[0]) from error

    def decode(self, ids: list[int]) -> str:
        return "".join(self.itos[token_id] for token_id in ids)
