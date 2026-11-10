# Project Charter: Cloud HCM & Payroll Integration

> **Synthetic work sample.** The organization, people, dates, and figures are invented. The structure, risk themes, and governance model reflect my experience on an internal HR system implementation.

| Field | Detail |
|---|---|
| Project name | Cloud HCM & Payroll Integration ("Project Keystone") |
| Organization | Calder & Finch Advisory (fictional), ~6,500 employees in the US, UK, and Canada |
| Charter version | v1.0 (approved at Gate 0) |
| Date | 06 Jan 2025 |
| Sponsor | Chief People Officer |
| Project manager | Brystal Pearson, CAPM |
| Methodology | Hybrid: predictive phase gates with iterative build and test sprints |

---

## 1. Purpose and business case

Calder & Finch runs core HR on a legacy, on-premise HRIS. Payroll is fed by nightly flat-file exports. The setup causes:

- **Manual rework.** HR operations re-keys about 400 employee changes a month into payroll.
- **Payroll errors.** Mismatched compensation, address, and status data drive off-cycle corrections every pay period.
- **No single source of truth.** Headcount reports differ between HR and Finance.
- **End of support.** The vendor ends support for the legacy HRIS on 31 Dec 2025.

Replacing it with a cloud HCM platform and an automated payroll integration removes the re-keying and the end-of-support risk, and gives HR and Finance one employee record.

## 2. Objectives (SMART)

| # | Objective | Measure | Target |
|---|---|---|---|
| O1 | Go live on cloud HCM before legacy end of support | Go-live date | On or before 01 Oct 2025 |
| O2 | Automate the HCM-to-payroll employee data feed | Manual payroll re-keys per month | 0 within 60 days of go-live |
| O3 | Reduce payroll data defects | Off-cycle corrections caused by HR data | 75% fewer than baseline by end of hypercare |
| O4 | Migrate employee records accurately | Records passing validation at final mock load | ≥ 99.5% |
| O5 | Stay within approved budget | Actual vs. baseline cost | Within ±5% |

## 3. Scope

**In scope**
- Core HR (employee central record, org structure, positions, job and compensation data)
- Integration from HCM to the existing third-party payroll provider (US, UK, Canada)
- Data migration of active employees plus 3 years of job history
- Role-based security and access provisioning
- Testing: unit, system integration (SIT), user acceptance (UAT), payroll parallel runs
- Training for HR operations and people managers
- Cutover, go-live, and 8 weeks of hypercare

**Out of scope**
- Replacing the payroll provider
- Recruiting, learning, and performance modules (planned as Phase 2)
- Benefits administration changes
- Migration of terminated employees older than 3 years (archived read-only)

## 4. Deliverables

| Deliverable | Phase | Acceptance owner |
|---|---|---|
| Approved design workbooks (Core HR, integration) | Explore | HRIS Lead |
| Source-to-target data mapping specification | Explore | Payroll Manager |
| Configured HCM tenant | Realize | HRIS Lead |
| Payroll integration (built and unit-tested) | Realize | Integration Lead |
| Test scripts, SIT and UAT sign-off | Realize | Business Process Owners |
| Two payroll parallel runs with variance report | Realize | Payroll Manager |
| Cutover plan and runbook | Deploy | Project Manager |
| Training materials and session completion | Deploy | Change Lead |
| Hypercare issues log and closure report | Run | Project Manager |

## 5. Milestones and phase gates

The steering committee approves each gate before the next phase starts.

| Gate | Milestone | Target date | Exit criteria |
|---|---|---|---|
| G0 | Charter approved | 06 Jan 2025 | Sponsor sign-off; budget released |
| G1 | Design complete | 28 Mar 2025 | Design workbooks signed; mapping spec approved |
| G2 | Build complete | 27 Jun 2025 | Configuration and integration unit-tested; no open critical defects |
| G3 | Test complete | 29 Aug 2025 | SIT and UAT passed; 2 parallel runs within variance tolerance (±0.5% gross pay) |
| G4 | Go / no-go | 26 Sep 2025 | Final mock load ≥ 99.5% valid; cutover rehearsed; training ≥ 90% complete |
| — | Go-live | 01 Oct 2025 | First live payroll processed |
| G5 | Hypercare exit and close | 26 Nov 2025 | No open P1/P2 issues; handover to HRIS support signed |

## 6. Budget summary

| Category | Amount (USD) |
|---|---|
| Software subscription (year 1) | 420,000 |
| Implementation services | 610,000 |
| Internal backfill (HR SMEs) | 145,000 |
| Training and change | 55,000 |
| **Baseline** | **1,230,000** |
| Management reserve (10%) | 123,000 |
| **Total authorized** | **1,353,000** |

Spending management reserve requires sponsor approval.

## 7. Stakeholders and governance

| Role | Who | Responsibility |
|---|---|---|
| Sponsor | Chief People Officer | Owns business case; approves gates, scope changes, and reserve |
| Steering committee | CPO, CFO, CIO | Meets monthly and at each gate; resolves escalations |
| Project manager | Brystal Pearson | Plan, schedule, RAID, status reporting, change control |
| HRIS Lead | HR Technology | Configuration and design decisions |
| Payroll Manager | Finance | Mapping approval, parallel runs, payroll sign-off |
| Integration Lead | IT | Interface build, monitoring, defects |
| Business process owners | HR Ops, Compensation | Test scripts and UAT sign-off |
| Change Lead | HR | Communications and training |

**Cadence**
- Weekly core team meeting and RAID review
- Weekly RAG status report to sponsor
- Monthly steering committee
- Daily stand-up during cutover and the first 2 weeks of hypercare

## 8. Escalation and change control

| Level | Threshold | Decides |
|---|---|---|
| Project manager | Schedule slip ≤ 5 working days with no milestone impact; no cost impact | PM, logged in RAID |
| Sponsor | Milestone slip, or cost up to the management reserve | Sponsor |
| Steering committee | Gate date or go-live change, scope change, cost beyond reserve | Steering committee |

All scope, schedule, and budget changes go through a change request with impact analysis. Approved changes are logged in the Decisions tab of the RAID log.

## 9. High-level risks, assumptions, and constraints

Full detail and owners are in the [RAID log](../raid/).

**Top risks**
- Legacy data quality is worse than expected and delays mock loads.
- Payroll parallel runs exceed variance tolerance.
- HR SMEs can't free up enough time for design and UAT.

**Assumptions**
- The payroll provider accepts the standard integration file format without custom development.
- HR SMEs are backfilled at 50% for design, testing, and UAT.

**Constraints**
- Go-live must happen before legacy end of support (31 Dec 2025).
- No go-live during the year-end payroll freeze (01 Dec to 15 Jan).

## 10. Approval

| Name | Role | Decision | Date |
|---|---|---|---|
| (Sponsor) | Chief People Officer | Approved | 06 Jan 2025 |
| (Finance) | Chief Financial Officer | Approved | 06 Jan 2025 |
| Brystal Pearson | Project Manager | Prepared | 06 Jan 2025 |
