# The Norvela Programme — 12 weeks, end to end

Seven phases. Each has a **mission**, **steps**, a **deliverable**, and a
**proof gate** you must pass before moving on. The proof gate is the point:
it is how you know you actually learned it rather than read it.

Pace assumes ~8 hours a week. Compress to 6 weeks at 16 h/wk if you want.
Do not skip phases. Phase 3 makes no sense without Phase 2's scoping work,
which is precisely the mistake most people make in real jobs.

**The rule that makes this work:** every phase ends with a written artefact
you could hand to a stranger. Not notes. Not a checklist you ticked. A
document with your name on it that would survive being read by an auditor.
Reading produces the feeling of learning. Writing produces the thing.

---

## Phase 0 — Set up and orient (Week 1, ~6 h)

**Mission.** Get the lab running and read yourself into the company the way
a new CISO would in their first three days.

**Steps**

1. Work through `02-stack/SETUP.md`. Stop when `healthcheck.sh` is green for
   CISO Assistant, Juice Shop, OpenSearch and Mailpit. Skip GVM for now.
2. Read `01-scenario/00-COMPANY-DOSSIER.md` once, fast, without taking notes.
3. Read it again, slowly, with a blank page. Write down every single thing
   that makes you uncomfortable. Do not organise it. Just list. You should
   reach 40+ items.
4. Now organise that list into three columns: **things that are broken**,
   **things I don't know yet**, **things I would need to ask someone**.
   The third column is the most valuable and the one beginners leave empty.
5. Load ISO 27001:2022, DORA and GDPR libraries into CISO Assistant. Create
   the `Norvela Pay` domain and the five perimeters.

**Deliverable — `Day 3 Observations Memo`, 2 pages max.**
Written to the CEO. What you found, what worries you most, what you need
from her in the next 30 days. No jargon. No framework names in the first
paragraph.

**Proof gate.** Give the memo to someone non-technical and ask them to tell
you back what the top three problems are. If they can't, rewrite it. Executive
communication is a testable skill and this is the test.

---

## Phase 1 — Governance and risk foundations (Weeks 2–3, ~16 h)

**Mission.** Build the machinery that everything else hangs off: risk
criteria, appetite, roles, and a register that is not embarrassing.

**Steps**

1. Open `03-workbooks/risk-register.xlsx`, sheet `INHERITED-REGISTER`.
   Write a critique. Find at least twelve structural defects. Some starters
   so you know the standard: risks stated as single nouns rather than
   cause-event-consequence; no defined scoring criteria so "High" is
   meaningless; departments as owners instead of named humans; "mitigation"
   stated as an aspiration ("AWS is reliable") rather than a control;
   no residual scoring; no link to assets or regulations; no review dates;
   one entry closed with no evidence of closure. Find the rest yourself.
2. Fill in `SCORING-CRITERIA`. The scales are drafted — challenge them.
   Are the financial impact bands right for a €61M-revenue firm? Defend
   your answer with a number (e.g. impact band 5 should be an amount that
   threatens capital adequacy or the licence, not an arbitrary round figure).
3. Complete `RISK-APPETITE`. The draft statements are derived from board
   behaviour in §10 of the dossier. Add at least two more and write the
   escalation path for each.
4. Rebuild the register in `RISK-REGISTER-V2`. Source material: the dossier's
   §4.3 technical facts, `assets.csv`, `vendors.csv`, `iam-users.csv`, and
   the incident pack. **Target 35–45 risks.**
5. Write the governance fix: RACI for the three lines, a Risk Committee
   charter that reflects reality, and a one-page paper on the acting-CISO
   conflict with a recommended resolution.

**Deliverable.** Completed workbook + governance pack (RACI, charter,
conflict paper).

**Proof gate.** Pick your five highest risks. For each, say out loud, in
under 60 seconds and without notes: what could happen, why it could happen
here specifically, what it would cost, and what you would do about it first.
Record yourself. Watch it back. This is literally the interview.

---

## Phase 2 — Scoping and the Statement of Applicability (Week 4, ~8 h)

**Mission.** Decide what is in scope for what, and produce a defensible SoA.
This is the phase people skip and the phase auditors attack.

**Steps**

1. **ISMS scope statement.** Which entities, which locations, which services,
   which assets? The Poland entity has production access — in or out?
   Justify. The sandbox environment — in or out? Justify. Write the scope
   statement in the form an auditor will read it, including exclusions and
   the reason for each.
2. **PCI DSS scope.** Draw the cardholder data environment. Where does PAN
   live? (Ledger, HSM, Datadog logs — the last one is the trap.) Which
   systems are connected-to or security-impacting? Decide SAQ type vs RoC
   and justify. The staging environment holding unmasked PANs blows your
   scope wide open — say so, and price the remediation against the cost of
   the expanded scope.
3. **DORA scope.** Identify the **critical or important functions**. This is
   a judgement call you will defend to a supervisor. Use the test: would
   disruption materially impair financial performance, soundness, or
   continuity of authorised services? Write the justification per function.
4. **NIS2/RJC scope.** Is Norvela an essential or important entity under
   Decreto-Lei 125/2025? Work through the sector and size tests. Then write
   the *lex specialis* analysis: where DORA displaces the RJC for a payment
   institution, and where the RJC still applies. Portugal's RJC entered into
   force 3 April 2026, with CNCS as the lead authority and CERT.PT as the
   national CSIRT — registration and incident duties run through them.
5. **AI Act scope.** Classify Sentinel and Flow. Note the timeline as it now
   stands: the Digital Omnibus (Reg. EU 2026/1744) moved Annex III high-risk
   obligations to **2 December 2027** and Annex I to **2 August 2028**, while
   Art. 50 transparency obligations applied from **2 August 2026**. Decide
   whether Flow is Annex III (creditworthiness) and whether Norvela is
   provider, deployer, or both. Argue it in writing.
6. **Build the SoA** in CISO Assistant against ISO 27001:2022 Annex A
   (93 controls, four themes: 37 organisational, 8 people, 14 physical,
   34 technological). For every control: applicable or not, why, current
   implementation status, and the evidence reference. **Excluding a control
   requires a written justification — those are the ones the auditor reads
   first.** Include Amendment 1:2024: your Clause 4.1 context analysis must
   record a determination on whether climate change is a relevant issue.

**Deliverable.** Five scope statements + a complete SoA.

**Proof gate.** Have someone pick three controls at random from Annex A and
ask you: applicable? why? what's the evidence? If you hesitate on more than
one, your SoA is decoration.

---

## Phase 3 — Control assessment and evidence (Weeks 5–6, ~16 h)

**Mission.** Stop asserting and start proving. This is where the lab stack
earns its keep.

**Steps**

1. **Design vs operating effectiveness.** Learn the distinction cold:
   *design* asks whether the control, as built, would prevent or detect the
   risk; *operating effectiveness* asks whether it actually did, consistently,
   over a period. SOC 2 Type I tests design at a point in time; Type II tests
   operation over 3–12 months. Interviewers ask this constantly.
2. **Write test procedures** for 20 controls before testing anything. Each
   procedure: control objective, test steps, sample size and selection basis,
   evidence required, pass/fail criteria. Sampling matters — for a control
   that operates daily over 12 months, why 25 and not 5? Write the rationale.
3. **Test them.**
   - Access review: use `iam-users.csv`. There are eight planted problems
     (two leavers with live IAM, two unmanaged root accounts, a shared
     contractor account, a dormant admin service account, the breach-vector
     service account, an external auditor account with no expiry). Find all
     eight. Produce the review artefact: who reviewed, when, what was removed.
   - Vulnerability management: `vuln-findings.csv`. There is no SLA. Define
     one, then measure current performance against it. 38 criticals, every
     one of them over 180 days old.
   - Cloud configuration: run Prowler against your AWS account or LocalStack.
     Map every failed check to an Annex A control and a DORA article.
   - Host hardening: OpenSCAP against a VM. Attach `scan-report.html` as
     evidence.
   - Logging: ship something to OpenSearch and write a query that would
     detect the NOR-2026-0908 pattern (service account, unusual source IP,
     payout volume anomaly). A detection you can demonstrate beats a policy
     that says you detect.
4. **Build the evidence library.** One folder per control. Naming convention,
   collection date, collector, period covered, and — critically — whether it
   is design or operating evidence.

**Deliverable.** 20 tested controls with workpapers and an evidence library.

**Proof gate.** Hand your access review workpaper to someone and ask: could
you re-perform this test from what's written here and get the same answer?
That is the actual standard for audit documentation.

---

## Phase 4 — Third-party risk and the DORA Register (Weeks 7–8, ~16 h)

**Mission.** The single most employable artefact in this lab.

**Steps**

1. Build a tiering model. Not "high/medium/low" — a model with criteria:
   does it support a critical or important function, does it process
   personal or cardholder data, is it substitutable, what is the
   concentration exposure?
2. Tier all 20 vendors in `vendors.csv`.
3. Run a full due-diligence assessment on the worst three. Sertã Systems is
   the deliberate horror: a two-person company with standing VPN access to
   the authoritative settlement ledger, a 2019 contract with no DORA clauses,
   no audit rights, no exit plan. Write the assessment, the risk acceptance
   or treatment recommendation, and the contract remediation asks.
4. **Build the Register of Information** in
   `03-workbooks/dora-register-of-information.xlsx`. Work the sheets in the
   order the HOW-TO tab gives. The function taxonomy comes first: you cannot
   populate anything until you have decided what is critical or important.
   Cite Art. 28(3) and the ITS (EU) 2024/2956 in your covering note.
5. Write the **data-quality statement**: every field you could not populate,
   why, who owns closing it, by when. This directly answers the Banco de
   Portugal letter of 2026-03-11 and is due 2026-11-30 in scenario time.
6. Concentration risk analysis: AWS supports 100% of production. Write the
   board paper on it — the options, the cost of each, and your recommendation.
   "Multi-cloud everything" is the wrong answer and you should be able to
   say why.

**Deliverable.** Completed RoI + data-quality statement + concentration
paper + three due-diligence reports.

**Proof gate.** Explain to a non-specialist, in three minutes, what the
Register of Information is for and why regulators wanted it. If you say
"because DORA requires it," you have not understood it. (It exists so
supervisors can see systemic concentration across the whole sector — which
is how the first critical provider designations were made.)

---

## Phase 5 — Incident, continuity, and the regulatory clock (Week 9, ~8 h)

**Mission.** Perform under time pressure with incomplete information.

**Steps**

1. Work `01-scenario/10-INCIDENT.md` **in real time**. Set a timer. Make each
   **[DECIDE]** call before reading on, and timestamp your decisions.
2. Produce all seven deliverables listed at the end of that pack.
3. Then go back and do the thing nobody does: **compare your T+11h
   classification to your T+2day classification** and write the note
   explaining why the first one was reasonable on the information available.
   Supervisors judge the process, not the hindsight.
4. Run the BIA Norvela never did. RTO/RPO per business service. Then check
   them against reality: the Ledger restore has never been successfully
   tested since a failed 2022 attempt. What is your *actual* RTO? It is not
   the number in the plan.
5. Write the DORA-aware incident response plan and the cloud-outage
   continuity plan the company lacks.

**Deliverable.** Full incident pack + BIA + revised IRP and BCP.

**Proof gate.** Have someone read you the incident timeline aloud, stopping
at each decision point, and answer cold. No notes. That is the tabletop
exercise and it is also how a panel interview for a risk role feels.

---

## Phase 6 — Reporting, audit and the board (Week 10, ~8 h)

**Mission.** Make the work land with people who have 90 seconds.

**Steps**

1. **Internal audit.** Plan and perform an ISO 27001 internal audit of three
   Annex A themes. Audit programme, checklist, evidence, findings with
   nonconformity classification (major/minor/observation), and a CAPA plan.
2. **Management review.** Produce the Clause 9.3 management review input
   pack and minutes. This is the clause auditors find missing most often.
3. **Metrics.** Build a KRI/KPI set that a board would actually use. Rules:
   no more than 8; each must have a threshold; each must be automatically
   collectable; each must be one someone would act on. Kill any metric where
   the honest answer to "what would we do if this went red?" is "nothing."
4. **Board paper.** One page. The quarterly risk report. Top risks, movement
   since last quarter, appetite breaches, the ask.
5. **The customer questionnaire.** 214 questions, three weeks, €4.1M ARR on
   the line. Build the answer library so the next one takes two days instead
   of three weeks. That reuse instinct is a senior-analyst trait.
6. **Quantify.** Run `tools/fair_analysis.py`, change the inputs to your own
   calibrated estimates, and write the investment case.

**Deliverable.** Audit report + management review pack + metrics dashboard +
board paper + questionnaire response.

**Proof gate.** Your board paper must fit on one page and survive the test:
would a CFO who reads only the first two sentences know what you want and
why? If not, rewrite.

---

## Phase 7 — Interview conversion (Weeks 11–12, ~16 h)

**Mission.** Turn twelve weeks of artefacts into offers.

**Steps**

1. Work `05-interview/QUESTION-BANK.md` — 120 questions across six
   categories, with what a strong answer contains.
2. Build your **STAR bank**: 12 stories drawn from this lab plus your actual
   professional background. If you come from SOC, DFIR, pentest or CTI,
   your operational history is a genuine advantage in GRC interviews — most
   GRC candidates have never seen an attack. Lead with that.
3. Do the **case studies** in `05-interview/CASE-STUDIES.md` under timed
   conditions.
4. Build the **portfolio**: a sanitised public version of the SoA, the RoI
   approach, the incident classification memo, the FAIR analysis. Redact
   nothing real because none of it is real — that is the advantage of a lab
   company. Write it up as "an assessment I performed against a simulated
   EU payments institution," and be explicit that it is a lab. Nobody minds;
   everybody is impressed that you built it.
5. Write your positioning: your background, your certifications, plus this
   lab. For candidates with a technical security background the strongest
   story is "I can assess a control and also tell you whether an attacker
   would actually care about it" — which is rare and valuable.

**Deliverable.** Portfolio, STAR bank, timed case-study performances.

---

## The self-assessment

Score yourself 1–5 on each, honestly, at the start and at the end.

| Capability | Phase |
|---|---|
| Write a risk statement that separates cause, event and consequence | 1 |
| Define and defend likelihood/impact criteria | 1 |
| Translate board behaviour into written risk appetite | 1 |
| Scope an ISMS and justify exclusions | 2 |
| Scope a CDE and explain what expands it | 2 |
| Identify critical or important functions under DORA | 2 |
| Build a defensible Statement of Applicability | 2 |
| Distinguish design from operating effectiveness | 3 |
| Write a re-performable test procedure | 3 |
| Choose and justify a sample size | 3 |
| Judge evidence strength | 3 |
| Tier third parties against criteria, not vibes | 4 |
| Build a DORA Register of Information | 4 |
| Analyse concentration risk and propose realistic treatment | 4 |
| Classify an incident under DORA against the RTS criteria | 5 |
| Determine the GDPR Art. 33 awareness moment | 5 |
| Run a BIA and derive honest RTOs | 5 |
| Plan and perform an internal audit | 6 |
| Build metrics someone would act on | 6 |
| Write one page a board will read | 6 |
| Quantify risk in money and defend the model | 6 |

Anything still at 3 or below after Phase 7: go back to that phase and redo
the deliverable. The gaps are always in the phases you rushed.

---

## A note on the regulatory dates in this lab

Regulation moves. The dates used here were current as of September 2026:
Portugal's NIS2 transposition (Decreto-Lei 125/2025) in force 3 April 2026;
the EU AI Act Digital Omnibus (Reg. EU 2026/1744) moving Annex III high-risk
obligations to 2 December 2027 and Annex I to 2 August 2028, with Art. 50
transparency applying from 2 August 2026; the ISO 27001:2013→2022 transition
having closed 31 October 2025.

**Verify every date before you cite it in an interview.** The habit of
checking rather than reciting is itself the professional skill — and saying
"that was the position as of [date], I'd confirm it's still current" is a
strictly better answer than a confident wrong number.
