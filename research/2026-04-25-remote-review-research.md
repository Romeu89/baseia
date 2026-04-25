# Remote Review Research

**Date:** 2026-04-25. **Budget:** 600 words. **Method:** WebSearch 2026-04-24. 4 findings, each cites sources and flags confidence.

---

## Finding 1 - Landing page conversion benchmark (X in SDD unit 2)

**Source:** Unbounce B2B CRO 2025 (unbounce.com/conversion-rate-optimization/b2b-conversion-rates); daydream SaaS landing page benchmarks (withdaydream.com); SurfaceLabs 2025 (withsurface.com). Credibility: Unbounce high (n~57k pages), others medium.

**Data point:** B2B SaaS landing-to-lead median 2.4% paid traffic, 3.8% all traffic. Self-serve high-intent signup: 4-10% median, 12-18% best-in-class. Forms <=5 fields convert 120% better than 6+.

**Confidence:** medium (no BR-specific fintech wedge benchmark exists; proxy from generic B2B SaaS).

**Implication for SDD:** X threshold in unit 2 validation_pattern. Regularizar CNPJ is a self-serve high-intent wedge with 2-3 fields; comparable band 4-10%. Proposed calibration: X=8% during first 500 sessions (conservative floor); revisit if >15% (top band) or <4% (below floor). Romeu picks.

---

## Finding 2 - MEI-to-ME transition triggers

**Source:** Contabilizei MEI 2026 guide (contabilizei.com.br); Cora Limite MEI 2025 (cora.com.br); Serasa Experian 2025. Credibility: Contabilizei high, others medium.

**Data point:** MEI cap R$81k since 2016 (inflation-eroded). PLP 60/2025 proposes R$140k (in Congress, not law). 14M MEIs nationally. Empirical transition triggers: (i) faturamento near cap, (ii) corporate client requires ME for NF, (iii) need 2nd employee (MEI allows only 1), (iv) need PJ account with higher credit.

**Confidence:** high on triggers, medium on proportions.

**Implication for SDD:** journey trigger (c) (bateu teto mas CLT impede contratar) collapses two empirical triggers (cap + needing 2nd FTE). For interview queue: consider split into (c1)=teto, (c2)=2nd-FTE. Different validation thresholds apply because (c1) is time-driven, (c2) is event-driven.

---

## Finding 3 - CLT-free framing reception

**Source:** CNN Brasil CLT/PJ/temporario analysis (cnnbrasil.com.br); Contabilizei Pejotizacao article (contabilizei.com.br); Decision Report 72% BR empresas early adoption (decisionreport.com.br - already cited in existing research file). Credibility: high/high/medium.

**Data point:** CLT encargos ~65-70% of nominal salary (CNN). Pejotizacao widespread but reforma trabalhista raises criminalization risk (Contabilizei). Fear-of-substitution concern cited by 72% BR adopters applies to EMPLOYERS worried about their own employees; solo-founder cohort has no employees to protect, so it inverts - nao contratar means not owing.

**Confidence:** medium. No BR survey probes nao CLT wedge framing directly; inference from adjacent literature.

**Implication for SDD:** reframe (amplia capacidade sem contratar proximo CLT) already shape-locked is defensible. A/B candidates for unit 2 golden-output: variant X = amplia capacidade sem contratar proximo CLT; variant Y = cresce sem precisar de mais gente no financeiro. Y is more neutral.

---

## Finding 4 - Contabilizei wedge playbook tactics

**Source:** Contabilizei 100 mil clientes (contabilizei.com.br/100-mil-clientes); Warburg Pincus press release Oct 2024 (warburgpincus.com). Credibility high (first-party + financial disclosure).

**Data point (specific tactics, not just the 100k metric):** free company registration at top of funnel; upsell to monthly recurring accounting; 99%-automated tax calc+pay as retention hook (not acquisition); cash-generation-first growth (break-even discipline); physical stores (SP/RJ malls, targeting 60+ cities) only as post-scale move; bundle layering over time (checking account, health plans, partnerships - not day one). Growth curve: 20k (2018) -> 30k (2020) -> 50k (Oct 2024) -> 100k recent. Doubling ~2yr cadence implies reinforcing-loop funnel, not viral spike.

**Confidence:** high on funnel shape, low on paid mix (no public CAC breakdown).

**Implication for SDD:** BaseIA regularizar CNPJ mirrors the Contabilizei wedge at funnel shape, not service. Unit 2 validation must be TWO-phase: (a) landing-to-CNPJ capture, (b) capture-to-first-recurring-payment. SDD currently hashes only (a). Add (b) as a separate unit in the parked steps 4+ zone.

---

## Notes

- No public CAC for Contabilizei wedge. Funnel shape proven; unit economics not.
- No BR survey probing nao CLT framing reception directly.

Prose word count target met (<600).
