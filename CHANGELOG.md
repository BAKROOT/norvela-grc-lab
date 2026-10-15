# Changelog

All notable changes to the Norvela GRC Lab. Dates are ISO 8601.

## [1.1.0] — 2026-10-15 · First public release

### Added
- `04-evidence/`: the evidence folder the dossier and incident pack already
  referred to, with `secret-scan-2025.md`, `cto-slack-excerpt.md`, and a
  README describing how to structure the Phase 3 evidence library.
- `02-stack/tools/api-examples.sh`: worked CISO Assistant REST API examples
  that create the domain and five perimeters and import `assets.csv`. It was
  referenced in `SETUP.md` but missing from the archive.
- `docs/logbook.html`: interactive progress tracker (8 phases, steps,
  deliverables, proof gates). Progress is stored in the browser only.
- `docs/build_pdfs.py`: rebuilds both PDFs from the Markdown sources.
- `docs/img/fair-settlement-fraud.png`: sample FAIR output for the README.
- Repository packaging: README, LICENSE (MIT), CITATION.cff, .gitignore.

### Fixed
- **SETUP.md:** script paths now work when run from `02-stack/`
  (`tools/...`, not `../tools/...`).
- **SETUP.md:** SimpleRisk HTTPS moved from 8443 to 8444. 8443 is already
  used by CISO Assistant.
- **SETUP.md:** vulnerability scanning is introduced in Phase 3 (control
  assessment), matching the curriculum. It previously said Phase 4.
- **SETUP.md:** FAIR dependencies corrected to `numpy matplotlib`. The script
  does not use `pyfair` or `pandas`.
- **`vuln-findings.csv`:** all 38 critical findings are now open and older than
  180 days, as the dossier and findings key state. Previously only 28 were.
- **`iam-users.csv`:** IAM usernames are now unique. The generator had
  produced duplicates (for example three `piotr.santos`), which cannot exist
  in a single AWS account. The 8 planted findings (IAM-121 to IAM-128) are
  unchanged.
- **`build_workbooks.py`:** the docstring now lists the files actually
  produced. Output is still deterministic (seed 1848).
- **`fair_analysis.py`:** the loss-exceedance chart now uses a log axis
  starting at €10k instead of symlog, so the curves are readable.
- **PDF Findings Key:** finding numbers now run 1–46 continuously instead of
  restarting in each domain. The cover now gives the correct domain count
  (seven).

### Changed
- Wording that addressed one specific reader (certifications held, years
  of experience) has been generalised so any learner can use the lab.
  Affected files: `CURRICULUM.md` Phase 7, `SETUP.md`, `QUESTION-BANK.md` Q119
  and the findings key's closing note.
- The PDFs moved to `docs/` and were rebuilt from the updated Markdown.

## [1.0.0] — 2026-09 · Private edition

- First complete version: scenario, curriculum, stack, workbooks, interview
  kit and print manual.
