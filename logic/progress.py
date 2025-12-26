# logic/progress.py
# KLAVA — Progress tracker


class Progress:
    """
    პროგრესის დათვლა პროცენტებში.
    """

    def __init__(self, total: int):
        self.total = total
        self.current = 0

    @property
    def percent(self) -> int:
        """
        პროგრესი პროცენტებში.
        """
        if self.total <= 0:
            return 0
        return int((self.current / self.total) * 100)

    def step(self):
        """
        ერთი სწორი სიმბოლოს დათვლა.
        """
        self.current += 1

    def reset(self, total: int):
        """
        ახალი დავალებისთვის განულება.
        """
        self.total = total
        self.current = 0
