# Secret scan — Git history, norvela GitHub org (2025)

> **Scenario artefact.** Fictional. All credential values are redacted
> placeholders — nothing here is a real secret.

| Field | Value |
|---|---|
| Scan type | Full Git history, all repositories in the `norvela` org |
| Tooling | Open-source secret scanner, run once by Platform Engineering |
| Scheduled re-scan | None defined |
| Live credentials found | **22** |
| Rotated after the scan | 16 |
| **Not rotated** | **6** |

## The six unrotated credentials

| # | Credential (redacted) | Type | Repository | Ticket | Ticket status |
|---|---|---|---|---|---|
| 1 | `svc-settlement-batch` — `AKIA****************` | AWS IAM access key | `settlement-batch` | PLAT-2291 | **Closed — "won't fix: legacy service, scheduled for decom Q1 2026"** |
| 2 | `svc-legacy-etl` — `AKIA****************` | AWS IAM access key | `legacy-etl` | PLAT-2292 | Closed — "won't fix: legacy service, scheduled for decom Q1 2026" |
| 3 | Ledger adapter DB password `********` | Oracle DB credential | `ledger-adapter` | PLAT-2293 | Open — no assignee |
| 4 | Notification service SMTP password `********` | SaaS credential | `notification-svc` | PLAT-2294 | Open — "blocked on vendor" |
| 5 | Datadog API key `********` | Observability API key | `infra-config` | PLAT-2295 | Open |
| 6 | Internal admin-console session secret `********` | Application secret | `admin-console` | PLAT-2296 | Open — "low priority, internal only" |

## Ticket trail — PLAT-2291

- Raised by: Platform Engineering (scan owner)
- Assigned to: Platform Engineering (service owner)
- Closed by: Platform Engineering
- Resolution: *Won't fix — legacy service, scheduled for decommission Q1 2026.*
- Decommission ticket: none linked
- Independent verification of closure: none

## Context recorded in the scan notes

- The `settlement-batch` repository was **public for 11 days in March 2024**
  after an organisation visibility setting was changed. No alert fired, and no
  retrospective assessment of what was exposed was performed.

## What an assessor should ask of this artefact

- Who decided "won't fix", and did anyone outside the owning team agree?
- What compensating control applied while the decommission was pending?
- Is a one-off scan with no re-scan date a control at all?
