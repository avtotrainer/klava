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
    Trainer არის UI-სა და ლოგიკის დამაკავშირებელი კლასი.
    აქ არ ხდება ლოგიკის გამოთვლა — მხოლოდ მართვა და კოორდინაცია.
    """

    # ==================================================
    #   INIT
    # ==================================================
    def __init__(self, root: tk.Tk):
        self.root = root

        # ── KIOSK MODE ──────────────────────────────
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.config(cursor="none")
        root.protocol("WM_DELETE_WINDOW", lambda: None)

        # ── LOGIC ──────────────────────────────────
        self.engine = TypingEngine("data/sentences.txt")
        self.progress = Progress(self.engine.total)

        self.running = True
        self.timer_started = False
        self.start_time: float | None = None
        self.timer_id = None

        # ── UI ─────────────────────────────────────
        self.ui = Canvas(root)
        self.keyboard = Keyboard(
            self.ui.canvas,
            self.ui.width,
            self.ui.height,
        )

        self.ui.draw_sentence(self.engine.letters)
        self.ui.draw_score_timer()

        # ── EVENTS ─────────────────────────────────
        root.bind("<Key>", self.on_key)
        root.bind("<Control-Shift-X>", self.force_exit)

        # ── INITIAL TARGET ─────────────────────────
        self.update_target()

    # ==================================================
    #   TARGET UPDATE
    # ==================================================
    def update_target(self):
        """
        მიმდინარე target კლავიშის გამოყოფა.
        """
        if self.engine.finished:
            return
        ch = self.engine.current()
        self.keyboard.highlight(ch)

    # ==================================================
    #   KEY HANDLER
    # ==================================================
    def on_key(self, event: tk.Event):
        """
        კლავიშზე დაჭერის დამუშავება.

        წესები:
        - არასწორი კლავიში არ შლის target-ს
        - სწორი კლავიში ცვლის target-ს
        """

        if not self.running:
            return

        ch = event.keysym.upper()
        if ch == "SPACE":
            ch = " "

        if not self.engine.acceptable(ch):
            return

        # ── TIMER START ────────────────────────────
        if not self.timer_started and ch == self.engine.letters[0]:
            self.timer_started = True
            self.start_time = time.time()
            self.tick()

        correct = self.engine.hit(ch)

        # ── WRONG KEY ──────────────────────────────
        if not correct:
            self.keyboard.highlight(ch, color="red")
            self.root.after(200, lambda: self.keyboard.reset_key(ch))
            return

        # ── CORRECT KEY ────────────────────────────
        self.ui.shade_letter(self.engine.pos - 1)
        self.keyboard.highlight(ch, color="lightgreen")

        self.progress.step()
        self.ui.update_score(self.progress.percent)

        # ძველი target იწმინდება და ინიშნება ახალი
        self.root.after(180, self.after_correct_key, ch)

    # ==================================================
    #   AFTER CORRECT KEY
    # ==================================================
    def after_correct_key(self, ch: str):
        """
        სწორი კლავიშის შემდეგ ვიზუალური მდგომარეობის გასუფთავება.
        """
        self.keyboard.reset_key(ch)
        self.keyboard.clear_all()

        if self.engine.finished:
            self.finish()
        else:
            self.update_target()

    # ==================================================
    #   TIMER
    # ==================================================
    def elapsed_seconds(self) -> int:
        """
        აბრუნებს გასულ დროს წამებში.
        """
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)

    def tick(self):
        """
        ტაიმერის ტიკი — იძახება ყოველ წამს.
        """
        if not self.timer_started or not self.running:
            return

        self.ui.update_timer(self.elapsed_seconds())
        self.timer_id = self.root.after(1000, self.tick)

    # ==================================================
    #   FINISH
    # ==================================================
    def finish(self):
        """
        ტრენაჟორის დასრულება.
        """
        self.running = False

        elapsed = self.elapsed_seconds() if self.timer_started else 0
        self.ui.show_result(f"ᲓᲠᲝ: {elapsed}   ᲥᲣᲚᲔᲑᲘ: {self.progress.percent}")

        self.root.config(cursor="arrow")

    # ==================================================
    #   FORCE EXIT
    # ==================================================
    def force_exit(self, event=None):
        """
        იძულებითი გამოსვლა (Ctrl+Shift+X).
        """
        self.root.config(cursor="arrow")
        self.root.destroy()


# ======================================================
#   ENTRY POINT
# ======================================================
if __name__ == "__main__":
    root = tk.Tk()
    Trainer(root)
    root.mainloop()
