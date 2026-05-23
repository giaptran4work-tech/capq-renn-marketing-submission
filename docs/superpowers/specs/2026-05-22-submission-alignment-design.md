# Submission Alignment — Renn Labs Marketing Challenge (all 3 tasks)

**Date:** 2026-05-22 (revised 2026-05-23 after Giap's review — see Revision note at the end)
**Status:** Active alignment for the **full submission**.

**Supersedes:**
- `5-submission/submission-spec.md` — covered Task 1 only, as an 11-slide deck.
- `docs/superpowers/plans/2026-05-22-submission-deck.md` — a plan for the Task-1-only deck.

This is the contract between Giap and Claude for the whole submission. Anything produced that doesn't match this doc is wrong. Anything here that doesn't match Giap's intent gets revised before more work is done.

---

## 1. The brief — three tasks, one submission

```
  TASK 1   AI in Marketing Operations  — 3 AI workflows, build 1 (optional)
  TASK 2   SEO                          — audit + fix plan for the top 1-2 issues
  TASK 3   Growth Hacking               — a mechanism for 30+ qualified leads
                                          in 2 weeks at $0 ad spend + a prototype
```

Brief constraints: free choice of format · working links must be functional · 72 hours · "quality thinking over quantity" · may be asked to present live.

## 2. Scope

**One submission covering all three tasks.** Company chosen: **capq.ai**.

## 3. The customer (ICP) — stated once, clearly

capq.ai's customer is the **emerging fund manager (a "GP")** — someone running or starting a small investment fund (Fund I–III) and raising the money to fill it.

```
  LPs ──give money──► THE FUND ──invested by──► startups / companies / assets
  (pension funds,     (the pool)   the GP
   endowments,            ▲
   family offices,        │
   wealthy individuals)  run by the GP  ◄── capq.ai's customer
```

- **Not** a startup founder raising a VC round for their own company.
- Evidence — capq.ai hero subheadline: *"The only platform that takes you from LP discovery to signed commitment. Built by fund managers who use it for our own raises."*
- This ICP is **consistent across all three tasks.** Task 2's audit must use this ICP, not a broader "assumed" one.

## 4. Format

- A **slide deck**, exported to **PDF** for submission.
- **~20 slides** — tolerance ±1–2 slides per task.
- **Three self-contained task stories.** No forced cross-task through-line — each task has its own internal logic and storytelling.
- **Equal depth** — ~6 slides per task.
- **Task 2 appendix** — Task 2 may carry a short appendix (~3 slides) after the core deck, holding the full SEO-audit detail and screenshots. It stays **inside the one submission PDF** — never a separate file. Appendix slides are beyond the ~20 core count.
- **Self-explanatory** — no presenter needed; a reviewer reads it cold.
- **Defensible by Giap cold** — a live interview is possible; nothing in the deck Giap cannot explain without notes.

**Operating principle — content first.** The deliverable is the **content**. Slides are only its presentation layer. So:

- All work is produced as **content in markdown, organized by task** — never as slide layouts.
- The structure in §5 is a **content outline** — a map of what content blocks exist — not a slide-design task.
- **Slide visual design is deferred entirely to the end** and is trivial (Giap, in a deck tool).
- The content must be **focused, carefully aligned per task, planned in detail, and executed cleanly.** This is the bar every task is held to.

## 5. Content outline — the ~20 content blocks (approved)

```
  [1]  COVER — the 3-task challenge, capq.ai, Giap's name, date

  TASK 1 · AI in Marketing Operations — ~6 slides
    T1.1  capq.ai + its marketing problem (the GP customer, the gaps)
    T1.2  3 workflows overview — sense → produce → capture
    T1.3  Workflow #1 — Competitive Intel (BUILT) + live demo link
    T1.4  Workflow #2 — Founder-Voice Content (DESIGNED)
    T1.5  Workflow #3 — AI-Edited Weekly Digest (DESIGNED)
    T1.6  Impact + shared stack

  TASK 2 · SEO — ~6 slides
    T2.1  The audit — 4 categories, free tools, headline findings
    T2.2  The reframe — site is a verification/conversion asset
    T2.3  Priority 1 — Homepage conversion clarity
    T2.4  Priority 1 — the 3-week fix plan
    T2.5  Priority 2 — Brand SERP defense + what was NOT picked
    T2.6  Expected impact

  TASK 3 · Growth Hacking — ~6 slides
    T3.1  Hypothesis
    T3.2  The mechanism — Google-index discovery → engagement
          → filter → outreach (GP-language queries)
    T3.3  The prototype — the lead-discovery engine + a real sample contact list
    T3.4  Launch plan + funnel math to 30+ leads
    T3.5  Success metrics
    T3.6  Scaling approach

  [20] CLOSE — all working links

  APPENDIX · SEO-audit detail (Task 2 only) — ~3 slides, same PDF
    A1  Technical audit — full findings + screenshots
    A2  Content + Backlinks — full findings + evidence
    A3  Competitive — brand-SERP findings + screenshot
```

The slide-by-slide content gets detailed per task during execution (Giap reviews each task before the next).

## 6. Per-task content source + treatment

**Task 1** — content already exists: `1-discovery/`, the 3 workflow designs (`2-design/` + the workflow-alignment spec), and the built+deployed Competitive Intel demo. This section is assembly + sharpening, not new work.

**Task 2** — built from Giap's website audit (`Website Audit.docx`). The full audit — every finding and every screenshot — is presented **inside the submission PDF** (the six core slides + a ~3-slide appendix, §5), not as an external linked document. Three review recommendations are baked in:
1. **Own the reframe.** Priority 1 ("Homepage conversion clarity") is CRO-led — present it as a deliberate challenge to the brief's hidden "SEO = ranking" assumption, confidently. On-page keyword work stays in the plan as the SEO bridge.
2. **Align the ICP.** The audit must state the customer as the GP (Section 3), consistent with Task 1 — not the broader "assumed" audience in the draft.
3. **Add a bounded impact number** to Priority 1 — an estimated demo-conversion lift, not just "begin tracking."

**Task 3** — built from Giap's growth mechanism (`growth mechanism.docx`). Decisions:
- **Re-aim the queries** to GP language (`"first close"`, `"raising our Fund I"`, `"emerging manager"`, `"anchor LP"`, `"LP commitments"`) — the draft's `"seed round"` / `"looking for investors"` queries target startup founders, the wrong customer.
- **Build the missing pieces** the brief requires — hypothesis, launch plan, success metrics, scaling approach, and the funnel math to 30+ leads in 2 weeks.

## 7. The Task 3 prototype

**The lead-discovery engine.**

- **What it does:** runs precision-tuned `site:linkedin.com/posts` queries (fund-manager fundraising language) through the **SerpAPI** search API, collects matching signal-rich posts, identifies each post's author as a potential contact, dedupes by profile, scores each by fund-signal strength (signal phrases add, noise phrases subtract), and outputs a **ranked contact list** with the signal post kept as evidence.
- **Why this scope:** it automates the *safe* half of the mechanism. It searches Google's index via SerpAPI — it **never** touches linkedin.com directly — so there is no ToS / account-ban risk. The engagement-mining half (reading commenters/reactors) is the designed next step, stated honestly.
- **Search backend:** SerpAPI, free tier — 100 searches/month. Chosen over the Google Custom Search API (brainstorming, 2026-05-23): it returns the real Google SERP (better coverage of indexed LinkedIn posts) and needs no Cloud-project setup. The tool is **quota-aware** — `--dry-run` (0 calls), a small demo run by default (~6 searches), `--full` for the complete sweep, and a `--max-searches` hard cap.
- **Cost:** $0 (SerpAPI free tier). **Built by:** Claude, in-session. **Published by:** Giap — as a GitHub repo (a CLI tool, not a hosted web app).

## 8. Execution order — write-first, with review gates

```
  1  Task 1 section drafted     →  Giap reviews  ─┐
  2  Task 2 section drafted     →  Giap reviews   │  STOP & review
  3  Task 3 prototype built     →  Giap tests     │  at each gate
  4  Task 3 section drafted     →  Giap reviews   │
  5  Cover + close slides       →                 │
  6  Full-deck pass             →  Giap reviews  ─┘
       ↓
  Giap: design slides → host prototype → export PDF → submit
```

Most content exists, so steps 1–2 are assembly. The prototype (step 3) is the only true build.

## 9. Division of labor

| Surface | Who |
|---|---|
| All deck content (every slide, in markdown) | Claude |
| The Task 3 prototype (code) | Claude |
| Slide visual design | Giap (deck tool / claude.ai) |
| Hosting the prototype | Giap |
| PDF export + submission to Renn Labs | Giap |

## 10. Working links (all must be live at submission)

- **Task 1** — the live Competitive-Intel demo + its GitHub repo.
- **Task 2** — **none.** The full audit and screenshots are presented in the deck (core slides + appendix), not as an external file.
- **Task 3** — the lead-discovery prototype's GitHub repo (code, README, and a real sample run).

## 11. Definition of done

```
  ☐ All ~20 core slides written, in markdown
  ☐ Task 2 SEO-audit appendix (~3 slides) written, in the same file
  ☐ Every slide defensible by Giap cold (no notes)
  ☐ Task 2 reflects the 3 review recommendations
  ☐ Task 2 full audit + screenshots presented in-deck (no external file)
  ☐ Task 3 queries re-aimed to GP language; hypothesis /
    launch / metrics / scaling all present
  ☐ Task 3 prototype outputs a ranked contact list (post authors)
  ☐ The lead-discovery prototype is built and functional
  ☐ Every working link is live (Task 1 demo + repo, Task 3 repo)
  ☐ Deck designed + exported to PDF
  ☐ Submitted before the deadline
```

## 12. Anti-goals

- Slides that need a presenter to make sense.
- Hedging ("might be useful") — state the mechanism.
- Generic AI claims with no specific tool or flow.
- A forced narrative gluing the 3 tasks together — they are deliberately self-contained.
- Anything Giap could not defend in a live interview.

## 13. Research access

When a capq.ai page is bot-blocked, fetch it via the project's existing Playwright fetcher (`3-build/src/fetch.py`), which renders JS and beats basic bot detection. Anything still blocked → Giap pastes it.

---

## Revision note — 2026-05-23 (Giap's review)

Four ambiguities surfaced in review, resolved here:

1. **§7 prototype output** — was "ranks them by engagement," which contradicted the same paragraph (engagement mining is the deferred next step) and isn't reachable from Google's index. Now: the tool identifies **post authors** as contacts and ranks the **contact list** by GP-signal strength. Commenter/reactor mining stays the designed next step, done manually.
2. **§10 Task 3 link** — a command-line tool can't be "hosted." Task 3's working link = its **GitHub repo**. §7 "Hosted by" → "Published by."
3. **§10 Task 2 link** — the audit no longer lives in an external Google Doc. The **full audit + screenshots are presented in the deck** — core slides + a ~3-slide appendix (§4, §5). Task 2 has no external link.
4. **Appendix** — §4 now permits a Task-2 appendix inside the one PDF; §5 lists appendix blocks A1–A3.

## Self-review

- **Placeholders:** none. The only deferred detail (per-slide content, prototype tech shape) is deliberately handled per task during execution, with Giap's review gates — not a TBD.
- **Internal consistency:** the ICP (Section 3) is enforced into Task 1 and Task 2 (Section 6); execution order (Section 8) matches the structure (Section 5); definition of done (Section 11) covers every section.
- **Scope:** one submission, three tasks, one deck — a single coherent deliverable. Appropriately scoped for one implementation plan.
- **Ambiguity:** "self-contained task stories" is made explicit in Sections 4 and 12 (no forced through-line).

## Next step after sign-off

Invoke the writing-plans skill to produce the step-by-step implementation plan — the executable version of Section 8, with exact content specified per slide.
