# exercises/typing.py
# KLAVA — Typing Exercise (single line)

from __future__ import annotations

import os
import tkinter as tk

from exercises.base import Exercise

# Windows virtual-key codes for the letter keys are VK_A..VK_Z (0x41..0x5A) and
# name the physical QWERTY position even when a Georgian or Russian layout is active.
_VK_A, _VK_Z = 0x41, 0x5A


def physical_key(event: tk.Event, platform: str | None = None) -> str:
    """Return the uppercase key name, falling back to the Windows key position.

    With a non-Latin layout Tk reports keysyms such as "Georgian_an"; the trainer
    teaches key positions, so on Windows the virtual-key code identifies the letter.
    """
    key = str(event.keysym).upper()
    if (len(key) == 1 and "A" <= key <= "Z") or key == "SPACE":
        return key
    platform = os.name if platform is None else platform
    keycode = getattr(event, "keycode", None)
    if platform == "nt" and isinstance(keycode, int) and _VK_A <= keycode <= _VK_Z:
        return chr(keycode)
    return key


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

        key = physical_key(event)
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
