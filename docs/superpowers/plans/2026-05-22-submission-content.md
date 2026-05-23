# Submission Content — Implementation Plan

> **For agentic workers:** Execute this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This is a **content** plan — the deliverable is written content, not code (except Task 3, the prototype). "Tests" are self-checks against the alignment spec. **No git commits** — per project decision, this repo is a workspace only. Each task ends at a **Giap review gate**.

**Goal:** Produce all written content for the ~20-block submission deck (Renn Labs, 3 tasks) — plus a ~3-block Task 2 SEO-audit appendix in the same file — plus the Task 3 lead-discovery prototype. Content first, slide design deferred.

**Architecture:** One content file, `5-submission/deck-content.md`, holds all ~20 content blocks in 3 self-contained task sections. The Task 3 prototype is a small Python CLI tool in `4-growth-prototype/`. Content is drawn from existing sources (`1-discovery/`, `2-design/`, `3-build/`, Giap's audit, Giap's growth mechanism). Each task is drafted, self-checked, then reviewed by Giap before the next.

**Source spec:** `docs/superpowers/specs/2026-05-22-submission-alignment-design.md`. Anything that conflicts with it is wrong.

**Tech Stack:** Markdown (content). Python 3 + Google Custom Search JSON API free tier (the prototype).

---

## File structure (what exists at the end)

```
5-submission/
└── deck-content.md          ~20 core blocks + Task 2 audit appendix,
                             3 task sections (built up by Tasks 1, 2, 4, 5)

4-growth-prototype/          the Task 3 prototype (Task 3 builds this)
├── README.md                what it is, how to run
├── queries.yml              GP-language search queries (config)
├── find_leads.py            the CLI tool
└── sample-output.md         a real ranked lead list from a run
```

## Standing rules for every content block

1. **Content first.** Write substance — arguments, evidence, numbers. No slide-layout concerns.
2. **ICP = the GP** (emerging fund manager raising a fund from LPs). Never a startup founder.
3. **Reasoning, not just conclusions.** Every tool/priority choice names what was rejected and why.
4. **No hedging.** State the mechanism. Bounded estimates are fine; vague ones are not.
5. **OpenRouter** is the LLM provider — never write "Gemini".
6. **Defensible by Giap cold** — nothing he could not explain in a live interview.
7. Each block is a `### [block-id] — <title>` heading inside `deck-content.md`.

---

## Task 1: Task 1 content section — AI in Marketing Operations

**Files:**
- Create: `5-submission/deck-content.md` (this task creates the file + its Task 1 section)

**Sources to read first:** `1-discovery/company.md`, `1-discovery/pain-points.md`, `1-discovery/use-case.md`, `2-design/workflow-2-founder-voice.md`, `2-design/workflow-3-weekly-digest.md`, `3-build/README.md`.

- [ ] **Step 1: Read all six source files above.**

- [ ] **Step 2: Create `deck-content.md` and draft block T1.1 — capq.ai + its marketing problem.**

Content it must contain:
- What capq.ai is: an AI fundraising platform for emerging fund managers; covers the full LP-raise lifecycle (LP discovery → matching → outreach → AI data room → NDA → LP portal → analytics → updates).
- The customer: the GP — an emerging fund manager (Fund I–III) raising a fund from LPs. One tight sentence defining it.
- The marketing problem: capq has real marketing gaps; Task 1 targets the three that AI can close — Gap 3 (no competitive defense behind its boldest claim), Gap 2 (bulk anonymous content, E-E-A-T-fragile), Gap 5 (no audience capture). One line each.
- Frame: capq's marketing is run by a founder-marketer — the question is AI as a force multiplier for one person.

- [ ] **Step 3: Draft block T1.2 — 3 workflows overview (sense → produce → capture).**

Three columns, one per workflow: WF#1 Competitive Intel `BUILT` (sense, closes Gap 3); WF#2 Founder-Voice Content `DESIGNED` (produce, closes Gap 2); WF#3 AI-Edited Weekly Digest `DESIGNED` (capture, closes Gap 5). One line of leverage each. State the sense→produce→capture arc as Task 1's *own* internal story.

- [ ] **Step 4: Draft block T1.3 — Workflow #1 Competitive Intel (BUILT).**

- 7-step pipeline, AI role per step: Fetch (Playwright — not AI) → Extract (readability — not AI) → Diff (difflib — not AI) → AI#1 Classify (OpenRouter: tag + score 1–5) → AI#2 Synthesize (OpenRouter: write the brief) → Render (Markdown→HTML, Tailwind — not AI) → Publish (GitHub Pages — not AI).
- Tools + rejected alternatives: OpenRouter free model over paid (must be $0); Playwright over plain HTTP (beats bot detection); difflib over LLM-diff (no tokens on noise); GitHub Pages over Streamlit (publication, not dev artifact).
- The live demo link + the GitHub repo link. Footer: $0/run, ~60–90s, weekly cron.

- [ ] **Step 5: Draft block T1.4 — Workflow #2 Founder-Voice Content (DESIGNED).**

From `2-design/workflow-2-founder-voice.md`: 5-step pipeline (Listen → Extract → Cluster → Draft → Review); the tool stack with rejected alternatives; closes Gap 2. The LinkedIn listening step *mentions* a scraper (`joeyism/linkedin_scraper`) as one option — no v1/v2 framing, no manual copy-paste step.

- [ ] **Step 6: Draft block T1.5 — Workflow #3 AI-Edited Weekly Digest (DESIGNED).**

From `2-design/workflow-3-weekly-digest.md`: pipeline (Scrape/Filter → Compile/Cluster → Draft → Review/Send); tools with rejected alternatives; guardrails (no autosend, no per-reader personalization); closes Gap 5.

- [ ] **Step 7: Draft block T1.6 — Impact + shared stack.**

Per-workflow impact (WF#1 recovers ~3 hrs/week + surfaces 1–2 plays/week; WF#2 replaces anonymous bulk with founder-voice content — bounded; WF#3 builds the owned email list capq has zero of — bounded). The shared-stack point: "build #1, and #2/#3 reuse ~70% of the stack."

- [ ] **Step 8: Self-check the Task 1 section against the spec.**

Confirm: ICP = GP throughout; every tool choice names a rejected alternative; OpenRouter not Gemini; BUILT/DESIGNED tags present; both Workflow #1 links present; impact is bounded, not vague.

- [ ] **Step 9: REVIEW GATE — present the Task 1 section to Giap.** Do not start Task 2 until Giap approves.

---

## Task 2: Task 2 content section — SEO

**Files:**
- Modify: `5-submission/deck-content.md` (add the Task 2 section)

**Source:** Giap's website audit (`C:/Users/PC'/Downloads/Website Audit.docx` — extract text if needed). The audit's findings, prioritization, and fix plan are the raw material.

- [ ] **Step 1: Re-read the audit content** (Technical / Content / Backlinks / Competitive findings, the Prioritization section, the Fix Plan).

- [ ] **Step 2: Draft block T2.1 — The audit.**

- How: 4 categories audited (technical, content, backlinks, competitive); free tools only (Google PageSpeed Insights, SEOptimer, Dr Link Check, Google site search, incognito SERP); evidence-based, screenshots in a Google Doc.
- Headline findings with real numbers: Technical — Mobile LCP 4.6s (poor), keyword distribution graded D, 178 broken links (mostly LinkedIn redirects, low impact), indexability healthy. Content — unclear value proposition, weak social proof, buried security messaging. Backlinks — Domain Strength 24 / Page Strength 6, 146 backlinks across 61 domains, suspicious spam referring domains, near-zero institutional (edu/gov) links. Competitive — brand-SERP crisis: "capq" does not rank #1 (7+ unrelated entities); "capq ai" ranks #1.

- [ ] **Step 3: Draft block T2.2 — The reframe.**

The key insight: capq's GP buyers do not discover it via generic search — acquisition runs through outbound, conferences, founder LinkedIn, referrals. The institutional buying journey is long (15–30 min of deep research per prospect). So the website is a **verification / conversion asset**, not a top-of-funnel acquisition asset. Therefore SEO-ranking fixes are deprioritized; what a researching prospect *sees on landing* is the priority. **State explicitly** that this deliberately challenges the brief's implicit "SEO = ranking" assumption — present it as a strength, confidently.

- [ ] **Step 4: Draft block T2.3 — Priority 1: Homepage conversion clarity.**

Combines the 3 content findings into one coordinated fix: (1) unclear value proposition — "Let AI Supercharge Your Fundraise" says neither *who* nor *what*; (2) weak social proof — only internal metrics ($455M+ invested, 50+ deals), no logos / testimonials / third-party proof; (3) buried security — SOC2 deep in the FAQ, not near sign-up. Why it ranks first: the value prop is the first thing a researcher reads; trust signals are exactly what an institutional researcher verifies; capq has real customers (50+ deals) but hides them; the fix is fully in capq's control, no Google reranking, ships in 2 weeks, affects demo conversion immediately.

- [ ] **Step 5: Draft block T2.4 — Priority 1 fix plan.**

The 3-week plan: **Week 1** strategy + assets (founder interview to sharpen the value prop, audit competitor messaging, draft 3 value-prop options, list customers for logo/testimonial permissions, inventory scattered trust signals). **Week 2** homepage rewrite + on-page SEO (rewrite hero, add social-proof logo bar, add outcome-metrics section, add 2–3 named testimonials, surface SOC2 above the fold, refactor FAQ, optimize Title/Meta/H1/H2 with primary keywords — this clears the D-grade keyword finding, and is the SEO bridge inside the CRO fix). **Week 3** launch + QA + enablement (mobile QA, schema markup, sitemap to GSC, brief sales, update outbound templates, track demo conversion weekly).

- [ ] **Step 6: Draft block T2.5 — Priority 2 + what was NOT picked.**

Priority 2: Brand SERP defense — "capq" does not rank #1 (7+ competing entities). Why second: it depends partly on Google reranking (slow, not fully in capq's control); most prospects arrive via a direct shared link, bypassing the bare "capq" SERP. Fix (Weeks 4–5): on-site — strengthen the About page, add Organization + Person schema, publish a founder-bylined post anchored to capq.ai; off-site — consistent LinkedIn brand entity, 2–3 industry pieces with backlinks. **What was deliberately NOT picked** (with the reason each): build domain authority via backlinks (months of payoff, niche search volume too low); Core Web Vitals for ranking (audience isn't searching in volume); disavow spam backlinks (hygiene, not impact-critical); fix broken links (LinkedIn redirects, minimal SEO impact).

- [ ] **Step 7: Draft block T2.6 — Expected impact.**

Give a **bounded** estimate, framed honestly as an estimate (recommendation #3): Priority 1 → a clearer value proposition + visible trust signals lifts B2B landing-page demo-CTA conversion — state a bounded range and the reasoning, defensible at interview. Priority 2 → owning the "capq" brand SERP recaptures branded-search visitors currently lost to 7+ unrelated entities. Timeframe: Priority 1 impact within ~2 weeks of ship; Priority 2 over weeks-to-months.

- [ ] **Step 8: Draft the SEO-audit appendix — blocks A1, A2, A3.**

The full audit is presented in the deck, not in an external file. Three appendix blocks, drawn from the full audit `.docx`, placed after the Close block under an `## APPENDIX` heading in `deck-content.md`:
- **A1 — Technical audit:** every technical finding in full (Mobile LCP 4.6s, keyword grade D, 178 broken links, indexability), each with the screenshot it rests on. Mark screenshot placements as `[screenshot: ...]` for Giap to drop in at design time.
- **A2 — Content + Backlinks:** the full content findings and the backlink evidence (Domain Strength 24 / Page Strength 6, 146 backlinks across 61 domains, suspicious spam referring domains, near-zero edu/gov links), each with its screenshot marker.
- **A3 — Competitive:** the full brand-SERP finding (7+ unrelated entities on "capq", "capq ai" ranks #1), with the incognito-SERP screenshot marker.
These are evidence blocks — full detail, lighter prose than the core slides.

- [ ] **Step 9: Self-check the Task 2 section against the spec.**

Confirm: ICP stated as the GP (consistent with Task 1); the reframe is owned, not buried; Priority 1 + Priority 2 + the explicit "not picked" list all present; T2.6 has a bounded number, not vague language; real audit numbers used throughout; appendix blocks A1–A3 present with screenshot markers; no external Google Doc referenced anywhere.

- [ ] **Step 10: REVIEW GATE — present the Task 2 section (core + appendix) to Giap.** Do not start Task 3 until Giap approves.

---

## Task 3: Build the lead-discovery prototype

**Files:**
- Create: `4-growth-prototype/README.md`, `4-growth-prototype/queries.yml`, `4-growth-prototype/find_leads.py`, `4-growth-prototype/sample-output.md`

> **Giap input:** the tool uses **SerpAPI** as its search backend (free tier — 100 searches/month). Giap supplies a `SERPAPI_KEY`, stored in a gitignored `.env`. Decided during brainstorming (2026-05-23): SerpAPI over the Google Custom Search API — it returns the real Google SERP (better coverage) and needs no Cloud-project setup.

- [ ] **Step 1: Scaffold the folder** — create `4-growth-prototype/` and the four empty files.

- [ ] **Step 2: Write `queries.yml`** — the GP-language search queries. Each query targets `site:linkedin.com/posts` plus GP-raise language, e.g.:

```yaml
queries:
  - 'site:linkedin.com/posts "first close"'
  - 'site:linkedin.com/posts "raising our fund"'
  - 'site:linkedin.com/posts "emerging manager" "raising"'
  - 'site:linkedin.com/posts "anchor LP"'
  - 'site:linkedin.com/posts "Fund I" "raising"'
  - 'site:linkedin.com/posts "LP commitments"'
  - 'site:linkedin.com/posts "first-time fund manager"'
```

- [ ] **Step 3: Write `find_leads.py`** — a CLI tool that: reads `queries.yml`; for each query calls **SerpAPI** (`SERPAPI_KEY` from a gitignored `.env`); collects the LinkedIn post results (URL, title, snippet); **derives each post's author as a potential contact** — name from the result title, profile slug from the post URL; **dedupes by profile** so one fund manager who posted several times is one row; scores each contact by fund-signal strength (signal phrases add, noise phrases subtract); outputs a **ranked contact list** to `sample-output.md` (and a `.csv`). Quota-aware run modes: `--dry-run` (0 API calls), a small **demo** run by default (~6 searches), `--full` for the complete sweep, and a `--max-searches` hard cap.

- [ ] **Step 4: Test-run the tool.** Run `python find_leads.py --dry-run` — expected: prints all queries, no API call, exits 0. If Giap has supplied the API key, run it live and confirm `sample-output.md` fills with a real ranked contact list (deduped GP post authors).

- [ ] **Step 5: Write `README.md`** — what the tool does (finds post authors who publicly signal a fund raise, outputs a ranked contact list), the ToS-safe scope (Google index via SerpAPI, never linkedin.com directly), how to get a free SerpAPI key, how to run (dry-run / demo / full). State plainly that commenter/reactor engagement mining is the designed next stage, not built.

- [ ] **Step 6: REVIEW GATE — show Giap the tool, a sample run, and confirm the prototype shape.** Do not start Task 4 until Giap approves.

---

## Task 4: Task 3 content section — Growth Hacking

**Files:**
- Modify: `5-submission/deck-content.md` (add the Task 3 section)

**Source:** Giap's growth mechanism (`C:/Users/PC'/Downloads/growth mechanism.docx`), plus the prototype from Task 3.

- [ ] **Step 1: Draft block T3.1 — Hypothesis.**

State it as a real, falsifiable hypothesis: *If we surface LinkedIn posts where emerging GPs publicly signal fundraising pain (via Google's index) and reach out at that moment of peak relevance, we can generate 30+ qualified leads in 2 weeks at $0 ad spend — because intent is self-identified and the timing is optimal.* Include the observation it rests on: GPs signal pain publicly; Google indexes those posts; that turns public signal into a precision list for free.

- [ ] **Step 2: Draft block T3.2 — The mechanism.**

4 steps: (1) **Discovery** — GP-language `site:linkedin.com/posts` queries surface signal-rich posts; (2) **Engagement mining** — commenters (highest intent) over reactors; (3) **Profile filter** — keep Founder / Co-founder / GP at an emerging fund, drop investors/consultants/students; (4) **Outreach** — direct, context-referencing message. Show the **re-aimed GP queries** and explicitly note the original `"seed round"` / `"looking for investors"` framing was corrected because it targeted startup founders, not GPs.

- [ ] **Step 3: Draft block T3.3 — The prototype.**

Describe the lead-discovery engine built in Task 3: what it does, that it automates the *safe* half (Google-index discovery → post authors as contacts) with no LinkedIn scraping / no ToS risk / $0; include a real sample of the ranked contact list it outputs; and link to its GitHub repo. State that commenter/reactor engagement mining is the designed next step.

- [ ] **Step 4: Draft block T3.4 — Launch plan + funnel math.**

A 2-week plan: **Week 1** — run the tool across the GP queries, build the ranked post list, mine engagement, filter profiles, begin outreach. **Week 2** — continue outreach, follow-ups, book calls. Funnel math to 30+: ~30–50 signal-rich posts → ~500 engagers → ~150 profiles checked → ~50 qualified GPs reached → **30+ qualified leads**. State each conversion assumption so it is defensible.

- [ ] **Step 5: Draft block T3.5 — Success metrics.**

Measurable, with targets: posts surfaced, qualified-lead count (target 30+), profile→qualified rate, outreach sent, reply rate (target a stated %), calls booked (target a stated number), cost (= $0). Define "qualified lead" precisely: an emerging-fund GP, ICP-fit, identified and contacted.

- [ ] **Step 6: Draft block T3.6 — Scaling approach.**

Concrete path: automate the engagement-mining layer (the designed next step); expand the query set + add Reddit / niche communities; templatize and A/B the outreach; pipe leads into a CRM; hand the run to a VA or fuller automation once proven.

- [ ] **Step 7: Self-check the Task 3 section against the spec.**

Confirm: hypothesis is falsifiable; queries are GP-language (no "seed round"); all 4 brief-required pieces present (hypothesis, launch plan, metrics, scaling); funnel math is explicit and adds to 30+; prototype described honestly re: ToS.

- [ ] **Step 8: REVIEW GATE — present the Task 3 section to Giap.** Do not start Task 5 until Giap approves.

---

## Task 5: Cover + Close content

**Files:**
- Modify: `5-submission/deck-content.md` (add the Cover block at the top and the Close block at the end)

- [ ] **Step 1: Draft the Cover block.**

Title: **AI, SEO & Growth for capq.ai**. Subtitle: Renn Labs Marketing Challenge — 3 tasks. Author + date: Giap Tran — May 2026. One line noting the deck is three self-contained task answers.

- [ ] **Step 2: Draft the Close block.**

All working links: Task 1 → live Competitive-Intel demo + GitHub repo; Task 2 → no external link (the full audit is in this deck — point to the appendix); Task 3 → the lead-discovery prototype's GitHub repo. One-line wrap.

- [ ] **Step 3: REVIEW GATE — show Giap the Cover + Close.**

---

## Task 6: Full-deck content review + assembly

**Files:**
- Modify: `5-submission/deck-content.md`

- [ ] **Step 1: Word-count the file.**

Run: `python -c "t=open('5-submission/deck-content.md',encoding='utf-8').read(); print('words:',len(t.split()))"`
Expected: a content-dense but reviewer-respectful total (rough guide ~3,000–4,500 words across ~20 blocks). If far over, tighten the longest blocks.

- [ ] **Step 2: Walk the whole file against the alignment spec** (`docs/superpowers/specs/2026-05-22-submission-alignment-design.md`). For each of the ~20 blocks confirm: it matches §5; ICP = GP everywhere; every tool/priority choice names a rejected alternative; the 3 Task-2 recommendations are reflected; Task 3 has all 4 brief-required pieces; every working link is present; nothing requires a presenter. Fix any gap inline.

- [ ] **Step 3: Confirm the working links resolve** — the live Competitive-Intel demo, the Workflow #1 repo, and the prototype repo. (Task 2 has no link — its full audit is in-deck.) Flag any not yet live for Giap.

- [ ] **Step 4: REVIEW GATE — present the complete `deck-content.md` to Giap** for the final content sign-off, before he moves to slide design.

---

## Self-review (done while writing this plan)

**Spec coverage:** §5's 20 core blocks + the Task 2 SEO-audit appendix (A1–A3, drafted in Task 2 Step 8) → Tasks 1, 2, 4, 5. §6 per-task treatment → the content specs in Tasks 1/2/4 (audit recommendations baked into Task 2 Steps 3/7; query re-aim into Task 4 Step 2). §7 prototype (ranked contact list, post authors) → Task 3. §8 execution order → task order (Task1 content → Task2 content → prototype → Task3 content → cover/close → review). §10 working links → Task 5 Step 2 + Task 6 Step 3. §11 definition of done → Task 6.

**Placeholder scan:** the only flagged input is the Google API key in Task 3 — a real external input from Giap, not a plan gap. No "TBD"/"TODO".

**Consistency:** the content file is `5-submission/deck-content.md` in every task; the prototype lives in `4-growth-prototype/` with consistent filenames across Tasks 3 and 4; block IDs (T1.1–T3.6, plus appendix A1–A3) match §5 of the spec.
