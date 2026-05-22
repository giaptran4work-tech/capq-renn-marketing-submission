from pathlib import Path

import pytest

from src import storage


@pytest.fixture(autouse=True)
def _temp_snapshot_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "SNAPSHOT_DIR", tmp_path)
    yield


def test_load_returns_none_when_no_snapshot():
    assert storage.load_snapshot("https://example.com/nothing") is None


def test_save_then_load_roundtrip():
    url = "https://example.com/page"
    content = "# Hello\n\nWorld"
    storage.save_snapshot(url, content)
    assert storage.load_snapshot(url) == content


def test_save_overwrites_existing():
    url = "https://example.com/page"
    storage.save_snapshot(url, "old")
    storage.save_snapshot(url, "new")
    assert storage.load_snapshot(url) == "new"


def test_different_urls_dont_collide():
    storage.save_snapshot("https://a.com", "alpha")
    storage.save_snapshot("https://b.com", "beta")
    assert storage.load_snapshot("https://a.com") == "alpha"
    assert storage.load_snapshot("https://b.com") == "beta"
