# logic/engine.py


class TypingEngine:
    """
    ბეჭვდის ლოგიკის ძრავა.
    UI-ს არაფერი ესმის.
    ზუსტად იმეორებს საბაზო Trainer-ის ქცევას.
    """

    def __init__(self, source: str):
        """
        ინიციალიზაცია.

        :param source: sentences.txt-ის ფაილის მისამართი
        """
        self.sentences = self._load_sentences(source)
        self.sentence_idx = 0

        self._load_current_sentence()

        self.score = 0

    # --------------------------------------------------
    #   LOAD
    # --------------------------------------------------
    def _load_sentences(self, path: str) -> list[str]:
        """
        კითხულობს წინადადებებს ფაილიდან.
        """
        try:
            with open(path, encoding="utf-8") as f:
                lines = [l.strip().upper() for l in f if l.strip()]
                return lines if lines else ["HELLO WORLD"]
        except Exception:
            return ["HELLO WORLD"]

    def _load_current_sentence(self) -> None:
        """
        ტვირთავს მიმდინარე წინადადებას.
        """
        self.letters = list(self.sentences[self.sentence_idx])
        self.pos = 0
        self.total = len(self.letters)

    # --------------------------------------------------
    #   API EXPECTED BY Trainer
    # --------------------------------------------------
    def acceptable(self, ch: str) -> bool:
        """
        ამოწმებს არის თუ არა სიმბოლო დასაშვები.
        """
        return ch in self.letters or ch == " "

    def current(self) -> str | None:
        """
        აბრუნებს მიმდინარე მიზნობრივ სიმბოლოს.
        """
        if self.pos >= self.total:
            return None
        return self.letters[self.pos]

    def hit(self, ch: str) -> bool:
        """
        ამუშავებს ერთ დაჭერას საბაზოს წესებით.

        სწორი  → +1 ქულა, pos++
        არასწორი → -3 ქულა
        """
        target = self.current()
        if target is None:
            return False

        if ch == target:
            self.score += 1
            self.pos += 1

            # თუ ხაზი დასრულდა — გადავდივართ შემდეგზე
            if self.pos >= self.total:
                self._advance_sentence()

            return True

        self.score -= 3
        return False

    def _advance_sentence(self) -> None:
        """
        გადადის შემდეგ წინადადებაზე, თუ არსებობს.
        """
        if self.sentence_idx + 1 < len(self.sentences):
            self.sentence_idx += 1
            self._load_current_sentence()

    @property
    def finished(self) -> bool:
        """
        დასრულებულია თუ არა მთელი დავალება.

        დასრულებულია მხოლოდ მაშინ, როცა
        ბოლო წინადადებაც ბოლომდეა აკრეფილი.
        """
        return self.sentence_idx == len(self.sentences) - 1 and self.pos >= self.total
