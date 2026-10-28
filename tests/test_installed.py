"""Installed data belongs to each runtime user, not the elevated installer."""
import sys

import pytest

from logic.resources import exercise_path, prepare_exercise_file


@pytest.fixture
def installed(tmp_path, monkeypatch):
    app = tmp_path / "Program Files" / "KLAVA"
    app.mkdir(parents=True)
    seed = app / "default-exercises.txt"
    seed.write_bytes(b"F J\nJ F\n")
    local = tmp_path / "user-profile" / "Local"
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(app / "KLAVA.exe"))
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.chdir(tmp_path)
    return app, local / "KLAVA" / "exercises.txt"


def test_installed_seed_is_copied_to_user_profile(installed):
    app, user_file = installed
    assert exercise_path("unused") == user_file
    assert not user_file.exists()
    assert prepare_exercise_file("unused") == user_file
    assert user_file.read_bytes() == (app / "default-exercises.txt").read_bytes()
    assert sorted(p.name for p in app.iterdir()) == ["default-exercises.txt"]


@pytest.mark.parametrize("content", [b"A\nB\n", b"", b"\xff\xfe"])
def test_relaunch_and_upgrade_never_overwrite_user_edits(installed, content):
    app, user_file = installed
    prepare_exercise_file("unused")
    user_file.write_bytes(content)
    (app / "default-exercises.txt").write_bytes(b"NEW\nDEFAULT\n")
    prepare_exercise_file("unused")
    assert user_file.read_bytes() == content


def test_different_windows_users_get_independent_exercises(installed, monkeypatch, tmp_path):
    _, first = installed
    prepare_exercise_file("unused")
    first.write_bytes(b"FIRST\nUSER\n")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "second-user"))
    second = prepare_exercise_file("unused")
    assert second != first
    assert second.read_bytes() == b"F J\nJ F\n"
    assert first.read_bytes() == b"FIRST\nUSER\n"


def test_portable_missing_file_is_not_silently_created(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "KLAVA.exe"))
    path = prepare_exercise_file("unused")
    assert path == tmp_path / "exercises.txt"
    assert not path.exists()


def test_editor_shortcut_opens_resolved_file_without_starting_session(monkeypatch, tmp_path):
    from unittest.mock import Mock
    import main

    root = Mock()
    trainer = Mock()
    path = tmp_path / "exercises.txt"
    prepare = Mock(return_value=path)
    editor = Mock()
    monkeypatch.setattr(main.tk, "Tk", Mock(return_value=root))
    monkeypatch.setattr(main, "Trainer", Mock(return_value=trainer))
    monkeypatch.setattr(main, "prepare_exercise_file", prepare)
    monkeypatch.setattr(main.os, "startfile", editor, raising=False)
    monkeypatch.setattr(main.sys, "argv", ["KLAVA.exe", "--edit-exercises"])
    main.main()
    editor.assert_called_once_with(path)
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
