"""Installed data belongs to each runtime user, not the elevated installer."""
from pathlib import PureWindowsPath
import sys

import pytest

from logic.resources import exercise_path, prepare_exercise_file


@pytest.fixture
def installed(tmp_path, monkeypatch):
    app = tmp_path / "Program Files" / "KLAVA"
    app.mkdir(parents=True)
    seed = app / "default-exercises.klv"
    seed.write_bytes(b"F J\nJ F\n")
    local = tmp_path / "user-profile" / "Local"
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(app / "KLAVA.exe"))
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.chdir(tmp_path)
    return app, local / "KLAVA" / "exercises.klv"


def test_installed_seed_is_copied_to_user_profile(installed):
    app, user_file = installed
    assert exercise_path() == user_file
    assert not user_file.exists()
    assert prepare_exercise_file("data/sentences.txt") == user_file
    assert user_file.read_bytes() == (app / "default-exercises.klv").read_bytes()
    assert sorted(p.name for p in app.iterdir()) == ["default-exercises.klv"]


@pytest.mark.parametrize("content", [b"A\nB\n", b"", b"\xff\xfe"])
def test_relaunch_and_upgrade_never_overwrite_user_edits(installed, content):
    app, user_file = installed
    prepare_exercise_file("data/sentences.txt")
    user_file.write_bytes(content)
    (app / "default-exercises.klv").write_bytes(b"NEW\nDEFAULT\n")
    prepare_exercise_file("data/sentences.txt")
    assert user_file.read_bytes() == content


def test_different_windows_users_get_independent_exercises(installed, monkeypatch, tmp_path):
    _, first = installed
    prepare_exercise_file("data/sentences.txt")
    first.write_bytes(b"FIRST\nUSER\n")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "second-user"))
    second = prepare_exercise_file("data/sentences.txt")
    assert second != first
    assert second.read_bytes() == b"F J\nJ F\n"
    assert first.read_bytes() == b"FIRST\nUSER\n"


def test_portable_missing_file_is_not_silently_created(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "KLAVA.exe"))
    with pytest.raises(FileNotFoundError):
        prepare_exercise_file("data/sentences.txt")


def test_editor_shortcut_opens_resolved_file_without_starting_session(monkeypatch, tmp_path):
    from unittest.mock import Mock
    import main

    root = Mock()
    trainer = Mock()
    path = tmp_path / "exercises.klv"
    prepare = Mock(return_value=path)
    editor = Mock()
    monkeypatch.setattr(main.tk, "Tk", Mock(return_value=root))
    monkeypatch.setattr(main, "Trainer", Mock(return_value=trainer))
    monkeypatch.setattr(main, "prepare_exercise_file", prepare)
    monkeypatch.setattr(main.subprocess, "Popen", editor)
    monkeypatch.setattr(main.sys, "argv", ["KLAVA.exe", "--edit-exercises"])
    main.main()
    editor.assert_called_once_with([main._notepad(), str(path)])
    notepad = PureWindowsPath(main._notepad())
    assert notepad.is_absolute()  # never a bare PATH lookup
    assert (notepad.parent.name.lower(), notepad.name.lower()) == ("system32", "notepad.exe")
    root.destroy.assert_called_once()
    root.mainloop.assert_not_called()
    trainer.start_training.assert_not_called()


def test_startup_data_failure_is_reported(monkeypatch):
    from unittest.mock import Mock
    import main

    root = Mock()
    error = Mock()
    monkeypatch.setattr(main.tk, "Tk", Mock(return_value=root))
    trainer = Mock()
    trainer.cfg.get.return_value = "data/sentences.txt"
    monkeypatch.setattr(main, "Trainer", Mock(return_value=trainer))
    monkeypatch.setattr(main, "prepare_exercise_file", Mock(side_effect=PermissionError("denied")))
    monkeypatch.setattr(main.messagebox, "showerror", error)
    main.main()
    error.assert_called_once()
    root.destroy.assert_called_once()
    root.mainloop.assert_not_called()


def test_unexpected_failure_is_logged_and_shown(monkeypatch, tmp_path):
    """EXE-ს კონსოლი არ აქვს: შეცდომა ჩანს დიალოგში და იწერება error.log-ში."""
    from unittest.mock import Mock
    import main

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(main.sys, "argv", ["KLAVA.exe"])
    monkeypatch.setattr(main, "_run_app", Mock(side_effect=ValueError("bad config value")))
    error = Mock()
    monkeypatch.setattr(main.messagebox, "showerror", error)
    main.main()
    log = tmp_path / "KLAVA" / "error.log"
    assert "ValueError: bad config value" in log.read_text(encoding="utf-8")
    assert "bad config value" in error.call_args.args[1]
    assert str(log) in error.call_args.args[1]


def test_choosing_exercise_leaves_no_temporary_file(monkeypatch, tmp_path):
    from logic.exercise_library import choose_exercise, library_dir, selected_exercise

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    library_dir().mkdir(parents=True)
    second = library_dir() / "second.klv"
    second.write_text("A\nB\n", encoding="utf-8")
    choose_exercise(second)
    assert selected_exercise() == second
    assert sorted(p.name for p in library_dir().iterdir()) == ["second.klv", "selected-exercise.txt"]
