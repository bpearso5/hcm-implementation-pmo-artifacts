# HCM Implementation PMO Artifacts: Charter & RAID Log

A project charter and a working RAID log for a cloud HCM and payroll integration, built the way I run governance on a system implementation.

> **All data is synthetic.** "Calder & Finch Advisory" and "Project Keystone" are invented. No client names, people, or figures appear anywhere in this repo.

## The problem

HR system go-lives rarely fail on configuration. They fail on data quality, payroll accuracy, and people who can't free up time to test, and those risks show up long before the go-live date if someone is tracking them. On an internal HR system implementation, I kept the payroll issues log through hypercare (115 items). That showed me how many go-live issues trace back to risks that could have been logged and managed in design. This repo shows the governance layer that catches them earlier.

## What's here

| File | What it is |
|---|---|
| [`charter/Project_Charter.md`](charter/Project_Charter.md) | Business case, SMART objectives, scope, deliverables, phase gates with exit criteria, budget with management reserve, governance, escalation thresholds, and approvals |
| [`raid/Project_Keystone_RAID_Log.xlsx`](raid/Project_Keystone_RAID_Log.xlsx) | RAID log as of mid-UAT: 11 risks, 6 assumptions, 8 issues, 6 dependencies, 5 decisions, plus a formula-driven summary |
| [`scripts/build_raid_log.py`](scripts/build_raid_log.py) | Python script that generates the workbook |

## How the RAID log works

- **Risks** are written as cause > event > effect, scored Probability × Impact (1–5 each), and rated High (15–25), Medium (8–14), or Low. Every risk has a response strategy, a trigger, and an owner.
- **Risks link to issues.** When a risk happens, it becomes an issue with the risk ID attached. For example, R-02 (parallel run variance) led to I-04 (variance at 0.8% against a 0.5% tolerance).
- **Issues age automatically.** Days Open and Overdue calculate from the as-of date on the Summary tab.
- **Decisions are logged** with options considered, rationale, and who decided, so change control has an audit trail.
- **The Summary tab** counts open risks by rating, P1/P2 issues, overdue items, and invalid assumptions, and lists the top 5 open risks by score for the weekly status report. Every number is a formula.

## Skills this demonstrates

| Skill | Where to see it |
|---|---|
| Project initiation and business case | Charter sections 1–2 |
| Scope definition and control | Charter section 3; Decision D-01 |
| Phase-gate governance | Charter section 5 (gates G0–G5 with measurable exit criteria) |
| Cost baseline and reserves | Charter section 6 |
| Stakeholder and escalation management | Charter sections 7–8 |
| Risk identification, scoring, and response planning | Risks tab |
| Issue management and root-cause follow-through | Issues tab (I-01, I-04) |
| Assumption validation | Assumptions tab (A-06 proven invalid, linked to I-03) |
| Status reporting | Summary tab |
| Excel (COUNTIFS, INDEX/MATCH, data validation, conditional formatting) | RAID workbook |

The structure follows PMI practice: the charter maps to Initiating, and the RAID log supports Monitoring & Controlling across the project lifecycle.

## Related work

- [hcm-payroll-data-mapping](https://github.com/bpearso5/hcm-payroll-data-mapping): the source-to-target mapping and SQL integrity checks that mitigate risks R-01, R-02, and R-06 in this log.
- [capital-project-submission-qa](https://github.com/bpearso5/capital-project-submission-qa): submission QA and weekly executive reporting.

## How this was built

The project structure, risk themes, and issue patterns come from my experience on an HR system implementation. I used Claude (AI) to help draft the documents and write the workbook script. I reviewed every item and can explain the reasoning behind each risk, score, and decision.

## About me

Brystal Pearson, CAPM · [LinkedIn](https://www.linkedin.com/in/brystal-pearson-capm) · [GitHub](https://github.com/bpearso5)
