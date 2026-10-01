# Water Intelligence kit registry

This is a **reviewed-design proposal** inside Blue Life Commons. The current K0 manifest describes a manual sampling prototype. It does not imply a physical build, an authorized water installation or validated water treatment.

Each `kits/<id>/manifest.json` has a versioned contract in [`schema/kit-schema.json`](../schema/kit-schema.json). People and agents can use the same record for a parts list, quote comparison, build workshop, maintenance plan and a public kit card. The editable design and scientific protocol remain separately linked files. All records intentionally omit a precise home location.

## Read the maturity signal

| State | Evidence required by the validator | Human decision still required |
| --- | --- | --- |
| Proposed | Cost range covers parts; source paths resolve; no measured-performance claim | Science, ecology and engineering review |
| Bench tested | A committed test report and cited measured-claim evidence | Check methods, controls, build reproducibility and independent print-fit |
| Authorized field trial | Test report, all three reviews approved, approval reference and explicit open-water classification | Verify location-specific rights, insured operator and retrieval |
| Replicated | Field requirements plus a second committed report | Independent reproducibility and publication approval |

The validator enforces *presence and coherence*, not scientific truth, safe operation, material certification or legal permission. Evidence and reviewers must establish those separately.

## Contribute a kit

Copy a manifest, replace its ID and complete bill of materials, and open a pull request. Every part states its contact class and total line cost in EUR, including its stated quantity. `vendor-listing` requires a live supplier URL and check date; `planning-estimate` remains explicitly unquoted. Specify a method to test substitutions. Work from editable CAD, include a real build log once a part is tested, and return every water-contact modification to expert review. Never publish exact household coordinates, addresses or vulnerable wildlife locations.

Run `python3 scripts/validate_kits.py` to check all manifests and `python3 -m unittest discover -s tests -p 'test_kit_contract.py'` for the critical gates. [K0's source protocol](../content/research/modular-urban-water-kits.md) is in draft expert review; [the dry-side parametric plate](../designs/urban-water/dry-side-cable-plate.scad) is a separate fit-test candidate, not a K0 part.
