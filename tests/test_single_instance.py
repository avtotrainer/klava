"""Real process contention and startup ordering on Windows and POSIX."""

import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import pytest

from logic.single_instance import single_instance

ROOT = Path(__file__).resolve().parents[1]
CHILD = """
import sys
from pathlib import Path
from logic.single_instance import single_instance
with single_instance(Path(sys.argv[1])) as acquired:
    print(int(acquired), flush=True)
    if acquired and len(sys.argv) > 2:
        sys.stdin.readline()
"""


def probe(path, cwd=None):
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    result = subprocess.run(
        [sys.executable, "-c", CHILD, str(path)], cwd=cwd or ROOT,
        env=env, capture_output=True, text=True, timeout=15, check=True,
    )
    return result.stdout.strip()


def test_competing_processes_and_restart(tmp_path):
    path = tmp_path / "instance.lock"
    with single_instance(path) as acquired:
        assert acquired
        for _ in range(5):
            assert probe(path, cwd=tmp_path) == "0"
    assert path.exists()  # A leftover file is not a leftover OS lock.
    assert probe(path) == "1"


def test_forced_process_death_releases_lock(tmp_path):
    path = tmp_path / "instance.lock"
    child = subprocess.Popen(
        [sys.executable, "-c", CHILD, str(path), "hold"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        # Probe until child owns the lock; communicate has a bounded timeout below.
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            ready = pool.submit(child.stdout.readline)
            try:
                assert ready.result(timeout=15).strip() == "1"
            except BaseException:
                child.kill()
                raise
        assert probe(path) == "0"
        child.kill()
        child.communicate(timeout=15)
        assert probe(path) == "1"
    finally:
        if child.poll() is None:
            child.kill()
        child.communicate(timeout=15)


def test_exception_releases_lock(tmp_path):
    path = tmp_path / "instance.lock"
    with pytest.raises(RuntimeError), single_instance(path) as acquired:
        assert acquired
        raise RuntimeError("startup failed")
    assert probe(path) == "1"


def test_independent_user_paths(tmp_path):
    with single_instance(tmp_path / "user-a" / "instance.lock"):
        assert probe(tmp_path / "user-b" / "instance.lock") == "1"


def test_unwritable_lock_location_fails_closed(tmp_path):
    parent = tmp_path / "not-a-directory"
    parent.write_text("occupied")
    with pytest.raises(OSError), single_instance(parent / "instance.lock"):
        pytest.fail("Lock failure must not permit startup")


def test_duplicate_does_not_construct_gui(monkeypatch, tmp_path):
    import main

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["KLAVA.exe"])
    root = Mock()
    trainer = Mock()
    monkeypatch.setattr(main.tk, "Tk", root)
    monkeypatch.setattr(main, "Trainer", trainer)
    with single_instance() as acquired:
        assert acquired
        main.main()
    root.assert_not_called()
    trainer.assert_not_called()


def test_editor_still_available_while_trainer_runs(monkeypatch, tmp_path):
    import main

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["KLAVA.exe", "--edit-exercises"])
    run = Mock()
    monkeypatch.setattr(main, "_run_app", run)
    with single_instance():
        main.main()
    run.assert_called_once()


def test_startup_lock_error_is_reported_without_trainer(monkeypatch):
    import main

    monkeypatch.setattr(sys, "argv", ["KLAVA.exe"])
    run = Mock()
    error = Mock()
    monkeypatch.setattr(main, "_run_app", run)
    monkeypatch.setattr(main.messagebox, "showerror", error)
    # Use an actual filesystem error, not a simulated duplicate.
    monkeypatch.setattr(main, "single_instance", lambda: single_instance(Path(__file__) / "lock"))
    main.main()
    run.assert_not_called()
    error.assert_called_once()


def test_guard_covers_entire_app_and_releases_after_failure(monkeypatch, tmp_path):
    import main

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["KLAVA.exe"])
    path = tmp_path / "KLAVA" / "instance.lock"

    def run():
        assert probe(path) == "0"
        raise RuntimeError("GUI startup failed")

    monkeypatch.setattr(main, "_run_app", run)
    with pytest.raises(RuntimeError):
        main.main()
    assert probe(path) == "1"
