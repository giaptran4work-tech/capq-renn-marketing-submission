# Folder Structure Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the phase-based folder structure for the Renn Labs Task 1 AI marketing workflow demo, with starter README/template files in every folder so the user can start filling in content immediately.

**Architecture:** A flat phase-based layout (`1-discovery/` through `5-submission/` + shared `assets/`) at the project root. Each phase folder gets template `.md` files with section headings so the user is never staring at an empty file. `3-build/` carries its own `README.md` so the prototype can be handed off independently. Empty subdirectories get `.gitkeep` files so git tracks them.

**Tech Stack:** Filesystem only. PowerShell on Windows for directory creation; the Write tool for file contents. No code, no dependencies.

**Notes on TDD applicability:** This is a scaffolding task, not code. There is nothing to assert programmatically. Verification = visual inspection via `tree` / `Get-ChildItem -Recurse`. Each task ends with a verify step and a commit.

---

## File Structure

After this plan runs, the project will contain:

```
Tet/
├── README.md
├── brief.md
├── .gitignore                 (already exists)
├── docs/superpowers/specs/    (already exists)
├── docs/superpowers/plans/    (already exists)
│
├── 1-discovery/
│   ├── company.md
│   ├── pain-points.md
│   └── use-case.md
├── 2-design/
│   ├── workflow.md
│   └── tools-comparison.md
├── 3-build/
│   ├── README.md
│   ├── .env.example
│   ├── prompts/.gitkeep
│   ├── src/.gitkeep
│   └── config/.gitkeep
├── 4-demo/
│   ├── walkthrough.md
│   ├── recording-link.md
│   ├── inputs/.gitkeep
│   └── outputs/.gitkeep
├── 5-submission/
│   ├── writeup.md
│   └── links.md
└── assets/.gitkeep
```

---

## Task 1: Create phase folders and `.gitkeep` placeholders

**Files:**
- Create: 6 directories + 7 `.gitkeep` files

- [ ] **Step 1: Create all phase directories**

Run (PowerShell, from project root):

```powershell
New-Item -ItemType Directory -Force -Path 1-discovery, 2-design, 3-build, 3-build/prompts, 3-build/src, 3-build/config, 4-demo, 4-demo/inputs, 4-demo/outputs, 5-submission, assets | Out-Null
```

Expected: 11 directories created (or already exist — `-Force` is idempotent).

- [ ] **Step 2: Verify directory structure**

Run:

```powershell
Get-ChildItem -Directory | Select-Object Name
```

Expected output includes: `1-discovery`, `2-design`, `3-build`, `4-demo`, `5-submission`, `assets`, plus existing `docs` and `.claude`.

- [ ] **Step 3: Create `.gitkeep` files in empty subdirectories**

Use the Write tool to create each of these empty files (only the folders that will stay empty after this plan completes):

- `3-build/prompts/.gitkeep` (content: empty)
- `3-build/src/.gitkeep` (content: empty)
- `3-build/config/.gitkeep` (content: empty)
- `4-demo/inputs/.gitkeep` (content: empty)
- `4-demo/outputs/.gitkeep` (content: empty)
- `assets/.gitkeep` (content: empty)

- [ ] **Step 4: Verify `.gitkeep` placement**

Run:

```powershell
Get-ChildItem -Recurse -Filter .gitkeep | Select-Object FullName
```

Expected: 6 `.gitkeep` files listed under the paths above.

- [ ] **Step 5: Commit**

```powershell
git add 1-discovery 2-design 3-build 4-demo 5-submission assets
git commit -m "chore: scaffold phase folders for Task 1 workflow demo"
```

---

## Task 2: Create root-level entry files (`README.md`, `brief.md`)

**Files:**
- Create: `README.md`
- Create: `brief.md`

- [ ] **Step 1: Write root `README.md`**

Use the Write tool to create `README.md` with this exact content:

````markdown
# Renn Labs — Task 1: AI Marketing Workflow Demo

> Working demo of one AI marketing workflow built for the Renn Labs 72-hour marketing challenge.

**Target company:** _TBD — choose capq.ai or karbonhq.com_
**Workflow format:** _TBD — prompt chain / custom GPT / Zapier_

## One-click demo

- **Live product:** _link goes here once deployed/published_
- **Walkthrough video:** _Loom or screen recording link_
- **Full submission write-up:** [`5-submission/writeup.md`](5-submission/writeup.md)
- **All working links:** [`5-submission/links.md`](5-submission/links.md)

## What's in this repo

| Folder | What it is |
|---|---|
| [`1-discovery/`](1-discovery/) | Company research, observed pain points, chosen use case |
| [`2-design/`](2-design/) | Workflow design + tool comparison |
| [`3-build/`](3-build/) | The actual built workflow — has its own [README](3-build/README.md) |
| [`4-demo/`](4-demo/) | Sample inputs, outputs, walkthrough, recording |
| [`5-submission/`](5-submission/) | Final write-up + every working link |
| `assets/` | Shared screenshots and diagrams |
| [`brief.md`](brief.md) | Original challenge brief |
| [`docs/`](docs/) | Design spec and implementation plan |

## Status

- [ ] Company chosen
- [ ] Use case decided
- [ ] Workflow designed
- [ ] Prototype built
- [ ] Demo recorded
- [ ] Submission finalized
````

- [ ] **Step 2: Write `brief.md`**

Use the Write tool to create `brief.md` with this content:

```markdown
# Renn Labs — Marketing Challenge Brief

> Original brief as received. This is the source of truth for what the deliverable must cover.

## Overview

Renn Labs is looking for someone who can blend strategic thinking with hands-on execution, particularly around leveraging AI and modern marketing tools. The challenge values quality thinking over quantity of output.

**Company choice (pick one):**

- **capq.ai** — Renn Labs' portfolio company, AI-powered capital markets intelligence.
- **karbonhq.com** — practice management platform for accounting firms (no affiliation; selected purely for assessment).

Spend 30–60 minutes getting to know the chosen platform — explore the website, understand features, analyze current marketing.

## Task 1 — AI in Marketing Operations

Demonstrate true AI proficiency in marketing operations (not another ChatGPT content calendar). Show AI as a force multiplier across the entire marketing function.

- Show **three different workflows** where AI creates real leverage (e.g. lead scoring, competitive intelligence, customer research, personalization engines, data analysis).
- Be specific about which tools and flows, and why over alternatives.
- **Optional:** build a working demo of one workflow — Zapier automation, custom GPT, prompt chain, or similar.

## Task 2 — SEO (depth over breadth)

- Audit the chosen company's web presence — technical issues, content gaps, backlinks, competitive disadvantages.
- Pick just **one or two** most critical issues. Explain prioritization (impact vs effort).
- Provide a **detailed fix plan** for the top priority: implementation steps, tools needed, timeline, expected impact on rankings and traffic.

## Task 3 — Growth Hacking with Substance

- Design a growth mechanism that could realistically generate **30+ qualified leads in 2 weeks**, with **zero advertising budget**.
- Build a **prototype or MVP** — landing page, automation sequence, interactive tool/calculator, community activation, etc.
- Include hypothesis, complete launch plan, success metrics, scaling approach.

## Submission

- Free choice of format: PDF, video walkthrough, Notion page, website, Loom, interactive demo — or any combination.
- No length restrictions, but respect reviewer's time.
- Include working links — anything you build must be functional, even if basic.
- 72 hours from receipt to submit.

## Evaluation Criteria

- AI mastery (sophisticated, not just basic prompt writing)
- Analytical depth and prioritization
- Execution ability via prototypes
- Strategic thinking, business impact, ROI
- Clarity of articulation

You may be asked to present and discuss your submission live, so be able to speak to every aspect.
```

- [ ] **Step 3: Verify root files exist and are non-empty**

Run:

```powershell
Get-ChildItem README.md, brief.md | Select-Object Name, Length
```

Expected: both files listed with `Length` > 0.

- [ ] **Step 4: Commit**

```powershell
git add README.md brief.md
git commit -m "docs: add root README and original challenge brief"
```

---

## Task 3: Create starter files for `1-discovery/` and `2-design/`

**Files:**
- Create: `1-discovery/company.md`
- Create: `1-discovery/pain-points.md`
- Create: `1-discovery/use-case.md`
- Create: `2-design/workflow.md`
- Create: `2-design/tools-comparison.md`

- [ ] **Step 1: Write `1-discovery/company.md`**

```markdown
# Company Research — [capq.ai | karbonhq.com]

> Spend 30–60 minutes on the site. Capture observations here.

## Product

- What does it do?
- Who is it for?

## Target audience / ICP

- Industry, size, role of buyer
- Where do they live online?

## Current marketing surface

- Website structure & key pages
- Content (blog, case studies, gated assets)
- SEO posture (rough impression)
- Paid presence
- Social / community

## Voice & positioning

- How do they sound? (formal, technical, founder-led, etc.)
- Differentiators they claim

## Notes / quotes / screenshots

(Drop links to `assets/` for screenshots.)
```

- [ ] **Step 2: Write `1-discovery/pain-points.md`**

```markdown
# Marketing Pain Points (Observed)

> What is this company's marketing not doing that it should? What is it doing inefficiently?

## Top observed gaps

1.
2.
3.

## Where AI could create leverage

- Lead scoring:
- Competitive intelligence:
- Customer research:
- Personalization:
- Data analysis:

## Constraints / context

(Anything that limits what would actually work for them — team size, budget signals, regulatory constraints.)
```

- [ ] **Step 3: Write `1-discovery/use-case.md`**

```markdown
# Chosen Use Case for the Workflow Demo

## The workflow I will build

**One sentence:** _e.g. "Automated competitive intel digest that scans 5 competitor sites weekly and produces a 1-page brief for the marketing lead."_

## Why this use case

- The pain it solves (link to `pain-points.md`)
- Why AI specifically (vs. a manual or simpler-automation alternative)
- Expected impact / leverage

## Why NOT the others

Brief rationale for rejecting the other 2 workflow candidates (the ones that go in the "3 workflows" write-up but aren't built).

## Success criteria for the demo

How will the assessor know it works? What does a successful run produce?
```

- [ ] **Step 4: Write `2-design/workflow.md`**

```markdown
# Workflow Design

## Inputs

- Source(s):
- Format:
- Frequency / trigger:

## Steps

1. **Step 1 — [name]:** what happens, which tool/prompt, expected output.
2. **Step 2 — [name]:**
3. **Step 3 — [name]:**

(Diagram lives in `assets/` — link from here.)

## Outputs

- What the workflow produces
- Where it goes (file, email, Slack, Notion, etc.)

## Failure modes

- What can go wrong?
- How does the workflow handle it (retry, fallback, human-in-the-loop)?

## Cost / performance estimate

- Approx tokens / API calls per run
- Approx runtime
- Approx $ per run
```

- [ ] **Step 5: Write `2-design/tools-comparison.md`**

```markdown
# Tool & Approach Comparison

> The brief asks: "why these tools over alternatives." This is where that lives.

## Tool selected

**Tool:** _e.g. n8n + GPT-4o-mini_

**Why:**

- Strength 1
- Strength 2
- Strength 3

## Alternatives considered

| Alternative | Pros | Cons | Why rejected |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

## Model choice

- Model used:
- Why this model (capability vs cost vs latency tradeoff):
- Fallback if it fails:
```

- [ ] **Step 6: Verify and commit**

Run:

```powershell
Get-ChildItem 1-discovery, 2-design -File | Select-Object FullName, Length
```

Expected: 5 files listed, all non-empty.

```powershell
git add 1-discovery 2-design
git commit -m "docs: add discovery and design phase templates"
```

---

## Task 4: Create starter files for `3-build/` (prototype workspace)

**Files:**
- Create: `3-build/README.md`
- Create: `3-build/.env.example`

- [ ] **Step 1: Write `3-build/README.md`**

````markdown
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
````

- [ ] **Step 2: Write `3-build/.env.example`**

```dotenv
# Copy this file to .env and fill in real values.
# .env is gitignored — never commit real keys.

# LLM provider (pick whichever you use)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Optional: web search / scraping
SERPAPI_API_KEY=
FIRECRAWL_API_KEY=

# Optional: integrations
NOTION_TOKEN=
SLACK_WEBHOOK_URL=
```

- [ ] **Step 3: Verify and commit**

Run:

```powershell
Get-ChildItem 3-build -File -Force | Select-Object Name, Length
```

Expected: `README.md` and `.env.example` listed, non-empty.

```powershell
git add 3-build/README.md 3-build/.env.example
git commit -m "docs: add build phase README and .env.example"
```

---

## Task 5: Create starter files for `4-demo/` and `5-submission/`

**Files:**
- Create: `4-demo/walkthrough.md`
- Create: `4-demo/recording-link.md`
- Create: `5-submission/writeup.md`
- Create: `5-submission/links.md`

- [ ] **Step 1: Write `4-demo/walkthrough.md`**

```markdown
# Demo Walkthrough

> Step-by-step of what the assessor sees when they run / view the demo. Pair this with the recording.

## Prerequisites

What the assessor needs (or doesn't) before clicking the link.

## Step-by-step

1. **Open:** _link to live demo_
2. **Action:** _what to click / type_
3. **Observe:** _what the assessor will see — paste expected output or screenshot from `assets/`_
4. **Action:**
5. **Observe:**

## What "working" looks like

The output shown in `outputs/` is what a successful run produces. Compare against `inputs/` for the matching input.

## If something breaks

Quick troubleshooting notes (rate-limit hit, key missing, etc.).
```

- [ ] **Step 2: Write `4-demo/recording-link.md`**

```markdown
# Recording

**Loom / video URL:** _paste here once recorded_

**Length:** _e.g. 3 min 42 sec_

**What it covers:**

- 0:00 — Intro: the use case and why it matters
- 0:30 — Workflow overview (diagram)
- 1:00 — Live run, input → output
- 2:30 — Quick tour of the code/config
- 3:15 — Wrap-up: cost, scaling, next steps

> Required for Zapier/Make workflows since the assessor can't run those directly.
```

- [ ] **Step 3: Write `5-submission/writeup.md`**

```markdown
# Submission — Task 1: AI in Marketing Operations

**Company chosen:** _capq.ai | karbonhq.com_

## Three AI workflows for [company]

### Workflow 1 — [name]

- **The leverage:** what this saves / unlocks
- **Tools:** [tool] for [reason]; chosen over [alternative] because [reason]
- **Flow:** brief 3–5 line description of how it runs

### Workflow 2 — [name]

(same structure)

### Workflow 3 — [name]

(same structure)

## Built demo — [name of the one I built]

- **Why this one of the three:** rationale
- **Live demo:** [link]
- **Walkthrough video:** [link]
- **Source / repo:** [link]
- **What it does:** 2–3 sentences
- **Result from a real run:** screenshot or sample output

## How I'd extend this

- Next workflow to build
- How these workflows compose into a fuller marketing-ops stack
- Estimated impact at company scale

## Notes for the live interview

(Private — talking points to be ready for.)
```

- [ ] **Step 4: Write `5-submission/links.md`**

```markdown
# All Working Links

> Single source of truth. Every link the assessor needs to experience the submission firsthand.

## Primary

- **This repo:** _GitHub URL_
- **Live demo / hosted product:** _URL_
- **Walkthrough video:** _Loom URL_
- **Submission write-up:** [`5-submission/writeup.md`](writeup.md)

## Supporting

- **Workflow diagram:** _link to image in `assets/`_
- **Sample input → output:** `4-demo/inputs/` + `4-demo/outputs/`
- **Original brief:** [`brief.md`](../brief.md)
- **Design spec:** [`docs/superpowers/specs/2026-05-20-folder-structure-design.md`](../docs/superpowers/specs/2026-05-20-folder-structure-design.md)

## Credentials note

If any link requires login or a key, instructions are in the relevant phase's README.
```

- [ ] **Step 5: Verify and commit**

Run:

```powershell
Get-ChildItem 4-demo, 5-submission -File | Select-Object FullName, Length
```

Expected: 4 files listed, all non-empty.

```powershell
git add 4-demo 5-submission
git commit -m "docs: add demo and submission phase templates"
```

---

## Task 6: Final verification

- [ ] **Step 1: Print the full tree**

Run:

```powershell
Get-ChildItem -Recurse -Force -Exclude .git, .claude, node_modules, .venv | Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.FullName -notmatch '\\\.claude\\' } | Select-Object FullName
```

Expected: All directories and files listed under the `File Structure` block at the top of this plan.

- [ ] **Step 2: Sanity-check that the README links resolve**

Open `README.md` in a previewer (VS Code's markdown preview, or push to GitHub). Click each linked path. Each should resolve to an existing file or folder.

- [ ] **Step 3: Verify git is clean**

Run:

```powershell
git status
```

Expected: `nothing to commit, working tree clean`.

- [ ] **Step 4: Print recent commits**

Run:

```powershell
git log --oneline -n 10
```

Expected: ~5 new commits from this plan, plus the prior spec commit and initial commit.

---

## Out of Scope

- Choosing the target company (capq.ai vs karbonhq.com) — content decision, not structure.
- Picking the workflow format — content decision.
- Writing actual workflow code or prompts — that's the next plan, after the user decides on use case + tool.
- Setting up git user identity — user must do this manually (see spec).
