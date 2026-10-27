"""Progress-ის პროცენტული დათვლის ქცევითი ტესტები."""


from logic.progress import Progress


def test_progress_counts_correct_steps():
    """პროგრესი იზრდება მხოლოდ step() გამოძახების შემდეგ."""
    progress = Progress(total=4)
    assert progress.percent == 0

    progress.step()
    assert progress.percent == 25

    progress.step()
    assert progress.percent == 50


def test_progress_reset_starts_new_exercise():
    """ახალი სავარჯიშო ანულებს წინა პროგრესს."""
    progress = Progress(total=3)
    progress.step()
    progress.reset(total=2)

    assert progress.percent == 0
    progress.step()
    assert progress.percent == 50


def test_zero_total_returns_zero_percent():
    """ნულოვანი მოცულობის შემთხვევაში ნულზე გაყოფა არ ხდება."""
    progress = Progress(total=0)
    assert progress.percent == 0
    progress.step()
    assert progress.percent == 0
