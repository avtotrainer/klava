# exercises/base.py
# KLAVA — Exercise Base Interface


class Exercise:
    """
    სავარჯიშოს საბაზო კონტრაქტი.

    Trainer იცნობს მხოლოდ ამ კლასის მეთოდებს.
    კონკრეტულ სავარჯიშოს არ აქვს უფლება:
    - მართოს root
    - იცოდეს kiosk რეჟიმის არსებობა
    - იმუშაოს menu-სთან
    """

    def start(self):
        """
        სავარჯიშოს დაწყება.
        აქ ხდება UI-ის ინიციალიზაცია.
        """
        raise NotImplementedError("start() არ არის იმპლემენტირებული")

    def stop(self):
        """
        სავარჯიშოს იძულებითი დასრულება.
        გამოიყენება secret key-ით.
        """
        raise NotImplementedError("stop() არ არის იმპლემენტირებული")

    def on_key(self, event):
        """
        კლავიატურის event-ის დამუშავება.
        Trainer პირდაპირ გადასცემს event-ს.
        """
        raise NotImplementedError("on_key() არ არის იმპლემენტირებული")

    @property
    def finished(self) -> bool:
        """
        აბრუნებს True-ს თუ სავარჯიშო დასრულებულია.
        Trainer ამას ამოწმებს ყოველ კლავიშზე.
        """
        raise NotImplementedError("finished property არ არის იმპლემენტირებული")
