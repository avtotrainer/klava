# exercises/typing.py
# KLAVA — Typing Exercise (single line)

from __future__ import annotations

import tkinter as tk

from exercises.base import Exercise


class TypingExercise(Exercise):
    """
    ერთსტრიქონიანი ბეჭდვის სავარჯიშო (მარტივი ვერსია).

    Does:
    - ერთ წინადადებაზე გავლა
    - სწორ/არასწორ დაჭერაზე UI ბრძანებების გაცემა

    Does not:
    - არ ითვლის ქულას/CPM-ს (ეს შემდეგი ეტაპია)
    """

    def __init__(self, ui, keyboard, sentence: str) -> None:
        self.ui = ui
        self.keyboard = keyboard

        self.sentence = sentence.upper()
        self.letters = list(self.sentence)

        self.pos = 0
        self._finished = False

    @property
    def finished(self) -> bool:
        return self._finished

    # ----------------------------
    def start(self) -> None:
        self._finished = False
        self.pos = 0

        self.ui.clear_sentence()
        self.ui.draw_sentence(self.letters)

        self._set_target()

    def stop(self) -> None:
        self._finished = True

    # ----------------------------
    def on_key(self, event: tk.Event) -> None:
        if self._finished:
            return

        key = str(event.keysym).upper()
        if key == "SPACE":
            key = " "

        # Keyboard-ში ჩვენ მხოლოდ ასოები გვაქვს, SPACE-სთვის სპეციალური ქცევა შემდეგ ეტაპზე იქნება
        if key != " " and key not in self.keyboard.key_boxes:
            return

        target = self.current_target()
        if target is None:
            return

        # არასწორი
        if key != target:
            if key != " ":
                self.keyboard.highlight_wrong(key)
            return

        # სწორი
        if key != " ":
            self.keyboard.highlight_correct(key)

        self.ui.mark_letter(self.pos)
        self.pos += 1

        if self.pos >= len(self.letters):
            self._finished = True
            return

        self._set_target()

    # ----------------------------
    def current_target(self) -> str | None:
        if self.pos >= len(self.letters):
            return None
        return self.letters[self.pos]

    def _set_target(self) -> None:
        target = self.current_target()
        if target is None:
            return

        # SPACE-სთვის target highlight მოგვიანებით დაემატება (როცა space key დავხატავთ)
        # if target != " ":
        self.keyboard.set_target(target)
