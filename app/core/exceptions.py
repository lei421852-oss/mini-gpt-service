class MiniGPTError(Exception):
    """Base exception for mini-gpt-service application errors."""


class InvalidModelInputError(MiniGPTError):
    """Raised when model input cannot be processed."""


class UnknownCharacterError(InvalidModelInputError):
    def __init__(self, character: str) -> None:
        self.character = character
        super().__init__(f"Unsupported character: {character!r}")
