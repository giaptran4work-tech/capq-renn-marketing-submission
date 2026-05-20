# Folder Structure Design — Renn Labs Task 1 Workflow Demo

**Date:** 2026-05-20
**Scope:** Folder layout for building one AI marketing workflow demo (Task 1 of the Renn Labs 72-hour challenge).

## Context

This is a single-task scratch project, not a long-lived codebase. The work is a 72-hour sprint to produce:

- Research on the chosen company (capq.ai or karbonhq.com — not yet decided)
- A working AI workflow demo (format TBD: prompt chain, custom GPT, or Zapier/Make automation)
- A submission write-up with working links

The folder structure must be flexible enough to host any workflow format without rework, and clear enough that a reviewer can navigate the deliverable without a tour.

## Goals

- Make progress visible at a glance — numbered phases force a natural display order.
- Give the reviewer one obvious entry point (`README.md`) and one obvious links page (`5-submission/links.md`).
- Keep build artifacts (code, configs, prompts) separate from research and write-ups so the prototype can be run independently.
- Avoid premature structure: no folders for things we may not produce.

## Non-Goals

- This structure is not intended for Tasks 2 (SEO audit) or 3 (growth hack). Those would get their own projects/folders.
- Not optimized for a multi-month codebase — phase folders are deliberately disposable after submission.

## Structure

```
Tet/
├── README.md                  # front door: what this is, status, how to view/run the demo
├── brief.md                   # original challenge brief, kept for reference
│
├── 1-discovery/
│   ├── company.md             # chosen company: features, audience, current marketing
│   ├── pain-points.md         # observed marketing problems
│   └── use-case.md            # which AI workflow + why
│
├── 2-design/
│   ├── workflow.md            # inputs, steps, outputs, tools chosen + why
│   ├── tools-comparison.md    # why this tool over alternatives (required by brief)
│   └── diagram.png            # flow diagram
│
├── 3-build/
│   ├── README.md              # how to run/reproduce the workflow
│   ├── prompts/               # prompt files, one per step
│   ├── src/                   # code if any (delete if not coding)
│   ├── config/                # GPT instructions / Zapier export / n8n workflow.json
│   └── .env.example           # required keys
│
├── 4-demo/
│   ├── inputs/                # sample input data
│   ├── outputs/               # output the workflow produced
│   ├── walkthrough.md         # step-by-step reviewer experience
│   └── recording-link.md      # Loom/video link
│
├── 5-submission/
│   ├── writeup.md             # final deliverable: 3 workflows + the demo, framed for reviewer
│   ├── links.md               # every working link in one place
│   └── final.pdf              # optional exported version
│
└── assets/                    # shared screenshots, logos, diagrams
```

## Product Location

The repo is the **source of truth + entry point**, not always the running product. Where the live, assessor-facing product lives depends on workflow format:

| Workflow type | Where the live product lives | What's in this repo |
|---|---|---|
| Custom GPT / Claude Project | Hosted platform — shareable URL (e.g. `chatgpt.com/g/g-XXX`) | Instructions + knowledge files in `3-build/config/` as backup & docs |
| Zapier / Make | Your Zapier/Make account — assessor cannot run it directly | Export JSON + screen recording link |
| Prompt chain with code | Either (a) repo only — assessor clones & runs, or (b) deployed (Vercel / Replit / Streamlit Cloud / HuggingFace Spaces) for one-click access | Source in `3-build/src/` |
| n8n / Flowise | Self-hosted URL or local-only | Workflow export JSON in `3-build/config/` |

**Key files for assessor access:**

- Root `README.md` — single entry point. Must contain the "click here to try it" link near the top.
- `5-submission/links.md` — canonical list of every working link (live demo, video, GPT, hosted prototype).
- `4-demo/recording-link.md` — Loom/video URL. Critical for Zapier/Make-type workflows where the assessor cannot run the product themselves.

**Rule of thumb:** if the assessor opens only one thing, it is the root `README.md`. From there, two clicks max to a working demo.

**Recommendation:** plan on both — source in the repo *and* a hosted/shared version. For code-based workflows, deploying to Streamlit Cloud or HuggingFace Spaces gives the assessor a one-click experience and is low-effort.

## Design Choices

**README at root, separate README in `3-build/`.** The root README orients the reviewer to the whole submission. The `3-build/` README is the prototype's own run instructions — independent so the prototype can be handed off without project-level context.

**Shared `assets/` folder, not per-phase.** Screenshots get referenced from multiple write-ups (design, demo, submission). One shared folder prevents duplicates and broken paths when work moves between phases.

**Numbered phase prefixes (`1-discovery/` …).** Forces display order in any file explorer or GitHub. Useful in a 72-hour sprint where you want to see progress at a glance. Removable later if the structure outlives the challenge.

**`5-submission/links.md` is a single source of truth.** The brief explicitly stresses "include working links so we can experience them firsthand." Centralizing links here means none get buried in prose.

**`3-build/src/` is a placeholder.** Delete it if the workflow turns out to be no-code (Zapier/GPT). Keeping it empty costs nothing if code may show up.

**`brief.md` lives at the root.** Keeps the original challenge alongside the work so context is never lost between phases.

## Trade-offs

- **Phase-based shuffling.** A screenshot taken during discovery may end up cited from submission. The shared `assets/` folder absorbs that; the cost is that "where does this file go" can be ambiguous for cross-phase artifacts. Rule of thumb: if it's referenced from multiple phases, it goes in `assets/`.
- **Disposable structure.** Optimized for one-shot submission, not long-term maintenance. If the project extends beyond the challenge, the numbered prefixes should be dropped.
- **No top-level `docs/`.** Documentation is colocated with each phase rather than centralized — fewer hops to find context, but no single doc index.

## Open Questions

- **Company choice (capq.ai vs karbonhq.com)** — independent of folder structure, but blocks content in `1-discovery/`.
- **Workflow format** — folder structure handles all three (prompt chain / GPT / Zapier) without changes, so this can be deferred.

## Next Step

Scaffold the empty structure: create folders, `.gitkeep` files where needed, and starter `README.md` / `brief.md` files. Drive this via the writing-plans skill.
