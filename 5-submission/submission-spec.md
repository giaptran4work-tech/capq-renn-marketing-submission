# Submission Spec — Renn Labs Marketing Challenge Task 1

**Locked:** 2026-05-21
**Status:** Approved by Giap; basis for all submission content from this point.

## Format

- **Single PDF slide deck.**
- **11 slides total.** Compact, content-dense per slide.
- **No video / Loom.** Deck stands alone.
- **Live demo URL + GitHub URL embedded as clickable links** in the PDF.

## Division of labor

| Surface | Who |
|---|---|
| Slide content (every word, every bullet, every "why over alternative") | Claude writes in markdown |
| Slide design (visuals, layout, branding) | Giap, in deck tool of choice (Google Slides / Keynote / Marp / etc.) |
| Working demo code | Claude writes (already drafted, untracked in `3-build/`) |
| Demo deployment to Streamlit Cloud | Giap |
| GitHub push | Giap |

## Non-content requirements

The slides must:

1. **Be self-explanatory.** No live presenter. A reviewer reads the deck cold and understands every slide.
2. **Show Giap's way of thinking.** Reasoning surfaced alongside decisions — not just the conclusions. Tool choices must show what was rejected and why. ICP dimensions marked as *stated* vs. *inferred*. Gap deep-dives include the evidence column.
3. **Keep tool choices separated per workflow.** Each workflow gets its own tools slide, not a combined comparison table.
4. **Stay compact.** ~225–275 words per slide. Total ~2,500–3,000 words.

## 11-Slide Outline

| # | Slide | Content |
|---|---|---|
| 1 | **Cover** | Title: "AI in Marketing Operations for capq.ai" / Subtitle: Renn Labs Marketing Challenge — Task 1 / Name + date / 1-line tagline |
| 2 | **capq.ai in one slide** | What the product is / who they serve / their boldest claim / company stage |
| 3 | **The ICP** | Primary segment summary / 3 buying triggers / decision process (self-serve, 1–4 weeks) / *stated* vs *inferred* dimensions marked |
| 4 | **5 Marketing Gaps (single slide)** | All 5 with severity bars; per gap = 1-line symptom + 1-line "why it matters" + 1-line evidence |
| 5 | **3 Workflows overview — sense → produce → capture** | One column per workflow; BUILT vs DESIGNED tags; the gap each closes |
| 6 | **Workflow #1: Competitive Intel (BUILT)** | Pipeline (6 steps, AI role per step) + tools chosen + why over alternatives + live demo link + GitHub link |
| 7 | **Workflow #2: Founder-Voice Content (DESIGNED)** | Pipeline (listen / cluster / brief / draft) + tools chosen + why over alternatives + why designed not built |
| 8 | **Workflow #3: AI-Edited Digest (DESIGNED)** | Pipeline (scrape / compile / draft) + tools chosen + why over alternatives + why designed not built |
| 9 | **Expected Impact** | Quantified-or-bounded impact per workflow + the combined story ("1 marketer doing the work of 4") |
| 10 | **Process & Methodology** | Time breakdown / tools used for research / 1-line lessons-learned acknowledgment |
| 11 | **Appendix Links** | GitHub repo / live demo / `1-discovery/` notes / `2-design/` design docs |

## Dropped from earlier versions

- TL;DR slide (originally slide 2)
- "How to use this deck" slide (originally slide 3)
- "How I'd Extend This" slide (originally slide 16)
- Loom video walkthrough
- Notion page format
- Combined "Tool Choices Across All 3 Workflows" slide

## Narrative arc

> Chose capq.ai → spent ~X hours understanding it → found 5 marketing gaps → designed 3 AI workflows in a sense → produce → capture story → built one end-to-end (Competitive Intel) → here it works on real competitor data → expected impact across the stack.

Everything in the deck ladders up to this arc. Anything that doesn't, gets cut.

## Reviewer experience

- **5-minute skim:** slides 1, 4, 5, 6 (cover, gaps overview, 3 workflows, built demo with link)
- **15-minute deep read:** all 11 slides
- **Live demo click:** sample brief pre-loaded so reviewer sees output instantly; "Run" button triggers a fresh brief on live competitor data

## What this spec depends on

- Discovery (`1-discovery/`) — done and committed.
- Design (`2-design/`) — done and committed.
- Build (`3-build/`) — code exists but is **uncommitted, not yet deployed**.
- Deployment — Streamlit Cloud, pending.

## Anti-goals

- Slides that need a presenter to make sense
- Wishy-washy hedging ("might be useful")
- Generic AI claims with no specific mechanism
- Bluffing — anything Giap couldn't defend at 11pm without notes
- Theatrical design over substance
