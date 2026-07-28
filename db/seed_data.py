"""Generate synthetic sample data for the GRC risk register and load it into SQLite.

All data here is fabricated for demonstration purposes — it does not represent any
real organization's actual risk posture.
"""
from __future__ import annotations

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "risk_register.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

random.seed(42)

CATEGORIES = ["Technology", "Third-Party", "Operational", "Compliance", "Financial"]
BUSINESS_UNITS = ["Payments Platform", "Cloud Infrastructure", "Enterprise IT", "Retail Banking", "Data Platform"]
OWNERS = ["J. Alvarez", "S. Chen", "M. Ajmera", "R. Patel", "T. Nguyen", "K. O'Brien", "D. Okafor"]
FRAMEWORK_REFS = [
    "NIST CSF 2.0 PR.AA-05", "NIST SP 800-53 AC-6", "PCI-DSS v4.0 8.2",
    "SOX ITGC - Access Mgmt", "ISO 27001 A.9.2", "NIST CSF 2.0 DE.CM-01",
    "FFIEC IT Handbook - Vendor Mgmt", "NIST CSF 2.0 GV.SC-04",
]
RISK_TITLES = [
    "Excessive standing access for privileged cloud accounts",
    "Third-party vendor lacking SOC 2 Type II attestation",
    "Unencrypted data-in-transit between legacy and cloud systems",
    "Segregation of duties gap in change management approval",
    "Incomplete MFA enforcement for administrative accounts",
    "Stale user access not revoked within SLA after termination",
    "Missing centralized logging for critical payment services",
    "Vulnerability remediation SLA breaches on internet-facing assets",
    "Undocumented data flows for PII in third-party integrations",
    "Manual evidence collection process prone to audit findings",
    "Cloud storage buckets with inconsistent public-access policies",
    "Concentration risk from single cloud region dependency",
    "Outdated disaster recovery runbook not tested in 12+ months",
    "Shadow IT SaaS usage outside procurement/security review",
    "Insufficient change management testing before production deploys",
]
ACTION_TEMPLATES = [
    "Implement least-privilege IAM policy for {bu}",
    "Complete vendor security questionnaire and SOC 2 review",
    "Enable encryption-in-transit for {bu} data pipeline",
    "Deploy MFA enforcement policy across admin roles",
    "Automate access revocation workflow tied to HR offboarding",
    "Onboard {bu} logs to centralized SIEM",
    "Remediate critical/high vulnerabilities per SLA",
    "Document data flow diagram and update DPIA",
    "Automate evidence collection via AWS Config rules",
    "Update and test disaster recovery runbook",
]
STATUSES = ["Open", "Mitigating", "Closed", "Accepted"]
ACTION_STATUSES = ["Not Started", "In Progress", "Overdue", "Complete"]


def random_date(start_days_ago: int, end_days_ago: int) -> str:
    d = date.today() - timedelta(days=random.randint(end_days_ago, start_days_ago))
    return d.isoformat()


def build_database() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())

    risks = []
    for i, title in enumerate(RISK_TITLES, start=1):
        risk_id = f"RISK-{i:03d}"
        likelihood = random.randint(1, 5)
        impact = random.randint(2, 5)
        control_effectiveness = round(random.uniform(0.2, 0.95), 2)
        status = random.choices(STATUSES, weights=[35, 30, 25, 10])[0]
        risks.append((
            risk_id, title, random.choice(CATEGORIES), random.choice(BUSINESS_UNITS),
            likelihood, impact, control_effectiveness, random.choice(OWNERS), status,
            "; ".join(random.sample(FRAMEWORK_REFS, k=random.randint(1, 2))),
            random_date(400, 200), random_date(90, 1),
        ))
    conn.executemany(
        "INSERT INTO risks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", risks
    )

    actions = []
    action_id = 1
    for r in risks:
        risk_id, title, category, bu = r[0], r[1], r[2], r[3]
        n_actions = random.randint(1, 3)
        for _ in range(n_actions):
            template = random.choice(ACTION_TEMPLATES)
            due_offset = random.randint(-60, 90)  # negative = overdue
            due_date = (date.today() + timedelta(days=due_offset)).isoformat()
            status = "Overdue" if due_offset < 0 and random.random() < 0.7 else random.choice(ACTION_STATUSES)
            actions.append((
                f"CAP-{action_id:04d}", risk_id, template.format(bu=bu),
                random.choice(OWNERS), due_date, status,
                f"CAP-{action_id:04d}" if random.random() < 0.5 else None,
            ))
            action_id += 1
    conn.executemany(
        "INSERT INTO remediation_actions VALUES (?,?,?,?,?,?,?)", actions
    )

    metrics = [
        ("Overdue Remediation Rate", 8.0, "%"),
        ("Critical Findings Open", 3.0, "count"),
        ("Control Test Pass Rate", 92.0, "%"),
        ("Third-Party Assessments Completed", 85.0, "%"),
        ("Avg Days to Remediate Critical", 21.0, "days"),
    ]
    kri_rows = []
    for months_ago in range(6, -1, -1):
        snap_date = (date.today().replace(day=1) - timedelta(days=months_ago * 30)).isoformat()
        for name, threshold, unit in metrics:
            drift = random.uniform(-0.15, 0.15)
            if name == "Control Test Pass Rate" or name == "Third-Party Assessments Completed":
                base = threshold * (1 + drift * 0.3)
                value = max(60.0, min(100.0, base + (6 - months_ago) * 0.8))
            else:
                base = threshold * (1 + drift)
                value = max(0.0, base - (6 - months_ago) * 0.3)
            kri_rows.append((snap_date, name, round(value, 1), threshold, unit))
    conn.executemany(
        "INSERT INTO kri_snapshots VALUES (?,?,?,?,?)", kri_rows
    )

    conn.commit()
    conn.close()
    print(f"Seeded {len(risks)} risks, {len(actions)} remediation actions, {len(kri_rows)} KRI snapshots -> {DB_PATH}")


if __name__ == "__main__":
    build_database()
