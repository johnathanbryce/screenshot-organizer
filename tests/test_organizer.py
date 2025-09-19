from pathlib import Path
from datetime import datetime
from screenshot_organizer import create_folder_structure, create_daily_directory


def test_create_folder_structure(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    daily_dir = create_folder_structure()
    assert daily_dir.exists()
    assert daily_dir.parent == tmp_path / "screenshots"
    assert daily_dir.name


def test_create_daily_directory(tmp_path):
    screenshots_dir = tmp_path / "screenshots"
    screenshots_dir.mkdir()
    test_daily_dir = create_daily_directory(screenshots_dir)
    assert test_daily_dir.exists()
    expected = datetime.now().strftime("%d %B %Y")
    assert test_daily_dir.name == expected
