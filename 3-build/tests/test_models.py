from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.models import (
    Classification,
    DiffChunk,
    FetchResult,
    SignificantChange,
    Surface,
)


def test_surface_basic():
    s = Surface(url="https://example.com", type="homepage", competitor="Acme")
    assert s.url == "https://example.com"
    assert s.type == "homepage"
    assert s.competitor == "Acme"


def test_surface_rejects_bad_type():
    with pytest.raises(ValidationError):
        Surface(url="https://x.com", type="totally-not-a-type", competitor="Acme")


def test_fetch_result_default_status_is_ok():
    s = Surface(url="https://x.com", type="homepage", competitor="A")
    r = FetchResult(surface=s, content_md="hello", fetched_at=datetime.now(timezone.utc))
    assert r.status == "ok"
    assert r.error is None


def test_classification_significance_must_be_1_to_5():
    Classification(id="x", change_type="noise", significance=1, reason="ok")
    Classification(id="x", change_type="noise", significance=5, reason="ok")
    with pytest.raises(ValidationError):
        Classification(id="x", change_type="noise", significance=0, reason="bad")
    with pytest.raises(ValidationError):
        Classification(id="x", change_type="noise", significance=6, reason="bad")


def test_diff_chunk_basic():
    c = DiffChunk(
        id="ch_1",
        competitor="Acme",
        url="https://acme.com",
        surface_type="pricing",
        kind="added",
        text="Free tier now $99/mo",
    )
    assert c.id == "ch_1"
    assert c.kind == "added"


def test_significant_change_basic():
    sc = SignificantChange(
        competitor="Acme",
        url="https://acme.com",
        surface_type="pricing",
        change_type="pricing_move",
        significance=5,
        reason="big",
        text="Free tier $99",
    )
    assert sc.significance == 5
