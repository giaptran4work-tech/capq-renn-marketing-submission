"""Shared Gemini client setup.

Single source of truth for the model name, the API-key lookup, and the
actionable error message when the key is missing.
"""

from __future__ import annotations

import os

from google import genai

GEMINI_MODEL = "gemini-2.5-flash"


def get_client() -> genai.Client:
    """Return a configured Gemini client.

    Raises RuntimeError with an actionable message if GOOGLE_API_KEY is unset.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key "
            "from https://aistudio.google.com."
        )
    return genai.Client(api_key=api_key)
