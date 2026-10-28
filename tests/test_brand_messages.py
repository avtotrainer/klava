"""Localized messages must render line breaks without touching training logic."""

from logic.resources import Resources


def test_translated_newlines():
    resources = Resources("resources", "ka", "default")
    assert resources.text("cover", "welcome").count("\n") == 2
    assert r"\n" not in resources.text("cover", "welcome")
    assert "\n" in resources.text("dialogs", "about_text")


def test_missing_key_fallback_preserves_literal_newline():
    resources = Resources("resources", "en", "default")
    assert resources.text("missing", "key", "one\\ntwo") == "one\ntwo"
