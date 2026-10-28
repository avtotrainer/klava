"""Opt-in real Tk widget integration; this is not human visual acceptance."""
import os
import sys
import tkinter as tk
from types import SimpleNamespace

import pytest

from trainer import Trainer

pytestmark = pytest.mark.skipif(
    os.environ.get("KLAVA_GUI_TEST") != "1", reason="Requires a desktop/Tk display"
)


def test_real_widgets_session_and_reload(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "KLAVA.exe"))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "user-local"))
    seed = tmp_path / "exercises.klv"
    seed.write_text("A B\nB\n", encoding="utf-8")
    from logic.resources import prepare_exercise_file
    exercises = prepare_exercise_file("data/sentences.klv")
    root = tk.Tk()
    try:
        trainer = Trainer(root)
        root.update()
        assert root.winfo_width() == 800 and root.winfo_height() == 600
        assert trainer.ui._welcome_visible
        assert trainer.ui.canvas.itemcget(trainer.ui.cover_image, 'state') == 'normal'
        assert set(trainer.keyboard.key_boxes) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
        trainer.start_training()
        root.update()
        trainer.on_key(SimpleNamespace(keysym="b"))
        assert trainer.exercise.pos == 0
        box = trainer.keyboard.key_boxes["B"]
        assert trainer.ui.canvas.itemcget(box["rect"], "fill") == trainer.keyboard.COLOR_WRONG
        for key in ["a", "space", "b", "b"]:
            trainer.on_key(SimpleNamespace(keysym=key))
            root.update()
        assert not trainer.training_active
        exercises.write_text("B A\nA\n", encoding="utf-8")
        trainer.start_training()
        root.update()
        assert trainer.exercise.sentence == "B A"
        trainer._secret_finish()
        assert not trainer.training_active
        # The completed-message overlay must track actual Tk canvas dimensions.
        trainer.ui.canvas.config(width=800, height=600)
        root.update()
        w, h = trainer.ui.canvas.winfo_width(), trainer.ui.canvas.winfo_height()
        assert trainer.ui.canvas.coords(trainer.ui.cover_text) == [w / 2, h / 2]
        assert trainer.ui.canvas.coords(trainer.ui.cover_rect) == [0.0, 0.0, float(w), float(h)]
        trainer._about()
        root.update()
        dialog = next(child for child in root.winfo_children() if isinstance(child, tk.Toplevel))
        dialog.destroy()
    finally:
        root.destroy()
