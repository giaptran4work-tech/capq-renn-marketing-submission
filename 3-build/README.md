# Workflow Prototype

> The actual built workflow. This README must be enough for a reviewer (or future-you) to run/view the demo on its own.

## What it does

_One paragraph — what goes in, what comes out, who it's for._

## Stack

- **Format:** _prompt chain / custom GPT / Zapier / n8n_
- **Model:** _e.g. GPT-4o-mini / Claude Sonnet 4.6_
- **Orchestration:** _Python script / n8n flow / Zapier zap_
- **Other tools:** _e.g. SerpAPI, Firecrawl_

## How to run / view

### Option A — One-click hosted demo

_Live URL:_

### Option B — Run locally

```bash
# example only — replace with the real instructions
pip install -r requirements.txt
cp .env.example .env   # fill in keys
python src/run.py --input examples/sample.json
```

## Files in this folder

| Path | What it is |
|---|---|
| `prompts/` | Prompt files used by the workflow, one per step |
| `config/` | Workflow config — GPT instructions, Zapier export JSON, n8n workflow.json |
| `src/` | Code (delete this folder if the workflow is fully no-code) |
| `.env.example` | Required environment variables |

## Required API keys

See `.env.example`. Get keys from:

- OpenAI:
- (other providers as needed)
