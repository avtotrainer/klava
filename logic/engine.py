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
    """

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
