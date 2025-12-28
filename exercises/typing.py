# exercises/typing.py
# KLAVA — Typing Exercise

from exercises.base import Exercise
from logic.engine import TypingEngine


class TypingExercise(Exercise):
    """
    ბეჭდვის სავარჯიშო — მუშაობს ზუსტად ერთ სტრიქონზე.

    პასუხისმგებლობა:
    - კლავიშის დამუშავება
    - სწორ/არასწორ ბეჭდვაზე რეაქცია
    - მიმდინარე სტრიქონის დასრულების ფლაგი

    არ აკეთებს:
    - სტრიქონების ციკლს
    - ფაილების კითხვას
    - Trainer-ის მართვას
    """

    def __init__(self, ui, keyboard, sentence: str):
        """
        :param ui: Canvas UI ობიექტი
        :param keyboard: Keyboard UI ობიექტი
        :param sentence: ერთი სტრიქონი ბეჭდვისთვის
        """
        self.ui = ui
        self.keyboard = keyboard

        self.engine = TypingEngine(sentence)

        self._finished = False
        self._current_key = None

    # ==================================================
    #   Exercise API
    # ==================================================
    def start(self):
        """
        სავარჯიშოს დაწყება (ერთი სტრიქონი).
        """
        self._finished = False
        self._current_key = None

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

        if correct:
            # სწორად აკრეფილი ასოს გამუქება
            self.ui.shade_letter(self.engine.pos - 1)

        if self.engine.finished:
            self._finished = True
            self.keyboard.reset_key(self._current_key)
        else:
            self._update_target()

    @property
    def finished(self) -> bool:
        """
        აბრუნებს True-ს, თუ მიმდინარე სტრიქონი დასრულებულია.
        """
        return self._finished

    # ==================================================
    #   Internal helpers
    # ==================================================
    def _update_target(self):
        """
        მიმდინარე სიმბოლოს ჰაილაითი კლავიატურაზე.
        """
        if self._current_key is not None:
            self.keyboard.reset_key(self._current_key)

        self._current_key = self.engine.current()
        self.keyboard.highlight(self._current_key)
