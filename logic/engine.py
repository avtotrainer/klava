# logic/engine.py
# KLAVA — Typing logic engine

import time


class TypingEngine:
    """
    ბეჭდვის ლოგიკა.
    UI არაფერი იცის.
    """

    STATE_NORMAL = "NORMAL"
    STATE_DIMMING = "DIMMING"
    STATE_BUG = "BUG"
    STATE_RESTORE = "RESTORE"

    def __init__(
        self,
        sentence: str,
        *,
        sweep_required: int = 8,
        sweep_time_window: float = 0.7,
        wrong_streak_limit: int = 3,
    ):
        """
        sentence: მიმდინარე დასაბეჭდი სტრიქონი
        sweep_required: სწრაფი არასწორი დაჭერების რაოდენობა
        sweep_time_window: დროის ფანჯარა sweep-ისთვის
        wrong_streak_limit: ზედიზედ არასწორი სიმბოლოები
        """
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("TypingEngine საჭიროებს არაცარიელ სტრიქონს")

        self.letters = list(sentence)
        self.pos = 0
        self.finished = False

        # behavioral guard params
        self._sweep_required = sweep_required
        self._sweep_time_window = sweep_time_window
        self._wrong_streak_limit = wrong_streak_limit

        # runtime state
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

    def current_char(self) -> str:
        if self.finished or self.pos >= len(self.letters):
            return ""
        return self.letters[self.pos]

    # --------------------------------------------------
    # INPUT
    # --------------------------------------------------
    def hit(self, ch: str) -> bool:
        """
        სიმბოლოზე დაჭერის დამუშავება.
        """
        if self.finished or self.is_locked():
            return False

        correct = ch == self.letters[self.pos]
        now = time.time()

        self._key_history.append((ch, now, correct))

        if not correct:
            if now - self._last_wrong_time <= 2.0:
                self._wrong_streak += 1
            else:
                self._wrong_streak = 1

            self._last_wrong_time = now

            if self._wrong_streak >= self._wrong_streak_limit:
                self.enter_error_state()

            if self._detect_sweep():
                self.enter_error_state()

            return False

        # correct
        self._wrong_streak = 0
        self.pos += 1

        if self.pos >= len(self.letters):
            self.finished = True

        return True

    # --------------------------------------------------
    # BEHAVIOR DETECTION
    # --------------------------------------------------
    def _detect_sweep(self) -> bool:
        now = time.time()

        recent_wrong = [
            ts
            for _, ts, ok in self._key_history
            if not ok and (now - ts) <= self._sweep_time_window
        ]

        return len(recent_wrong) >= self._sweep_required

    # --------------------------------------------------
    # STATE CONTROL
    # --------------------------------------------------
    def enter_error_state(self):
        if self.state != self.STATE_NORMAL:
            return
        self.state = self.STATE_DIMMING

    def reset_error_state(self):
        self.state = self.STATE_NORMAL
        self._wrong_streak = 0
        self._last_wrong_time = 0.0

    def is_locked(self) -> bool:
        return self.state in (
            self.STATE_DIMMING,
            self.STATE_BUG,
            self.STATE_RESTORE,
        )
