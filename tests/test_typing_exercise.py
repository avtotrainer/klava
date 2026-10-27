"""TypingExercise-ის არსებული ქცევის ტესტები რეალური GUI ფანჯრის გარეშე."""

from types import SimpleNamespace

from exercises.typing import TypingExercise


class FakeUI:
    """ინახავს სავარჯიშოს მიერ მოთხოვნილ ვიზუალურ ცვლილებებს."""

    def __init__(self):
        self.drawn = []
        self.marked = []
        self.cleared = 0

    def clear_sentence(self):
        self.cleared += 1

    def draw_sentence(self, letters):
        self.drawn = list(letters)

    def mark_letter(self, index):
        self.marked.append(index)


class FakeKeyboard:
    """ამოწმებს სამიზნესა და ფერად უკუკავშირს Tkinter-ის გარეშე."""

    def __init__(self):
        self.key_boxes = {"A": {}, "B": {}, " ": {}}
        self.targets = []
        self.correct = []
        self.wrong = []

    def set_target(self, key):
        self.targets.append(key)

    def highlight_correct(self, key):
        self.correct.append(key)

    def highlight_wrong(self, key):
        self.wrong.append(key)


def key(symbol):
    """ქმნის მხოლოდ იმ keysym ველს, რომელსაც სავარჯიშო კითხულობს."""
    return SimpleNamespace(keysym=symbol)


def test_exercise_advances_only_after_correct_keys():
    """არასწორი კლავიში არ ცვლის პოზიციას; სწორი ასრულებს სტრიქონს."""
    ui, keyboard = FakeUI(), FakeKeyboard()
    exercise = TypingExercise(ui, keyboard, "ab")
    exercise.start()

    assert ui.drawn == ["A", "B"]
    assert keyboard.targets == ["A"]
    assert exercise.finished is False

    exercise.on_key(key("b"))
    assert exercise.pos == 0
    assert keyboard.wrong == ["B"]

    exercise.on_key(key("a"))
    assert exercise.pos == 1
    assert ui.marked == [0]
    assert keyboard.correct == ["A"]

    exercise.on_key(key("b"))
    assert exercise.finished is True
    assert ui.marked == [0, 1]


def test_space_is_accepted_as_part_of_sentence():
    """SPACE სიმბოლო უნდა ჩაითვალოს ტექსტის ნაწილად და არა გამოტოვებად."""
    ui, keyboard = FakeUI(), FakeKeyboard()
    exercise = TypingExercise(ui, keyboard, "a b")
    exercise.start()

    exercise.on_key(key("a"))
    assert keyboard.targets[-1] == " "

    exercise.on_key(key("space"))
    assert exercise.pos == 2
    assert ui.marked == [0, 1]

    exercise.on_key(key("b"))
    assert exercise.finished is True


def test_stop_prevents_subsequent_key_processing():
    """სესიის შეჩერების შემდეგ კლავიშები არ უნდა დამუშავდეს."""
    ui, keyboard = FakeUI(), FakeKeyboard()
    exercise = TypingExercise(ui, keyboard, "ab")
    exercise.start()
    exercise.stop()

    exercise.on_key(key("a"))
    assert exercise.finished is True
    assert exercise.pos == 0
