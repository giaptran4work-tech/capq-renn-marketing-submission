# Submission Deck Content — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the complete written content for the 11-slide submission PDF deck (Renn Labs Marketing Challenge — Task 1), in one markdown file, ready for Giap to drop into a deck tool with no rewriting.

**Architecture:** This is a *writing* deliverable, not code. One file — `5-submission/deck.md` — holds 11 slide sections matching the locked outline in `5-submission/submission-spec.md`. Content is drawn only from existing source files (`1-discovery/`, `docs/superpowers/specs/2026-05-21-workflow-alignment.md`, `3-build/README.md`). Workflows #2 and #3 have only paragraph summaries today, so two short design notes are written **first** into a new `2-design/` folder — they give slides 7–8 real pipelines and tool reasoning, and make Slide 11's links resolve.

**"Tech stack":** Markdown. No build step. Each slide is reviewed against `submission-spec.md` rather than unit-tested — the spec checklist *is* the test.

---

## Source-of-truth map (which slide pulls from where)

```
  SLIDE                         PRIMARY SOURCE FILE
  ───────────────────────────   ───────────────────────────────────────
  1  Cover                      submission-spec.md (outline row 1)
  2  capq.ai in one slide        1-discovery/company.md  (Product, claims)
  3  The ICP                     1-discovery/company.md  (ICP section)
  4  5 Marketing Gaps            1-discovery/pain-points.md (Top gaps)
  5  3 Workflows overview        1-discovery/use-case.md (the three)
  6  Workflow #1 (BUILT)         workflow-alignment.md + 3-build/README.md
  7  Workflow #2 (DESIGNED)      2-design/workflow-2-founder-voice.md  ◄ created in Task 2
  8  Workflow #3 (DESIGNED)      2-design/workflow-3-weekly-digest.md  ◄ created in Task 3
  9  Expected Impact             use-case.md + pain-points leverage list
  10 Process & Methodology       lessons/ + Giap input (time breakdown)
  11 Appendix Links              all of the above
```

## Files created or modified

```
  Create:  2-design/workflow-2-founder-voice.md     Task 2
  Create:  2-design/workflow-3-weekly-digest.md     Task 3
  Create:  5-submission/deck.md                      Task 1 (skeleton) → Tasks 4-14 (filled)
  Modify:  5-submission/links.md                     Task 14
  Modify:  README.md (Status checklist)              Task 14
```

## Standing rules for every slide task

Apply these to every drafted slide — they encode the spec's non-content requirements and Giap's stated feedback:

1. **Word budget: ~225–275 words per content slide** (Slide 1 is shorter, ~40). Whole deck target: 2,500–3,000 words.
2. **Self-explanatory.** A reviewer with no presenter understands every line. No "as discussed", no dangling references.
3. **Reasoning, not just conclusions.** Every tool choice names what was rejected and why. ICP dimensions marked *stated* vs *inferred*. Gaps carry an evidence line.
4. **No hedging.** Ban "might be useful", "could potentially". State the mechanism.
5. **LLM provider is OpenRouter (free model).** The build switched off Gemini — commits `310a386` and `9306ad9` supersede the "Gemini" wording still in the alignment spec. Never write "Gemini" in the deck.
6. **Workflow #2 listening step:** mention *a LinkedIn scraper* as one option for automated ingestion. Do **not** name a specific product, do **not** say "v1/v2", do **not** describe a manual copy-paste step. Frame it as automated, ToS being the reason it stays "designed not built".
7. Slide sections in `deck.md` use `## Slide N — <title>` headers with an HTML comment word-budget marker, e.g. `<!-- budget: ~250 words -->`.

---

### Task 1: Create the deck skeleton

**Files:**
- Create: `5-submission/deck.md`

- [ ] **Step 1: Write the skeleton file**

Create `5-submission/deck.md` with exactly this content — 11 empty slide sections, each with its title and word budget. No body content yet.

```markdown
# Submission Deck — AI in Marketing Operations for capq.ai

> Renn Labs Marketing Challenge — Task 1. Slide content only — design lives in Giap's deck tool.
> Source spec: `5-submission/submission-spec.md` (locked 2026-05-21).

## Slide 1 — Cover
<!-- budget: ~40 words -->

## Slide 2 — capq.ai in one slide
<!-- budget: ~250 words -->

## Slide 3 — The ICP
<!-- budget: ~260 words -->

## Slide 4 — 5 Marketing Gaps
<!-- budget: ~270 words -->

## Slide 5 — 3 Workflows: sense → produce → capture
<!-- budget: ~240 words -->

## Slide 6 — Workflow #1: Competitive Intel (BUILT)
<!-- budget: ~270 words -->

## Slide 7 — Workflow #2: Founder-Voice Content (DESIGNED)
<!-- budget: ~260 words -->

## Slide 8 — Workflow #3: AI-Edited Weekly Digest (DESIGNED)
<!-- budget: ~260 words -->

## Slide 9 — Expected Impact
<!-- budget: ~250 words -->

## Slide 10 — Process & Methodology
<!-- budget: ~230 words -->

## Slide 11 — Appendix Links
<!-- budget: ~120 words -->
```

- [ ] **Step 2: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): scaffold 11-slide deck skeleton"
```

---

### Task 2: Design note — Workflow #2 (Founder-Voice Content Engine)

**Files:**
- Create: `2-design/workflow-2-founder-voice.md`

- [ ] **Step 1: Read sources**

Read `1-discovery/use-case.md` (the "Founder-Voice Content Engine" paragraph) and `1-discovery/pain-points.md` (Gap 2 + the "Customer research → content briefs" leverage bullet).

- [ ] **Step 2: Write the design note**

Create `2-design/workflow-2-founder-voice.md`. It must contain, in this order, lead with a visual per Giap's preference:

1. **One-line purpose:** closes Gap 2 — replaces anonymous bulk `/insights` content with original posts in CQ's founder voice.
2. **ASCII pipeline**, 4 stages:
   ```
   LISTEN  →  CLUSTER  →  BRIEF  →  DRAFT
   ```
   - **LISTEN** — an automated listener pulls public emerging-GP conversations from LinkedIn, Reddit (r/venturecapital, r/privateequity) and niche Substacks. A LinkedIn scraper is one option for the LinkedIn portion. (No product name, no version, no manual step.)
   - **CLUSTER** — an LLM groups the raw posts into recurring pain themes.
   - **BRIEF** — per theme, generate a content brief (angle, the pain it answers, proof points to use).
   - **DRAFT** — generate posts in CQ's founder voice, conditioned on a positioning/voice context file (same pattern as the built workflow's `cq-context.md`).
3. **AI role per stage:** CLUSTER, BRIEF, DRAFT are LLM; LISTEN is deterministic ingestion.
4. **Tools table** — each row names the choice AND the rejected alternative with a reason. Minimum rows: ingestion (automated scraper/API over manual collection — manual doesn't scale weekly), clustering+drafting LLM (OpenRouter free model over paid — consistency with WF#1, $0), voice conditioning (a context file over fine-tuning — no training data, no cost, editable).
5. **Why designed, not built:** voice-fit is subjective to validate inside a 72-hour window; scraping LinkedIn at scale carries platform-ToS complexity. Honest, one short paragraph.

- [ ] **Step 3: Self-check**

Verify: pipeline has exactly 4 named stages; every tool row has a rejected alternative + reason; the LinkedIn scraper is *mentioned*, not prescribed; no "copy and paste" anywhere; no version numbers.

- [ ] **Step 4: Commit**

```bash
git add 2-design/workflow-2-founder-voice.md
git commit -m "docs(2-design): add Workflow #2 founder-voice content design note"
```

---

### Task 3: Design note — Workflow #3 (AI-Edited Weekly Digest)

**Files:**
- Create: `2-design/workflow-3-weekly-digest.md`

- [ ] **Step 1: Read sources**

Read `1-discovery/use-case.md` (the "AI-Edited Weekly Digest" paragraph) and `1-discovery/pain-points.md` (Gap 5 + the "Personalized newsletter assembly" leverage bullet).

- [ ] **Step 2: Write the design note**

Create `2-design/workflow-3-weekly-digest.md`, same shape as Task 2, visual-first:

1. **One-line purpose:** closes Gap 5 — turns CQ's `/insights` library into an owned email audience asset.
2. **ASCII pipeline**, 3 stages:
   ```
   SCRAPE/FILTER  →  COMPILE/CLUSTER  →  DRAFT
   ```
   - **SCRAPE/FILTER** — pull new articles from CQ's own `/insights` CMS, filter by editorial fit.
   - **COMPILE/CLUSTER** — an LLM groups the issue's articles into 2–4 themes.
   - **DRAFT** — an LLM writes per-article summaries + takeaways, an editor's intro, and 3 subject-line variants, all voice-matched to CQ's founder tone.
3. **Scope guardrails (state explicitly):** human reviews before send — no autosend; no per-reader personalization at this stage.
4. **Tools table** — choice + rejected alternative + reason. Minimum rows: source (CQ's own CMS over scraping the open web — first-party, no ToS risk), LLM (OpenRouter free model over paid — $0, consistency), delivery (a standard newsletter platform such as Beehiiv/ConvertKit over a custom mailer — deliverability + compliance handled). Note delivery is named generically as a category, not endorsed as one product.
5. **Why designed, not built:** a meaningful demo needs a real subscriber base or a live newsletter-platform integration to be worth showing — more 72-hour budget for less defensibility than the built workflow.

- [ ] **Step 3: Self-check**

Verify: 3 named stages; the no-autosend / no-personalization guardrails are present; every tool row has a rejected alternative + reason.

- [ ] **Step 4: Commit**

```bash
git add 2-design/workflow-3-weekly-digest.md
git commit -m "docs(2-design): add Workflow #3 weekly-digest design note"
```

---

### Task 4: Slides 1–2 (Cover, capq.ai in one slide)

**Files:**
- Modify: `5-submission/deck.md` (Slide 1, Slide 2 sections)

- [ ] **Step 1: Read source**

Read `1-discovery/company.md` (Product + "Differentiators claimed" + "Notes/quotes").

- [ ] **Step 2: Draft Slide 1 — Cover**

Fill the Slide 1 section. Must contain exactly these lines:
- Title: **AI in Marketing Operations for capq.ai**
- Subtitle: Renn Labs Marketing Challenge — Task 1
- Author + date: Giap Tran — May 2026
- One-line tagline: a single sentence on the arc — three AI workflows that let one founder-marketer *sense, produce, and capture*, with one built and running live.

- [ ] **Step 3: Draft Slide 2 — capq.ai in one slide**

Fill the Slide 2 section. Must cover, compactly:
- **What it is:** AI fundraising platform for emerging fund managers; covers the full 8-stage fundraising lifecycle (LP discovery → AI matching → outreach → AI data room → NDA signing → LP portal → analytics → updates).
- **Who they serve:** emerging GPs raising Fund I–III across alternatives (PE-leaning, plus VC / hedge / secondaries).
- **Boldest claim** (quote it): "the only platform covering all 8 stages, while alternatives only cover 2–3."
- **Company stage:** recently launched (2026 footer); founder-operator-led; proof points are internal team metrics ("$455M+ invested by our team", "50+ deals closed by our team").

- [ ] **Step 4: Self-check against spec**

Verify against `submission-spec.md` outline rows 1–2: cover has all 4 elements; Slide 2 covers what / who / claim / stage; Slide 2 within ~225–275 words; no hedging.

- [ ] **Step 5: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slides 1-2 (cover, company)"
```

---

### Task 5: Slide 3 — The ICP

**Files:**
- Modify: `5-submission/deck.md` (Slide 3 section)

- [ ] **Step 1: Read source**

Read `1-discovery/company.md` — the full "Target audience / ICP" section.

- [ ] **Step 2: Draft Slide 3**

Fill the Slide 3 section. Must contain:
- **Primary segment** named: emerging fund managers, Fund I–III.
- **Dimension table**, each row tagged *[stated]* or *[inferred]* exactly as in `company.md`:
  asset class — PE-leaning *[inferred]*; fund size $10M–$250M target raise *[inferred]*; buyer = Managing Partner / GP who is also the fund's founder *[inferred]*; geography US-dominant *[stated]*; stage pre-launch–Fund III *[stated]*; team size 1–8 *[inferred]*.
- **3 buying triggers** (pick the 3 sharpest of the 5): just incorporated the fund; first close approaching; replatforming off stitched-together tools.
- **Decision process:** self-serve buyer, 1–4 weeks to decide, GP signs off alone up to ~$10K/year, no procurement or committee.

- [ ] **Step 3: Self-check against spec**

Verify: every dimension carries a *stated*/*inferred* tag; exactly 3 triggers; decision process names the self-serve + 1–4 week detail; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 3 (ICP)"
```

---

### Task 6: Slide 4 — 5 Marketing Gaps

**Files:**
- Modify: `5-submission/deck.md` (Slide 4 section)

- [ ] **Step 1: Read source**

Read `1-discovery/pain-points.md` — the "Top observed gaps" section.

- [ ] **Step 2: Draft Slide 4**

Fill the Slide 4 section. All 5 gaps, each as: a severity marker (e.g. a 1–5 bar `███░░`), a 1-line symptom, a 1-line "why it matters", a 1-line evidence point. The 5 gaps:
1. **Credibility floor too low** — all homepage proof is internal; no external logos, testimonials, case studies, SOC 2, or demo video. Evidence: "$455M by our team" is the only proof type on the page.
2. **Content is bulk-published & anonymous** — ~67 `/insights` articles, all dated "Dec 2025", no bylines. Why: trips Google's helpful-content / E-E-A-T systems; reads machine-generated. Evidence: uniform date + zero attribution.
3. **No competitive defense** — the "8 stages vs 2–3" claim is defended by nothing; no "vs." pages. Why: buyers search "capq.ai vs X" and find only competitor SEO. Evidence: no comparison content sitewide.
4. **Zero top-of-funnel personalization** — one homepage for PE / VC / HF / secondaries visitors. Why: the product *is* precision targeting; broadcast marketing contradicts it. Evidence: single hero, no segmented landing pages.
5. **Content builds no audience** — ~67 articles, zero email capture, handbook ungated with no wall. Why: content cost paid, never compounded; no remarketing, no list. Evidence: no subscribe CTA anywhere.

- [ ] **Step 3: Self-check against spec**

Verify: all 5 gaps; each has symptom + why + evidence; severity bars present; ~225–275 words (tight — favor terse lines).

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 4 (5 marketing gaps)"
```

---

### Task 7: Slide 5 — 3 Workflows overview

**Files:**
- Modify: `5-submission/deck.md` (Slide 5 section)

- [ ] **Step 1: Read source**

Read `1-discovery/use-case.md` — "The three workflows in the final write-up".

- [ ] **Step 2: Draft Slide 5**

Fill the Slide 5 section. A 3-column layout, one column per workflow, framed as **sense → produce → capture**:
- **WF #1 — Competitive Intel** · `BUILT` · the *sensing* layer · closes Gap 3 · one line: weekly competitor scan → classified diffs → a 1-page brief with suggested CQ plays.
- **WF #2 — Founder-Voice Content** · `DESIGNED` · the *producing* layer · closes Gap 2 · one line: listens to emerging-GP conversations, clusters pain themes, drafts posts in CQ's founder voice.
- **WF #3 — AI-Edited Weekly Digest** · `DESIGNED` · the *capture* layer · closes Gap 5 · one line: turns `/insights` into a weekly email that compounds content into an owned audience.

Include a one-line statement of the arc: each workflow hands leverage to the next; together one founder-marketer covers a function that normally needs a team.

- [ ] **Step 3: Self-check against spec**

Verify: 3 columns; each has a BUILT/DESIGNED tag and the gap it closes; the sense→produce→capture framing is explicit; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 5 (3 workflows overview)"
```

---

### Task 8: Slide 6 — Workflow #1: Competitive Intel (BUILT)

**Files:**
- Modify: `5-submission/deck.md` (Slide 6 section)

- [ ] **Step 1: Read sources**

Read `3-build/README.md` (pipeline diagram + "Why these tools" table) and `docs/superpowers/specs/2026-05-21-workflow-alignment.md` (sections 6–8).

- [ ] **Step 2: Draft Slide 6**

Fill the Slide 6 section. Must contain:
- **Pipeline, 7 steps, AI role per step:** Fetch (Playwright headless Chromium — not AI) → Extract (readability — not AI) → Diff (difflib — not AI) → **AI #1 Classify** (OpenRouter free model: tag change type + score 1–5, drop noise) → **AI #2 Synthesize** (OpenRouter: write the 1-page brief) → Render (markdown → HTML, Tailwind — not AI) → Publish (GitHub Pages — not AI).
- **Tool choices with rejected alternatives:**
  - LLM: OpenRouter free model — over paid Anthropic/OpenAI, because the run must cost $0.
  - Fetch: Playwright — over plain HTTP requests, because competitor sites block bots; a headless browser renders JS and gets through.
  - Diff: difflib (stdlib) — over an LLM diff, because spending tokens to detect CSS noise is waste; deterministic diff is free and exact.
  - Hosting: GitHub Pages — over Streamlit, because a static polished page reads as a publication, not a developer artifact.
- **Live demo link:** https://giaptran4work-tech.github.io/cq-competitive-intel/
- **GitHub link:** the repo URL.
- **Footer facts:** $0 per run, ~60–90s end-to-end, runs weekly on a GitHub Actions cron.

- [ ] **Step 3: Self-check against spec**

Verify: 7-step pipeline with AI role marked per step; at least 4 tool choices each with a rejected alternative + reason; both links present; says OpenRouter, never Gemini; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 6 (workflow #1 built)"
```

---

### Task 9: Slide 7 — Workflow #2: Founder-Voice Content (DESIGNED)

**Files:**
- Modify: `5-submission/deck.md` (Slide 7 section)

- [ ] **Step 1: Read source**

Read `2-design/workflow-2-founder-voice.md` (created in Task 2).

- [ ] **Step 2: Draft Slide 7**

Fill the Slide 7 section from the design note. Must contain:
- **Pipeline, 4 steps:** Listen → Cluster → Brief → Draft, with AI role per step (Cluster/Brief/Draft are LLM; Listen is ingestion).
- **The Listen step** — describe it as an automated listener pulling public emerging-GP posts from LinkedIn, Reddit, and niche Substacks; note a LinkedIn scraper as one option. No product name, no version, no manual copy-paste step.
- **Tool choices with rejected alternatives** (from the design note's table): ingestion, LLM, voice conditioning — each with the rejected alternative + reason.
- **Why designed, not built:** voice-fit is subjective to validate in 72 hours; scraping LinkedIn at scale carries ToS complexity.

- [ ] **Step 3: Self-check against spec**

Verify: 4-step pipeline; tool choices each carry a rejected alternative; "why designed not built" present; **no product name, no v1/v2, no "copy and paste"**; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 7 (workflow #2 designed)"
```

---

### Task 10: Slide 8 — Workflow #3: AI-Edited Weekly Digest (DESIGNED)

**Files:**
- Modify: `5-submission/deck.md` (Slide 8 section)

- [ ] **Step 1: Read source**

Read `2-design/workflow-3-weekly-digest.md` (created in Task 3).

- [ ] **Step 2: Draft Slide 8**

Fill the Slide 8 section from the design note. Must contain:
- **Pipeline, 3 steps:** Scrape/Filter → Compile/Cluster → Draft, with AI role per step.
- **Scope guardrails:** human reviews before send (no autosend); no per-reader personalization at this stage.
- **Tool choices with rejected alternatives:** source (CQ's own CMS over open-web scraping), LLM (OpenRouter free model over paid), delivery (a standard newsletter platform category over a custom mailer) — each with reason.
- **Why designed, not built:** a meaningful demo needs a real subscriber base or live newsletter-platform integration — poor budget-to-defensibility ratio inside 72 hours.

- [ ] **Step 3: Self-check against spec**

Verify: 3-step pipeline; guardrails stated; tool choices each carry a rejected alternative; "why designed not built" present; says OpenRouter; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 8 (workflow #3 designed)"
```

---

### Task 11: Slide 9 — Expected Impact

**Files:**
- Modify: `5-submission/deck.md` (Slide 9 section)

- [ ] **Step 1: Read source**

Read `1-discovery/use-case.md` ("Expected impact / leverage") and `1-discovery/pain-points.md` ("Where AI could create leverage").

- [ ] **Step 2: Draft Slide 9**

Fill the Slide 9 section. Per workflow, a quantified-or-bounded impact line:
- **WF #1:** recovers ~3 hours/week of marketer time; surfaces 1–2 actionable plays per week; over time produces the comparison/"vs." content CQ lacks.
- **WF #2:** replaces anonymous bulk content with original founder-voice posts — bounded as "fixes the E-E-A-T decay risk on ~67 articles"; state it as a bounded outcome, not an invented number.
- **WF #3:** converts one-shot `/insights` readers into an owned email list — bounded as "builds the audience asset CQ has zero of today".
- **Combined story:** the three together = one founder-marketer covering sense + produce + capture — "one marketer doing the work of four."

- [ ] **Step 3: Self-check against spec**

Verify: each workflow has a quantified OR explicitly-bounded impact (no fabricated precision); the combined "1 marketer = 4" story is present; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 9 (expected impact)"
```

---

### Task 12: Slide 10 — Process & Methodology

**Files:**
- Modify: `5-submission/deck.md` (Slide 10 section)

> **Giap input required:** the time breakdown needs Giap's real hours. Draft the slide with clearly-bracketed slots — `[discovery: ~X hrs]` etc. — for Giap to fill. This is a genuine external input, not a plan placeholder. Do not invent hours.

- [ ] **Step 1: Read source**

Read `lessons/2026-05-21-rushing-phases-without-review.md` and `CLAUDE.md` (phase-review framework).

- [ ] **Step 2: Draft Slide 10**

Fill the Slide 10 section. Must contain:
- **Time breakdown** across the phases — discovery / design / build / write-up — as bracketed slots for Giap to fill.
- **Tools used for research:** browser-based company research, a Playwright-based fetch layer, Claude Code as the build/writing environment.
- **One-line lessons-learned acknowledgment:** the phase-review framework — desired outcome / blockers / principles stated before each phase, with a review gate at every boundary — drawn from the `lessons/` entry.

- [ ] **Step 3: Self-check against spec**

Verify: time breakdown present (bracketed for Giap); research tools listed; one honest lessons-learned line; ~225–275 words.

- [ ] **Step 4: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 10 (process & methodology)"
```

---

### Task 13: Slide 11 — Appendix Links

**Files:**
- Modify: `5-submission/deck.md` (Slide 11 section)

- [ ] **Step 1: Draft Slide 11**

Fill the Slide 11 section. A clean link list:
- **GitHub repo:** the `cq-competitive-intel` repo URL.
- **Live demo:** https://giaptran4work-tech.github.io/cq-competitive-intel/
- **Discovery notes:** `1-discovery/` — company, pain-points, use-case.
- **Design docs:** `2-design/workflow-2-founder-voice.md`, `2-design/workflow-3-weekly-digest.md`, and `docs/superpowers/specs/2026-05-21-workflow-alignment.md` (Workflow #1's design contract).

- [ ] **Step 2: Self-check against spec**

Verify: all four link groups present; the design-docs links point to files that now exist (Tasks 2–3); ~80–150 words.

- [ ] **Step 3: Commit**

```bash
git add 5-submission/deck.md
git commit -m "docs(5-submission): draft slide 11 (appendix links)"
```

---

### Task 14: Full-deck review + sync surrounding docs

**Files:**
- Modify: `5-submission/deck.md`
- Modify: `5-submission/links.md`
- Modify: `README.md`

- [ ] **Step 1: Whole-deck word count**

Run:

```bash
python -c "t=open('5-submission/deck.md',encoding='utf-8').read(); print('words:',len(t.split()))"
```

Expected: between ~2,500 and ~3,200 (deck body; the skeleton headers add a little). If well over 3,200, tighten the longest slides.

- [ ] **Step 2: Review every slide against `submission-spec.md`**

Open `submission-spec.md` and walk its 11-slide outline + the 4 non-content requirements. For each slide confirm: it covers every content item the outline lists; it is self-explanatory; every tool choice names a rejected alternative; *stated*/*inferred* tags are on Slide 3; OpenRouter (never Gemini) throughout; Slide 7 has no product name / no v1-v2 / no copy-paste. Fix any gap inline.

- [ ] **Step 3: Update `links.md`**

Replace the placeholder URLs in `5-submission/links.md` with the real repo URL and the live demo URL; point the "Submission write-up" line at `deck.md` instead of `writeup.md`; remove the Loom line (spec dropped video).

- [ ] **Step 4: Update `README.md` Status checklist**

In the root `README.md`, check off the boxes that are now true: Company chosen, Use case decided, Workflow designed, Prototype built. Leave "Demo recorded" (N/A — no video) and "Submission finalized" per actual state.

- [ ] **Step 5: Commit**

```bash
git add 5-submission/deck.md 5-submission/links.md README.md
git commit -m "docs(5-submission): full-deck review + sync links and README status"
```

---

## Self-review (done while writing this plan)

**Spec coverage:** every one of the 11 outline rows in `submission-spec.md` maps to a task (Slides 1–2 → Task 4; 3 → T5; 4 → T6; 5 → T7; 6 → T8; 7 → T9; 8 → T10; 9 → T11; 10 → T12; 11 → T13). The 4 non-content requirements are enforced by the "Standing rules" block + Task 14 Step 2. The spec's dependency on `2-design/` (which did not exist) is resolved by Tasks 2–3.

**Placeholder scan:** the only bracketed slot is the Slide 10 time breakdown — and that is a deliberate, flagged request for Giap's real hours, not a plan failure. No "TBD/TODO" elsewhere.

**Consistency:** `deck.md` section headers in Task 1 match the slide titles referenced in Tasks 4–14. `2-design/` filenames are identical in Tasks 2, 3, 9, 10, 13. LLM provider is "OpenRouter" everywhere.

**Known gap surfaced:** Slide 10's time breakdown is the one item this plan cannot complete without Giap — handled by Task 12's input note.
