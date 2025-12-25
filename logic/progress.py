class Progress:
    """
    პროგრესის ლოგიკა.
    ინახავს მიმდინარე ნაბიჯს და ითვლის პროცენტს.
    """

    def __init__(self, total: int):
        self.total = total
        self.current = 0

    def step(self) -> None:
        """ზრდის პროგრესს ერთით"""
        if self.current < self.total:
            self.current += 1

    @property
    def percent(self) -> int:
        """აბრუნებს პროგრესს პროცენტებში"""
        if self.total == 0:
            return 0
        return int((self.current / self.total) * 100)
