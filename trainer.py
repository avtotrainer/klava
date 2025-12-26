# trainer.py
# KLAVA — Trainer (UI + Logic connector)

import tkinter as tk
import time

from logic.engine import TypingEngine
from logic.progress import Progress
from ui.canvas import Canvas
from ui.keyboard import Keyboard


class Trainer:
    """
    UI-სა და ლოგიკის დამაკავშირებელი.
    """

    def __init__(self, root: tk.Tk):
        self.root = root

        # KIOSK MODE
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.config(cursor="none")
        root.protocol("WM_DELETE_WINDOW", lambda: None)
        root.bind("<Control-Shift-Alt-BackSpace>", self._force_exit)
        # LOGIC
        self.engine = TypingEngine("data/sentences.txt")
        self.progress = Progress(self.engine.total)

        self.running = True
        self.timer_started = False
        self.start_time = None

        # UI
        self.ui = Canvas(root)
        self.keyboard = Keyboard(self.ui.canvas, self.ui.width, self.ui.height)

        self.ui.draw_sentence(self.engine.letters)
        self.ui.draw_score_timer()

        root.bind("<Key>", self.on_key)
        root.bind("<Control-Shift-X>", self.force_exit)

        self.update_target()

    def _force_exit(self, event=None):
        """
            საიდუმლო ავარიული გამოსვლა მასწავლებლისთვის.
            მუშაობს კიოსკ რეჟიმშიც.
        """
        self.root.destroy()    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    # --------------------------------------------------
    # დრო
    # --------------------------------------------------
    def elapsed_seconds(self) -> int:
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)

    # --------------------------------------------------
    # target
    # --------------------------------------------------
    def update_target(self):
        if self.engine.finished:
            return
        self.keyboard.highlight(self.engine.current())

    # --------------------------------------------------
    # კლავიში
    # --------------------------------------------------
    def on_key(self, event: tk.Event):
        if not self.running:
            return

        ch = event.keysym.upper()
        if ch == "SPACE":
            ch = " "

        if not self.engine.acceptable(ch):
            return

        if not self.timer_started and ch == self.engine.letters[0]:
            self.timer_started = True
            self.start_time = time.time()
            self.tick()

        if not self.engine.hit(ch):
            self.keyboard.highlight(ch, color="red")
            self.root.after(200, lambda: self.keyboard.reset_key(ch))
            return

        self.ui.shade_letter(self.engine.pos - 1)
        self.keyboard.highlight(ch, color="lightgreen")

        self.progress.step()
        self.ui.update_score(self.progress.percent)

        self.root.after(180, lambda: self.after_correct(ch))

    def after_correct(self, ch: str):
        self.keyboard.reset_key(ch)
        self.keyboard.clear_all()

        if self.engine.finished:
            self.load_next_sentence()
        else:
            self.update_target()

    # --------------------------------------------------
    # წინადადებების გადართვა
    # --------------------------------------------------
    def load_next_sentence(self):
        self.ui.clear_sentence()

        if not self.engine.next_sentence():
            self.finish_all()
            return

        self.progress.reset(self.engine.total)
        self.ui.update_score(0)
        self.ui.draw_sentence(self.engine.letters)
        self.update_target()

    # --------------------------------------------------
    # ტაიმერი
    # --------------------------------------------------
    def tick(self):
        if not self.timer_started or not self.running:
            return

        self.ui.update_timer(self.elapsed_seconds())
        self.root.after(1000, self.tick)

    # --------------------------------------------------
    # დასრულება
    # --------------------------------------------------
    def finish_all(self):
        self.running = False
        self.ui.show_result(
            f"ᲓᲠᲝ: {self.elapsed_seconds()}   ᲥᲣᲚᲔᲑᲘ: {self.progress.percent}"
        )
        self.root.config(cursor="arrow")

    def force_exit(self, event=None):
        self.root.config(cursor="arrow")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Trainer(root)
    root.mainloop()
