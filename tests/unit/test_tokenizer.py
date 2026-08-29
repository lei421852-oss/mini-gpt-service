import pytest

from app.core.exceptions import UnknownCharacterError
from app.model.tokenizer import CharTokenizer


def make_tokenizer() -> CharTokenizer:
    stoi = {"\n": 0, " ": 1, "a": 2, "b": 3, "c": 4}
    itos = {token_id: character for character, token_id in stoi.items()}
    return CharTokenizer(stoi=stoi, itos=itos)


def test_encode() -> None:
    tokenizer = make_tokenizer()

    assert tokenizer.encode("cab\n") == [4, 2, 3, 0]


def test_decode() -> None:
    tokenizer = make_tokenizer()

    assert tokenizer.decode([4, 2, 3, 1]) == "cab "


def test_encode_decode_round_trip() -> None:
    tokenizer = make_tokenizer()
    text = "a cab\n"

    assert tokenizer.decode(tokenizer.encode(text)) == text


def test_encode_raises_unknown_character_error() -> None:
    tokenizer = make_tokenizer()

    with pytest.raises(
        UnknownCharacterError,
        match="Unsupported character: '你'",
    ) as exc_info:
        tokenizer.encode("a你")

    assert exc_info.value.character == "你"
    assert isinstance(exc_info.value.__cause__, KeyError)
