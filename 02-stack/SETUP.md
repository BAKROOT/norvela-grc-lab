# Lab Setup — one evening, start to finish

Target: a working GRC lab in about 3 hours, most of which is downloads.

Hardware: 16 GB RAM is comfortable, 8 GB works if you skip the scanning
profile. ~60 GB disk. Linux or macOS; Windows needs WSL2.

---

## Part 1 — CISO Assistant (your GRC platform) — 30 min

This is the centre of the lab. It is AGPL-licensed, self-hosted, and carries
built-in libraries for ISO 27001:2022, NIS2, DORA, GDPR, SOC 2, PCI DSS 4.0.1,
NIST CSF 2.0, CIS, EU AI Act, ISO 42001 and ~200 more — plus automatic
mapping between them. That last part is what makes it worth the setup: you
will physically see one control satisfying six frameworks, which is the
single most important intuition in this job.

```bash
git clone --single-branch -b main \
  https://github.com/intuitem/ciso-assistant-community.git
cd ciso-assistant-community
./docker-compose.sh          # Linux / macOS
# ./docker-compose.ps1       # Windows (Docker Desktop + WSL2)
```

It prompts for a superuser email and password. Then open
**https://localhost:8443** and accept the self-signed certificate.

> Use a release tag rather than `main` if you want stability — `main` is the
> merge upstream and can break. `git tag -l | tail -5` then `git checkout` it.

**First things to do inside it, in this order:**

1. **Governance → Libraries → Load** the frameworks you need. Start with
   exactly three: `ISO 27001:2022`, `DORA`, `GDPR`. Adding twenty on day one
   is how people drown. Add NIS2, PCI DSS 4.0.1 and EU AI Act in Phase 3.
2. Create a **Domain** called `Norvela Pay` and **Perimeters** for each
   product line (PayRails, Vault, Flow, Sentinel) plus `Corporate`.
3. Load your assets from `03-workbooks/assets.csv` — the data import wizard
   takes CSV, or use the REST API (see `tools/api-examples.sh`, which
   creates the domain and perimeters and imports `assets.csv` for you).
4. Do **not** start an audit yet. Scope first. Phase 2 explains why.

The REST API is the reason to prefer this tool over clicking: create a
Personal Access Token from your profile and drive it with
`Authorization: Token <token>` (note: `Token`, not `Bearer`). Automating
evidence collection through that API is a portfolio piece on its own.

---

## Part 2 — Second opinion platform: SimpleRisk — 15 min (optional)

Worth doing once, because interviewers ask "which GRC tools have you used"
and two is a better answer than one. It also models risk differently, which
teaches you that the tool's data model is an opinion, not a law.

```bash
docker run -d --name simplerisk -p 8080:80 -p 8444:443 simplerisk/simplerisk:latest
```

Then http://localhost:8080. (HTTPS is mapped to 8444 because CISO Assistant
already owns 8443.) It carries CIS Controls, NIST 800-171, PCI DSS
and HIPAA self-assessments out of the box.

Skip this if you are short on time. CISO Assistant alone is enough.

---

## Part 3 — The supporting stack — 20 min

```bash
cd norvela-grc-lab/02-stack
docker compose up -d
```

| Service | URL | Why it exists |
|---|---|---|
| Juice Shop | http://localhost:3000 | A target that actually fails controls |
| DVWA | http://localhost:8081 | Second target (admin/password) |
| OpenSearch | http://localhost:9200 | Evidence store you can query |
| Dashboards | http://localhost:5601 | Build a real control-monitoring dashboard |
| Mailpit | http://localhost:8025 | Proves an alert fired |

Add vulnerability scanning when you get to Phase 3 (control assessment):

```bash
docker compose --profile scanning up -d
# https://localhost:9392  admin / labadmin
# First start syncs the NVT feed — 30-60 min. Leave it.
```

---

## Part 4 — Cloud configuration assessment — 30 min

You need a cloud account to assess. Two honest options:

**Option A — a real AWS free-tier account (recommended).** Build a small,
deliberately flawed estate: an S3 bucket with public read, a security group
open on 0.0.0.0/0:22, an IAM user with no MFA and an ancient access key, an
unencrypted RDS snapshot, CloudTrail disabled in one region. Then scan it.
Total cost if you stay in free tier and tear down after: near zero. Set a
billing alarm at €5 before you start, and delete everything when done.

**Option B — LocalStack**, if you will not touch a real account. Free tier
covers enough services for most Prowler checks.

Then:

```bash
pip install prowler
prowler aws --compliance cis_3.0_aws
prowler aws --compliance iso27001_2013_aws
prowler aws --compliance nis2_aws
prowler dashboard          # local UI over your findings
```

Prowler ships compliance mappings for CIS, NIST 800-53, NIST CSF, ISO 27001,
PCI DSS 4.0, SOC 2, GDPR, HIPAA, FedRAMP, NIS2, MITRE ATT&CK and more. The
exercise is not "run the scanner." The exercise is: take the JSON output,
map each failed check to an ISO 27001 Annex A control and a DORA article,
and decide which failures are *risks* and which are *findings*. That
translation step is the job.

Export findings for the register:

```bash
prowler aws --compliance iso27001_2013_aws --output-formats json csv \
  --output-directory ./prowler-out
```

---

## Part 5 — Host hardening evidence — 20 min

```bash
# Debian/Ubuntu host or VM
sudo apt install -y openscap-scanner ssg-debderived
oscap xccdf eval --profile cis_level1_server \
  --results scan-results.xml --report scan-report.html \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml
```

`scan-report.html` is a genuine piece of audit evidence. Attach it to a
control in CISO Assistant. That is what "evidence" means — a
machine-generated, timestamped artefact, not a screenshot of a settings page.

**Learn this distinction now, because it is an interview question:**

| Weak evidence | Strong evidence |
|---|---|
| Screenshot of a config screen | Config exported by API with a timestamp |
| "The policy says we do X" | A log showing X happened 400 times last month |
| An email saying access was reviewed | The reviewed list, the reviewer, the date, the removals that followed |
| A vendor's ISO certificate | The certificate *plus* the Statement of Applicability *plus* whether your service is in scope |

---

## Part 6 — Quantitative risk — 10 min

```bash
pip install numpy matplotlib
python3 tools/fair_analysis.py       # run from 02-stack/
```

This models the settlement-fraud scenario from the incident pack with a
Monte Carlo simulation and gives you a loss-exceedance curve. Being able to
say "the 90th percentile annual loss for this scenario is €X, and this
control reduces it to €Y, at a cost of €Z" is what separates GRC people who
get listened to by a CFO from GRC people who show heat maps.

---

## Verify your lab

```bash
bash tools/healthcheck.sh            # run from 02-stack/
```

---

## What you deliberately do NOT need

- **Not a commercial GRC tool.** Archer/ServiceNow/OneTrust experience is
  nice on a CV but nobody expects you to have licensed one. Knowing the
  *concepts* transfers completely; every one of these tools is a risk
  register, a control library, a mapping engine and a workflow.
- **Not a certification first.** Build the artefacts, then certify. A
  portfolio of a real RoI, a real SoA and a real incident pack beats a
  certificate with nothing behind it. If you already hold one (CISM, CISA,
  ISO 27001 LI), this is what gives it substance.
- **Not a big lab.** Everything above runs on one laptop.
