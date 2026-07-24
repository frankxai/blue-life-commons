# For Sanctuaries, Rehab & Stranding Networks

You answer the stranding call, run the triage, manage the transport, make the rehab and release decisions, and carry the lifelong husbandry of non-releasable animals. Today that often means paper forms re-keyed into three systems, no live facility-capacity view, and protocol knowledge that lives in one veteran's head. This system is built to hold that knowledge — and to do it under the strictest welfare rules in the commons.

## What the system gives you

- **Artifact types for your exact workflow** — `stranding-protocol`, `rehab-case-card`, `release-criteria`, `sanctuary-profile`, `husbandry-guide`, and `necropsy-summary`. Ready-to-fill templates exist (e.g. `welfare-assessment`, `sanctuary-profile`, `stranding-protocol`, `local-knowledge`).
- **Two guardian design patterns scoped to your work** — `sanctuary-guardian` and `stranding-network-guardian`. They are requirements briefs, not public implementations linked by this guide. Any implementation must follow one non-negotiable principle: **it assembles evidence; it never adjudicates.**
- **The welfare frame, applied to individuals** — the Five Domains adapted to a patient in your care: feeding response and body condition (Nutrition), the disturbance footprint of handling (Behaviour), entanglement/disease load (Health) — all in [`WELFARE.md`](../../WELFARE.md).
- **UME alarm integration** — a stranding-rate anomaly maps to NOAA's seven Unusual Mortality Event criteria and can escalate a guild, prompting a `necropsy-summary` or region review.

## How to use it today

1. **Read the strict rules first** — [`ETHICS.md`](../../ETHICS.md) § *Rehabilitation, sanctuary & individual animals*. These are the tightest rules in the commons; everything below depends on them.
2. **Capture a stranding protocol** — take the procedure your team runs from memory and author a `stranding-protocol` artifact from the template. Set `review.ethics: required` and `review.science: required` for any triage/dosing content. This pulls tribal knowledge out of one person's head into a reviewed, durable form.
3. **Open a de-identified rehab case card** — a `rehab-case-card` with `individual_animal: true`. The schema's location guardrail will *fail CI* if you attach precise coordinates — that protection is intentional and applies in rehab, in transport, and **post-release**.
4. **Assemble release evidence — never a verdict** — use `release-criteria` to compile evidence against published criteria. The artifact (and the `sanctuary-guardian`) stays silent on the decision: dosing, euthanasia, and releasability are calls for your licensed veterinarian and the responsible authority (e.g. the NOAA Regional Administrator). *Grounded or silent extends to evidence, never verdict.*
5. **Run `/ethics-check` and `/validate-artifact`** ([`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills)) before any PR — the ethics check is blocking.

## The rules that apply to you

- **No precise locations of live animals — ever.** This extends the vulnerable-taxa rule to *every* animal in rehab, transport, and post-release. Telemetry is aggregated and delayed, never live-public.
- **Evidence, never adjudication.** The system compiles evidence against criteria and stays silent on the clinical/legal verdict. Licensed vets and authorities decide.
- **Release > lifelong captivity is the default.** Sanctuary residency for non-releasable animals is the justified *exception*, never framed as a happy outcome. No glamorizing captivity.
- **Individual-animal dignity.** Case cards are de-identified. Donor storytelling around a named animal must never compromise the animal's interests or location — welfare-over-content holds.
- **Honesty about invasiveness.** Tagging, sampling, and handling are described plainly with their welfare cost, never euphemized.
- **Clinical content is review-gated and credentialed** — reviewers should include relevant veterinary/rehabilitation expertise.

## Your first contribution

**Author one `stranding-protocol` from a procedure your team already runs.** It's the single highest-value thing you can give the commons: it preserves knowledge that's currently fragile (one person, one binder), and it's immediately useful to every other network on your coastline. Start from the `stranding-protocol` template, keep it de-identified and location-free, set the ethics/science reviews to `required`, and open an `artifact-request` issue or hand it to a commons steward.

> Built on SIP · Blue Life Commons (CC-BY-4.0).
