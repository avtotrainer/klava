"""Read-only Markdown link audit regression tests."""

from pathlib import Path

from scripts.check_resource_links import find_broken_local_links


def test_local_target_is_resolved_relative_to_parent(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "target.md").write_text("# target", encoding="utf-8")
    page = tmp_path / "README.md"
    page.write_text("[works](docs/target.md)\n", encoding="utf-8")
    assert find_broken_local_links(page) == []


def test_reports_missing_target(tmp_path: Path):
    page = tmp_path / "README.md"
    page.write_text("[broken](missing.md)\n", encoding="utf-8")
    assert find_broken_local_links(page) == [
        f"{page}: missing local link missing.md"
    ]


def test_does_not_claim_external_links_were_checked(tmp_path: Path):
    page = tmp_path / "README.md"
    page.write_text(
        "[web](https://example.com) [anchor](#section) "
        "![image](missing.png) [email](mailto:a@example.com)",
        encoding="utf-8",
    )
    assert find_broken_local_links(page) == []
