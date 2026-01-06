# logic/progress.py
# KLAVA — Progress tracker


class Progress:
    """
    პროგრესის დათვლა პროცენტებში.
    UI არ იცის.
    """

    def __init__(self, total: int):
        self.total = total
        self.current = 0

    @property
    def percent(self) -> int:
        if self.total <= 0:
            return 0
        return int((self.current / self.total) * 100)

    def step(self):
        self.current += 1

    def reset(self, total: int):
        self.total = total
        self.current = 0
