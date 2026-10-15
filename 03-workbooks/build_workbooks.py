#!/usr/bin/env python3
"""Generate the Norvela Pay lab data files.

Produces:
  vendors.csv                        - third-party register (TPRM + DORA RoI input)
  assets.csv                         - asset inventory (deliberately inconsistent)
  iam-users.csv                      - identity extract for access review practice
  vuln-findings.csv                  - open vulnerability findings extract
  risk-register.xlsx                 - the stale register you inherit, plus a
                                       properly designed register to rebuild into
  dora-register-of-information.xlsx  - DORA Register of Information working template

Usage:  pip install openpyxl && python3 build_workbooks.py
Output is deterministic (fixed seed), so regenerating reproduces the
committed files.
"""
import csv
import os
import random
from datetime import date, timedelta

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(1848)

HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(color="FFFFFF", bold=True, size=10)
SUB_FILL = PatternFill("solid", fgColor="DDEBF7")


def style_header(ws, row=1, freeze=True):
    for cell in ws[row]:
        if cell.value is None:
            continue
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 32
    if freeze:
        ws.freeze_panes = ws.cell(row=row + 1, column=1)


def autosize(ws, maxw=52):
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        width = max((len(str(c.value)) for c in col if c.value is not None), default=8)
        ws.column_dimensions[letter].width = min(max(width + 2, 10), maxw)


# --------------------------------------------------------------------------
# vendors.csv
# --------------------------------------------------------------------------
VENDORS = [
    # name, service, country, hosting, entity_served, contract_start, annual_eur,
    # supports_critical_fn, data_shared, last_review, has_dora_clauses,
    # exit_plan, cert_held, subprocessors_mapped, notes
    ("Amazon Web Services", "Cloud infrastructure (IaaS/PaaS)", "IE", "EU (IE, DE)",
     "Norvela Pay S.A.", "2019-04-01", 2_940_000, "Yes",
     "All production data incl. PAN", "2025-02-14", "Partial", "No",
     "ISO 27001, SOC 2, PCI DSS", "No",
     "Concentration risk: 100% of production. Exit plan is a slide, not a plan."),
    ("Banco Astera, S.A.", "Lending partner (Flow product)", "ES", "EU (ES)",
     "Norvela Pay S.A.", "2022-06-15", 0, "Yes",
     "Merchant financials, credit scores", "2024-09-01", "No", "No",
     "Not provided", "No",
     "Revenue-share not fee. Is this an ICT third party under DORA? Argue it."),
    ("Sertã Systems, Lda.", "Oracle Ledger reconciliation support", "PT", "On-prem access",
     "Norvela Pay S.A.", "2019-01-10", 84_000, "Yes",
     "Full settlement ledger", "Never", "No", "No",
     "None", "No",
     "TWO-PERSON COMPANY with standing VPN to the Ledger. No audit rights. "
     "Key-person risk. Worst vendor exposure in the estate."),
    ("Cloudflare", "WAF / CDN / DDoS", "US", "Global anycast",
     "Norvela Pay S.A.", "2020-03-01", 96_000, "Yes",
     "Traffic metadata, TLS termination", "2025-06-30", "Partial", "No",
     "ISO 27001, SOC 2", "No",
     "All merchant traffic transits. Single point of failure."),
    ("GitHub (Microsoft)", "Source control + CI/CD", "US", "US",
     "Norvela Pay S.A.", "2019-02-01", 62_000, "Yes",
     "Source code, deployment credentials", "2025-01-20", "Partial", "No",
     "ISO 27001, SOC 2", "No",
     "CI/CD is the production change path. Org went public for 11 days Mar-2024."),
    ("Snowflake", "Analytics data warehouse", "US", "EU (DE)",
     "Norvela Pay S.A.", "2024-08-01", 210_000, "Yes",
     "Full transaction history, customer PII", "Never", "No", "No",
     "ISO 27001, SOC 2", "No",
     "SHADOW IT: procured on a data-team credit card. Never went through "
     "vendor review. No DPA on file."),
    ("Onfido", "KYC identity verification", "GB", "EU (IE)",
     "Norvela Pay S.A.", "2021-05-01", 340_000, "No",
     "ID documents, biometric facial data", "2025-03-11", "Yes", "Partial",
     "ISO 27001, SOC 2", "No",
     "Biometric = GDPR Art. 9 special category. Sub-processor chain unmapped. "
     "Post-Brexit UK transfer — adequacy decision basis?"),
    ("Talkdesk", "Contact centre / call recording", "US", "US (us-east-1)",
     "Norvela Pay Iberia S.L.", "2021-09-01", 128_000, "No",
     "Call recordings, customer PII", "2024-02-20", "No", "No",
     "SOC 2", "No",
     "US hosting. Recordings kept indefinitely. Consent basis claimed but "
     "no consent is actually collected on inbound calls."),
    ("Datadog", "Observability / logging", "US", "EU (DE)",
     "Norvela Pay S.A.", "2020-11-01", 187_000, "Yes",
     "Application logs — 3 confirmed cases of PAN leakage", "2025-05-02",
     "Partial", "No", "ISO 27001, SOC 2, PCI DSS", "No",
     "PAN in logs = PCI DSS scope expansion. Confirmed, unremediated."),
    ("Oracle", "Database licences + support (Ledger)", "US", "On-prem",
     "Norvela Pay S.A.", "2019-01-01", 156_000, "Yes",
     "None (licence only)", "2023-01-15", "No", "N/A",
     "Various", "N/A", "Support contract lapsed to 'sustaining support' tier."),
    ("Iron Mountain", "Offsite tape storage", "PT", "PT",
     "Norvela Pay S.A.", "2019-06-01", 18_000, "Yes",
     "Ledger backups (encrypted)", "2024-11-01", "No", "No",
     "ISO 27001", "N/A", "Restore never tested. Last attempt 2022 failed."),
    ("Thales", "HSM hardware + firmware", "FR", "On-prem",
     "Norvela Pay S.A.", "2020-02-01", 240_000, "Yes",
     "Cryptographic keys", "2025-04-18", "Yes", "N/A",
     "FIPS 140-2 L3, Common Criteria", "N/A", "PCI-critical. Well managed."),
    ("Salesforce", "CRM", "US", "EU (DE)",
     "Norvela Pay Iberia S.L.", "2020-01-15", 145_000, "No",
     "Merchant contacts, pipeline", "2025-07-01", "No", "No",
     "ISO 27001, SOC 2", "No", "Standard SaaS. Low criticality."),
    ("BambooHR", "HRIS", "US", "US",
     "Norvela Pay S.A.", "2021-03-01", 41_000, "No",
     "Employee personal data", "2024-06-10", "No", "No",
     "SOC 2", "No",
     "Does NOT cover the Poland entity — separate HR system. This is why "
     "the leaver process breaks."),
    ("Personio", "HRIS (Poland entity only)", "DE", "EU (DE)",
     "Norvela Tech Sp. z o.o.", "2022-04-01", 12_000, "No",
     "Employee personal data (PL)", "Never", "No", "No",
     "ISO 27001", "No",
     "Unknown to Lisbon IT. Not integrated with Entra ID provisioning."),
    ("Atlassian", "Jira / Confluence", "AU", "EU (DE)",
     "Norvela Pay S.A.", "2019-05-01", 58_000, "No",
     "Internal documentation, tickets", "2025-01-08", "No", "No",
     "ISO 27001, SOC 2", "No", "Contains architecture docs and some secrets."),
    ("Okta", "(DECOMMISSIONED 2023)", "US", "EU",
     "Norvela Pay S.A.", "2020-07-01", 0, "No",
     "Formerly identity", "2023-03-01", "No", "N/A", "SOC 2", "N/A",
     "STILL IN THE REGISTER. Contract terminated but never removed. "
     "Register hygiene finding."),
    ("Stripe", "Card acquiring (fallback rail)", "IE", "EU (IE)",
     "Norvela Pay S.A.", "2023-02-01", 0, "Yes",
     "Transaction data", "2025-08-19", "Yes", "Partial",
     "PCI DSS L1, SOC 2", "No", "Fallback acquirer. Variable cost model."),
    ("Jamf", "macOS endpoint management", "US", "EU (DE)",
     "Norvela Pay S.A.", "2021-01-01", 34_000, "No",
     "Device inventory, config", "2025-02-28", "No", "No",
     "ISO 27001, SOC 2", "No", "Covers 280 Macs. Not the 15 Linux boxes."),
    ("Snyk", "SAST / SCA", "GB", "EU (IE)",
     "Norvela Pay S.A.", "2022-09-01", 72_000, "No",
     "Source code metadata", "2025-06-15", "No", "No",
     "ISO 27001, SOC 2", "No", "1,247 open findings, no SLA defined."),
]

VENDOR_HEADERS = [
    "vendor_name", "service_description", "country_of_incorporation",
    "data_hosting_location", "contracting_entity", "contract_start",
    "annual_spend_eur", "supports_critical_or_important_function",
    "data_shared", "last_risk_review", "dora_contractual_clauses",
    "documented_exit_plan", "certifications_held", "subprocessors_mapped",
    "analyst_notes",
]


def write_vendors():
    path = os.path.join(HERE, "vendors.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(VENDOR_HEADERS)
        w.writerows(VENDORS)
    return path


# --------------------------------------------------------------------------
# assets.csv  (three inconsistent sources, merged with conflicts intact)
# --------------------------------------------------------------------------
ASSETS = [
    # id, name, type, owner, environment, classification, source_inventory,
    # hosting, supports_cif, notes
    ("AST-001", "Ledger (Oracle 19c)", "Database", "Finance Ops", "Production",
     "Restricted", "CMDB", "On-prem Lisbon", "Yes",
     "Authoritative merchant balances. Restore untested since 2022."),
    ("AST-002", "Vault balance service", "Application", "Platform Eng",
     "Production", "Restricted", "CMDB", "AWS eu-west-1", "Yes",
     "Real-time fund movement. App logs 14-day retention."),
    ("AST-003", "PayRails API gateway", "Application", "Platform Eng",
     "Production", "Restricted", "CMDB", "AWS eu-west-1", "Yes", ""),
    ("AST-004", "Sentinel fraud model", "ML model", "Data Science",
     "Production", "Confidential", "Spreadsheet-DataTeam", "AWS eu-central-1",
     "Yes", "Retrained monthly. No approval gate, no model card, no bias test."),
    ("AST-005", "Flow credit model", "ML model", "Data Science", "Production",
     "Confidential", "Spreadsheet-DataTeam", "AWS eu-central-1", "Yes",
     "Feeds Banco Astera lending decision. AI Act classification unresolved."),
    ("AST-006", "HSM cluster (Thales)", "Hardware", "Platform Eng",
     "Production", "Restricted", "CMDB", "On-prem Lisbon", "Yes",
     "Reachable from any office VLAN — no segmentation."),
    ("AST-007", "Entra ID tenant", "Identity", "IT", "Production",
     "Restricted", "IT-Asset-List", "Microsoft cloud", "Yes",
     "IdP for 31 SaaS apps. MFA enforced."),
    ("AST-008", "norvela-data lake (S3)", "Data store", "Data Science",
     "Production", "Restricted", "Spreadsheet-DataTeam", "AWS eu-central-1",
     "Yes", "7 years of transactions. Queried during NOR-2026-0908."),
    ("AST-009", "norvela-staging environment", "Environment", "Platform Eng",
     "Staging", "Internal", "CMDB", "AWS eu-west-1", "No",
     "CLASSIFICATION WRONG: holds unmasked production PANs from Nov-2025 "
     "restore. 60 developers have read access."),
    ("AST-010", "norvela-sandbox (merchant test)", "Environment",
     "Developer Relations", "Sandbox", "Public", "CMDB", "AWS eu-west-1",
     "No", "Root account MFA not enforced. Credential holder unknown."),
    ("AST-011", "norvela-dev", "Environment", "Platform Eng", "Development",
     "Internal", "CMDB", "AWS eu-west-1", "No",
     "60 engineers hold PowerUserAccess. Root MFA not enforced."),
    ("AST-012", "norvela-audit (log archive)", "Data store", "Security",
     "Production", "Restricted", "CMDB", "AWS eu-west-1", "Yes",
     "CloudTrail org trail, 400-day retention. Saved the 2026-09 investigation."),
    ("AST-013", "ESXi host 01", "Hardware", "IT", "Production", "Internal",
     "IT-Asset-List", "On-prem Lisbon", "No",
     "Version end-of-support since 2024."),
    ("AST-014", "ESXi host 02", "Hardware", "IT", "Production", "Internal",
     "IT-Asset-List", "On-prem Lisbon", "No",
     "Version end-of-support since 2024."),
    ("AST-015", "GitHub org (norvela)", "SaaS", "Platform Eng", "Production",
     "Confidential", "Spreadsheet-DataTeam", "GitHub US", "Yes",
     "Deploy pipeline. 22 secrets found in history 2025, 6 unrotated."),
    ("AST-016", "Snowflake warehouse", "SaaS", "Data Science", "Production",
     "Restricted", "NOT IN ANY INVENTORY", "Snowflake EU-DE", "Yes",
     "SHADOW IT. Discovered only via the expense report. No DPA."),
    ("AST-017", "Corporate WiFi (Lisbon)", "Network", "IT", "Production",
     "Internal", "IT-Asset-List", "On-prem Lisbon", "No",
     "Flat network — reaches the server room."),
    ("AST-018", "Poland NOC workstations (15x Linux)", "Endpoint",
     "Norvela Tech", "Production", "Internal", "NOT IN ANY INVENTORY",
     "Kraków office", "Yes",
     "Unmanaged. No EDR, no patch management. Have production access."),
    ("AST-019", "Jamf-managed Macs (280)", "Endpoint", "IT", "Production",
     "Internal", "IT-Asset-List", "Distributed", "No", ""),
    ("AST-020", "Intune-managed Windows (45)", "Endpoint", "IT", "Production",
     "Internal", "IT-Asset-List", "Distributed", "No", ""),
    ("AST-021", "Backup tapes (Ledger)", "Media", "IT", "Production",
     "Restricted", "CMDB", "Iron Mountain PT", "Yes",
     "Weekly. Restore untested."),
    ("AST-022", "Merchant portal (web)", "Application", "Product",
     "Production", "Confidential", "CMDB", "AWS eu-west-1", "Yes", ""),
    ("AST-023", "Settlement batch service", "Application", "Platform Eng",
     "Production", "Restricted", "CMDB", "AWS eu-west-1", "Yes",
     "Runs as svc-settlement-batch. Key last rotated 2023. Breach vector."),
    ("AST-024", "Talkdesk call recordings", "Data store", "Customer Support",
     "Production", "Confidential", "NOT IN ANY INVENTORY", "Talkdesk US",
     "No", "~9,000/yr, retained indefinitely, US-hosted."),
]

ASSET_HEADERS = ["asset_id", "asset_name", "asset_type", "owner", "environment",
                 "classification", "source_inventory", "hosting_location",
                 "supports_critical_or_important_function", "notes"]


def write_assets():
    path = os.path.join(HERE, "assets.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(ASSET_HEADERS)
        w.writerows(ASSETS)
    return path


# --------------------------------------------------------------------------
# iam-users.csv — access review practice
# --------------------------------------------------------------------------
FIRST = ["Ana", "João", "Miguel", "Beatriz", "Tomás", "Inês", "Rui", "Carolina",
         "Pedro", "Mariana", "Diogo", "Sofia", "André", "Catarina", "Ricardo",
         "Piotr", "Agnieszka", "Krzysztof", "Magdalena", "Tomasz", "Marek",
         "Elena", "Javier", "Lucía", "Carlos"]
LAST = ["Silva", "Santos", "Ferreira", "Pereira", "Oliveira", "Costa", "Rodrigues",
        "Martins", "Sousa", "Fernandes", "Gonçalves", "Nowak", "Kowalski",
        "Wiśniewski", "Wójcik", "Kamiński", "García", "Martínez", "López"]
DEPTS = ["Platform Engineering", "Data Science", "Finance Ops", "Customer Support",
         "Product", "Security", "IT", "Sales", "Compliance", "NOC (Poland)"]
ROLES = ["ReadOnlyAccess", "PowerUserAccess", "prod-admin (break-glass)",
         "DeveloperAccess", "BillingAccess", "SecurityAudit", "AdministratorAccess"]


def write_iam():
    path = os.path.join(HERE, "iam-users.csv")
    rows = []
    today = date(2026, 9, 22)
    seen = set()
    for i in range(1, 121):
        # IAM usernames are unique per account — redraw on collision.
        fn, ln = random.choice(FIRST), random.choice(LAST)
        while f"{fn}.{ln}".lower() in seen:
            fn, ln = random.choice(FIRST), random.choice(LAST)
        seen.add(f"{fn}.{ln}".lower())
        dept = random.choice(DEPTS)
        role = random.choice(ROLES)
        created = today - timedelta(days=random.randint(30, 1500))
        last_used = today - timedelta(days=random.choice(
            [0, 1, 2, 3, 5, 8, 14, 21, 45, 90, 180, 240, 400]))
        mfa = random.choice(["Yes"] * 8 + ["No"] * 2)
        key_age = random.choice([None, 30, 90, 180, 400, 900, 1200])
        status = "Active"
        rows.append([
            f"IAM-{i:03d}", f"{fn.lower()}.{ln.lower()}", f"{fn} {ln}", dept,
            role, created.isoformat(), last_used.isoformat(), mfa,
            key_age if key_age else "", status, "",
        ])

    # Planted findings — these are the ones you must catch.
    planted = [
        ["IAM-121", "svc-settlement-batch", "SERVICE ACCOUNT", "Platform Engineering",
         "PowerUserAccess", "2020-02-11", "2026-09-08", "No", 1320, "Active",
         "Breach vector in NOR-2026-0908. Key not rotated since 2023."],
        ["IAM-122", "svc-legacy-etl", "SERVICE ACCOUNT", "Data Science",
         "AdministratorAccess", "2019-08-04", "2024-03-02", "No", 1800, "Active",
         "Not used in 2.5 years. Still AdministratorAccess."],
        ["IAM-123", "r.tavares", "Rúben Tavares", "Platform Engineering",
         "prod-admin (break-glass)", "2021-06-01", "2026-07-11", "Yes", 640,
         "Active", "LEFT THE COMPANY 2026-07-18. Entra disabled, IAM not."],
        ["IAM-124", "l.moreira", "Lara Moreira", "Data Science",
         "PowerUserAccess", "2022-01-17", "2026-07-04", "Yes", 410, "Active",
         "LEFT THE COMPANY 2026-07-31. Entra disabled, IAM not."],
        ["IAM-125", "contractor-nocturne-01", "Agency contractor (Poland NOC)",
         "NOC (Poland)", "prod-admin (break-glass)", "2025-11-03", "2026-09-08",
         "No", 320, "Active",
         "Shared account used by rotating agency staff. No individual "
         "accountability. Used during the incident."],
        ["IAM-126", "root-norvela-sandbox", "AWS ROOT", "Unknown", "root",
         "2019-03-01", "2025-12-14", "No", "", "Active",
         "Root account, no MFA, owner unknown."],
        ["IAM-127", "root-norvela-dev", "AWS ROOT", "Unknown", "root",
         "2019-03-01", "2026-02-02", "No", "", "Active",
         "Root account, no MFA."],
        ["IAM-128", "audit-readonly-external", "Atlântico Certificação", "External",
         "SecurityAudit", "2026-08-01", "2026-08-14", "Yes", "", "Active",
         "External auditor account — no expiry set."],
    ]
    rows.extend(planted)

    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["iam_id", "username", "display_name", "department",
                    "aws_role", "created", "last_used", "mfa_enabled",
                    "access_key_age_days", "status", "notes"])
        w.writerows(rows)
    return path


# --------------------------------------------------------------------------
# risk-register.xlsx
# --------------------------------------------------------------------------
INHERITED = [
    ("R-01", "Cyber attack", "IT", "High", "High", "Firewall in place", "Open", "2025-04-02"),
    ("R-02", "Data breach", "IT", "High", "Medium", "Encryption", "Open", "2025-04-02"),
    ("R-03", "Staff leaving", "HR", "Medium", "Medium", "Retention bonuses", "Open", "2024-11-15"),
    ("R-04", "Cloud outage", "IT", "Medium", "High", "AWS is reliable", "Open", "2025-04-02"),
    ("R-05", "GDPR fine", "Legal", "Low", "High", "We have a DPO", "Open", "2024-06-01"),
    ("R-06", "Fraud", "Finance", "Medium", "High", "Sentinel model", "Open", "2025-04-02"),
    ("R-07", "Regulatory change", "Compliance", "High", "Medium", "We monitor", "Open", "2025-01-10"),
    ("R-08", "Key person dependency", "Ops", "Medium", "Medium", "Documentation", "Open", "2024-09-20"),
    ("R-09", "Vendor failure", "Procurement", "Low", "High", "Contracts", "Open", "2024-06-01"),
    ("R-10", "Ransomware", "IT", "Medium", "High", "Backups", "Open", "2025-04-02"),
    ("R-11", "Insider threat", "IT", "Low", "High", "Background checks", "Open", "2024-06-01"),
    ("R-12", "DDoS", "IT", "Medium", "Medium", "Cloudflare", "Closed", "2024-03-11"),
    ("R-13", "Physical security", "Facilities", "Low", "Low", "Badge access", "Open", "2023-12-01"),
    ("R-14", "Phishing", "IT", "High", "Medium", "Training", "Open", "2025-04-02"),
    ("R-15", "Legacy systems", "IT", "High", "Medium", "Roadmap", "Open", "2024-06-01"),
    ("R-16", "Third party access", "IT", "Medium", "High", "VPN", "Open", "2024-06-01"),
    ("R-17", "Change failure", "Eng", "Medium", "Medium", "Testing", "Open", "2025-04-02"),
    ("R-18", "Backup failure", "IT", "Low", "High", "Tapes", "Open", "2023-08-14"),
    ("R-19", "AML breach", "Compliance", "Low", "High", "Screening", "Open", "2025-04-02"),
    ("R-20", "Licence withdrawal", "Compliance", "Low", "High", "Good relations", "Open", "2024-06-01"),
    ("R-21", "Model risk", "Data", "Medium", "Medium", "Monitoring", "Open", "2025-04-02"),
    ("R-22", "Concentration risk", "Procurement", "Medium", "High", "None", "Open", "2025-04-02"),
    ("R-23", "Skills shortage", "HR", "High", "Low", "Recruiting", "Open", "2025-04-02"),
]

NEW_COLUMNS = [
    "risk_id", "risk_title",
    "risk_statement (Cause -> Event -> Consequence)",
    "risk_category", "affected_asset_ids", "affected_business_service",
    "threat_source", "vulnerability_exploited",
    "risk_owner (named individual)", "date_identified",
    "inherent_likelihood (1-5)", "inherent_impact (1-5)", "inherent_score",
    "existing_controls (control IDs)", "control_effectiveness (E/PE/I/NT)",
    "residual_likelihood (1-5)", "residual_impact (1-5)", "residual_score",
    "within_appetite? (Y/N)", "treatment_decision",
    "treatment_actions", "action_owner", "target_date", "status",
    "annual_loss_expectancy_eur (FAIR)",
    "regulatory_linkage (DORA/NIS2/GDPR/PCI/ISO/AI Act)",
    "last_reviewed", "next_review_due", "evidence_reference",
]

APPETITE_ROWS = [
    ("Regulatory & licence", "Zero tolerance",
     "No finding that could reasonably lead to a licence condition, "
     "restriction or withdrawal by Banco de Portugal.",
     "Any Category 1 supervisory finding; any missed statutory "
     "notification deadline",
     "Immediate CEO + Board notification"),
    ("Settlement accuracy", "Zero tolerance",
     "No unreconciled settlement discrepancy persisting beyond one "
     "business day.",
     ">1 business day unreconciled, OR any single discrepancy >€10,000",
     "CFO notification, incident raised"),
    ("Confidentiality of customer data", "Low",
     "Accept residual risk only where the exposure window is <24h and "
     "affected records <1,000.",
     "Any confirmed exposure >1,000 records OR any special-category data",
     "DPO + CRO, Art.33 assessment within 24h"),
    ("Availability — payment rails", "Low",
     "99.95% monthly availability for PayRails and Vault.",
     "<99.9% in any month, OR any single outage >30 min",
     "CTO + COO, DORA incident assessment"),
    ("Availability — non-payment features", "Moderate",
     "Accept degradation of reporting, portal and analytics features "
     "where payments are unaffected.",
     ">4h outage of merchant portal",
     "Product owner, no board escalation"),
    ("Third-party concentration", "Moderate (currently exceeded)",
     "No single provider should support >60% of critical or important "
     "functions without a tested exit plan.",
     "AWS currently at 100% — breach of appetite, board-accepted with "
     "time-bound remediation",
     "Quarterly board reporting until remediated"),
    ("Financial loss from fraud", "Moderate",
     "Annual fraud loss net of recovery below €750,000 (≈1.2% of revenue).",
     ">€250,000 in any quarter",
     "CFO + CRO review"),
    ("Change failure", "Moderate",
     "Change failure rate below 5%; no change-induced payment outage.",
     "Any change-induced payment incident",
     "CTO review, CAB reinstatement considered"),
]


def build_risk_register():
    wb = openpyxl.Workbook()

    # Sheet 0 — README
    ws = wb.active
    ws.title = "README"
    readme = [
        ["NORVELA PAY — RISK REGISTER WORKBOOK"],
        [],
        ["This workbook has four sheets. Work them in order."],
        [],
        ["1. INHERITED-REGISTER",
         "What you actually inherit on day one. 23 rows of near-useless "
         "entries. Your first exercise is to critique it — write down every "
         "structural defect you can find before you rebuild. There are at "
         "least twelve."],
        ["2. RISK-REGISTER-V2",
         "The rebuilt register. Columns are designed to survive an auditor, "
         "a supervisor and a board. Populate it from the dossier, the "
         "incident pack, the asset list and the vendor register."],
        ["3. SCORING-CRITERIA",
         "Defined 1-5 scales for likelihood and impact. Without these, a "
         "'High' rating is an opinion. With them, it is a finding."],
        ["4. RISK-APPETITE",
         "Draft appetite statements derived from board behaviour. You will "
         "present these for approval in Phase 1."],
        [],
        ["TARGET: 35-45 well-formed risks. Fewer means you missed things; "
         "many more means you are logging findings as risks."],
        [],
        ["The difference between a FINDING and a RISK:"],
        ["FINDING", "A control that does not exist, or exists and does not "
         "work. Present tense. Has an owner and a fix date. "
         "Example: 'Service account credentials are not rotated.'"],
        ["RISK", "A future loss scenario with a cause, an event and a "
         "consequence. Has a likelihood and an impact. "
         "Example: 'Because service credentials are long-lived and stored "
         "in code, an attacker obtaining repository history could initiate "
         "unauthorised payouts, resulting in direct financial loss and "
         "supervisory action.'"],
        ["", "One risk can be caused by many findings. Do not create one "
         "risk per finding — that is the most common way junior analysts "
         "produce a 200-row register that nobody reads."],
    ]
    for row in readme:
        ws.append(row)
    ws["A1"].font = Font(bold=True, size=14)
    for r in (5, 6, 7, 8, 14, 15):
        ws.cell(row=r, column=1).font = Font(bold=True)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 110
    for row in ws.iter_rows(min_col=2, max_col=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    # Sheet 1 — inherited
    ws = wb.create_sheet("INHERITED-REGISTER")
    ws.append(["Risk ID", "Risk", "Owner", "Likelihood", "Impact",
               "Mitigation", "Status", "Last updated"])
    for r in INHERITED:
        ws.append(list(r))
    style_header(ws)
    autosize(ws)

    # Sheet 2 — v2
    ws = wb.create_sheet("RISK-REGISTER-V2")
    ws.append(NEW_COLUMNS)
    style_header(ws)
    for col_idx in (11, 12, 16, 17):
        dv = DataValidation(type="whole", operator="between",
                            formula1=1, formula2=5, allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{get_column_letter(col_idx)}2:{get_column_letter(col_idx)}200")
    dv_eff = DataValidation(
        type="list",
        formula1='"Effective,Partially Effective,Ineffective,Not Tested"',
        allow_blank=True)
    ws.add_data_validation(dv_eff)
    dv_eff.add("O2:O200")
    dv_tr = DataValidation(
        type="list", formula1='"Treat,Tolerate,Transfer,Terminate"',
        allow_blank=True)
    ws.add_data_validation(dv_tr)
    dv_tr.add("T2:T200")
    # score formulas
    for r in range(2, 201):
        ws.cell(row=r, column=13).value = f"=IF(AND(K{r}<>\"\",L{r}<>\"\"),K{r}*L{r},\"\")"
        ws.cell(row=r, column=18).value = f"=IF(AND(P{r}<>\"\",Q{r}<>\"\"),P{r}*Q{r},\"\")"
    autosize(ws, maxw=40)

    # Sheet 3 — scoring
    ws = wb.create_sheet("SCORING-CRITERIA")
    ws.append(["LIKELIHOOD SCALE"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Score", "Label", "Definition", "Frequency guide"])
    like = [
        (1, "Rare", "Would require multiple independent control failures",
         "Less than once in 10 years"),
        (2, "Unlikely", "Possible but no known occurrence in the sector recently",
         "Once in 5-10 years"),
        (3, "Possible", "Has occurred at comparable firms; controls are partial",
         "Once in 2-5 years"),
        (4, "Likely", "Has occurred here or is occurring at peers regularly",
         "Once or more per year"),
        (5, "Almost certain", "Occurring now or control is absent entirely",
         "Multiple times per year"),
    ]
    for r in like:
        ws.append(list(r))
    ws.append([])
    ws.append(["IMPACT SCALE — score the HIGHEST applicable dimension"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, size=12)
    ws.append(["Score", "Financial", "Regulatory", "Customer / operational",
               "Reputational"])
    imp = [
        (1, "<€25k", "Internal observation only", "<10 merchants, <1h",
         "No external awareness"),
        (2, "€25k-€100k", "Supervisory query, informal",
         "<100 merchants or <4h degradation", "Customer complaints"),
        (3, "€100k-€500k", "Formal supervisory finding requiring remediation plan",
         ">100 merchants or payment outage <30min", "Trade press coverage"),
        (4, "€500k-€2.5M", "Enforcement action, fine, or public reprimand",
         "Payment outage >30min or settlement error",
         "National press, merchant churn"),
        (5, ">€2.5M", "Licence condition, restriction or withdrawal",
         "Sustained payment failure or unrecoverable settlement loss",
         "Existential reputational damage"),
    ]
    for r in imp:
        ws.append(list(r))
    ws.append([])
    ws.append(["SCORE BANDS (Likelihood x Impact)"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, size=12)
    ws.append(["Band", "Range", "Governance requirement"])
    for r in [("Low", "1-4", "Risk owner manages. Annual review."),
              ("Moderate", "5-9", "Risk owner manages with documented treatment. "
               "Semi-annual review."),
              ("High", "10-15", "CRO oversight. Treatment plan with dates. "
               "Quarterly review. Reported to Risk Committee."),
              ("Critical", "16-25", "Board notification within 5 business days. "
               "Named executive owner. Monthly review until reduced.")]:
        ws.append(list(r))
    for row_i in (2, 9, 17):
        for cell in ws[row_i]:
            if cell.value:
                cell.fill = SUB_FILL
                cell.font = Font(bold=True)
    autosize(ws, maxw=48)
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    # Sheet 4 — appetite
    ws = wb.create_sheet("RISK-APPETITE")
    ws.append(["Risk category", "Appetite level", "Appetite statement",
               "Tolerance threshold (breach trigger)", "Escalation on breach"])
    for r in APPETITE_ROWS:
        ws.append(list(r))
    style_header(ws)
    autosize(ws, maxw=58)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    path = os.path.join(HERE, "risk-register.xlsx")
    wb.save(path)
    return path


# --------------------------------------------------------------------------
# roi-template.xlsx — DORA Register of Information
# --------------------------------------------------------------------------
ROI_TABLES = {
    "B_01.01 Entity": [
        "LEI of the entity maintaining the register",
        "Name of the entity", "Country of the entity",
        "Type of financial entity", "Competent authority",
        "Date of the reporting",
    ],
    "B_01.02 Entities in scope": [
        "LEI of the entity", "Name of the entity", "Country",
        "Type of financial entity", "Hierarchy of the entity within the group",
        "LEI of the direct parent undertaking", "Date of integration in scope",
        "Date of deletion from scope", "Currency", "Value of total assets",
    ],
    "B_02.01 Contractual arrangements": [
        "Contractual arrangement reference number",
        "Type of contractual arrangement",
        "Overarching contractual arrangement reference number",
        "Currency of the amount reported", "Annual expense or estimated cost",
    ],
    "B_02.02 Arrangement details": [
        "Contractual arrangement reference number",
        "LEI of the financial entity making use of the ICT service",
        "Identification code of the ICT third-party service provider",
        "Type of code to identify the ICT third-party service provider",
        "Function identifier", "Type of ICT services",
        "Start date of the contractual arrangement",
        "End date of the contractual arrangement",
        "Reason of the termination or ending",
        "Notice period for the financial entity",
        "Notice period for the ICT third-party service provider",
        "Country of the governing law", "Country of provision of the ICT services",
        "Storage of data (Yes/No)", "Location of the data at rest (storage)",
        "Location of management of the data (processing)",
        "Sensitiveness of the data stored by the ICT third-party",
        "Level of reliance on the ICT service",
    ],
    "B_03.01 Entities signing": [
        "Contractual arrangement reference number",
        "LEI of the entity signing the contractual arrangement",
    ],
    "B_03.02 Providers signing": [
        "Contractual arrangement reference number",
        "Identification code of the ICT third-party service provider",
        "Type of code to identify the ICT third-party service provider",
    ],
    "B_04.01 Entities using": [
        "Contractual arrangement reference number",
        "LEI of the entity making use of the ICT services",
        "Nature of the entity making use of the ICT services",
    ],
    "B_05.01 Provider details": [
        "Identification code of the ICT third-party service provider",
        "Type of code to identify the ICT third-party service provider",
        "Additional identification code", "Legal name",
        "Name in Latin alphabet", "Type of person",
        "Country of the ICT third-party service provider's headquarters",
        "Currency", "Total annual expense",
        "Identification code of the ICT third-party service provider's "
        "ultimate parent undertaking",
        "Type of code to identify the ultimate parent",
    ],
    "B_05.02 Supply chain": [
        "Contractual arrangement reference number",
        "Type of ICT services",
        "Identification code of the ICT third-party service provider",
        "Type of code", "Rank",
        "Identification code of the recipient of sub-contracted services",
    ],
    "B_06.01 Functions": [
        "Function identifier", "LEI of the financial entity",
        "Licenced activity", "Function name", "Level of criticality "
        "or importance", "Reasons for criticality or importance",
        "Date of the last assessment of criticality or importance",
        "Recovery time objective", "Recovery point objective",
        "Impact of discontinuing the function",
    ],
    "B_07.01 Assessments": [
        "Contractual arrangement reference number",
        "Identification code of the ICT third-party service provider",
        "Type of code",
        "Substitutability of the ICT third-party service provider",
        "Reason if not substitutable or difficult",
        "Date of the last audit on the ICT third-party service provider",
        "Existence of an exit plan",
        "Possibility of reintegration of the contracted ICT service",
        "Impact of discontinuing the ICT services",
        "Are there alternative ICT third-party service providers identified?",
        "Identification of alternative ICT TPP",
    ],
    "B_99.01 Function taxonomy": [
        "Function identifier", "Function name (EBA taxonomy)",
        "Mapped Norvela business service", "Owner",
        "Critical or important? (C/I/N)", "Justification",
    ],
}


def build_roi():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "HOW-TO"
    lines = [
        ["DORA REGISTER OF INFORMATION — WORKING TEMPLATE"],
        [],
        ["Legal basis", "Regulation (EU) 2022/2554 Article 28(3); "
         "Commission Implementing Regulation (EU) 2024/2956 (ITS on "
         "registers of information)."],
        [],
        ["IMPORTANT", "This is a TRAINING template modelled on the ITS table "
         "structure so you learn the shape of the submission and the data "
         "you need to hold. It is NOT the official validated taxonomy "
         "package. For any real submission, download the current ITS "
         "templates, DPM data model and validation rules from the EBA and "
         "from your national competent authority — the field list, "
         "enumerations and validation rules are versioned and change."],
        [],
        ["Why this exercise matters more than any other in the lab"],
        ["", "The RoI is the single artefact that most exposed EU financial "
         "firms in 2025-2026. Firms with a queryable inventory submitted in "
         "hours. Firms with spreadsheets spent weeks and still got data "
         "quality findings — exactly the finding Norvela received from "
         "Banco de Portugal in March 2026. If you can walk an interviewer "
         "through building one of these from a messy vendor list, you are "
         "immediately more credible than a candidate who can only name the "
         "regulation."],
        [],
        ["ORDER OF WORK"],
        ["1.", "B_99.01 first. You cannot fill anything else until you have "
         "decided which business functions are CRITICAL OR IMPORTANT. That "
         "determination is a judgement you must be able to defend — it is "
         "the question a supervisor opens with."],
        ["2.", "B_06.01 — describe those functions, with RTO/RPO. Norvela has "
         "never done a BIA, so you must derive these. Say so in your notes."],
        ["3.", "B_05.01 — the provider master list, from vendors.csv. "
         "You will need LEI codes; where a provider has none, note which "
         "alternative identifier you used and why."],
        ["4.", "B_02.01 / B_02.02 — the contracts and their detail. This is "
         "where most data gaps surface."],
        ["5.", "B_05.02 — the sub-contracting chain. Norvela has NOT mapped "
         "this for any provider. Document the gap rather than leaving blanks."],
        ["6.", "B_07.01 — substitutability, exit plans, audit dates. This is "
         "where Norvela looks worst, and where your remediation plan writes "
         "itself."],
        [],
        ["DELIVERABLE", "A completed register PLUS a one-page data-quality "
         "statement listing every field you could not populate, why, who "
         "owns closing the gap, and by when. Supervisors respect a declared "
         "gap far more than a plausible-looking blank."],
    ]
    for line in lines:
        ws.append(line)
    ws["A1"].font = Font(bold=True, size=14)
    for r in (3, 5, 7, 10, 18):
        ws.cell(row=r, column=1).font = Font(bold=True)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 108
    for row in ws.iter_rows(min_col=2, max_col=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    for sheet_name, headers in ROI_TABLES.items():
        s = wb.create_sheet(sheet_name[:31])
        s.append(headers)
        style_header(s)
        autosize(s, maxw=34)

    path = os.path.join(HERE, "dora-register-of-information.xlsx")
    wb.save(path)
    return path


# --------------------------------------------------------------------------
# findings.csv — vulnerability extract
# --------------------------------------------------------------------------
def write_findings():
    path = os.path.join(HERE, "vuln-findings.csv")
    sev_mix = (["Critical"] * 38 + ["High"] * 180 + ["Medium"] * 520
               + ["Low"] * 509)
    random.shuffle(sev_mix)
    today = date(2026, 9, 22)
    comps = ["vault-api", "payrails-gateway", "merchant-portal",
             "settlement-batch", "sentinel-scorer", "flow-scorer",
             "ledger-adapter", "notification-svc", "admin-console",
             "esxi-host-01", "esxi-host-02", "k8s-node-pool"]
    rows = []
    for i, sev in enumerate(sev_mix, start=1):
        age = random.choice([3, 9, 17, 30, 55, 90, 140, 190, 260, 400])
        if sev == "Critical":
            # The dossier states all 38 criticals are older than 180 days.
            age = random.choice([190, 220, 260, 310, 400])
        rows.append([
            f"VF-{i:04d}", sev, random.choice(comps),
            (today - timedelta(days=age)).isoformat(), age,
            random.choice(["Snyk", "AWS Inspector", "Manual pentest"]),
            # Criticals stay open: the finding is that none were remediated.
            ("Open" if sev == "Critical" else
             random.choice(["Open", "Open", "Open", "Risk accepted", "In progress"])),
            "", "",
        ])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["finding_id", "severity", "component", "first_detected",
                    "age_days", "source", "status", "sla_target",
                    "owner"])
        w.writerows(rows)
    return path


if __name__ == "__main__":
    outputs = [write_vendors(), write_assets(), write_iam(),
               write_findings(), build_risk_register(), build_roi()]
    for o in outputs:
        print(f"  {os.path.basename(o):45s} {os.path.getsize(o):>9,d} bytes")
