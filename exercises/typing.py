# exercises/typing.py
# KLAVA — Typing Exercise (single line)

from __future__ import annotations

import tkinter as tk


class TypingExercise:
    """
    ერთსტრიქონიანი ბეჭდვის სავარჯიშო.

    პასუხისმგებლობა:
    - ერთი სტრიქონის/წინადადების გავლა
    - სწორი/არასწორი დაჭერის შეფასება
    - UI-სთვის საჭირო ბრძანებების გაცემა (Canvas + Keyboard)

    შენიშვნა:
    - ეს კლასი არ ქმნის Canvas/Keyboard-ს — ის მხოლოდ იღებს მათ და იყენებს.
    """

    def __init__(self, ui, keyboard, sentence: str) -> None:
        self.ui = ui
        self.keyboard = keyboard

        self.sentence: str = sentence.upper()
        self.letters: list[str] = list(self.sentence)

        self.pos: int = 0
        self.finished: bool = False

    # ======================================================
    #   LIFECYCLE
    # ======================================================
    def start(self) -> None:
        """
        სავარჯიშოს დაწყება:
        - ტექსტის დახატვა
        - პირველი target-ის დაყენება
        """
        self.finished = False
        self.pos = 0

        # ტექსტი თავიდან დახატე (თუ Canvas-ში ძველი რამ დარჩა)
        self.ui.clear_sentence()
        self.ui.draw_sentence(self.letters)

        # პირველი target
        self._set_target()

    def stop(self) -> None:
        """სავარჯიშოს შეჩერება."""
        self.finished = True

    # ======================================================
    #   INPUT
    # ======================================================
    def on_key(self, event: tk.Event) -> None:
        """
        იღებს Tkinter key event-ს და ამუშავებს მხოლოდ მისაღებ ღილაკებს.
        """
        if self.finished:
            return

        key = str(event.keysym).upper()
        if key == "SPACE":
            key = " "

        # ჩვენთვის მისაღებია მხოლოდ ის კლავიშები, რაც კლავიატურაზეა
        if key not in self.keyboard.key_boxes:
            return

        target = self.current_target()
        if target is None:
            return

        # არასწორი
        if key != target:
            self.keyboard.highlight_wrong(key)
            return

        # სწორი
        self.keyboard.highlight_correct(key)

        # ტექსტში მონიშვნა (სწორი სიმბოლო გამუქდეს)
        self.ui.mark_letter(self.pos)

        self.pos += 1
        if self.pos >= len(self.letters):
            self.finished = True
            return

        # შემდეგი target
        self._set_target()

    # ======================================================
    #   HELPERS
    # ======================================================
    def current_target(self) -> str | None:
        """აბრუნებს მიმდინარე სამიზნე სიმბოლოს, ან None თუ დასრულებულია."""
        if self.pos >= len(self.letters):
            return None
        return self.letters[self.pos]

    def _set_target(self) -> None:
        """
        აყენებს target-ს კლავიატურაზე იგივე პრინციპით, როგორც ძველ root Trainer-ში იყო:
        - target ყოველთვის ყვითელია
        - სწორის შემდეგ გადადის ახალ target-ზე
        - არასწორი არ ცვლის target-ს
        """
        target = self.current_target()
        if target is None:
            return

        self.keyboard.set_target(target)
