# Project Instructions for Claude

## Read this first, every session

Before doing anything else, read [`PROGRESS.md`](PROGRESS.md) — it is the single source of truth for what phase the work is in and what's next. Each session starts with no memory of the previous chat; `PROGRESS.md` is how that gap is closed. Keep it updated as work lands.

## How I work best

- **I'm a visual learner.** Use ASCII diagrams for anything with steps, data flow, or branching decisions. A pipeline drawn as boxes and arrows is easier for me than a bulleted description.
- **Simple wording.** Use plain language. "Compares paragraph by paragraph" beats "uses difflib SequenceMatcher on paragraph blocks". Reserve technical terms for places where the term itself is the point.
- **Visual-first in design docs.** Not just in chat — `workflow.md`, `tools-comparison.md`, and any future design doc should lead with a visual and explain underneath.

## Minimize popup questions

Default to making the reasonable call and narrating in one sentence. Reserve `AskUserQuestion` popups for rare, genuinely consequential choices where my read of intent is unreadable. Auto mode means "drive efficiently," not "popup heavily."

## Phase-review framework

For any meaningful phase of work (discovery, design, build, write-up):

1. State the **desired outcome** before producing the work — what does success look like, what will I do with the output.
2. List **blockers** — what could prevent that outcome.
3. State **principles** that overcome each blocker.
4. **Stop at every phase boundary** for me to review. Even in auto-mode. Auto-mode means "don't ask trivial clarifying questions"; it does **not** mean "skip review gates on evaluated deliverables."

## Submission spec for this project

The locked submission target is documented in [`5-submission/submission-spec.md`](5-submission/submission-spec.md):

- **Format:** Single PDF slide deck, 11 slides, self-explanatory (no presenter)
- **Tool choices separated per workflow** — not a combined table
- **Slides must show reasoning, not just conclusions** — surface what was rejected and why for every tool choice

## Lessons learned for this project

Tracked in [`lessons/`](lessons/). Each lesson uses the format: desired outcome / blockers / principles.

## Working directory note

This project lives on a Windows path with a Vietnamese-named folder (`Máy tính`). Always use absolute paths in tools to avoid quoting issues.
