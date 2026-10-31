"""TypingEngine-ის არსებული ქცევის რეგრესიული ტესტები (UI-ის გარეშე)."""

import pytest

import logic.engine as engine_module
from logic.engine import TypingEngine


def test_blank_sentence_is_rejected():
    """სავარჯიშოს უნდა ჰქონდეს რეალური ტექსტი."""
    for sentence in ("", "   "):
        with pytest.raises(ValueError):
            TypingEngine(sentence)


def test_correct_keys_advance_and_complete():
    """სწორი სიმბოლო გადაადგილებს სამიზნეს და ასრულებს სტრიქონს."""
    engine = TypingEngine("AB")
    assert engine.total == 2
    assert engine.current_char() == "A"

    assert engine.hit("A") is True
    assert engine.current_char() == "B"
    assert engine.finished is False

    assert engine.hit("B") is True
    assert engine.finished is True
    assert engine.current_char() == ""
    assert engine.hit("B") is False


def test_wrong_key_does_not_advance():
    """ერთი არასწორი კლავიში არ უნდა ჩაითვალოს შესრულებად."""
    engine = TypingEngine("A")

    assert engine.hit("Z") is False
    assert engine.pos == 0
    assert engine.finished is False
    assert engine.current_char() == "A"


def test_wrong_streak_locks_until_reset(monkeypatch):
    """ზედიზედ შეცდომები ააქტიურებს არსებული guard-ის დაბლოკვას."""
    monkeypatch.setattr(engine_module.time, "monotonic", lambda: 100.0)
    engine = TypingEngine("A", wrong_streak_limit=3, sweep_required=99)

    for key in ("X", "Y", "Z"):
        assert engine.hit(key) is False

    assert engine.state == engine.STATE_DIMMING
    assert engine.is_locked() is True
    assert engine.hit("A") is False
    assert engine.pos == 0

    engine.reset_error_state()
    assert engine.is_locked() is False
    assert engine.hit("A") is True


def test_fast_wrong_keys_trigger_sweep_guard(monkeypatch):
    """მოკლე ინტერვალში ბევრი შეცდომა ააქტიურებს sweep guard-ს."""
    monkeypatch.setattr(engine_module.time, "monotonic", lambda: 100.0)
    engine = TypingEngine(
        "A",
        wrong_streak_limit=99,
        sweep_required=3,
        sweep_time_window=0.7,
    )

    for key in ("X", "Y", "Z"):
        assert engine.hit(key) is False

    assert engine.state == engine.STATE_DIMMING
    assert engine.pos == 0


def test_lock_releases_after_configured_duration(monkeypatch):
    """lock_duration-ის მითითებისას დაბლოკვა დროის გასვლის შემდეგ იხსნება."""
    clock = [100.0]
    monkeypatch.setattr(engine_module.time, "monotonic", lambda: clock[0])
    engine = TypingEngine("A", wrong_streak_limit=3, sweep_required=99, lock_duration=1.5)

    for key in ("X", "Y", "Z"):
        engine.hit(key)
    assert engine.is_locked() is True

    clock[0] += 1.4
    assert engine.is_locked() is True

    clock[0] += 0.2
    assert engine.is_locked() is False
    assert engine.hit("A") is True


def test_lock_without_duration_keeps_existing_behavior(monkeypatch):
    """ნაგულისხმევად (lock_duration=None) დაბლოკვა თავისით არ იხსნება."""
    clock = [100.0]
    monkeypatch.setattr(engine_module.time, "monotonic", lambda: clock[0])
    engine = TypingEngine("A", wrong_streak_limit=3, sweep_required=99)

    for key in ("X", "Y", "Z"):
        engine.hit(key)
    clock[0] += 3600
    assert engine.is_locked() is True


def test_key_history_is_bounded():
    """გრძელ სესიაზე შეცდომების ისტორია მეხსიერებას შეუზღუდავად არ ზრდის."""
    engine = TypingEngine("A" * 1000, sweep_required=8)
    for _ in range(1000):
        assert engine.hit("A") is True
    assert engine.finished is True
    assert len(engine._key_history) == 32
