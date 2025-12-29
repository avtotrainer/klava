# logic/engine.py
# KLAVA — Typing logic engine


class TypingEngine:
    """
    ბეჭდვის ლოგიკა.

    პასუხისმგებლობა:
    - ერთ სტრიქონზე ბეჭდვის კონტროლი
    - მიმდინარე სიმბოლოს მართვა
    - დასრულების მდგომარეობის დაფიქსირება

    არ აკეთებს:
    - ფაილების კითხვას
    - ტექსტის არჩევას
    - fallback ტექსტის გენერაციას

     NOTE:
    Error feedback / behavioral guard-ისთვის
    ემატება state სისტემა.
    """

    # ===============================
    #   INPUT STATES
    # ===============================
    STATE_NORMAL = "NORMAL"
    STATE_DIMMING = "DIMMING"
    STATE_BUG = "BUG"
    STATE_RESTORE = "RESTORE"

    def __init__(self, sentence: str):
        """
        ქმნის ბეჭდვის ლოგიკას ერთ სტრიქონზე.

        :param sentence: არაცარიელი სტრიქონი
        """
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("TypingEngine საჭიროებს არაცარიელ სტრიქონს")

        self.letters = list(sentence)
        self.pos = 0
        self.finished = False

        # ...
        self.state = self.STATE_NORMAL

        # ბოლო დაჭერების ისტორია (sweep detection-ისთვის)
        self._key_history = []  # [(char, timestamp, correct)]

    # --------------------------------------------------
    # API
    # --------------------------------------------------
    @property
    def total(self) -> int:
        """
        სტრიქონის სიგრძე.
        """
        return len(self.letters)

    def acceptable(self, ch: str) -> bool:
        """
        დასაშვები სიმბოლოების ფილტრი.
        """
        return isinstance(ch, str) and len(ch) == 1

    def current_char(self) -> str:
        """
        მიმდინარე სამიზნე სიმბოლო.
        """
        if self.finished or self.pos >= len(self.letters):
            return ""
        return self.letters[self.pos]

    # backward compatibility TypingExercise-ისთვის
    def current(self) -> str:
        return self.current_char()

    def hit(self, ch: str) -> bool:
        """
        სიმბოლოზე დაჭერის დამუშავება.

        :return: True თუ სწორია, False — თუ არა
        """
        if self.finished:
            return False

        if ch != self.letters[self.pos]:
            return False

        self.pos += 1

        if self.pos >= len(self.letters):
            self.finished = True

        return True

    # ==================================================
    #   STATE CONTROL (SKELETON)
    # ==================================================
    def enter_error_state(self):
        """
        გადაყავს engine შეცდომის ანიმაციის მდგომარეობაში.
        UI ამ state-ზე რეაგირებს.
        """
        self.state = self.STATE_DIMMING

    def reset_error_state(self):
        """
        აბრუნებს engine-ს ნორმალურ მდგომარეობაში.
        """
        self.state = self.STATE_NORMAL
        self._key_history.clear()

    def is_locked(self) -> bool:
        """
        აბრუნებს True-ს, თუ input დროებით დაბლოკილია.
        """
        return self.state in (
            self.STATE_DIMMING,
            self.STATE_BUG,
            self.STATE_RESTORE,
        )
