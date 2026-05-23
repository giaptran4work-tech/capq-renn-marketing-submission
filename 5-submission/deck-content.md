# AI, SEO & Growth for capq.ai

**Renn Labs Marketing Challenge — three tasks**

Giap Tran · May 2026

*Three self-contained answers: AI workflows for marketing operations · an SEO
audit and prioritised fix plan · a growth mechanism for 30+ qualified leads in
two weeks at $0 ad spend.*

---

## TASK 1 · AI in Marketing Operations

### [T1.1] — capq.ai and its three marketing gaps

**What capq.ai is.** capq.ai is an AI fundraising platform for emerging fund
managers. It covers the full LP-raise lifecycle — eight stages — in one place:

```
   LP discovery → AI matching → outreach → AI data room → NDA signing
                → LP portal → analytics → ongoing updates
```

**The customer.** *capq.ai's customer is the user — an emerging fund manager
running a Fund I–III and raising the capital to fill it from LPs.* The user buys
self-serve and leads marketing personally, as part of a lean team.

**Three marketing gaps.** Task 1 focuses on three gaps where AI can add the most
marketing leverage. Everything that follows — all three workflows — addresses
exactly these three:

- **Gap 1 — Competitive defense.** capq.ai's homepage makes a confident, specific
  claim: "the only platform covering all 8 stages, while alternatives cover
  2–3." The site does not yet carry the comparison content that backs that claim
  up. So when a user hears it and searches "capq.ai vs [competitor]," the results
  surface competitors' material first. **The opportunity:** own that comparison
  moment.
- **Gap 2 — Content credibility.** The ~67 articles on `/insights` are published
  in bulk, dated uniformly ("Dec 2025"), and run without bylines. Search engines
  increasingly reward visible expertise and authorship (Google's E-E-A-T
  signals). **The opportunity:** give the library a distinct founder voice, so
  it ranks durably and reinforces the credibility the homepage builds.
- **Gap 3 — Audience capture.** The library draws readers, but there is no
  email-capture step, so each visit is a single touch. **The opportunity:** add
  a capture path that turns existing traffic into an audience capq.ai can reach
  again — compounding the content investment already being made.

**The frame.** Marketing at capq.ai is founder-led and runs lean. So Task 1's
question is focused: **how can AI multiply the reach of one person?** Each of the
three workflows that follows answers that question for one of these three
gaps — Gap 1, Gap 2, Gap 3, in order.

### [T1.2] — Three workflows, one for each gap

The three gaps from T1.1 are not addressed in isolation. Task 1 designs one AI
workflow for each — and together they form a single marketing function that
moves in three steps: **sense → produce → capture.**

```
   SENSE ───────────────► PRODUCE ───────────────► CAPTURE

   WF#1                   WF#2                     WF#3
   Competitive Intel      Founder-Voice Content    AI-Edited Weekly Digest
   [BUILT]                [DESIGNED]               [DESIGNED]

   closes Gap 1           closes Gap 2             closes Gap 3
   Competitive defense    Content credibility      Audience capture
```

**Why this order.** The three gaps run in sequence, and each workflow feeds the
next:

- **Sense — WF#1 closes Gap 1.** A founder-marketer cannot back a competitive
  claim against rivals they cannot see. Competitive Intelligence is the sensing
  layer: it watches what competitors do and turns that into clear input.
- **Produce — WF#2 closes Gap 2.** Sensing only pays off if it drives output.
  Founder-Voice Content takes the user's pain points and positioning that
  sensing surfaces, and turns them into credible, founder-voice articles.
- **Capture — WF#3 closes Gap 3.** Producing content only pays off if readers
  stay. The AI-Edited Weekly Digest captures those readers into an owned
  audience.

One workflow — Competitive Intelligence — is **built and live**; the other two
are **designed in full**. The next four slides take each in turn, then sum the
impact.

### [T1.3] — Workflow #1: Competitive Intelligence (BUILT)

This workflow gives capq.ai's marketer a weekly, automatic read on what
competitors are doing — and a clear recommendation on how to respond. It is
built, live, and runs at $0 per run. It addresses **Gap 1**.

**How it works.** Each week the workflow runs a seven-step pipeline:

```
  watchlist.yml ── 4 competitors, ~13 URLs
        │
   1 FETCH       Playwright headless browser        (not AI)
        ▼
   2 EXTRACT     strip nav/ads, keep article text   (not AI)
        ▼
   3 DIFF        difflib vs last week's snapshot     (not AI)
        ▼
   4 CLASSIFY    OpenRouter LLM — tag + score 1–5    ◄ AI #1
        ▼        (only changes scoring ≥3 continue)
   5 SYNTHESIZE  OpenRouter LLM — write the brief    ◄ AI #2
        ▼
   6 RENDER      Markdown → HTML, Tailwind           (not AI)
        ▼
   7 PUBLISH     GitHub Pages                        (not AI)
```

The pipeline is built in two deliberate halves.

**Steps 1–3 are mechanical.** The run starts from a short watchlist — four
competitors, about thirteen pages. Playwright loads each page the way a real
browser would; the extract step keeps only the meaningful article text and
discards navigation and ads; and `difflib` compares that text against last
week's saved snapshot to isolate what actually changed. None of this needs AI —
it is reliable plumbing, and keeping it AI-free is also what keeps the run free.

**Steps 4–5 are where AI does the judgment work.** A raw list of changed text is
not yet useful, because most changes are trivial. So the first AI call reads each
change, tags it (a feature ship, a pricing move, a positioning shift, a new
content angle) and scores how important it is from 1 to 5; only changes scoring 3
or higher continue. The second AI call takes those, and — given capq.ai's own
positioning as context — writes the actual brief: what changed, why it matters to
capq.ai, and a concrete suggested response. **Steps 6–7** turn that brief into a
clean web page and publish it, so the marketer simply opens a link.

The design principle behind this shape: **AI is used in only two of the seven
steps — exactly where judgment is needed, and nowhere else.** That keeps the
workflow accurate, fast, and free.

**Tool choices — and what was considered instead:**

| Choice | Considered instead | Why this one |
|---|---|---|
| OpenRouter free model | a paid LLM API | the workflow is designed to cost $0 per run |
| Playwright | plain HTTP requests | some competitor sites block simple requests; Playwright loads pages as a real browser would |
| difflib | an LLM-based diff | there is no need to spend tokens, or money, detecting routine noise |
| GitHub Pages | a Streamlit app | the output is a finished brief to read, not a tool the marketer has to go and run |

**▸ Live demo:** https://giaptran4work-tech.github.io/cq-competitive-intel/
**▸ Repo:** https://github.com/giaptran4work-tech/cq-competitive-intel

$0 per run · ~60–90 seconds end to end · runs automatically each week.

### [T1.4] — Workflow #2: Founder-Voice Content (DESIGNED)

This workflow closes **Gap 2 — Content credibility.** It listens to what
emerging fund managers actually ask online, finds the real pain themes, and drafts
articles in capq.ai's founder voice — so the content library carries clear
expertise and a distinct authorial voice.

**How it works.** A five-step pipeline:

```
   1 LISTEN    pull recent posts where users talk —   (not AI)
        ▼      Reddit · Substacks · LinkedIn
   2 EXTRACT   LLM pulls recurring questions,         ◄ AI
        ▼      objections, and exact user wording
   3 CLUSTER   embeddings group pains into 3–5        (math)
        ▼      themes; pick the strongest one
   4 DRAFT     LLM writes a brief + a first-draft     ◄ AI
        ▼      article in capq.ai's founder voice
   5 REVIEW    founder edits and publishes            (human)
```

The pipeline starts and ends with people, with AI in the middle. **Step 1**
gathers raw material — recent posts from the places emerging fund managers actually talk.
**Step 2** is the first AI step: it reads those posts and pulls out the
recurring questions, objections, and the exact words GPs use. **Step 3** groups
those pain points by meaning, so related concerns fall into three to five
themes, and the strongest theme — the one capq.ai has not yet covered well — is
chosen. **Step 4** is the second AI step: it writes a content brief and a
first-draft article in capq.ai's founder voice, grounded in capq.ai's own
homepage and handbook copy as a voice reference. **Step 5** keeps the founder in
control — they edit and publish. AI drafts; the founder owns.

**Tool choices — and what was considered instead:**

| Choice | Considered instead | Why this one |
|---|---|---|
| Reddit API (PRAW) | scraping Reddit HTML | official, free, ToS-clean; scraping breaks and violates ToS |
| feedparser + curated Substack RSS | scraping newsletters | RSS is the sanctioned, stable, free way to read them |
| `joeyism/linkedin_scraper` | LinkedIn has no free read API | LinkedIn is the richest surface for this audience; this tool is Playwright-based, so it fits the stack. Honest note: scraping LinkedIn is against its ToS — a real constraint, stated openly |
| OpenRouter free model | a paid LLM API | the same $0 LLM stack as WF#1 — one provider across all three workflows |
| sentence-transformers + scikit-learn | keyword matching | real semantic grouping catches paraphrased pain that keyword matching misses |

The result for Gap 2: one publish-ready, operator-credible, voice-consistent
article each week — content that strengthens the credibility the homepage
builds. AI drafts; the founder owns.

### [T1.5] — Workflow #3: AI-Edited Weekly Digest (DESIGNED)

This workflow closes **Gap 3 — Audience capture.** It turns capq.ai's existing
`/insights` library into a weekly email digest, so the readers the library
already attracts become subscribers capq.ai can reach again.

**How it works.** A four-step pipeline, working only from capq.ai's own content:

```
   capq.ai's own /insights CMS   (first-party — no third-party scraping)
        │
   1 SCRAPE & FILTER    pull the week's new articles;   ◄ AI assists
        ▼               LLM drops thin pieces
   2 COMPILE & CLUSTER  LLM groups them into 2–4 themes ◄ AI
        ▼
   3 DRAFT             per article: summary + takeaway; ◄ AI
        ▼              editor's intro + 3 subject lines
   4 REVIEW & SEND     marketer reviews, presses send   (human)
```

**Step 1** pulls the week's new articles straight from capq.ai's own CMS, and an
AI check drops thin pieces so only digest-worthy articles continue. **Step 2**
uses AI to group those articles into two to four themes, which gives each issue
a clear shape. **Step 3** is the main drafting step: for each article the AI
writes a short summary and one key takeaway, then adds an editor's introduction
and three subject-line options — all in capq.ai's voice. **Step 4** keeps a
person in charge: the marketer reviews the draft and presses send.

**Guardrails, stated up front.** No autosend — a human always presses send. And
no per-reader personalization at this stage — one well-edited issue goes to
everyone, which keeps the workflow simple, safe, and easy to trust while the
audience is still being built.

**Tool choices — and what was considered instead:**

| Choice | Considered instead | Why this one |
|---|---|---|
| feedparser + capq.ai's own RSS/sitemap | third-party scraping | capq.ai owns the source — the clean, sanctioned, licensing-free way to read it |
| OpenRouter free model | a paid LLM API | the same $0 LLM stack as WF#1 and WF#2 |
| sentence-transformers + scikit-learn | keyword grouping | the same free, local embedding + clustering pair as WF#2 |
| Beehiiv free tier | ConvertKit / Mailchimp | Beehiiv is built for audience growth (signup forms, public archive, referrals); the others are focused on sending |

The result for Gap 3: a steady path from one-shot reader to subscriber — the
start of an owned audience capq.ai can reach again and again.

### [T1.6] — Impact and the shared stack

**What each workflow returns — gap by gap.**

- **Gap 1, Competitive defense — WF#1 (built).** Recovers about 3 hours a week of
  the marketer's time, and surfaces 1–2 concrete plays each week — a
  comparison-content angle, an ad headline, a positioning adjustment. This is
  the material capq.ai needs to back its "all 8 stages" claim.
- **Gap 2, Content credibility — WF#2 (designed).** Produces one founder-voice,
  operator-credible article each week — building a content library with the
  visible expertise that search engines and GPs both reward.
- **Gap 3, Audience capture — WF#3 (designed).** Turns existing readers into an
  owned email list — an audience capq.ai can reach again, one that compounds and
  is not exposed to a single SEO algorithm change.

**One coherent system, not three separate tools.** The three workflows are built
on a shared stack:

```
   ALL THREE   Python  +  LLM via OpenRouter (free)
   #2 AND #3   sentence-transformers + scikit-learn · feedparser
   #1 ONLY     Playwright · difflib
```

Roughly 70% of the stack is shared, so the three workflows reuse each other's
parts rather than standing alone. That is the payoff of the sense → produce →
capture design: one founder-marketer can run all three as a single, coherent
marketing-ops platform.

---

## TASK 2 · SEO

### [T2.1] — The audit

capq.ai's website was audited across the four categories the brief calls for —
**technical, content, backlinks, and competitive** — using free tools only:
Google PageSpeed Insights, SEOptimer, Dr Link Check, and Google site-search and
incognito SERP checks. Every finding is evidence-based, with screenshots.

**Headline findings:**

```
  TECHNICAL     Mobile Largest Contentful Paint 4.6s (poor — above the
                4s threshold); desktop healthy. Indexability and
                crawlability healthy (AI Visibility 100/100). 178 broken
                links out of ~2,000 URLs — mostly external LinkedIn
                redirects, low SEO impact. Keyword distribution graded D:
                main keywords missing from Title, Meta, and Heading tags.

  CONTENT       Three opportunities on the homepage — a clearer value
                proposition, stronger external social proof, and more
                visible security messaging.

  BACKLINKS     Domain Strength 24, Page Strength 6 — 146 backlinks across
                61 referring domains. A few low-quality referring domains
                present; near-zero institutional (.edu / .gov) links.

  COMPETITIVE   A search for "capq" does not return capq.ai first — the
                results are held by 7+ unrelated entities. The
                disambiguated search "capq ai" returns capq.ai #1 with
                rich sitelinks.
```

The full detail behind each finding, with screenshots, is in the appendix
(A1–A3). The next slide explains how these findings were prioritized — and why
the priority order is not the obvious one.

### [T2.2] — The reframe: the website is a verification asset

Before prioritizing the fixes, one question shapes everything: **how do
capq.ai's customers actually arrive at the site?**

capq.ai's customer is the user — the same emerging fund manager described in
Task 1. Buyers like this rarely discover a fundraising platform by typing
generic terms into Google; search volume in this niche is very low. Most
acquisition happens through **outbound, conferences, founder LinkedIn presence,
and referrals.**

That shapes what the website is really *for*:

```
  A COMMON VIEW                  WHAT IS TRUE FOR capq.ai
  ───────────────────────        ──────────────────────────────────
  SEO mainly means ranking       The user arrives via a shared link or a
  higher in generic search       name heard in passing — already in the
                                 funnel, not found through search.

  The website is a               The website is a VERIFICATION and
  top-of-funnel acquisition      CONVERSION asset — where a prospect
  channel                        who is already curious decides.
```

A user who becomes curious from an outbound message typically spends **15–30
minutes** on capq.ai — reading the homepage, clicking into product pages,
checking the team, and looking for security and compliance signals before
booking a demo.

This points to a clear, deliberate focus: for capq.ai, the most valuable SEO
work is less about climbing generic search results and more about making sure
the website **converts the prospect who has already arrived.** The two
priorities that follow come directly from that.

### [T2.3] — Priority 1: Homepage conversion clarity

**Priority 1 brings the three content findings together into one coordinated
fix:** helping the homepage tell a researching user, quickly, what capq.ai is
and why to trust it.

The three findings, and the opportunity in each:

- **A clearer value proposition.** The hero headline — "Let AI Supercharge Your
  Fundraise" — is energetic and aspirational. Making it also state *who* capq.ai
  is for and *what* it does would help a user grasp the offer in the first few
  seconds, so the rest of the page gets a fair read.
- **External social proof.** The homepage shows strong internal numbers —
  "$455M+ invested" and "50+ deals closed." Adding customer logos, testimonials,
  and third-party endorsements would place external proof alongside them.
  capq.ai has 50+ real deals to draw on — an asset the homepage can surface.
- **More visible security messaging.** SOC2 compliance and data-security
  assurances are already present, currently within the FAQ. Bringing them near
  the sign-up area would place them exactly where an institutional researcher
  looks.

**Why this is Priority 1:**

```
  + The value proposition is the first thing a researching user reads —
    making it clear gives the rest of the page a fair chance.
  + Trust signals are exactly what an institutional researcher verifies.
  + capq.ai has real customers (50+ deals) — an asset ready to surface.
  + The fix is fully within capq.ai's control — no Google reranking.
  + It can ship in ~2 weeks and begin affecting demo conversion quickly.
```

### [T2.4] — Priority 1: the three-week fix plan

Priority 1 ships over three weeks:

```
  WEEK 1 — Strategy and assets
    - Founder interview to sharpen the ICP and the value proposition
    - Audit competitor homepage messaging (Affinity, DealCloud,
      Juniper Square) for positioning patterns
    - Draft 3 value-proposition options for founder approval
    - List existing customers from the 50+ deals; request logo and
      testimonial permissions
    - Inventory every trust signal (SOC2, funding, press, advisors)
      currently scattered or buried

  WEEK 2 — Homepage rewrite + on-page SEO
    - Rewrite the hero: clear value proposition, a specific outcome
      line, one primary CTA
    - Add a social-proof bar — 5-8 customer logos
    - Add an outcome-metrics section ($455M+ invested, 50+ deals),
      with named customers where possible
    - Add 2-3 testimonials with names and fund affiliations
    - Surface SOC2 and security badges above the fold, by the sign-up CTA
    - Refactor the FAQ so security and compliance come first
    - Optimise Title, Meta, H1, and H2 with primary keywords —
      this clears the keyword-distribution "D" grade from the audit

  WEEK 3 — Launch, QA, enablement
    - Mobile-responsive QA across the new homepage
    - Schema markup: Organization, SoftwareApplication, Review
    - Submit the updated sitemap to Google Search Console
    - Brief the sales team on the new messaging
    - Update outbound email and LinkedIn DM templates to match
    - Begin tracking demo-conversion rate week over week
```

**One point worth noting:** Week 2 includes the on-page keyword work (Title,
Meta, H1, H2). That is the *SEO bridge* inside a conversion-focused fix — it
clears the audit's one graded technical finding without making ranking the goal.

### [T2.5] — Priority 2, and what was deliberately not chosen

**Priority 2 — Brand SERP defense.** A search for the bare term "capq" does not
return capq.ai first; the results are currently held by 7+ unrelated entities
(among them the Cleveland Adaptive Personality Questionnaire, Capital Q
Ventures, and CAPQ BDC). Google clearly *can* identify the brand — the search
"capq ai" returns capq.ai #1 with rich sitelinks — so the work is to anchor the
brand entity to the bare term.

**Why it matters.** When a prospect hears the name and searches "capq," a clean
result — capq.ai owning the page — reinforces credibility at exactly the moment
they are checking that the company is real and established. A result that
instead mixes in unrelated organisations can leave a researching prospect
briefly unsure they have found the right company. Owning the brand SERP turns
that verification moment into a credibility gain for capq.ai.

**Why Priority 2, not Priority 1 — two reasons:**

- Fixing it depends partly on **Google reranking**, which is slow and not fully
  in capq.ai's control; even strong on-site signals take weeks to months to move
  the SERP.
- Most prospects from outbound and LinkedIn arrive at capq.ai **directly via a
  shared link**, bypassing the bare "capq" search entirely.

The fix runs in Weeks 4–5: on-site — strengthen the About page, add Organization
and Person schema, publish a founder-bylined post anchored to capq.ai; off-site
— a consistent LinkedIn brand entity and 2–3 industry pieces that link back.

**What was deliberately not chosen as a priority** — each with the reason:

```
  Build domain authority via backlinks  - many months to pay off;
                                          niche search volume too low
                                          to justify the spend now.
  Core Web Vitals for ranking           - the audience is not searching
                                          in volume, so ranking gains
                                          do not convert to revenue.
                                          (The mobile-LCP fix is still
                                          worth doing - for user
                                          experience, not ranking.)
  Disavow suspicious backlinks          - routine hygiene; the current
                                          profile is not penalised, so
                                          not impact-critical now.
  Fix the 178 broken links              - mostly LinkedIn redirects;
                                          minimal SEO impact.
```

This is the reasoning, not just the conclusion: each item is real, but none
changes revenue at capq.ai's current stage the way the two chosen priorities do.

### [T2.6] — Expected impact

Both priorities are stated here as **honest estimates**, with the reasoning —
not promises.

**Priority 1 — Homepage conversion clarity.** A clearer value proposition
alongside visible trust signals (logos, testimonials, surfaced SOC2) directly
addresses what a researching user needs in order to convert. The expectation
is **an increase in primary-CTA (demo) conversion** — the fix strengthens all
three levers at once (clarity, proof, trust), and surfaces capq.ai's real
customers rather than asking the reader to take the homepage on faith. The
Week 3 week-over-week tracking captures the actual figure.

**Priority 2 — Brand SERP defense.** Anchoring the brand entity to the bare term
"capq" does two things. It recaptures branded-search visitors — prospects who
heard the name and went looking. And, just as importantly, it strengthens
**credibility at the verification moment**: a prospect who searches "capq" and
sees capq.ai cleanly owning the result gains confidence they have found the
right, legitimate company. The volume is smaller than Priority 1 today, but the
credibility gain compounds as outbound and LinkedIn presence grow.

**Timeframe:**

```
  Priority 1   impact visible within ~2 weeks of ship — it depends
               only on capq.ai's own homepage, not on Google.
  Priority 2   weeks to months — it depends partly on Google reranking.
```

---

## TASK 3 · Growth Hacking

### [T3.1] — The idea

Emerging fund managers raising a fund often **announce it publicly on
LinkedIn** — *"first close"*, *"raising our Fund I"*, *"anchor LP"*. Google
indexes those posts. That public signal is the entry point.

**The mechanism in one line:** instead of buying a cold list or spending on
ads, use Google's index of LinkedIn to surface those posts → turn them into a
precision outreach list. **$0 ad spend.**

**How it works, at a glance — four steps:**

```
   1  SURFACE     find the posts (Google-index search)
        ▼
   2  MINE        read the engagement on each post
                  (commenters > reactors)
        ▼
   3  FILTER      keep emerging fund managers who fit capq.ai's user
        ▼
   4  REACH OUT   send a personal message that references their post
```

The next slides take this from a one-line idea to a testable claim, the full
workflow, what was built, the math to 30+ leads, and how it scales.

### [T3.2] — The hypothesis

The mechanism makes one clear, testable claim:

> **If** we surface LinkedIn posts where emerging fund managers publicly
> signal that they are raising a fund — and capq.ai reaches out at that
> moment — **then** the mechanism can generate **30+ qualified leads in two
> weeks, at $0 ad spend.**

It is a genuine hypothesis because it can be proven wrong: it names a number
(30+), a timeframe (two weeks), and a cost ($0 ad spend). If a two-week run
produces fewer than 30 qualified leads, or needs paid ads to get there, the
claim fails.

*(A "qualified lead" is defined precisely in T3.6 — in short: an emerging fund
manager who fits capq.ai's user, identified and contacted.)*

**Why the claim should hold — two reasons:**

```
   1  INTENT IS SELF-IDENTIFIED
      These are not cold names. Each person has publicly
      posted that they are raising a fund — they have
      already raised their own hand.

   2  THE TIMING IS RIGHT
      capq.ai reaches them while fundraising is their
      active, current problem — not at a random moment.
```

A cold outreach list has neither advantage: it *guesses* who might be raising,
and reaches them at a random time. This mechanism replaces both guesses with a
public, dated signal.

### [T3.3] — The workflow

The mechanism is four steps. The first is automated by the tool (T3.4); the
rest are designed and currently done by a person — automating them honestly is
the next stage (T3.7).

```
   Google's index of LinkedIn (public posts)
            │
   1  SURFACE       (tool)   precision queries find posts where an
        ▼                    emerging fund manager publicly signals
                             they are raising a fund.
   2  MINE          (human)  on each post, read the comments first
        ▼                    (commenters have the highest intent),
                             then the reactors.
   3  FILTER        (human)  click into each person's profile. Keep
        ▼                    Founders / Co-founders / fund managers
                             at an emerging fund. Drop investors,
                             consultants, and service providers.
   4  REACH OUT     (human)  send a personal message that references
                             their actual post — acknowledge the raise,
                             then a relevant capq.ai angle.
```

**The queries are aimed at capq.ai's actual user.** An earlier draft of the
mechanism used phrases like *"seed round"* and *"looking for investors"* —
those target **startup founders**, not capq.ai's user. The queries have been
re-aimed to **fund-manager language**, and organised into **precision tiers**:

```
   TIER 1  First-person raise announcements      (highest signal)
           "held our first close" · "raising our first fund"
           "launching our first fund" · "closed our first fund"

   TIER 2  Emerging-manager identity              (combine with Tier 1 or 3)
           "emerging manager" · "first-time fund manager"
           "solo GP" · "debut fund" · "Fund I"

   TIER 3  LP-relationship signals                (combine with above)
           "anchor LP" · "LP commitments" · "soft commitments"

   TIER 4  Noise — the scorer SUBTRACTS these     (see T3.4)
           "guide" · "tips" · "Fund IV/V/VI" · "webinar"
```

Combining tiers in each query — e.g. `"first close" "emerging manager"`,
`"solo GP" "raising"` — narrows the surface from "anyone raising any money" to
"the user capq.ai is built for." A small wording change with a large effect.

### [T3.4] — The prototype

A small, $0, ToS-safe tool that **automates Step 1 — the safe half** of the
mechanism. It is built, tested, and published.

**What it does:**

```
   queries.yml  →  SerpAPI (Google search) → LinkedIn post results
                                                     │
   ranked contact list  ◄── rate ◄── dedupe ◄── extract author
   (sample-output.md)                              (name + profile)
```

**Why the prototype only automates Step 1.** Step 1 stays inside Google's index
— the tool **never opens linkedin.com directly**, so there is no Terms-of-
Service or account-ban risk. Steps 2–4 are deliberately left to a human, for
three real reasons:

```
   STEP 2  Mine engagement (commenters, reactors)
           Reading who commented requires loading the LinkedIn
           post page directly. Both options are blocked:
             - Scraping LinkedIn → against LinkedIn's ToS,
               account-ban risk.
             - LinkedIn's official APIs → do not expose post
               engagement to third parties for this use case.

   STEP 3  Filter profiles  (is this person actually an emerging
           fund manager?)
           Two blockers: it needs reading the full LinkedIn
           profile (same ToS issue as Step 2), AND it is a
           judgment call no simple heuristic does reliably.
           Our own verification proved this — 7 of 12 strong-
           looking candidates were excluded on review (fund
           employees, name mismatches) — exactly the kind of
           call only a person catches.

   STEP 4  Direct outreach
           Automating LinkedIn messages = the same ToS / ban
           risk. And the mechanism's edge IS the message being
           genuinely personal — referencing the specific post in
           a way that lands. Automated mass-personalisation
           reads as spam and undercuts the whole approach.
```

These are not shortcuts skipped — they are the boundary the tool deliberately
respects. The prototype automates what is **safe, scalable, and
judgment-free**; the rest stays human, and a careful automation of the next
stage is in T3.7.

**How it rates posts — simple and transparent:**

```
   score  =  (signal words × 2)   −   (noise words)

   SIGNAL  drawn from Tiers 1–3 (T3.3)     each match: +2
           "first close" · "raising our" · "anchor LP" ...
   NOISE   drawn from Tier 4 (T3.3)        each match: −1
           "guide" · "tips" · "Fund IV/V/VI" · "webinar" ...
```

The score is a **sorter**, not a verdict — it pushes likely-real raises to the
top so a person reviews those first. The score never decides "this is a lead."
A human always confirms.

**The real run — and what it proves:**

```
   16 searches         →   126 candidate contacts
                           (sample-output.md, in the repo)

   12 strongest checked →  5 VERIFIED — real emerging fund managers
                           (verified-leads.md, in the repo)
```

**The 5 verified leads — real people, real funds:**

| # | Name | Fund | Role | The raise (verified) |
|---|------|------|------|----------------------|
| 1 | Joseph Alalou | Daring Ventures | Co-founder & GP, first-time fund manager | raising the firm's debut fund |
| 2 | Nader Amiri | Homegrown Ventures 🇦🇪 | Co-founder | closed debut Fund I at **$22.8M** (beat $20M target) |
| 3 | Saum Vahdat | Bridgewest Ventures 🇳🇿 | CEO | Fund I — **$55.3M first close**, ahead of target |
| 4 | Avijeet Alagathi, CFA | Veda VC 🇮🇳 | Co-founder | first close of **$30M** fund (₹150 Cr committed) |
| 5 | Rabeel Warraich | Sarmayacar 🇵🇰 | Founder & CEO | first close of debut **$30M** fund |

**Each lead — profile + the post that surfaced them:**

- **Joseph Alalou** · https://www.linkedin.com/in/josephalalou · *"we've been raising our first fund, and here's…"*
- **Nader Amiri** · https://www.linkedin.com/in/nader-amiri-cpg · *"we just closed our first fund, and this…"*
- **Saum Vahdat** · https://www.linkedin.com/in/saum-vahdat · *"proud to be launching our fund alongside…"*
- **Avijeet Alagathi** · https://www.linkedin.com/in/avialagathi · *"Veda VC announces first close of its $30M fund"*
- **Rabeel Warraich** · https://www.linkedin.com/in/rabeel-warraich-572a5714 · *"excited to announce the first close of Sarmayacar…"*

The assessor can click any of these and verify them. These 5 are **proof the
candidates the tool surfaces are real, clickable people** — they are
evidence, **not** the mechanism's yield. The actual lead count lives in T3.5.

**Repo (Task 3's working link):**
https://github.com/giaptran4work-tech/capq-lead-discovery

### [T3.5] — Launch plan + funnel math

A two-week launch — the mechanism running end to end.

```
   WEEK 1
     - Run the tool across the full query set (one --full sweep
       per workday; ~16 searches each = well inside the free
       SerpAPI tier's 100/month).
     - Sort the ranked output. Mine engagement on the top posts.
     - Click into commenter profiles. Filter to emerging fund
       managers who fit capq.ai's user.
     - Begin first-touch outreach — personal, referencing each
       person's actual post.

   WEEK 2
     - Continue outreach.
     - Send follow-ups (one nudge after 3-4 days).
     - Book demos / calls with respondents.
     - Tighten the queries based on what landed best.
```

**The funnel math — a single run already exceeds the 30+ target:**

```
   1 SURFACE    16 searches per --full run
                →  ~126 candidate contacts
                   (observed in the built prototype, T3.4)

   2 VET        × ~40% genuine emerging-manager raises
                   (the rate from 5 verified out of 12 hand-checked)
                →  ~50 qualified leads — from ONE run.

   3 SCALE      Two weeks → multiple runs + engagement mining
                →  comfortably above 30+, with quota to spare
                   (free SerpAPI tier = 100 searches/month).
```

So the 30+ figure is not a stretch — it is the funnel applied to what the
prototype **actually produced** from one small run. The numbers reach the
target without leaving the free tier and without spending a dollar on ads.

### [T3.6] — Success metrics

Every metric is measurable and has a stated target.

```
   Candidates surfaced (tool)   per run     target  ~100+ / run
   Vetting pass-rate            % genuine   target  ≥30%
   Qualified leads (the goal)   count       target  30+ in 2 weeks
   Outreach messages sent       count       target  ≥30
   Reply rate                   % replied   target  ≥15%
   Calls / demos booked         count       target  ≥5
   Cost                         dollars     target  $0
```

**Qualified lead — precise definition.** A *qualified lead* is a person who
meets **all four**:

```
   ✓  Identified by name AND with a verified LinkedIn profile
   ✓  Confirmed as an emerging fund manager (Fund I–III) currently
      or recently raising a fund — verified against the original
      post and a public source
   ✓  ICP-fit for capq.ai (the user described in Task 1)
   ✓  Contacted with a personal first-touch message
```

Anyone who fails any of the four is **not** counted toward the 30+ target.
That keeps the number honest.

### [T3.7] — Scaling

The mechanism's real ceiling is set by the manual half — Steps 2–4. Three
moves take it from a per-week practice to a continuous engine.

```
   1  AUTOMATE THE ENGAGEMENT-MINING LAYER  (Step 2)
      The designed next step. It needs a tool that reads commenters
      and reactors on each surfaced post — which means LinkedIn-side
      access, handled carefully (an official partner API, or an
      opt-in browser helper the user runs in their own session;
      never automated scraping).

   2  WIDEN THE SURFACE
      - Expand the query set inside the existing tool.
      - Add a post-recency filter so only recent raises surface.
      - Bring Reddit, niche Substacks, and conference attendee lists
        into the same pipeline.

   3  PRODUCTIONISE THE PIPELINE
      - Templatise the outreach and A/B test angles.
      - Push qualified leads straight into capq.ai's CRM.
      - Hand the loop to a VA or a scheduled cron, once the
        conversion numbers are stable.
```

Each step adds capacity without adding ad spend — and each is independent, so
they can be added in any order as the mechanism scales.

---

## CLOSE

**Working links — all live, all clickable**

- **Task 1 — Workflow #1 (Competitive Intelligence, built)**
  - Live demo: https://giaptran4work-tech.github.io/cq-competitive-intel/
  - Repo: https://github.com/giaptran4work-tech/cq-competitive-intel

- **Task 2 — SEO audit and fix plan**
  - The full audit, with screenshots, lives in this deck — see the
    **Appendix (A1–A3)** that follows. No external file.

- **Task 3 — Lead-discovery prototype**
  - Repo (code + README + a real sample run):
    https://github.com/giaptran4work-tech/capq-lead-discovery

---

Three tasks, three self-contained stories — one submission.

---

## APPENDIX · SEO audit detail

### [A1] — Appendix: Technical audit detail

**Tools:** Google PageSpeed Insights, SEOptimer.

- **Page speed.** Mobile Largest Contentful Paint measured at **4.6 seconds** —
  inside the "poor" band (above the 4-second threshold). Desktop performance is
  healthy. `[screenshot: PageSpeed Insights — mobile result]`
- **Indexability & crawlability.** Healthy. The audit's AI Visibility score is
  **100/100**. `[screenshot: indexability / AI visibility]`
- **Broken links.** **178 broken links** flagged out of ~2,000 URLs scanned.
  Almost all are external LinkedIn redirects — low SEO impact.
  `[screenshot: Dr Link Check result]`
- **Keyword distribution — graded D.** capq.ai's main keywords (*deal, product,
  start, profiles, ai data, ai concierge, chasing lp, 150k lp, lp profiles, cold
  email*) are largely missing from the Title, Meta Description, and Heading
  tags. Keywords carry more ranking weight when they appear consistently across
  these tags. `[screenshot: SEOptimer keyword distribution]`

### [A2] — Appendix: Content and backlink detail

**Content findings (homepage).**

- **Value proposition.** The hero headline "Let AI Supercharge Your Fundraise"
  is aspirational but does not communicate what the platform does, or for whom —
  a first-time visitor may not realise it is an LP-discovery and
  fundraising-workflow tool. `[screenshot: homepage hero]`
- **Social proof.** The only trust signals are internal metrics ($455M+
  invested, 50+ deals closed) — no customer logos, testimonials, or third-party
  endorsements. `[screenshot: homepage social-proof area]`
- **Security messaging.** SOC2 compliance and data-security assurances sit deep
  in the FAQ, rather than near the sign-up areas where a researcher looks.
  `[screenshot: FAQ — security entry]`

**Backlink findings.** *Tools: SEOptimer, Dr Link Check.*

- **Authority.** Domain Strength **24**, Page Strength **6** — a modest profile.
  Total backlinks **146** across **61 referring domains**.
  `[screenshot: backlink authority]`
- **Quality.** A few low-quality referring domains appear (justpaste.me,
  takes.sbs, drjack.world, atomizelink.icu, bye.fyi) — typical low-quality
  directory links. `[screenshot: referring domains]`
- **Institutional links.** Zero `.edu` backlinks and only 2 government backlinks
  — limited institutional-credibility signals.

### [A3] — Appendix: Competitive / brand-SERP detail

**Tools:** Google site search, incognito SERP checks.

- **The bare term "capq".** capq.ai does **not** rank #1. The first page is
  dominated by 7+ unrelated entities: the Cleveland Adaptive Personality
  Questionnaire, Verista CAPQ, Changi Animal and Plant Quarantine, Capital Q
  Ventures, CAPQ BDC, CAPQH, and InDevR 5'CapQ.
  `[screenshot: incognito SERP — "capq"]`
- **The disambiguated term "capq ai".** capq.ai ranks **#1**, with rich
  sitelinks. `[screenshot: SERP — "capq ai"]`
- **What this means.** Google can already identify the brand correctly once the
  query is unambiguous — so the brand-SERP work (Priority 2) is about anchoring
  the brand entity to the bare term, not teaching Google the brand from scratch.
