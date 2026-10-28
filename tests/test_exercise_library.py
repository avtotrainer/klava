"""KLV selection and safe migration regression tests."""
import sys

import pytest

from logic.exercise_library import available_exercises, choose_exercise, resolve_choice, selected_exercise
from logic.resources import prepare_exercise_file


def test_selection_persists_between_sessions(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.delattr(sys, "frozen", raising=False)
    first = prepare_exercise_file("data/sentences.txt")
    library = first.parent
    custom = library / "ქართული.KLV"
    custom.write_text("A B\nB A\n", encoding="utf-8")
    assert custom in available_exercises()
    assert choose_exercise(custom) == custom
    assert selected_exercise() == custom
    assert prepare_exercise_file("data/sentences.txt") == custom
    custom.unlink()
    assert selected_exercise() == first


def test_reject_paths_outside_user_library(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    prepare_exercise_file("data/sentences.txt")
    for name in ("../outside.klv", "C:/tmp/something.klv", "anything.txt", "", "/tmp/x.klv"):
        with pytest.raises((ValueError, FileNotFoundError)):
            resolve_choice(name)


def test_legacy_txt_migrates_without_deleting_original(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    library = tmp_path / "KLAVA"
    library.mkdir()
    legacy = library / "exercises.txt"
    legacy.write_bytes(b"OLD\nUSER\n")
    new = prepare_exercise_file("data/sentences.txt")
    assert new.name == "exercises.klv"
    assert new.read_bytes() == legacy.read_bytes()
    assert legacy.exists()
    new.write_bytes(b"EDITED\nUSER\n")
    prepare_exercise_file("data/sentences.txt")
    assert new.read_bytes() == b"EDITED\nUSER\n"


def test_portable_txt_next_to_exe_is_migrated(tmp_path, monkeypatch):
    app_dir = tmp_path / "portable"
    app_dir.mkdir()
    (app_dir / "exercises.klv").write_bytes(b"NEW\\nSEED\\n")
    old = app_dir / "exercises.txt"
    old.write_bytes(b"PREVIOUS\\nEDITS\\n")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "user"))
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(app_dir / "KLAVA.exe"))
    path = prepare_exercise_file("data/sentences.klv")
    assert path.read_bytes() == old.read_bytes()
    assert old.exists()
