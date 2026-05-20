# Marketing Pain Points — capq.ai

> What CQ's marketing is *not* doing that it should, observed from `/`, `/insights`, `/handbook`, and the 404 on `/about`. These are the gaps that AI workflows could meaningfully close.

## Top observed gaps

### 1. Credibility floor is too low for a B2B SaaS selling to capital allocators

- **Symptom.** Every proof point on the homepage is **internal** ("$455M invested by our team", "50+ deals closed by our team"). Zero external logos, named testimonials, case studies, or media coverage. The `/about` page returns 404. No security/compliance badges (SOC 2, ISO) despite handling LP PII.
- **Why it matters.** Their buyer (an emerging GP) is themselves selling trust to LPs. They will not adopt a fundraising platform that itself has no visible trust signals. This is the *most expensive* gap: it suppresses paid-ads conversion, organic-search conversion, and outbound-reply rates simultaneously.

### 2. Content is bulk-published, anonymously bylined, and ranks-only-because-keyword-density

- **Symptom.** ~67 articles on `/insights` all dated **"Dec 2025"** (likely a single AI-generated drop, or template-date bug). No bylines anywhere. No engagement signals (no comments, shares, dates of update). Internal linking is shallow. No newsletter capture, no original data.
- **Why it matters.** Google's helpful-content and E-E-A-T systems specifically target this pattern. Even if it ranks today, the ranking will decay. Worse, a sharp prospect lands on a post and immediately reads it as machine-generated — which kills the founder-led credibility the homepage tries to build. The content marketing is actively *degrading* the brand right now.

### 3. Three inconsistent voices = no coherent positioning

- **Symptom.** Homepage = founder-led, conversational, "built by an asset manager". Handbook = systematic, curricular, authoritative. Insights = generic, anonymous, SEO-templated. The same prospect moving across these surfaces sees three different companies.
- **Why it matters.** Buyers piece a vendor together from many touchpoints. Inconsistency reads as "not really a real company". This compounds the credibility floor problem.

### 4. No competitive defense despite an aggressive positioning claim

- **Symptom.** Homepage claim: "the only platform covering all 8 stages, while alternatives only cover 2–3". Yet **no competitor is named, compared, or refuted anywhere** on the site. No comparison page, no battlecards-as-content, no "vs. Affinity / vs. DealCloud / vs. Carta" pages.
- **Why it matters.** Buyers who hear that claim immediately search "capq.ai vs [competitor]" — and find nothing CQ-controlled, only competitor SEO. They lose the high-intent moment to competitors who *do* run comparison content.

### 5. Top-of-funnel personalization is zero despite a data-rich product

- **Symptom.** One homepage for all visitors. Same hero, same value props for a venture GP, a PE GP, a hedge-fund manager, and a secondaries shop — even though CQ's own product matches LPs by mandate type. No traffic-source-aware landing pages, no segmented case studies, no segmented social proof.
- **Why it matters.** Their *product* is precision targeting; their *marketing* is broadcast. The mismatch is both a conversion-rate cost and a credibility cost (the marketing experience contradicts the product promise).

## Where AI could create leverage

Each opportunity tied to a gap above.

- **Lead scoring (Gaps 1, 5).** Free-tier signups arrive with thin form data (email + name). AI enrichment + scoring would let sales prioritize the ~15% of signups that are real emerging GPs vs. analysts, students, and competitors. Routes the highest-fit signups to a same-day human follow-up.
- **Competitive intelligence (Gap 4).** Weekly automated scan of competitor product/pricing/blog pages → diff detection → 1-page brief for the marketing lead. Both defensive (know when they ship features) and offensive (generate "vs." content from their own marketing claims). CQ is literally the type of company that should publish a "State of Fundraising Software" map and own that SERP.
- **Customer research (Gaps 3, 5).** Scrape LinkedIn posts + Reddit (r/venturecapital, r/privateequity) + niche Substacks for emerging-GP language and pain. Cluster the themes. Feed into a content-brief generator that produces *original*, voice-consistent posts — the opposite of the current bulk anonymous output.
- **Personalization engine (Gap 5).** Dynamic homepage hero + landing-page hero that rewrites based on referrer / UTM (PE vs VC vs HF). Could be done client-side via AI on a CDN edge function in under a day.
- **Data analysis / original research (Gaps 1, 2).** They sit on 150K LP profiles. Anonymized aggregate trend reports ("LP allocation trends Q1 2026", "Which mandate types are funding what stage") published as quarterly reports + LinkedIn snippets — instantly differentiated, instantly link-worthy, immediately fixes the trust + E-E-A-T + thought-leadership problem at once.

## Constraints / context

- **Team size unknown, likely small.** The site signals founder/operator-led; no team page; no careers link. Workflows should assume a single marketer or founder-marketer running them — no large MarOps stack.
- **Regulatory.** They sell to SEC-regulated capital allocators. Anything that touches LP outreach or personalization must respect the marketing-rules constraints CQ themselves teach in the handbook. For *CQ's own* marketing this is less constraining (B2B SaaS to GPs), but workflows should avoid scraping LP data from public sources.
- **Brand voice.** The "founder-led, battle-tested" voice on the homepage is their strongest asset. Workflows that produce content must *preserve* this voice — not produce more anonymous bulk.
- **Optimize for "1 marketer's full week"** of leverage, not "10 marketers + ops stack". The brief asks for force multiplication, not enterprise scale.
