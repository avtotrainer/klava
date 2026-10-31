"""Exercise text rules shared by the trainer and the packaging script.

Does:
- defines which characters the on-screen keyboard can teach (A–Z and SPACE)
- normalizes KLV lines (trim, skip blank lines, uppercase)
- reports the first unsupported character with its 1-based line number

Does not:
- read files or show dialogs (callers decide how to report problems)
"""

from __future__ import annotations

from collections.abc import Iterable

SUPPORTED_CHARACTERS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")


class UnsupportedCharacterError(ValueError):
    """A line contains a character the trainer cannot ask the learner to type."""

    def __init__(self, line_number: int, character: str, line: str) -> None:
        self.line_number = line_number
        self.character = character
        self.line = line
        super().__init__(
            f"Line {line_number}: unsupported character {describe_character(character)}"
        )


def describe_character(character: str) -> str:
    """Make invisible characters (TAB, NBSP, ...) readable in an error dialog."""
    if character.isprintable() and not character.isspace():
        return f"'{character}'"
    return f"U+{ord(character):04X}"


def normalize_lines(raw_lines: Iterable[str]) -> list[str]:
    """Return uppercase, trimmed, non-empty lines that use only supported characters.

    Raises UnsupportedCharacterError for the first problem found, so a session never
    starts with a line the learner cannot finish.
    """
    lines: list[str] = []
    for number, raw in enumerate(raw_lines, start=1):
        line = raw.strip().upper()
        if not line:
            continue
        for character in line:
            if character not in SUPPORTED_CHARACTERS:
                raise UnsupportedCharacterError(number, character, line)
        lines.append(line)
    return lines
