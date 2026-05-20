# Lesson — Rushing phases without review gates

**Date:** 2026-05-21
**Where it happened:** Tasks 1 discovery → design → build, in a single push.

## What happened

Discovery (`1-discovery/`), design (`2-design/`), and ~9 Python files in `3-build/` were produced in one continuous run, without checkpointing with the user. The user (Giap) had to interrupt at `pip install` to stop the build and reset. Both of us recognized that we'd skipped specifying:

- what a *good* output of each phase would look like
- what could prevent that
- what principles to follow to avoid those failures

Auto-mode amplified the speed but the responsibility is shared: I drove past review gates I should have stopped at; the user didn't review as work landed.

## Desired outcome (for any phase from now on)

When a phase ends, the user can:

1. Read the output in under 5 minutes.
2. Say "this is right" or point at the specific thing to redo — with no ambiguity.
3. Use the output downstream (in the next phase, in the submission, in a live interview) without rework.

## Blockers (what gets in the way)

| Blocker | How it bit us |
|---|---|
| No success criteria stated upfront | We didn't agree what `company.md` had to contain before I wrote it. |
| Auto-mode misread as "no pauses ever" | I treated auto-mode as license to chain 5+ phases without check-ins. |
| Sunk-cost momentum | Once discovery was "done", we rolled straight into design, then build — making it expensive to revisit if discovery was off. |
| No explicit phase boundary | "Phase" was implicit. There was no moment that said "STOP here, review." |
| Optimism about time spent | Building 9 Python files felt productive — but value is zero if discovery is wrong. |

## Principles (rules to overcome the blockers)

1. **Write down the desired outcome before starting a phase.** Two or three lines, visible in the phase's own doc or in a kickoff note. Includes: what the user needs to be able to do with the output.
2. **Identify blockers and principles for each phase, not just the project overall.** What could go wrong *in this phase* — and the rule that prevents it.
3. **Stop at every phase boundary.** No exceptions for auto-mode. Auto-mode means "don't ask trivial clarifying questions"; it does not mean "skip review gates on evaluated deliverables".
4. **Review checkpoint output must be reviewable in under 5 minutes.** If it's longer, summarize it for review.
5. **Bias toward redoing earlier phases over building on shaky ground.** If discovery is 80% right, sharpen the 20% before designing — not after.
6. **No code until design is reviewed and explicitly approved.** No design until the use case is reviewed and explicitly approved.

## Status of work in progress

- **Committed:** discovery files (`1-discovery/`) and design files (`2-design/`) — but they need re-review under the new framework.
- **Uncommitted:** `3-build/` Python files, config, and prompts written but not installed, not run, not tested, not committed. Sitting in the working tree.
- **Decision pending:** whether to revise discovery + design and rebuild, or keep what's there and patch from here.
