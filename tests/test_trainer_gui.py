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
        # The approved welcome PNG is bundled and displayed on startup.
        assert trainer.ui._welcome_visible
        assert trainer.ui._welcome_image is not None
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


@pytest.mark.parametrize("size", [(1280, 800), (1366, 768), (800, 600)])
def test_longest_seed_line_fits_window(size):
    """H2: ყველა ასო ეკრანზე ჩანს 39-სიმბოლოიან ჩაშენებულ ხაზზეც."""
    import configparser

    from logic.exercise_text import normalize_lines
    from logic.resources import bundled_path
    from ui.canvas import Canvas

    lines = normalize_lines(bundled_path("data/sentences.klv").read_text(encoding="utf-8-sig").splitlines())
    longest = max(lines, key=len)
    root = tk.Tk()
    try:
        root.geometry(f"{size[0]}x{size[1]}")
        theme = configparser.ConfigParser()
        theme.read(bundled_path("resources/themes/default.ini"), encoding="utf-8")
        ui = Canvas(root, theme)
        root.update()
        ui.draw_sentence(list(longest))
        root.update()
        width = ui.canvas.winfo_width()
        boxes = [ui.canvas.bbox(t) for t, ch in zip(ui.text_ids, longest, strict=True) if ch != " "]
        assert min(b[0] for b in boxes) >= 0
        assert max(b[2] for b in boxes) <= width
    finally:
        root.destroy()


def test_keyboard_follows_window_and_space_label_hides(tmp_path, monkeypatch):
    """M4 + L1: კლავიატურა ფანჯრის ზომას მიჰყვება; SPACE-ის წარწერა იმალება."""
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    root = tk.Tk()
    try:
        trainer = Trainer(root)
        root.update()
        kb, canvas = trainer.keyboard, trainer.ui.canvas
        assert canvas.itemcget(kb.space_box["text"], "state") == "hidden"
        trainer.ui.show_keyboard()
        kb.set_target("F")
        root.geometry("1000x700")
        root.update()
        right = max(canvas.bbox(box["rect"])[2] for box in kb.key_boxes.values())
        assert right <= canvas.winfo_width()
        # The target survives the redraw and the cover stays above new items.
        assert canvas.itemcget(kb.key_boxes["F"]["rect"], "fill") == kb.COLOR_TARGET
        assert canvas.find_all()[-1] in canvas.find_withtag("cover")
    finally:
        root.destroy()


def test_already_running_notice_closes_itself():
    """M5: მეორე გაშვების შეტყობინება თავისით იხურება (ინსტალატორის CI ამას ელის)."""
    import time

    import main

    started = time.monotonic()
    main._notify_already_running(timeout_ms=200)
    assert time.monotonic() - started < 5
