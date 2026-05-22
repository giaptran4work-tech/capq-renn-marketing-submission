from src.diff import compute_diff
from src.models import Surface


def _surface():
    return Surface(url="https://example.com", type="homepage", competitor="Acme")


def test_no_baseline_returns_added_chunks():
    new = "## Para 1\n\nThis is paragraph one with enough text.\n\n## Para 2\n\nSecond paragraph here, also enough text."
    chunks = compute_diff(_surface(), old=None, new=new, id_prefix="s0")
    assert len(chunks) >= 1
    assert all(c.kind == "added" for c in chunks)
    assert all(c.competitor == "Acme" for c in chunks)


def test_identical_returns_empty():
    text = "Same text here, long enough to count.\n\nSecond block, also long enough."
    chunks = compute_diff(_surface(), old=text, new=text, id_prefix="s0")
    assert chunks == []


def test_added_paragraph_detected():
    old = "Block one is long enough to register.\n\nBlock two same here."
    new = old + "\n\nBlock three is also long enough now."
    chunks = compute_diff(_surface(), old=old, new=new, id_prefix="s0")
    assert any(c.kind == "added" and "three" in c.text for c in chunks)


def test_removed_paragraph_detected():
    old = "Block A is long.\n\nBlock B that goes away.\n\nBlock C that stays."
    new = "Block A is long.\n\nBlock C that stays."
    chunks = compute_diff(_surface(), old=old, new=new, id_prefix="s0")
    assert any(c.kind == "removed" and "B" in c.text for c in chunks)


def test_tiny_blocks_filtered_out():
    new = "tiny\n\nyo\n\nThis block here is long enough to register, more text more text."
    chunks = compute_diff(_surface(), old=None, new=new, id_prefix="s0")
    for c in chunks:
        assert "tiny" not in c.text
        assert "yo" not in c.text


def test_chunk_text_truncated_to_max():
    long_block = "x" * 5000
    new = f"Header that is long enough to register here.\n\n{long_block}"
    chunks = compute_diff(_surface(), old=None, new=new, id_prefix="s0")
    for c in chunks:
        assert len(c.text) <= 1501  # 1500 + ellipsis
