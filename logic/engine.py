# logic/engine.py
# KLAVA — Typing logic engine

import time


class TypingEngine:
    """
    ბეჭდვის ლოგიკა.
    """

    STATE_NORMAL = "NORMAL"
    STATE_DIMMING = "DIMMING"
    STATE_BUG = "BUG"
    STATE_RESTORE = "RESTORE"

    def __init__(self, sentence: str):
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("TypingEngine საჭიროებს არაცარიელ სტრიქონს")

        self.letters = list(sentence)
        self.pos = 0
        self.finished = False

        # behavioral guard
        self._wrong_streak = 0
        self._last_wrong_time = 0.0
        self._key_history = []

        self.state = self.STATE_NORMAL

    # --------------------------------------------------
    # API
    # --------------------------------------------------
    @property
    def total(self) -> int:
        return len(self.letters)

    def acceptable(self, ch: str) -> bool:
        return isinstance(ch, str) and len(ch) == 1

    def current_char(self) -> str:
        if self.finished or self.pos >= len(self.letters):
            return ""
        return self.letters[self.pos]

    def current(self) -> str:
        return self.current_char()

    # --------------------------------------------------
    # INPUT
    # --------------------------------------------------
    def hit(self, ch: str) -> bool:
        """
        სიმბოლოზე დაჭერის დამუშავება.
        """

        # ⛔ input lock
        if self.finished or self.is_locked():
            return False

        correct = ch == self.letters[self.pos]
        now = time.time()

        # history
        self._key_history.append((ch, now, correct))

        # wrong streak (ერთ ასოზე)
        if not correct:
            if now - self._last_wrong_time <= 0.8:
                self._wrong_streak += 1
            else:
                self._wrong_streak = 1

            self._last_wrong_time = now

            if self._wrong_streak >= 5:
                self.enter_error_state()
        else:
            self._wrong_streak = 0

        # burst sweep
        if not correct and self._detect_sweep():
            self.enter_error_state()

        # core logic
        if not correct:
            return False

        self.pos += 1

        if self.pos >= len(self.letters):
            self.finished = True

        return True

    # --------------------------------------------------
    # BEHAVIOR DETECTION
    # --------------------------------------------------
    def _detect_sweep(self) -> bool:
        REQUIRED_WRONG = 8
        TIME_WINDOW = 0.7

        now = time.time()

        recent_wrong = [
            ts
            for _, ts, ok in self._key_history
            if not ok and (now - ts) <= TIME_WINDOW
        ]

        return len(recent_wrong) >= REQUIRED_WRONG

    # --------------------------------------------------
    # STATE CONTROL
    # --------------------------------------------------
    def enter_error_state(self):
        """
        შეცდომის რეჟიმში გადასვლა (ერთხელ).
        """
        if self.state != self.STATE_NORMAL:
            return

        self.state = self.STATE_DIMMING

    def reset_error_state(self):
        """
        UI იძახებს ანიმაციის დასრულების შემდეგ.
        """
        self.state = self.STATE_NORMAL
        self._wrong_streak = 0
        self._last_wrong_time = 0.0

    def is_locked(self) -> bool:
        return self.state in (
            self.STATE_DIMMING,
            self.STATE_BUG,
            self.STATE_RESTORE,
        )
