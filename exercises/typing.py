# exercises/typing.py
# KLAVA — Typing Exercise

from exercises.base import Exercise
from logic.engine import TypingEngine
from logic.progress import Progress


class TypingExercise(Exercise):
    """
    ბეჭდვის სავარჯიშო.

    ეს კლასი:
    - არ იცნობს Trainer-ს
    - არ მართავს root-ს
    - არ იცის kiosk რეჟიმის არსებობა
    """

    def __init__(self, ui, keyboard):
        """
        :param ui: Canvas UI ობიექტი
        :param keyboard: Keyboard UI ობიექტი
        """
        self.ui = ui
        self.keyboard = keyboard

        self.engine = TypingEngine("data/sentences.txt")
        self.progress = Progress(self.engine.total)

        self._finished = False

    # ==================================================
    #   Exercise API
    # ==================================================
    def start(self):
        """
        სავარჯიშოს დაწყება.
        """
        self.ui.clear()
        self.ui.draw_sentence(self.engine.letters)
        self._update_target()

    def stop(self):
        """
        იძულებითი დასრულება (secret exit).
        """
        self._finished = True

    def on_key(self, event):
        """
        კლავიშის დამუშავება.
        """
        if self._finished:
            return

        ch = event.keysym.upper()
        if ch == "SPACE":
            ch = " "

        if not self.engine.acceptable(ch):
            return

        correct = self.engine.hit(ch)
        self.ui.shade_letter(self.engine.pos - 1)

        if correct:
            self.progress.step()
            self.ui.update_progress(self.progress.percent)

        if self.engine.finished:
            self._finished = True
        else:
            self._update_target()

    @property
    def finished(self) -> bool:
        """
        აბრუნებს True-ს თუ სავარჯიშო დასრულებულია.
        """
        return self._finished

    # ==================================================
    #   Internal helpers
    # ==================================================
    def _update_target(self):
        """
        მიმდინარე სიმბოლოს ჰაილაითი.
        """
        self.keyboard.highlight(self.engine.current())
