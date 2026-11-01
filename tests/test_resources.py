"""არსებული კონფიგურაციისა და რესურსების ფაილების წაკითხვის ტესტები."""

from pathlib import Path

import pytest

from logic.config import Config
from logic.resources import Resources


def test_config_loads_existing_training_limit():
    """MIN_LINES-ის აქტიური კონფიგურაცია არ უნდა დაიკარგოს."""
    config = Config()

    assert config.getint("training", "min_lines") == 2
    assert config.get("app", "language") == "ka"


def test_config_reports_missing_file():
    """არარსებული კონფიგურაცია უნდა ჩაითვალოს გამოკვეთილ შეცდომად."""
    with pytest.raises(FileNotFoundError):
        Config(path="this-config-file-must-not-exist.ini")


def test_resources_load_existing_language_and_keyboard():
    """ქართული ტექსტები და კლავიატურის მოდელი იკითხება GUI-ის გარეშე."""
    root = Path(__file__).resolve().parents[1]
    resources = Resources(
        base_dir=str(root / "resources"),
        language="ka",
        theme_name="default",
    )

    assert resources.texts.sections()
    assert resources.text("app", "title")
    assert resources.keyboard_model["groups"]
    assert resources.keyboard_model["colors"]


def test_resources_reject_missing_language():
    """არარსებული ლოკალიზაციის ფაილი არ უნდა ჩაიტვირთოს ჩუმად."""
    root = Path(__file__).resolve().parents[1]
    with pytest.raises(FileNotFoundError):
        Resources(
            base_dir=str(root / "resources"),
            language="nonexistent-language",
            theme_name="default",
        )


def test_keyboard_colors_must_be_six_digit_hex(tmp_path):
    """Keyboard._lighten() მხოლოდ #rrggbb-ს ითვლის; სხვა ფორმატი ადრევე უარიყოფა."""
    import json
    import shutil

    root = Path(__file__).resolve().parents[1]
    base = tmp_path / "resources"
    shutil.copytree(root / "resources", base)
    model_path = base / "keyboard" / "fingers.json"
    model = json.loads(model_path.read_text(encoding="utf-8"))
    model["colors"]["left_pinky"] = "red"
    model_path.write_text(json.dumps(model), encoding="utf-8")
    with pytest.raises(ValueError, match="left_pinky"):
        Resources(base_dir=str(base), language="ka", theme_name="default")
