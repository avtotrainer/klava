# main.py
# KLAVA — Entry point

from contextlib import nullcontext, suppress
from datetime import datetime
import os
from pathlib import Path, PureWindowsPath
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import traceback

from logic.exercise_library import library_dir
from logic.resources import exercise_path, prepare_exercise_file
from logic.single_instance import single_instance
from trainer import Trainer

__version__ = "0.3.2-beta.1"

ALREADY_RUNNING = "KLAVA უკვე გაშვებულია.\nგამოიყენეთ უკვე გახსნილი ფანჯარა."
STARTUP_FAILED = "პროგრამის გაშვება ვერ მოხერხდა.\n{error}\n\nდეტალები: {log}"
RUNTIME_FAILED = "პროგრამაში შეცდომა მოხდა.\n{error}\n\nდეტალები: {log}"


def main() -> None:
    """Reject duplicate trainers before constructing the trainer or touching user data."""
    # The editor shortcut opens Notepad, not another training session.
    guard = nullcontext(True) if "--edit-exercises" in sys.argv else single_instance()
    try:
        with guard as acquired:
            if acquired:
                _run_app()
            else:
                _notify_already_running()
    except Exception as exc:  # noqa: BLE001 - last resort: the EXE has no console.
        _report_startup_failure(exc)


def _run_app() -> None:
    """Initialize installed user data and optionally open the exercise editor."""
    root = tk.Tk()
    root.withdraw()
    root.report_callback_exception = _report_callback_exception
    trainer = Trainer(root)
    source = trainer.cfg.get("training", "sentence_file", fallback="data/sentences.txt")
    try:
        path = prepare_exercise_file(source)
        if "--edit-exercises" in sys.argv:
            # .klv has no required file association; use the system Notepad by full path
            # so a notepad.exe placed next to KLAVA or in the working folder is never run.
            subprocess.Popen([_notepad(), str(path)])  # noqa: S603 - fixed program, own file
            root.destroy()
            return
    except OSError as exc:
        messagebox.showerror(
            trainer.res.text("errors", "title"),
            trainer.res.text("errors", "file_missing").format(path=exercise_path(), err=str(exc)),
            parent=root,
        )
        root.destroy()
        return
    root.deiconify()
    root.mainloop()


def _notepad() -> str:
    """Absolute path of the Windows Notepad."""
    system_root = os.environ.get("SystemRoot") or r"C:\Windows"
    return str(PureWindowsPath(system_root, "System32", "notepad.exe"))


def _notify_already_running() -> None:
    """A second launch explains itself instead of silently doing nothing."""
    messagebox.showinfo("KLAVA", ALREADY_RUNNING)


def _write_error_log(exc: BaseException) -> Path | None:
    """Append the traceback to the per-user log; never raise from error handling."""
    log = library_dir() / "error.log"
    with suppress(OSError):
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a", encoding="utf-8") as handle:
            handle.write(f"\n=== {datetime.now().isoformat(timespec='seconds')} "
                         f"KLAVA {__version__} ===\n")
            handle.write("".join(traceback.format_exception(exc)))
        return log
    return None


def _report_startup_failure(exc: BaseException, template: str = STARTUP_FAILED) -> None:
    log = _write_error_log(exc)
    messagebox.showerror("KLAVA", template.format(error=exc, log=log or "—"))


def _report_callback_exception(exc_type, exc, tb) -> None:  # noqa: ARG001 - Tk signature
    """Tk callback errors would otherwise vanish in the windowed EXE."""
    _report_startup_failure(exc.with_traceback(tb), RUNTIME_FAILED)


if __name__ == "__main__":
    main()
