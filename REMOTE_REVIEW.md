# Remote Review - Phase 1 Scaffolding Artifacts

**Run date:** 2026-04-24
**Branch:** claude/phase1-remote-review (stacked on claude/phase1-interview)
**Scope:** Critical review of CUSTOMER_JOURNEY.md, SDD.md, AI_EXECUTION_MAP.md, _tools/hash_units.py.
**Constraint:** Nothing in the NEVER list was edited. No decisions locked. Proposals only.

## Pre-flight verification

| Check | Result |
|-------|--------|
| Git identity scoped to romeuhrechdan@gmail.com | PASS |
| gh auth status | PASS (authenticated as romeuhr) |
| Python version | 3.14.4 (meets 3.11+ requirement) |
| _tools/hash_units.py --self-test | PASS: 22/22 checks |
| _tools/hash_units.py (drift) | PASS: 2 units hashed, no drift |
| Branch created | claude/phase1-remote-review from claude/phase1-interview at SHA e4e0598 |

---

## Summary of findings

| # | Title | Artifact | Type | Severity |
|---|-------|----------|------|----------|
| 1 | X threshold in unit 2 validation is untestable as written | SDD.md unit phase_id=2 | weakness | blocking |
| 2 | Unit 1 validation has a logical circularity; it assumes step 2 already happened | SDD.md unit 1 / CUSTOMER_JOURNEY row 1 | gap | important |
| 3 | which_trigger enum allows other but no downstream routing handles it | CUSTOMER_JOURNEY row 1 / SDD unit 1 / AI_EXECUTION_MAP row 1 | gap | important |
| 4 | AI_EXECUTION_MAP classifies unit 2 as ai_executable_at_scale despite non-empty missing_infra | AI_EXECUTION_MAP row 2 | misclassification | important |
| 5 | hash_units.py silently drops rows with <8 columns | _tools/hash_units.py lines 116-117 | weakness | minor |
| 6 | canonical_buttons fallback splits on  /  - breaks for tokens containing  /  | _tools/hash_units.py lines 56-58 | weakness | minor |
| 7 | Hash input does not include validation_pattern; silent validation edits invisible to drift | _tools/hash_units.py + SDD.md schema | gap | important |
| 8 | Step 2 decision buttons mix 3 semantic classes; sorted hash loses semantics | CUSTOMER_JOURNEY row 2 / SDD unit 2 | weakness | minor |
| 9 | other >40% vs other >=40% - off-by-one between artifacts | CUSTOMER_JOURNEY row 1 vs SDD unit 1 | contradiction | minor |
| 10 | Wedge Regularizar CNPJ gratis has no funnel for the abrir CNPJ visitor | CUSTOMER_JOURNEY row 2 | gap | important |

---

## CUSTOMER_JOURNEY.md

### Finding 1 - X threshold in unit 2 validation is untestable as written
**Artifact:** SDD.md phase_id=2 / CUSTOMER_JOURNEY.md row 2 (validation pattern cell)
**Type:** weakness
**Detail:** The validation_pattern for step 2 says "landing->submit conversion >=X% (X a calibrar; define Phase 5 go/no-go)". X is a free variable with no declared source, no default, and no calibration procedure. A validation_pattern with an unset threshold is vacuous - nothing can pass or fail it. The shape file (2026-04-24 Canal B LOCKED) itself notes "Custo de aquisicao real ainda desconhecido", reinforcing that X has no empirical anchor.
**Evidence:** SDD.md line 52; shape entry Trade-offs aceitos in Canal B lock; research/2026-04-24-discovery-channel-hypotheses.md does not publish a BR wedge CNPJ conversion benchmark.
**Proposed fix:** Replace X with (a) a cited industry benchmark and (b) an explicit calibration-phase duration before the threshold is binding. Example: ">=8% landing->submit during calibration (first 500 landing sessions), >=15% steady-state (Contabilizei / Conta Azul early-stage anchor)". The research/2026-04-25-remote-review-research.md file in this PR provides candidate numbers.
**Severity:** blocking - Phase 5 explicitly gates ai_executable_at_scale on validation being measurable; without a number, unit 2 cannot legitimately hold that classification.

### Finding 2 - Unit 1 validation has a logical circularity
**Artifact:** SDD.md phase_id=1 / CUSTOMER_JOURNEY.md row 1
**Type:** gap
**Detail:** Step 1 validation is "Behavioral self-report em onboarding questionnaire. Metric threshold: >60% self-select". But the questionnaire only fires AFTER step 2 submission (SDD.md interface: "Output = trigger self-report capturado no primeiro touchpoint downstream (step 2 submission)"). So unit 1 validation runs entirely inside unit 2. Unit 1 becomes ungradeable in isolation; any unit 2 failure (low conversion) starves unit 1 of data indefinitely. This is a hard dependency, not a fallback path.
**Evidence:** SDD.md lines 38-41 vs lines 49-52; AI_EXECUTION_MAP.md Notes implicitly acknowledges ("AI so roda o questionnaire", line 43).
**Proposed fix:** Either (a) collapse unit 1 into unit 2 (the real observable unit is "landing page submit captures trigger + intent"), or (b) add a separate pre-landing measurement (ad-impression trigger proxy, paid-panel survey) so unit 1 has independent observability. Option (a) is cleaner - current unit 1 is an abstraction layer without a system boundary.
**Severity:** important - does not block progress but the units-as-drawn will fall apart under SDD Phase 4 rigor.

### Finding 3 - other in which_trigger has no defined routing
**Artifact:** CUSTOMER_JOURNEY.md row 1 + SDD.md unit 1 + AI_EXECUTION_MAP.md row 1
**Type:** gap
**Detail:** Row 1 lists which_trigger (a/b/c/d/other). SDD.md uses other >=40% as an escalation signal. But no artifact documents what happens when a single user self-reports other. No downstream routing, no comms segmentation. The shape lists only 4 comms tones (a+c, b, d). A realistic funnel will see 10-20% other from day 1, none with a defined next step.
**Evidence:** CUSTOMER_JOURNEY.md Comm tone table lines 35-41 has 4 rows; SDD.md escalation_rule line 41 only fires at sustained >=40%.
**Proposed fix:** Add a 5th comm tone (other -> generic operational nurture + weekly Romeu review). Define a routing rule in unit 1 interface: "trigger=other AND email captured -> manual-review queue". Avoid treating other only as a data-quality signal.
**Severity:** important - funnel leaks users from day 1 otherwise.

### Finding 8 - Decision buttons mix 3 semantic classes; sorted hash loses semantics
**Artifact:** CUSTOMER_JOURNEY.md row 2 / SDD.md unit 2 decision_buttons
**Type:** weakness
**Detail:** Row 2 buttons are start_regularization (primary CTA), talk_to_human (escape), learn_more (educational). Each has different business semantics and different validation thresholds. The hash sorts alphabetically: [learn_more, start_regularization, talk_to_human]. Sorting is necessary for hash stability but destroys the "which is primary" semantic. A future rename start_regularization -> begin shifts sort order and produces a totally different hash - a legitimate rename would read as structural drift.
**Evidence:** SDD.md line 47; _tools/hash_units.py canonical_buttons line 58.
**Proposed fix:** Extend schema: decision_buttons becomes {id, semantic_class} pairs where class in {primary_cta, escape, educational, branching}. Hash on (id, class) pairs sorted by id. Survives renames within a class; flags class changes as drift.
**Severity:** minor - works today; bites on first rename.

### Finding 10 - Regularizar CNPJ wedge has no funnel for abrir CNPJ visitor
**Artifact:** CUSTOMER_JOURNEY.md row 2 / shape Sub-flavor do wedge LOCKED
**Type:** gap
**Detail:** Sub-flavor locked to regularizar (operator batendo teto); abrir was rejected as ICP mismatch. But any SEO or paid strategy targeting CNPJ keywords brings both populations to the same landing page. There is no row, segmentation logic, or button for "user is pre-revenue, wants to abrir CNPJ". Silent exclusion (e.g., CNPJ ja existe? gate) loses that audience; silent inclusion poisons unit 2 conversion because pre-revenue users have materially different conversion patterns.
**Evidence:** shape entry Sub-flavor do wedge LOCKED lines 213-224; CUSTOMER_JOURNEY.md row 2 has no filter.
**Proposed fix:** Add explicit branching button segment:is_existing_cnpj in row 2, with the abrir path routed to (a) off-funnel redirect or (b) waitlist. Proposal only - locking requires Romeu. In the meantime, unit 2 conversion threshold must be defined on the regularizar segment only.
**Severity:** important - any paid/SEO spend exposes this gap immediately.

---

## SDD.md

### Finding 7 - validation_pattern is part of unit identity but not hashed
**Artifact:** SDD.md schema (lines 14-26) + _tools/hash_units.py compute_hash (lines 61-76)
**Type:** gap
**Detail:** hash_units.py hashes phase_id | customer_action | io_signature | sorted(decision_buttons). It does NOT hash validation_pattern, yet the shape testing-as-planning decision treats validation as a first-class constraint. An editor can silently weaken validation (e.g. >=60% -> >=30%) without the drift checker noticing, because only CUSTOMER_JOURNEY row cells feed the hash - and SDD.md validation text does not round-trip to the journey row after initial lock.
**Evidence:** SDD.md line 6 (hash formula omits validation); _tools/hash_units.py line 67; shape entry Testing-as-planning lines 68-80.
**Proposed fix:** Extend hash to include a normalized form of validation_pattern. Either (a) hash the validation cell from the CUSTOMER_JOURNEY row (simpler, couples directly), or (b) introduce a separate validation_hash in SDD.md. Option (a) preserves the one hash per unit invariant. Schema change - Romeu must decide.
**Severity:** important - subverts the drift checker whole point for the field that matters most.

### Finding 9 - other >40% vs other >=40%: off-by-one between artifacts
**Artifact:** CUSTOMER_JOURNEY.md row 1 vs SDD.md unit 1
**Type:** contradiction
**Detail:** Journey row 1 says Se other >40% (strict). SDD unit 1 says Se other >=40% (inclusive). At exactly 40% the two artifacts produce different verdicts. Minor but exactly the kind of thing that surfaces in post-hoc dispute.
**Evidence:** CUSTOMER_JOURNEY.md line 52; SDD.md line 40.
**Proposed fix:** Pick one. Recommend >=40% since 40% is already the bad outcome zone. Note: since validation text is not hashed today (Finding 7), fixing this does not move the hash.
**Severity:** minor.

---

## AI_EXECUTION_MAP.md

### Finding 4 - Unit 2 classified ai_executable_at_scale despite non-empty missing_infra
**Artifact:** AI_EXECUTION_MAP.md row af58f450... (line 24)
**Type:** misclassification
**Detail:** The vocabulary says blocked_by_missing_infra is for units that would be AI-executable but falta infra (ex: sem database, sem webhook, sem credential). Row 2 missing_infra column lists THREE missing pieces: Feature-flag/experiment infra; analytics webhook; landing page CMS com slot de headline dinamica. By the schema own rule the unit is currently blocked_by_missing_infra - it becomes ai_executable_at_scale only after those three are built. Classifying it as ai_executable_at_scale today overstates readiness and invites downstream planning to treat it as shovel-ready.
**Evidence:** AI_EXECUTION_MAP.md vocabulary lines 13-16 vs row 2 line 24.
**Proposed fix:** Change classification to blocked_by_missing_infra, add a dedicated unblock_path column (or append to missing_infra), and document the transition: once infra exists -> re-classify to ai_executable_at_scale. Alternative: add a readiness_state column (blocked|ready) orthogonal to classification if Romeu prefers aspirational classification.
**Severity:** important - exactly the kind of silent over-promising that poisons planning docs.

---

## _tools/hash_units.py

### Finding 5 - Silent row-drop on <8 columns
**Artifact:** _tools/hash_units.py lines 116-117
**Type:** weakness
**Detail:** if len(cells) < 8: continue silently drops malformed rows. Adding a 9th column is fine, but splitting a cell across lines or deleting a pipe makes a row vanish from the drift check with zero warning. Combined with default exit 0 when no drift, malformed tables produce false-green drift checks.
**Evidence:** _tools/hash_units.py lines 115-117; self-test does not cover malformed-row case.
**Proposed fix:** Emit a stderr warning when a row starting with pipe is skipped for column-count reasons. Exit code stays 0 unless real drift. Add a self-test: malformed row triggers warning, exit stays 0.
**Severity:** minor - edge case today; foot-gun as table grows.

### Finding 6 - canonical_buttons fallback breaks on tokens containing  /  
**Artifact:** _tools/hash_units.py lines 56-58
**Type:** weakness
**Detail:** When a cell has no backticks, the fallback splits on  /  (space-slash-space). start / stop toggle (no backticks, token with  / ) produces [start, stop toggle] - 2 buttons, not 1. Primary (backtick) path is fine; fallback is fragile.
**Evidence:** _tools/hash_units.py lines 56-58; self-test covers backtick path with 7 cases, fallback only once.
**Proposed fix:** Make backticks mandatory (document in CUSTOMER_JOURNEY.md schema preamble). Change the fallback to raise ValueError(decision_buttons must be backtick-delimited). Fail loud > tolerate ambiguity.
**Severity:** minor - fallback unused in current artifacts.

---

## Cross-cutting observation (not a finding - context for Romeu)

The three artifacts (CUSTOMER_JOURNEY.md, SDD.md, AI_EXECUTION_MAP.md) stay in sync on the happy path but implicitly duplicate information: validation_pattern appears in all three with slightly different wording. A future edit to any one creates drift that hash_units.py catches only if it hits customer_action / io_signature / decision_buttons. Finding 7 calls this out for validation; the broader point is that SDD.md is the weakest synchronization pivot and deserves a second drift-check against AI_EXECUTION_MAP (today there is none).

---

## Halts / parked items

None. All 10 findings are proposals - Romeu decides which to adopt on return. No edits to any artifact in the NEVER list.
