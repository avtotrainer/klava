"""Portable paths and Trainer lifecycle regressions without a desktop."""
from types import SimpleNamespace
from unittest.mock import Mock
import sys
from zipfile import ZipFile

import pytest

from logic.config import Config
from logic.resources import Resources, bundled_path, exercise_path
from trainer import Trainer
from scripts.package_windows import package


@pytest.fixture
def portable(tmp_path, monkeypatch):
    folder = tmp_path / "ქართული საქაღალდე"
    folder.mkdir()
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(folder / "KLAVA.exe"))
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path / "unrelated-extraction"), raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "user" / "Local"))
    trainer = Trainer.__new__(Trainer)
    trainer.cfg = Config()
    trainer.res = Resources("resources", "ka", "default")
    trainer.root = Mock()
    trainer.ui = Mock()
    trainer.keyboard = Mock()
    trainer.keyboard.key_boxes = {"A": {}, "B": {}, " ": {}}
    trainer.menu = Mock()
    trainer.training_active = False
    trainer.exercise = None
    trainer.sentences = []
    trainer.current_index = 0
    (folder / "exercises.klv").write_text("A\nB\n", encoding="utf-8")
    from logic.resources import prepare_exercise_file
    return trainer, prepare_exercise_file("data/sentences.txt")


def test_source_paths_ignore_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delattr(sys, "frozen", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "Local"))
    from logic.resources import prepare_exercise_file
    assert prepare_exercise_file("data/sentences.txt").is_file()
    assert Config().getint("training", "min_lines") == 2
    assert Resources("resources", "ka", "default").keyboard_model["groups"]


def test_bundled_paths_use_module_location(tmp_path, monkeypatch):
    import logic.resources as resources
    monkeypatch.setattr(resources, "__file__", str(tmp_path / "logic/resources.py"))
    assert bundled_path("config.ini") == tmp_path / "config.ini"
    assert bundled_path("resources") == tmp_path / "resources"


def test_portable_normalization_and_bom(portable):
    trainer, path = portable
    path.write_text("  a b  \n\n b a \n", encoding="utf-8-sig")
    assert exercise_path() == path
    assert trainer._load_sentences() == ["A B", "B A"]


@pytest.mark.parametrize("contents", [
    None, b"", b" \n\n", b"\xff\xfe\x00\x00", b"A\n",
    # Characters the on-screen keyboard cannot teach would trap the learner in kiosk mode.
    b"A, B\nB\n", b"A\nB 2\n", b"A\tB\nB\n", "A\n\u10d0\n".encode(),
])
def test_invalid_exercises_leave_session_inactive_and_file_unchanged(portable, monkeypatch, contents):
    trainer, path = portable
    if contents is not None:
        path.write_bytes(contents)
    errors = Mock()
    monkeypatch.setattr("trainer.messagebox.showerror", errors)
    trainer.start_training()
    if contents is None:
        assert trainer.training_active
        trainer._secret_finish()
        return
    errors.assert_called_once()
    assert errors.call_args.args[1]
    assert not trainer.training_active
    trainer.menu.hide.assert_not_called()
    trainer.root.attributes.assert_not_called()
    if contents is not None:
        assert path.read_bytes() == contents
    if contents == b"\xff\xfe\x00\x00":
        assert "UTF-8" in errors.call_args.args[1]
    # Correcting the file allows retry without restarting the program.
    path.write_text("A\nB\n", encoding="utf-8")
    trainer.start_training()
    assert trainer.training_active


@pytest.mark.parametrize(("contents", "line", "char"), [
    ("A\nHI, YOU\n", 2, "','"),
    ("\n\nA\tB\n", 3, "U+0009"),
    ("\u10d2\u10d0\n", 1, "'\u1c92'"),  # Georgian is uppercased to Mtavruli first
])
def test_unsupported_character_error_names_line_and_character(
    portable, monkeypatch, contents, line, char
):
    trainer, path = portable
    path.write_text(contents, encoding="utf-8")
    errors = Mock()
    monkeypatch.setattr("trainer.messagebox.showerror", errors)
    trainer.start_training()
    message = errors.call_args.args[1]
    assert str(line) in message and char in message and str(path) in message
    assert not trainer.training_active


def test_session_completion_and_reload(portable):
    trainer, path = portable
    path.write_text("a b\nb\n", encoding="utf-8")
    trainer.start_training()
    trainer.on_key(SimpleNamespace(keysym="b"))
    assert trainer.exercise.pos == 0
    trainer.keyboard.highlight_wrong.assert_called_with("B")
    for key in ["a", "space", "b", "b"]:
        trainer.on_key(SimpleNamespace(keysym=key))
    assert not trainer.training_active
    assert trainer.exercise is None
    trainer.menu.show.assert_called_once()
    path.write_text("B\nA\n", encoding="utf-8")
    trainer.start_training()
    assert trainer.sentences == ["B", "A"]
    assert trainer.exercise.current_target() == "B"
    # Editing during a session is applied only at the next session boundary.
    path.write_text("A\nA\n", encoding="utf-8")
    trainer.start_training()
    assert trainer.sentences == ["B", "A"]


def test_seed_is_supported_and_packaging_is_exact(tmp_path):
    (tmp_path / "data").mkdir()
    seed = bundled_path("data/sentences.txt").read_bytes()
    (tmp_path / "data/sentences.klv").write_bytes(seed)
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist/KLAVA.exe").write_bytes(b"test executable placeholder")
    archive = package(tmp_path)
    with ZipFile(archive) as zipped:
        assert sorted(zipped.namelist()) == ["KLAVA/KLAVA.exe", "KLAVA/exercises.klv"]
        assert zipped.read("KLAVA/exercises.klv") == seed
    (tmp_path / "dist/KLAVA/unexpected.ini").touch()
    with pytest.raises(ValueError, match="exactly"):
        package(tmp_path)
