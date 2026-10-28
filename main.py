# main.py
# KLAVA — Entry point

import os
import sys
import tkinter as tk
from tkinter import messagebox

from logic.resources import exercise_path, prepare_exercise_file
from trainer import Trainer

__version__ = "0.3.1-alfa"


def main() -> None:
    """Initialize installed user data and optionally open the exercise editor."""
    root = tk.Tk()
    root.withdraw()
    trainer = Trainer(root)
    source = trainer.cfg.get("training", "sentence_file", fallback="data/sentences.txt")
    try:
        path = prepare_exercise_file(source)
        if "--edit-exercises" in sys.argv:
            os.startfile(path)  # Windows Start-menu editor shortcut; no elevation.
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
