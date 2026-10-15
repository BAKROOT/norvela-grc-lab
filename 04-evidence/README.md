# 04-evidence — the evidence library

This folder does two jobs.

**1. Scenario artefacts.** A few documents the dossier and the incident pack
refer to. Treat them like anything else you would collect during an
assessment: they are evidence, not conclusions.

| File | Referenced from | What it is |
|---|---|---|
| `secret-scan-2025.md` | `01-scenario/10-INCIDENT.md` (T+14h) | The 2025 Git-history secret scan summary and the remediation ticket trail |
| `cto-slack-excerpt.md` | `01-scenario/00-COMPANY-DOSSIER.md` §8 | The CTO's "the audit is a tax" thread |

**2. Your evidence library (Phase 3).** Build it here, one folder per control:

```
04-evidence/
  A.5.18-access-rights/
    2026-10-02_iam-access-review_workpaper.xlsx
    2026-10-02_iam-extract_api-export.csv
    EVIDENCE.md        # collector, collection date, period covered,
                       # design or operating evidence, linked test procedure
  A.8.8-technical-vulnerabilities/
    ...
```

Rules that make the library worth something to an auditor:

- **Name files `YYYY-MM-DD_what_how`** so the collection date and method are
  visible without opening them.
- **Record the period covered.** A single export proves a point in time; an
  operating-effectiveness claim needs evidence across the whole period.
- **Flag design vs operating evidence** in every `EVIDENCE.md`.
- **Prefer machine-generated, timestamped artefacts** (API exports, scan
  reports, logs) over screenshots and emails. See `02-stack/SETUP.md` Part 5.

Everything here is fictional. Credential values are redacted placeholders.
