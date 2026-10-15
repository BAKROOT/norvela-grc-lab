# NORVELA PAY — Company Dossier
**Your assessment target. Treat everything in this file as ground truth.**

Version 1.0 · Lab scenario for GRC risk & compliance practice
Fictional company. Any resemblance to a real entity is coincidental.

---

## 1. Why this company was designed this way

You need one organisation that legitimately triggers *multiple* regulatory
regimes at once, because that is the situation real GRC people are hired into
and the situation interviews probe. Norvela Pay is built so that:

| Regime | Why it bites | What it forces you to practise |
|---|---|---|
| **DORA** (Reg. EU 2022/2554) | Authorised payment institution in the EU | ICT risk framework, Register of Information, incident classification, TLPT scoping, exit strategies |
| **NIS2 / PT Decreto-Lei 125/2025** | Subsidiary is an in-scope entity; also a digital provider | Registration with CNCS, 24h/72h/1-month reporting chain, management-body liability |
| **GDPR** | Processes payment + identity data of EU data subjects | RoPA, DPIA, transfers, breach notification, DSR |
| **PCI DSS 4.0.1** | Touches cardholder data through one product line | Scoping, segmentation, SAQ vs RoC, compensating controls |
| **ISO/IEC 27001:2022 (+Amd 1:2024)** | Customers demand the certificate | ISMS, SoA, internal audit, management review, certification cycle |
| **SOC 2 Type II** | US enterprise customers demand it | Trust Services Criteria, evidence over a period, exceptions |
| **EU AI Act** (Reg. 2024/1689, as amended by Reg. 2026/1744) | Runs an AI fraud-scoring and a credit-decisioning model | Risk classification, Art. 50 transparency, timeline realism |

That overlap is the whole point. A control like MFA is evidence for six of
those at once, and a real GRC analyst's value is knowing that and not testing
it six times.

---

## 2. The business

**Norvela Pay, S.A.** — headquartered Lisbon, Portugal.
Founded 2019. 340 employees. Revenue €61M (FY2025).

Norvela Pay is an **embedded payments and treasury platform**. Mid-market
European retailers and marketplaces plug Norvela into their checkout and
back office to:

1. Accept card, SEPA and open-banking payments (**PayRails** product)
2. Hold and move funds in multi-currency wallets (**Vault** product)
3. Get short-term working-capital advances against receivables (**Flow** product)
4. Screen transactions for fraud using an in-house ML model (**Sentinel**)

**Regulatory status.** Authorised as a Payment Institution by Banco de
Portugal (licence PI-2021-0447), passported into 14 EEA states. The Flow
product is delivered through a partnership with a licensed credit institution,
Banco Astera (Spain), because Norvela cannot lend on its own licence.

**Legal entities:**

| Entity | Country | Role | Headcount |
|---|---|---|---|
| Norvela Pay, S.A. | Portugal | Licensed PI, group parent, main engineering | 240 |
| Norvela Pay Iberia, S.L. | Spain | Sales, merchant onboarding, support | 55 |
| Norvela Tech Sp. z o.o. | Poland | Engineering hub, 24/7 platform ops (NOC) | 40 |
| Norvela Pay Inc. | USA (Delaware) | US sales entity, no processing | 5 |

**Why the entity structure matters.** The Polish entity runs the night shift
and therefore has production access. It is a separate employer with separate
HR onboarding. That single fact breaks three controls in the lab — find them.

---

## 3. Governance as it actually exists

**Board of Directors (Conselho de Administração)** — 5 members. Meets monthly.
Cybersecurity is a standing agenda item **only since March 2026**, added after
the Banco de Portugal supervisory letter (see §9).

| Role | Name | Note |
|---|---|---|
| CEO | Marta Quintela | Founder. Vocal that "compliance shouldn't slow the roadmap." |
| CFO | Duarte Salgado | Owns the DORA budget line. Sceptical of headcount asks. |
| CTO | Ivo Brandão | Founder. Owns engineering. Resists change-freeze windows. |
| COO | Sofia Rendeiro | Owns operations, vendor contracts, BCP. Your best ally. |
| Non-exec | Katarína Hoferová | Ex-regulator. Asks the hardest questions in the room. |

**Second line:**

- **Chief Risk Officer — Helena Vaz.** Joined Jan 2026. Came from insurance,
  strong on enterprise risk, learning ICT risk. Reports to CEO.
- **Head of Compliance — Nuno Peralta.** AML/CFT focused. Has never run an
  ISO audit. Reports to CEO.
- **DPO — Cláudia Reis.** Part-time (0.5 FTE), also company secretary.
  *Flag this: is a part-time DPO with a secretarial role an Art. 38(6)
  conflict? That's a real interview question.*
- **CISO — vacant.** Left August 2026. **This is your role in the lab.**
  Currently the Head of Platform Engineering is "acting CISO," which is a
  first-line/second-line conflict you should write up on day one.

**Third line:** Internal Audit is one person, Rita Mendonça, who spends 80%
of her time on AML file reviews. No ICT audit has ever been performed.

**Committees:** There is a Risk Committee on paper (charter dated 2022, never
amended). It has met 3 times in 18 months. There is no Change Advisory Board;
changes are approved in the pull request.

---

## 4. Technology estate

### 4.1 Cloud

**AWS** is primary — accounts:

| Account | Purpose | Notes |
|---|---|---|
| `norvela-prod` | Production payments platform | eu-west-1 (Ireland), eu-central-1 (Frankfurt) |
| `norvela-staging` | Pre-prod | Contains a **restored copy of production data** from 2025-11 |
| `norvela-dev` | Development | 60 engineers have `PowerUserAccess` |
| `norvela-data` | Data lake, ML training | Sentinel + Flow model training data |
| `norvela-sandbox` | Merchant test environment | Public-facing API |
| `norvela-audit` | Log archive | CloudTrail org trail, 400-day retention |

**Azure** — a single tenant for Microsoft 365 (Exchange, SharePoint, Teams,
Entra ID). Entra ID is the identity provider for SSO into 31 SaaS apps.

**On-prem** — one Lisbon office server room with: a legacy Oracle DB running
the merchant settlement reconciliation (the "Ledger"), two ESXi hosts, and
the physical HSM cluster required for the card product.

### 4.2 The crown jewels (candidate list — you will refine this)

1. **The Ledger** (Oracle, on-prem) — the authoritative record of merchant
   balances. If it's wrong, Norvela owes money it can't prove.
2. **HSM cluster** — card data encryption keys. PCI-critical.
3. **Vault balance service** (AWS, Kubernetes) — real-time fund movement.
4. **Sentinel model + feature store** — fraud decisions.
5. **Entra ID tenant** — compromise = everything.
6. **The `norvela-data` lake** — full transaction history, 7 years.

### 4.3 Known technical facts (these are your findings source)

These are deliberate. Each one maps to at least one control failure.

- Production deploys happen **12–20 times per day** via GitHub Actions. There
  is no separate deployment approval; PR merge triggers deploy.
- **Break-glass access**: a shared `prod-admin` AWS role exists. 11 people can
  assume it. There is no session recording. It was used 43 times last quarter.
- **MFA**: enforced in Entra ID for all staff. **Not** enforced on the AWS
  root accounts of `norvela-sandbox` and `norvela-dev`. Nobody knows who holds
  the sandbox root credentials.
- **Staging data**: the November 2025 production restore in staging includes
  live PANs and customer names. It has never been masked. 60 developers can
  read it. *This is your GDPR + PCI headline finding.*
- **Logging**: CloudTrail is on in all accounts and centralised to
  `norvela-audit`. But application-level logs from the Vault service are
  retained for **14 days** only, because of cost.
- **Backups**: RDS automated backups, 7 days. The Ledger (Oracle) is backed up
  to tape weekly and shipped to an Iron Mountain facility. **The Ledger restore
  has never been tested.** Last documented attempt: 2022, failed.
- **Vulnerability management**: Snyk on repos, AWS Inspector on workloads.
  There are 1,247 open findings; 38 are critical and older than 180 days. No
  SLA is documented.
- **Patching**: Kubernetes nodes are immutable and replaced weekly. The two
  ESXi hosts are on a version that went end-of-support in 2024.
- **Endpoint**: Jamf for 280 Macs, Intune for 45 Windows machines. 15 Linux
  workstations in the Poland office are **unmanaged**.
- **Network**: no segmentation between the corporate network and the Lisbon
  server room. The HSM cluster is reachable from any office VLAN.
- **Secrets**: AWS Secrets Manager is used for new services. Legacy services
  read from a `.env` file baked into the container image. A 2025 secret scan
  found 22 live credentials in Git history; 6 have not been rotated.
- **Sentinel model**: retrained monthly on production data. No documented
  approval gate, no bias testing, no model card. Decisions are
  **auto-declining** transactions with no human review path below €500.
- **Flow model**: scores merchant creditworthiness. Outputs feed Banco
  Astera's lending decision. *Is this an Annex III high-risk AI system? Whose
  obligation — Norvela's as provider, or the bank's as deployer? Argue it.*

---

## 5. Data

### 5.1 Personal data processed

| Category | Volume | Lawful basis (as claimed) | Where |
|---|---|---|---|
| Merchant contact details | ~14,000 | Contract | Salesforce, AWS |
| End-customer payment data (PAN, name) | ~40M transactions/yr | Contract + legal obligation | AWS, HSM, Ledger |
| KYC/identity docs of merchant directors | ~11,000 | Legal obligation (AML) | Onfido → S3 |
| Transaction behaviour for fraud scoring | All transactions | **Legitimate interest** | `norvela-data` |
| Employee data | 340 | Contract / legal | BambooHR, M365 |
| Support call recordings | ~9,000/yr | **Consent** (claimed) | Talkdesk (US) |
| Website analytics | — | Consent | GA4 |

**Deliberate problems planted here** — find them yourself before reading the
answer key in `01-scenario/99-FINDINGS-KEY.md`:
- One lawful basis is almost certainly wrong for what's actually done with it.
- One processor is in a third country with no documented transfer mechanism.
- One category is retained far beyond any stated retention period.
- The RoPA (`03-workbooks`) is 14 months out of date and misses two systems.

### 5.2 Retention as practised

There is a retention policy document (2021). It says "7 years for financial
records." In practice, nothing is ever deleted. The data lake holds records
from 2019. Support recordings are kept indefinitely.

---

## 6. Third parties (the TPRM problem)

Norvela uses 31 SaaS applications and 9 infrastructure providers. Here are the
ones that matter for the lab. The full machine-readable register is in
`03-workbooks/vendors.csv`.

| Vendor | Service | Criticality | Problem to find |
|---|---|---|---|
| AWS | Cloud infrastructure | Critical / supports CIF | Concentration risk; no tested exit plan |
| Banco Astera (ES) | Lending partner for Flow | Critical | Is this ICT third-party or a business partner? Scope argument |
| Onfido | KYC identity verification | Important | Sub-processor chain not mapped |
| Talkdesk | Contact centre | Important | US-hosted; call recordings = personal data |
| Snowflake | Analytics warehouse | Important | Added by the data team; **never went through vendor review** |
| Datadog | Observability | Important | Logs contain PANs in 3 known cases |
| A small Portuguese ISV, "Sertã Systems" | Ledger reconciliation support | **Critical** | Two-person company. Has standing VPN access to the Oracle Ledger. Contract from 2019, no DORA clauses, no exit plan, no audit rights. **This is the single worst vendor risk in the lab.** |
| GitHub | Source control + CI/CD | Critical | Deploy pipeline = production change path |
| Cloudflare | WAF/CDN | Critical | Single point of failure for all merchant traffic |

**The DORA Register of Information exercise**: you will build a real RoI from
this vendor list using the ITS (EU) 2024/2956 templates. That is the single
most job-relevant artefact in this lab.

---

## 7. What already exists (your starting documentation)

Do not assume a greenfield. Real jobs start mid-mess.

| Document | State |
|---|---|
| Information Security Policy | v2.1, approved 2023, never reviewed since |
| Acceptable Use Policy | Exists, signed by 61% of staff |
| Access Control Policy | Exists, references a joiner-mover-leaver process that HR does not follow |
| Incident Response Plan | v1.0, 2022. Does not mention DORA or NIS2 timelines. Never exercised. |
| Business Continuity Plan | Exists for the Lisbon office (fire/flood). Nothing for cloud outage. |
| BIA | Never performed |
| Risk register | A spreadsheet with 23 entries, last updated 2025-04. Scored High/Medium/Low with no defined criteria. |
| RoPA | Exists, 14 months stale |
| DPIA | One, for the Sentinel model, dated 2023, two pages |
| SoA | Does not exist |
| Vendor register | Procurement's spreadsheet — 22 of 40 vendors |
| Asset inventory | Three partial inventories that disagree with each other |
| Training records | Annual awareness training, 74% completion |

---

## 8. The people problem

- Engineering views security as a blocker. The CTO has said in writing
  (Slack, quoted in `04-evidence/`) that "the audit is a tax."
- The Poland NOC team was never included in the awareness training rollout
  because their HR system is separate.
- Two engineers left in July 2026. Their AWS IAM users are still active.
  Their Entra accounts were disabled correctly. *Why the difference? Because
  the leaver process only covers SSO-integrated apps. This is a joiner-mover-
  leaver finding with teeth.*
- The Head of Platform Engineering is "acting CISO" — first line policing
  itself.

---

## 9. Live pressures (your clock)

These give the lab urgency and give you deadline-management practice.

1. **Banco de Portugal supervisory letter (2026-03-11)** — following the 2026
   DORA Register of Information submission, the supervisor noted "material
   data quality deficiencies" in Norvela's RoI and requested a remediation
   plan. **Response due 2026-11-30.**
2. **ISO 27001 Stage 1 audit booked for 2027-02-15.** Certification body:
   fictional "Atlântico Certificação." The SoA does not exist yet.
3. **NIS2 / RJC** — Portugal's Decreto-Lei 125/2025 entered into force
   2026-04-03. Norvela must determine whether it is an essential or important
   entity, register with CNCS, and align. Note the DORA *lex specialis*
   argument — work out where DORA displaces the RJC for a payment institution
   and where it does not.
4. **Largest customer (a German marketplace) has issued a security
   questionnaire** — 214 questions, due in 3 weeks, and their contract renewal
   (€4.1M ARR) depends on it.
5. **An incident occurred 2026-09-08** — see `01-scenario/10-INCIDENT.md`.
   You must classify it under DORA, decide on NIS2 and GDPR notification, and
   run the post-incident process.

---

## 10. Risk appetite (as the board would articulate it if pushed)

Nobody has written this down. One of your Phase 1 deliverables is to draft it
and get it "approved." Use these signals from board behaviour:

- Will accept availability risk for non-payment features; will not accept any
  single-transaction settlement error.
- Fears regulatory action more than a breach — a Banco de Portugal
  intervention is existential for the licence.
- Will spend on things customers ask about (ISO cert) faster than on things
  only regulators ask about (BIA).
- Zero tolerance stated for AML failures; no stated tolerance for anything else.

Your job in Phase 1 is to turn that into quantified appetite statements with
thresholds. That exercise alone is a senior-level interview answer.
