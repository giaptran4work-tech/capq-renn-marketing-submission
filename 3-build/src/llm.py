"""Shared OpenRouter client setup.

Single source of truth for the model name, the API-key lookup, and the
actionable error message when the key is missing.

OpenRouter exposes an OpenAI-compatible API, so we use the standard `openai`
SDK pointed at OpenRouter's base URL.
"""

from __future__ import annotations

import os

from openai import OpenAI

# OpenRouter free model. The `:free` suffix marks zero-cost models that work
# regardless of region. Swap to another free model if this one is
# rate-limited or unavailable:
#   deepseek/deepseek-v4-flash:free
#   meta-llama/llama-3.3-70b-instruct:free
OPENROUTER_MODEL = "openai/gpt-oss-120b:free"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_client() -> OpenAI:
    """Return a configured OpenRouter client.

    Raises RuntimeError with an actionable message if OPENROUTER_API_KEY is unset.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your "
            "key from https://openrouter.ai/keys."
        )
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/giaptran4work-tech/cq-competitive-intel",
            "X-Title": "CQ Competitive Intel",
        },
    )
