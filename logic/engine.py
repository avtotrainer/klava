# logic/engine.py
# KLAVA — Typing logic engine


class TypingEngine:
    """
    ბეჭდვის ლოგიკა.
    UI არაფერი იცის.
    """

    def __init__(self, path: str):
        """
        წინადადებების ჩატვირთვა ფაილიდან.
        """
        try:
            with open(path, encoding="utf-8") as f:
                self.sentences = [line.strip().upper() for line in f if line.strip()]
        except FileNotFoundError:
            self.sentences = ["HELLO WORLD"]

        self.index = 0
        self._load_current_sentence()

    # --------------------------------------------------
    # შიდა ჩატვირთვა
    # --------------------------------------------------
    def _load_current_sentence(self):
        """
        იტვირთავს მიმდინარე წინადადებას index-ის მიხედვით.
        """
        self.current_sentence = self.sentences[self.index]
        self.letters = list(self.current_sentence)
        self.pos = 0
        self.finished = False

    # --------------------------------------------------
    # API
    # --------------------------------------------------
    @property
    def total(self) -> int:
        """
        მიმდინარე წინადადების სიგრძე.
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

    # ბექვორდ-კომპატიბილითი Trainer-ისთვის
    def current(self) -> str:
        return self.current_char()

    def hit(self, ch: str) -> bool:
        """
        სიმბოლოზე დაჭერის დამუშავება.
        """
        if self.finished:
            return False

        if ch != self.letters[self.pos]:
            return False

        self.pos += 1

        if self.pos >= len(self.letters):
            self.finished = True

        return True

    def next_sentence(self) -> bool:
        """
        შემდეგ წინადადებაზე გადასვლა.
        """
        self.index += 1
        if self.index >= len(self.sentences):
            return False

        self._load_current_sentence()
        return True
