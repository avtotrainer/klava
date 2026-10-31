"""სავარჯიშოს ტექსტის წესები: მხოლოდ ის სიმბოლოები, რაც ეკრანის კლავიატურაზეა."""

import pytest

from logic.exercise_text import (
    SUPPORTED_CHARACTERS,
    UnsupportedCharacterError,
    describe_character,
    normalize_lines,
)


def test_supported_characters_match_on_screen_keyboard():
    from ui.keyboard import KEYBOARD, SPACE_KEY

    assert SUPPORTED_CHARACTERS == {ch for row in KEYBOARD for ch in row} | {SPACE_KEY}


def test_normalization_trims_skips_blank_and_uppercases():
    assert normalize_lines(["  f j \n", "\n", "   ", "gh\n"]) == ["F J", "GH"]


@pytest.mark.parametrize(("raw", "line", "char"), [
    (["A", "B,"], 2, ","),
    (["", "A1"], 2, "1"),
    (["A\tB"], 1, "\t"),
    (["A B"], 1, " "),
    (["ä"], 1, "Ä"),
])
def test_first_unsupported_character_is_reported(raw, line, char):
    with pytest.raises(UnsupportedCharacterError) as caught:
        normalize_lines(raw)
    assert (caught.value.line_number, caught.value.character) == (line, char)


def test_invisible_characters_are_described_by_code_point():
    assert describe_character("\t") == "U+0009"
    assert describe_character(" ") == "U+00A0"
    assert describe_character(",") == "','"
