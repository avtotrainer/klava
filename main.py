# main.py
# KLAVA — Entry point

from contextlib import nullcontext
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

from logic.resources import exercise_path, prepare_exercise_file
from logic.single_instance import single_instance
from trainer import Trainer

__version__ = "0.3.2-beta.1"


def main() -> None:
    """Reject duplicate trainers before constructing Tk or touching user data."""
    # The editor shortcut opens Notepad, not another training session.
    guard = nullcontext(True) if "--edit-exercises" in sys.argv else single_instance()
    try:
        with guard as acquired:
            if acquired:
                _run_app()
    except OSError as exc:
        messagebox.showerror("KLAVA", f"პროგრამის გაშვება ვერ მოხერხდა.\n{exc}")


def _run_app() -> None:
    """Initialize installed user data and optionally open the exercise editor."""
    root = tk.Tk()
    root.withdraw()
    trainer = Trainer(root)
    source = trainer.cfg.get("training", "sentence_file", fallback="data/sentences.txt")
    try:
        path = prepare_exercise_file(source)
        if "--edit-exercises" in sys.argv:
            subprocess.Popen(["notepad.exe", str(path)])  # .klv has no required file association.
            root.destroy()
            return
    except OSError as exc:
        messagebox.showerror(
            trainer.res.text("errors", "title"),
            trainer.res.text("errors", "file_missing").format(path=exercise_path(source), err=str(exc)),
            parent=root,
        )
        root.destroy()
        return
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
