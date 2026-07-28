-- GRC Risk & Compliance Dashboard schema
-- Modeled after a typical enterprise risk register (RSA Archer / ServiceNow GRC style)

CREATE TABLE IF NOT EXISTS risks (
    risk_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,             -- e.g. Technology, Third-Party, Operational, Compliance
    business_unit TEXT NOT NULL,
    likelihood INTEGER NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
    impact INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
    control_effectiveness REAL NOT NULL CHECK (control_effectiveness BETWEEN 0 AND 1), -- 0=none,1=fully effective
    owner TEXT NOT NULL,
    status TEXT NOT NULL,               -- Open, Mitigating, Closed, Accepted
    framework_refs TEXT,                -- e.g. "NIST CSF 2.0 PR.AA-05; PCI-DSS 8.2"
    identified_date TEXT NOT NULL,
    last_reviewed TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS remediation_actions (
    action_id TEXT PRIMARY KEY,
    risk_id TEXT NOT NULL REFERENCES risks(risk_id),
    description TEXT NOT NULL,
    owner TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL,               -- Not Started, In Progress, Overdue, Complete
    cap_id TEXT                          -- linked Corrective Action Plan id, if any
);

CREATE TABLE IF NOT EXISTS kri_snapshots (
    snapshot_date TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value REAL NOT NULL,
    threshold REAL NOT NULL,
    unit TEXT NOT NULL,
    PRIMARY KEY (snapshot_date, metric_name)
);
