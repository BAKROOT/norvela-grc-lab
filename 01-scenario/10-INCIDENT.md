# INCIDENT PACK — NOR-2026-0908
**Use this for incident classification, regulatory notification and
post-incident review practice. Work it in real time against the clock.**

---

## How to use this pack

Do **not** read the whole thing at once the first time. Read one timeline
block, make your decisions, write them down with a timestamp, then read the
next block. That is how the information actually arrives in a real incident,
and the discipline of deciding on incomplete information is precisely what
separates people who have done this from people who have read about it.

Your decision points are marked **[DECIDE]**. Write your answer before moving on.

---

## T+0 — Tuesday 2026-09-08, 03:14 WEST

The Poland NOC receives a Datadog alert: the Vault balance service in
`eu-west-1` is returning HTTP 500 on 12% of requests. The on-call engineer
(Poland, contractor via an agency) restarts the service. Errors drop to 3%.
He does not open a ticket because "restart fixed it."

## T+4h — 07:20 WEST

A merchant in Germany emails support: their settlement report shows two
payouts they did not initiate, totalling €48,200, to an IBAN they don't
recognise. Support tags it "billing query" and routes it to Finance with a
48-hour SLA.

**[DECIDE 1]** At this point, is anything reportable to anyone? On what basis?
What is the single question you most need answered in the next 30 minutes?

## T+9h — 12:05 WEST

Finance notices three more merchants with the same pattern. Total now
€310,000 across 5 merchants, all to two beneficiary IBANs in a non-EEA
jurisdiction. Finance escalates to the COO. The COO calls the acting CISO.

## T+11h — 14:30 WEST

Initial technical finding: the payouts were made through the legitimate Vault
API using a valid API key belonging to a *Norvela internal service account*,
`svc-settlement-batch`, not a merchant key. The calls originated from an IP
in a commercial VPN range. The service account's key was last rotated in
**2023**.

**[DECIDE 2]** Under **DORA Art. 18**, run the classification. You need the
criteria from the RTS on incident classification: clients affected, data
losses, economic impact, service downtime, geographical spread, criticality
of services affected, reputational impact. Does this meet the **major
incident** threshold? Write your reasoning against each criterion — the
reasoning is what a supervisor asks for, not the conclusion.

**[DECIDE 3]** The DORA initial notification clock. When does it start, and
by when must the initial notification reach Banco de Portugal? What are the
intermediate and final report deadlines? *Do not guess — look it up and cite
the article. Getting this wrong in an interview is fatal; saying "I'd confirm
the exact deadline against Art. 19 and the RTS before committing" is not.*

**[DECIDE 4]** Is this also a **personal data breach** under GDPR Art. 4(12)?
If yes, is it notifiable under Art. 33, and is Art. 34 communication to data
subjects triggered? Note the distinction between the merchants (Norvela's
customers, mostly legal persons) and any natural persons involved.

**[DECIDE 5]** Portugal's RJC (DL 125/2025) also has notification duties.
Does DORA displace them here as *lex specialis*? Write the argument both ways
and then commit to a position. This exact question is being argued by real
compliance teams right now and a good answer will impress anyone interviewing
you.

## T+14h — 17:45 WEST

Log review finds the truth, and it is worse:

- The `svc-settlement-batch` credential was one of the **6 unrotated secrets
  found in Git history in the 2025 secret scan.** The scan report is in
  `04-evidence/secret-scan-2025.md`. It was assigned to a ticket that was
  closed as "won't fix — legacy service, scheduled for decom Q1 2026." The
  decom never happened.
- The repository containing it was **public for 11 days in March 2024** due to
  a misconfigured GitHub org setting.
- Vault application logs are retained **14 days**. The intrusion may predate
  the log window. **You cannot prove when access began.** You can only prove
  the earliest event you still have logs for.

**[DECIDE 6]** You cannot establish the start date. How do you communicate
that to (a) the board, (b) the supervisor, (c) affected merchants? Write the
actual sentence you would use for each. Vague hedging fails; overclaiming
certainty is worse. This is a communication skill interviews test hard.

**[DECIDE 7]** What compensating evidence sources exist that might extend your
visibility backwards? List at least five before reading on.
*(CloudTrail in `norvela-audit` at 400 days; VPC flow logs; the bank's own
records of received payments; Datadog metric retention vs log retention;
GitHub audit log; HSM logs; beneficiary IBAN first-seen date in the AML system.)*

## T+2 days — 2026-09-10

CloudTrail (400-day retention — the one control that saves you) shows the
credential was first used from the VPN range on **2026-07-29**. Six weeks of
access. During that window there were **no** unauthorised payouts until
September. The attacker was reconnoitring.

Total confirmed loss: €310,000, of which €96,000 is recoverable.
Merchants affected: 5. End-customers affected: 0 directly, but the
`norvela-data` lake was queried — **41,000 customer records** were read.

**[DECIDE 8]** Now re-run your DORA classification with the full facts. Did
your T+11h answer change? Document *why* — supervisors care enormously about
whether your classification was reasonable *at the time you made it*, not
whether it matched the final facts. Write the reclassification note.

**[DECIDE 9]** GDPR Art. 33: the 72-hour clock runs from **awareness**. When
did Norvela become "aware"? 03:14 on the 8th? 12:05? 14:30? T+2 days?
Defend your answer. This is the highest-frequency GDPR interview question
there is.

## T+9 days — 2026-09-17

Root cause analysis complete. Contributing factors:

1. Secret in Git history, never rotated, ticket closed without remediation
2. No credential rotation policy for service accounts
3. Repository briefly public — no alerting on org visibility change
4. No egress filtering; the data lake query went to an external endpoint
5. Application log retention too short to support investigation
6. On-call engineer restarted a service without raising a ticket — no
   "unexplained anomaly" escalation criterion existed
7. The decom ticket was closed by the same team that owned the risk

**[DECIDE 10]** Which of these are *findings* (control failures) and which are
*risks* (conditions that could cause future loss)? They are not the same
thing and conflating them is the most common junior GRC error. Produce:
- a findings list with severity, owner, and remediation dates
- risk register entries with inherent/residual scoring
- **one** entry for the board risk report, written in business language,
  under 120 words

---

## Deliverables for this pack

Produce all of these. They are portfolio pieces.

1. **Incident classification memo** (DORA Art. 18 criteria, one page)
2. **Regulatory notification drafts** — initial notification to Banco de
   Portugal; GDPR Art. 33 notification to CNPD; decision note on RJC/CNCS
3. **Merchant communication** — the actual email to the 5 affected merchants
4. **Board paper** — one page, what happened, what it cost, what we're doing
5. **Post-incident review** — findings, root causes, corrective actions with
   owners and dates
6. **Risk register updates** — new and revised entries with scoring rationale
7. **Lessons-learned control changes** — which specific ISO 27001 Annex A and
   DORA articles now need attention, and what evidence will prove closure

## Self-check

If your post-incident review blames the on-call engineer, rewrite it. He
followed a process that did not exist. Findings that terminate at a person
rather than at a system are how you fail a Big 4 interview.
