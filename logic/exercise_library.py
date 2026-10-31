"""User-owned KLV library; installed files are never edited by Setup."""
from __future__ import annotations

import os
from pathlib import Path

LIBRARY_NAME = "KLAVA"
EXTENSION = ".klv"
DEFAULT_NAME = "exercises.klv"


def library_dir() -> Path:
    """Per-user library for both portable and installed KLAVA."""
    return Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local")) / LIBRARY_NAME


def available_exercises() -> list[Path]:
    """Find only directly contained .klv files (case-insensitive), sorted by name."""
    directory = library_dir()
    if not directory.is_dir():
        return []
    return sorted(
        (p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == EXTENSION),
        key=lambda p: p.name.casefold(),
    )


def resolve_choice(name: str) -> Path:
    """Reject absolute paths/traversal and files outside the user library."""
    if not name or Path(name).name != name or Path(name).suffix.lower() != EXTENSION:
        raise ValueError("Invalid KLV exercise name")
    target = library_dir() / name
    if target not in available_exercises():
        raise FileNotFoundError(target)
    return target


def selected_exercise() -> Path:
    """Recover last selection if it still exists; fall back to default/first."""
    choices = available_exercises()
    if not choices:
        return library_dir() / DEFAULT_NAME
    state = library_dir() / "selected-exercise.txt"
    try:
        name = state.read_text(encoding="utf-8").strip()
        return resolve_choice(name)
    except (OSError, ValueError):
        default = library_dir() / DEFAULT_NAME
        return default if default in choices else choices[0]


def choose_exercise(path: Path) -> Path:
    """Save only a validated file name; no arbitrary paths persisted."""
    target = resolve_choice(path.name)
    state = library_dir() / "selected-exercise.txt"
    # Write then rename: a crash or full disk never leaves a half-written selection.
    temporary = state.with_name(state.name + ".tmp")
    temporary.write_text(target.name, encoding="utf-8")
    os.replace(temporary, state)
    return target
