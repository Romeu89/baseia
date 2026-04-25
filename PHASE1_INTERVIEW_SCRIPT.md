# Phase 1 Interview Script - Steps 3+

**Purpose:** Unlock CUSTOMER_JOURNEY.md steps 3-8 in a single 30-min sprint with Romeu. Replaces the 10-turn interactive dialogue.
**Scope:** Post-wedge journey (primeiro contato through retention/expansion). Steps 1-2 already LOCKED.
**Format:** Each Q has purpose, context, direct question, answer scaffold (multiple-choice where possible), follow-up probes.
**Usage:** Romeu answers each Q in order. For MCQs, pick letter(s) plus one-line rationale. Free-text where scaffold is insufficient.
**Constraint:** Questions map to CUSTOMER_JOURNEY Phase 2 table columns (action, input, output, system touchpoint, comm trigger, decision buttons, validation pattern).

---

## Step 3 - Primeiro Contato (after wedge submit)

### Q1 - What arrives in the solo founder inbox immediately after CNPJ submit?
**Purpose:** Defines step 3 input/output and the first comm trigger.
**Context:** Step 2 ends with {email, CNPJ, trigger_self_report, headline_variant} captured. Step 3 is what happens next that the user notices. Unit 2 retention-at-D7 metric is meaningless without knowing what gets sent on D0.
**Question:** What does the user experience in the first 5 minutes after submitting the wedge form?
**Answer scaffold (multiple choice, can pick multiple):**
- (A) Email auto-responder with regularization next steps, no human touch
- (B) Email + WhatsApp message with a calendar link to book 15-min call
- (C) Email + inline product walkthrough (landing page -> tour page, no auth yet)
- (D) Email + auto-provisioned sandbox login to a limited BaseIA demo account
- (E) Just email, user must re-engage via cold nurture after 3 days
**Follow-up probes:** If (B): who takes the call, Romeu or future operator? If (D): what does the sandbox show - dummy data or live scraping of their own financial docs?

### Q2 - Who owns the first human conversation?
**Purpose:** Decides if step 3 is AI-executable or human_in_loop in the AI execution map.
**Context:** The shape locked solo founder as persona. If Romeu himself takes the call, step 3 is human_in_loop forever. If an AI chatbot qualifies, step 3 may be ai_executable_at_scale.
**Question:** Who handles the first conversation that requires back-and-forth?
**Answer scaffold:**
- (A) Romeu personally (founder-led, not scalable past ~20 clients)
- (B) Async AI agent (WhatsApp/email bot answers common questions, escalates to Romeu on edge cases)
- (C) Tiered: AI handles routing; live person (Romeu or contracted contador) handles substance
- (D) No conversation - fully self-serve flow
**Follow-up probes:** If (A): what is the volume cap before this breaks? If (B): what questions DOES the bot answer vs. escalate?

### Q3 - What does a successful step 3 look like (validation threshold)?
**Purpose:** Sets unit 3 validation_pattern. Without a measurable success signal, unit 3 cannot be classified ai_executable_at_scale per AI_EXECUTION_MAP rule.
**Context:** Step 2 has a conversion metric (landing -> submit). Step 3 needs its own measurable exit state.
**Question:** What concrete event proves step 3 succeeded for a given user?
**Answer scaffold:**
- (A) User books a call (calendar link click-through rate >N%)
- (B) User replies to the email with a question (reply rate >N%)
- (C) User uploads first financial document to sandbox (upload rate >N%)
- (D) User completes regularization flow end-to-end (form completion >N%)
- (E) User is still engaged at D7 (retention metric already in unit 2)
**Follow-up probes:** What numeric N feels right for the chosen metric? What minimum sample size before this metric becomes binding?

---

## Step 4 - Onboarding (produto real, nao mais wedge)

### Q4 - When does regularization deliverable hand off to BaseIA product proper?
**Purpose:** Step 4 marks the wedge-to-product transition. This is the KEY risk point in the Contabilizei-style funnel (Finding 4 of research).
**Context:** Wedge CNPJ is topic-of-funnel service; BaseIA real product is back-office recurring (conciliacao, prestacao de contas). These are different UX surfaces. The transition moment is fragile.
**Question:** How is the CNPJ-regularized user introduced to the ongoing BaseIA product?
**Answer scaffold:**
- (A) At regularization completion, auto-enrolled in free trial of back-office product
- (B) Email sequence starts D30 post-regularization, separates the two products explicitly
- (C) Single product: regularization service includes ongoing monthly compliance = BaseIA is the monthly service
- (D) User opts in on wedge form with a checkbox I want ongoing back-office help
- (E) Manual Romeu outreach - no automated handoff yet
**Follow-up probes:** What % drop-off is acceptable at the wedge-to-product boundary? Is the regularization service free forever or a freemium-to-paid transition?

### Q5 - What is the minimum product state at first login?
**Purpose:** Defines step 4 io_signature (input) and system touchpoint. Needed for SDD unit 4 hash.
**Context:** Solo founder has low tech literacy. A blank product = abandonment. Pre-populated = setup friction.
**Question:** When the solo founder logs into BaseIA for the first time, what is already there?
**Answer scaffold:**
- (A) Empty canvas - user uploads their own docs to see anything
- (B) Pre-populated with CNPJ data from Receita Federal (seeded by regularization step)
- (C) Pre-populated PLUS first month of bank statement imported via Pluggy/Belvo open-banking (one-click consent during regularization)
- (D) Pre-populated AND a mock-demo-data mode to click-through before connecting real data
**Follow-up probes:** If (C): what banks supported at MVP? If (D): is demo-mode isolated from real account to avoid confusion?

### Q6 - What requires the user to do something, and what does BaseIA do for them?
**Purpose:** Sets ai_role per SDD Phase 4 vocabulary (none/assist/execute/autonomous) for units 4+.
**Context:** Persona is low literacy, short on time. Every user action is a drop-off risk. Every zero-action magic moment is also a trust risk.
**Question:** At first login, does BaseIA auto-execute the first conciliation/prestacao run, or wait for user approval?
**Answer scaffold:**
- (A) Auto-run then show result for user review (ai_role=execute, human approval after the fact)
- (B) Wait for explicit click Run on each task (ai_role=assist)
- (C) Run the first task to show value, then ask user to approve future runs as default (mixed)
- (D) Fully autonomous - run, commit, notify. User overrides only via dispute flow.
**Follow-up probes:** What is the escalation_rule when AI is unsure? What is the golden-output validation pattern for the first conciliation run?

---

## Step 5 - Primeira Win

### Q7 - What is the first tangible win the user experiences?
**Purpose:** Step 5 is the moment that converts trial-mindset into paying-mindset. Defines the wow output.
**Context:** For trigger (a/c) audience (operational urgency), the win is back-office done without hiring. For (b) (control), the win is finding an error. For (d) (FOMO), the win is I used AI and it worked. Comm tone differs, but the underlying WIN must be a single measurable event.
**Question:** What is the ONE concrete output that proves BaseIA delivered?
**Answer scaffold:**
- (A) First auto-generated conciliacao report passes without edits
- (B) An error/discrepancy is surfaced that the user would otherwise have missed (trust-building)
- (C) The user receives a ready-to-file prestacao de contas at month-end, zero manual work
- (D) A dashboard shows X hours saved this week via auto-categorizacao
- (E) User-selectable - they set what a win means for them during onboarding
**Follow-up probes:** Is the win guaranteed by end of D7 / D14 / D30? Is it surfaced via push notification, email, or in-app only?

### Q8 - How is the first win validated as correct (not just generated)?
**Purpose:** Validation_pattern for unit 5. AI-executable requires a measurable check - golden output vs human review vs n8n webhook.
**Context:** First win that looks right but is wrong kills trust forever with a low-literacy persona. The validation must run BEFORE the win is shown.
**Question:** Before BaseIA shows the first-win output to the user, how does the system verify accuracy?
**Answer scaffold:**
- (A) Human-in-loop checkpoint: Romeu or contador reviews first 3 outputs per client
- (B) Golden-output comparison: the AI output is checked against a rule-based reference (deterministic conciliacao as baseline)
- (C) Confidence-score gate: if AI confidence <X%, route to human; if >=X%, auto-ship
- (D) Mixed: (A) for first client, then (B) or (C) at scale
**Follow-up probes:** What failure rate is the budget? (1 in 100, 1 in 1000, zero tolerance?) At what scale does (A) stop being feasible?

---

## Step 6 - Retention / Recurring

### Q9 - What is the first paywall event?
**Purpose:** Defines the monetization moment. Step 6 is where regularization wedge (free) transitions to recurring (paid).
**Context:** Research finding 4 (Contabilizei): wedge drives registration; upsell is the ACTUAL growth metric. BaseIA needs the same two-phase validation.
**Question:** At what user state does the paywall appear?
**Answer scaffold:**
- (A) After N successful conciliation runs (proof of value gated by volume)
- (B) At the end of the first month (time-based trial, always converts at D30)
- (C) Immediately post-regularization (pay to unlock ongoing service)
- (D) Never - freemium forever; revenue comes from add-ons (contador-on-demand, reports, filings)
- (E) Usage-based: free tier with a doc-count cap, upgrade when cap hit
**Follow-up probes:** What price point feels right for a solo founder (R$50, R$150, R$300, more)? Monthly or annual first pitch?

### Q10 - What keeps the user engaged between month-end close cycles?
**Purpose:** Back-office is a monthly cadence. User may forget BaseIA exists for 25/30 days. Step 6 validation pattern needs a stickiness signal.
**Context:** Churn for monthly-cadence products is driven by user never re-opens the app. Need a reason to come back mid-cycle.
**Question:** What triggers the user to open BaseIA between monthly closes?
**Answer scaffold:**
- (A) Push notification when an unusual transaction is detected
- (B) Weekly digest email (cash position, pending items, action required)
- (C) Contador escalation - contador pings the user via BaseIA inbox when something needs attention
- (D) Nothing - monthly cycle is enough; engagement gap is acceptable
**Follow-up probes:** If (A): what is an unusual transaction in the algorithm (threshold, category, pattern)? If (D): what is the churn rate tolerance?

---

## Step 7+ - Expansion (deferred scope)

### Q11 - Does Phase 1 lock through retention (step 6) or extend into expansion/upsell?
**Purpose:** Scope discipline. Phase 1 only has to define enough to SDD-lock. Expansion may belong in Phase 2 of product roadmap.
**Context:** ULTRAPLAN scope is customer journey in the lifecycle sense, but steps 7+ (upsell, referral, contador layer, multi-entity) can explode scope if not bounded.
**Question:** Where does Phase 1 STOP?
**Answer scaffold:**
- (A) At step 6 (first paying month). Steps 7+ deferred to later phase.
- (B) Extend one step: step 7 = first-referral event (user tells another solo founder).
- (C) Extend two steps: step 7 = referral, step 8 = expansion within same client (multi-CNPJ, contador add-on).
- (D) Full lifecycle 7 steps up to churn/cancel event.
**Follow-up probes:** If (A): what is the Phase 2 trigger to unlock steps 7+ (N paying clients, M months, revenue threshold?)

---

## Meta questions (affect all steps 3+)

### Q12 - Is the other trigger path (Finding 3 of REMOTE_REVIEW) defined now or deferred?
**Purpose:** Step 1 has a/b/c/d + other. REMOTE_REVIEW Finding 3 notes other has no downstream routing today. Interview must decide: add 5th comm tone now, or defer.
**Context:** Realistic funnel will see 10-20 percent other responses from day 1.
**Question:** Does the other bucket route to:
**Answer scaffold:**
- (A) Generic operational nurture + Romeu weekly review (quick fix)
- (B) Free-text follow-up question - LLM classifies into 4 existing buckets or expands taxonomy
- (C) Drop them - ICP mismatch, no follow-up
- (D) Defer to Phase 2 iteration
**Follow-up probes:** If (B): what is the review cadence for new taxonomy categories?

### Q13 - Is the abrir CNPJ visitor (Finding 10 of REMOTE_REVIEW) routed or excluded?
**Purpose:** Any SEO/paid on CNPJ keyword brings pre-revenue visitors who do not match ICP. Unit 2 conversion is poisoned if they count.
**Context:** Sub-flavor locked to regularizar but the keyword surface is shared.
**Question:** The abrir-CNPJ visitor lands on the wedge. What happens?
**Answer scaffold:**
- (A) Gate question CNPJ ja existe? filters at top of form
- (B) Redirect to partner (Contabilizei-style abertura service) for affiliate kickback
- (C) Route to waitlist - capture email, nurture until they are existing-CNPJ
- (D) Accept them into the flow; treat as a separate ICP cohort with different metrics
**Follow-up probes:** If (A): what is the estimated drop-off at the gate?

### Q14 - Unit 1 circularity (Finding 2 of REMOTE_REVIEW) - collapse or add pre-landing signal?
**Purpose:** Decides SDD structure. Collapsing unit 1 into unit 2 vs. keeping it separate changes the journey row count.
**Context:** Current unit 1 validation runs entirely inside unit 2 (questionnaire after submit). No independent observability.
**Question:** How should unit 1 be restructured?
**Answer scaffold:**
- (A) Collapse into unit 2 (single landing-page-captures-trigger-intent unit)
- (B) Keep unit 1 separate; add ad-impression or paid-panel survey as pre-landing signal
- (C) Keep unit 1 as human_in_loop only (accept it is not system-measurable)
- (D) Defer decision; revisit during Phase 4 SDD lock
**Follow-up probes:** If (B): what budget exists for a panel survey? If (C): how does human_in_loop interact with the trigger segmentation in comms?

### Q15 - Should validation_pattern feed the unit hash (Finding 7 of REMOTE_REVIEW)?
**Purpose:** Schema-level decision on drift detection. Affects hash_units.py contract and SDD round-trip.
**Context:** Today, hash covers phase_id + customer_action + io_signature + decision_buttons. Validation drift is invisible. Finding 7 proposes extending the hash.
**Question:** Extend the hash to include validation_pattern?
**Answer scaffold:**
- (A) Yes - add validation cell from CUSTOMER_JOURNEY row to the hash payload (simpler)
- (B) Yes - add a separate validation_hash field stored in SDD.md (cleaner separation)
- (C) No - accept manual review of validation drift; keep hash narrow
- (D) Defer - Phase 2 post-mortem after first real edit cycle
**Follow-up probes:** If (A) or (B): who updates hash_units.py self-test matrix?

---

## Appendix - Mapping of Q to journey columns

| Q | Journey column primarily affected | SDD unit |
|---|----------------------------------|----------|
| Q1 | Customer action, Input, Output, System touchpoint | Unit 3 |
| Q2 | System touchpoint, Comm trigger, ai_role | Unit 3 |
| Q3 | Validation pattern | Unit 3 |
| Q4 | Customer action, Decision buttons | Unit 4 |
| Q5 | Input, System touchpoint | Unit 4 |
| Q6 | ai_role, Validation pattern | Unit 4 |
| Q7 | Customer action, Output | Unit 5 |
| Q8 | Validation pattern, escalation_rule | Unit 5 |
| Q9 | Decision buttons, Customer action | Unit 6 |
| Q10 | Comm trigger | Unit 6 |
| Q11 | Phase scope | Meta |
| Q12 | Comm trigger (step 1 revisit) | Unit 1 |
| Q13 | Decision buttons (step 2 revisit) | Unit 2 |
| Q14 | Schema (unit 1 structure) | Units 1-2 |
| Q15 | Hash contract | Meta |

Estimated total answer time: 30 min if Romeu picks letters + one-line rationales. Double if he writes prose.
