# azure-break-fix
Azure security lab: build with Terraform, plant misconfigurations, detect them with a read-only Python scanner mapped to CIS and MITRE ATT&amp;CK, fix them, and rescan to prove it. Includes before/after diffs and validation against Prowler.

# azure-break-fix

> **Status:** Early design phase. Nothing here is production-ready. The scanner is read-only, and the vulnerable environment is for lab use only.

## Project Lifecycle

| Phase | What happens | Output |
|-------|--------------|--------|
| 1. Build | Provision a baseline Azure environment with IaC | Terraform code |
| 2. Break | Introduce planned misconfigurations, each mapped to a CIS control | Misconfiguration catalog |
| 3. Scan | Run the Python scanner against the environment | JSON findings (before) |
| 4. Document | Record each finding with severity, impact, and ATT&CK technique | Findings report |
| 5. Fix | Remediate through IaC changes | Hardened Terraform code |
| 6. Rescan | Run the scanner again and diff against the first scan | JSON findings (after) + diff |

## Frameworks and Benchmarks

| Framework | Role in this project |
|-----------|----------------------|
| **CIS Microsoft Azure Foundations Benchmark** | Primary benchmark. Every scanner check carries a CIS recommendation ID. Version is pinned in `docs/benchmarks.md`. |
| **Microsoft Cloud Security Benchmark (MCSB)** | Secondary cross-reference. Used to compare against Microsoft Defender for Cloud scoring. |
| **MITRE ATT&CK (Cloud matrix)** | Maps each planted misconfiguration to the attacker technique it enables. |
| **NIST CSF 2.0** | Optional. Used to translate findings into business-level language in the final report. |

## Tech Stack

| Layer | Tool |
|-------|------|
| Scanner language | Python 3 |
| Azure access | Azure SDK for Python (`azure-identity`, `azure-mgmt-*`) |
| Authentication | `DefaultAzureCredential` with a dedicated read-only identity |
| Infrastructure as Code | Terraform |
| Architecture diagrams | Python [`diagrams`](https://diagrams.mingrammer.com/) library (requires Graphviz) |
| Validation (ground truth) | Prowler or ScoutSuite, run against the same environment |
| Output format | JSON findings, plus a before/after diff report |
| Version control | Git + GitHub |

## Scanner Design Principles

- **Read-only.** The scanner identity gets reader-level roles only and can never modify resources.
- **Control plane only.** It inspects resource configuration through Azure Resource Manager and never reads data inside resources.
- **One check, one unit.** Each check is a self-contained module that declares its CIS ID, severity, and resource type.
- **Structured findings.** Results are machine-readable so the before and after scans can be diffed automatically.
- **Validated.** Results are compared against Prowler/ScoutSuite to find gaps in coverage.

## Planned Repository Layout

```
azure-break-fix/
├── docs/                 # system design, diagrams, benchmark notes, findings reports
├── infra/
│   ├── baseline/         # secure-by-default environment
│   ├── vulnerable/       # intentionally misconfigured environment
│   └── remediated/       # hardened environment after fixes
├── scanner/              # Python scanner (checks, core engine, reporting)
├── results/              # scan output (before / after / diff)
└── README.md
```

## Safety and Cost Notes

- The vulnerable environment runs in a **dedicated Azure subscription** with no real data.
- MFA is enabled on the account, and budget alerts are configured.
- Resources are destroyed after each lab session.
- Credentials, secrets, and Terraform state files are never committed (see `.gitignore`).

## Roadmap

- [ ] System design and architecture diagrams
- [ ] Pin benchmark versions and build the misconfiguration catalog
- [ ] Baseline Terraform environment
- [ ] Scanner core (auth, check interface, findings schema)
- [ ] First check slice: identity, storage, networking
- [ ] Vulnerable environment + first scan
- [ ] Findings report
- [ ] Remediation + rescan + diff
- [ ] Validation against Prowler/ScoutSuite
