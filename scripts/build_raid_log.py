"""Build the RAID log workbook for the synthetic Project Keystone case study.

All data is invented. Run: python3 scripts/build_raid_log.py
"""
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parent.parent / "raid" / "Project_Keystone_RAID_Log.xlsx"

FONT = "Arial"
BLACK = "000000"
WHITE = "FFFFFF"
GRAY = "D9D9D9"
LIGHT = "F2F2F2"
thin = Side(style="thin", color="808080")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD_FILL = PatternFill("solid", fgColor=BLACK)
HEAD_FONT = Font(name=FONT, bold=True, color=WHITE, size=10)
BODY_FONT = Font(name=FONT, size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)
MAX_ROWS = 200  # formulas and validation extend to this row so new entries work

wb = Workbook()


def title(ws, text, sub):
    ws["A1"] = text
    ws["A1"].font = Font(name=FONT, bold=True, size=14)
    ws["A2"] = sub
    ws["A2"].font = Font(name=FONT, italic=True, size=9, color="595959")


def table(ws, headers, widths, rows, start=4, formula_cols=None, center_cols=()):
    """Write headers + rows. formula_cols: {col_index: lambda r: formula} applied to MAX_ROWS."""
    formula_cols = formula_cols or {}
    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=start, column=c, value=h)
        cell.font, cell.fill, cell.border = HEAD_FONT, HEAD_FILL, BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[start].height = 30
    last = start + MAX_ROWS
    for r in range(start + 1, last + 1):
        data = rows[r - start - 1] if r - start - 1 < len(rows) else None
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=r, column=c)
            if c in formula_cols:
                cell.value = formula_cols[c](r)
            elif data is not None and c - 1 < len(data):
                cell.value = data[c - 1]
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = CENTER if c in center_cols or c in formula_cols else WRAP
            if isinstance(cell.value, date):
                cell.number_format = "dd-mmm-yy"
    ws.freeze_panes = ws.cell(row=start + 1, column=3)
    ws.auto_filter.ref = f"A{start}:{get_column_letter(len(headers))}{start + len(rows)}"
    return start + 1, last


def dropdown(ws, col, options, first, last):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    dv.error, dv.errorTitle = "Pick a value from the list.", "Invalid entry"
    ws.add_data_validation(dv)
    dv.add(f"{col}{first}:{col}{last}")


def date_cols(ws, cols, first, last):
    for col in cols:
        for r in range(first, last + 1):
            ws[f"{col}{r}"].number_format = "dd-mmm-yy"


def shade_closed(ws, status_col, ncols, first, last):
    rng = f"A{first}:{get_column_letter(ncols)}{last}"
    ws.conditional_formatting.add(
        rng,
        FormulaRule(formula=[f'OR(${status_col}{first}="Closed",${status_col}{first}="Validated",'
                             f'${status_col}{first}="Met")'],
                    font=Font(color="808080"), fill=PatternFill("solid", fgColor=LIGHT)))


PHASES = ["Initiate", "Explore", "Realize", "Deploy", "Run"]
D = date

# ---------------------------------------------------------------- Read Me
ws = wb.active
ws.title = "Read Me"
title(ws, "Project Keystone: RAID Log",
      "Synthetic work sample. Organization, people, and figures are invented.")
guide = [
    ("What this is", "The working risk, assumption, issue, dependency, and decision log for a cloud HCM "
                     "and payroll integration. Reviewed weekly with the core team; top items go to the "
                     "sponsor in the weekly status report."),
    ("As-of date", "Set on the Summary tab (cell B4). Issue ageing and overdue flags calculate from it."),
    ("Cells you edit", "White cells in each log tab. Use the dropdowns for Phase, Status, Owner role, "
                       "Probability, Impact, and Priority."),
    ("Cells you don't edit", "Gray columns are formulas: Score, Rating, Days Open, Overdue. They extend "
                             "to row 204, so new rows calculate automatically."),
    ("Risk scoring", "Score = Probability (1-5) x Impact (1-5). High = 15-25, Medium = 8-14, Low = 1-7. "
                     "High risks need a mitigation owner and a trigger, and go on the weekly status report."),
    ("Risk vs. issue", "A risk might happen; an issue has happened. When a risk triggers, set its status to "
                       "Converted to Issue and log the issue with a link to the risk ID."),
    ("Closed items", "Closed, Validated, and Met rows are grayed out but kept for the audit trail."),
    ("Example row", "R-01 on the Risks tab shows the expected level of detail for a new entry."),
]
ws["A4"], ws["B4"] = "Topic", "Guidance"
for c in ("A4", "B4"):
    ws[c].font, ws[c].fill, ws[c].border = HEAD_FONT, HEAD_FILL, BORDER
for i, (k, v) in enumerate(guide, 5):
    ws.cell(row=i, column=1, value=k).font = Font(name=FONT, bold=True, size=10)
    ws.cell(row=i, column=2, value=v).font = BODY_FONT
    for c in (1, 2):
        ws.cell(row=i, column=c).border = BORDER
        ws.cell(row=i, column=c).alignment = WRAP
ws.column_dimensions["A"].width = 22
ws.column_dimensions["B"].width = 95
ws.sheet_view.showGridLines = False

# ---------------------------------------------------------------- Risks
rk = wb.create_sheet("Risks")
title(rk, "Risks", "Score and Rating are formulas. Review weekly; High risks go on the status report.")
risk_headers = ["ID", "Risk (cause > event > effect)", "Phase", "Category", "Probability (1-5)",
                "Impact (1-5)", "Score", "Rating", "Response", "Mitigation / contingency", "Trigger",
                "Owner role", "Date raised", "Next review", "Status"]
risks = [
    ["R-01", "Legacy HRIS data has inconsistent job codes and missing fields, so mock loads fail "
             "validation and the build-complete gate slips.", "Explore", "Data", 4, 4, None, None,
     "Mitigate", "Run data profiling in Explore; HR Ops cleanses at source with a weekly defect burn-down. "
                 "Contingency: add a third mock load.",
     "Mock 1 validation pass rate < 95%", "Data Migration Lead", D(2025, 1, 20), D(2025, 8, 22), "Open"],
    ["R-02", "Payroll parallel runs exceed the ±0.5% gross pay tolerance because of mapping or rule "
             "errors, delaying the go / no-go decision.", "Realize", "Payroll", 3, 5, None, None,
     "Mitigate", "Field-level source-to-target spec with SQL integrity checks before each run; "
                 "variance triage within 48 hours. Contingency: third parallel run (2 weeks).",
     "Parallel 1 variance > 0.5%", "Payroll Manager", D(2025, 2, 3), D(2025, 8, 19), "Open"],
    ["R-03", "HR SMEs are pulled into year-end and BAU work, so UAT execution falls behind.",
     "Realize", "Resourcing", 4, 3, None, None, "Mitigate",
     "Backfill at 50% confirmed by sponsor; UAT schedule locked 6 weeks out; daily execution tracker.",
     "UAT execution < 80% of plan at end of week 1", "Project Manager", D(2025, 1, 15), D(2025, 8, 18), "Open"],
    ["R-04", "Payroll provider needs custom file changes, adding cost and build time.",
     "Explore", "Vendor", 2, 4, None, None, "Mitigate",
     "Confirm standard file spec in writing at design kickoff.",
     "Provider rejects standard spec", "Integration Lead", D(2025, 1, 15), D(2025, 3, 28), "Closed"],
    ["R-05", "Security roles are designed too broadly, exposing compensation data to people managers.",
     "Realize", "Security", 2, 5, None, None, "Mitigate",
     "Role-based access matrix signed by HR and Legal; negative testing in SIT.",
     "Any SIT test shows unauthorized field access", "HRIS Lead", D(2025, 3, 10), D(2025, 8, 25), "Open"],
    ["R-06", "UK and Canada statutory fields (NI category, province of employment) are missed in "
             "mapping, causing payroll rejections for non-US employees.", "Explore", "Data", 3, 4, None, None,
     "Mitigate", "Country-specific mapping review with each payroll lead; dedicated SIT scenarios per country.",
     "Any non-US record rejected in SIT", "Payroll Manager", D(2025, 2, 17), D(2025, 8, 20), "Open"],
    ["R-07", "Managers don't complete training before go-live, increasing hypercare ticket volume.",
     "Deploy", "Change", 3, 3, None, None, "Mitigate",
     "Short role-based modules; completion tracked weekly by business unit; escalate below 70% at T-3 weeks.",
     "Completion < 70% at 3 weeks before go-live", "Change Lead", D(2025, 4, 7), D(2025, 9, 5), "Open"],
    ["R-08", "Go-live slips past October and collides with the year-end payroll freeze.",
     "Deploy", "Schedule", 2, 5, None, None, "Mitigate",
     "Schedule buffer of 2 weeks before G4; go / no-go criteria agreed in advance. "
     "Contingency: legacy support extension quote held by procurement.",
     "G3 slips more than 10 working days", "Project Manager", D(2025, 1, 6), D(2025, 8, 29), "Open"],
    ["R-09", "Integration lead is the only person who knows the interface build, creating a "
             "single point of failure.", "Realize", "Resourcing", 2, 4, None, None, "Mitigate",
     "Pair a second developer on build; document interface runbook before SIT.",
     "Lead unavailable > 3 days", "Integration Lead", D(2025, 5, 12), D(2025, 8, 25), "Open"],
    ["R-10", "Integration fails silently after go-live and payroll misses employee changes.",
     "Run", "Technical", 2, 5, None, None, "Mitigate",
     "Daily interface reconciliation report during hypercare; alerts on failed records.",
     "Any unreconciled record > 1 day", "Integration Lead", D(2025, 6, 2), D(2025, 9, 26), "Open"],
    ["R-11", "Historical job data beyond 3 years is requested after scope sign-off.",
     "Explore", "Scope", 2, 2, None, None, "Accept",
     "Archive available read-only; any change goes through change control.",
     "Change request raised", "Project Manager", D(2025, 2, 24), D(2025, 9, 26), "Open"],
]
f, l = table(rk, risk_headers, [7, 46, 10, 12, 11, 10, 8, 10, 11, 46, 28, 18, 11, 11, 18], risks,
             formula_cols={
                 7: lambda r: f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})',
                 8: lambda r: f'=IF(G{r}="","",IF(G{r}>=15,"High",IF(G{r}>=8,"Medium","Low")))'},
             center_cols=(1, 3, 5, 6, 9, 13, 14, 15))
for r in range(f, l + 1):
    for c in (7, 8):
        rk.cell(row=r, column=c).fill = PatternFill("solid", fgColor=GRAY)
dropdown(rk, "C", PHASES, f, l)
dropdown(rk, "D", ["Data", "Payroll", "Resourcing", "Vendor", "Security", "Change", "Schedule",
                   "Technical", "Scope", "Budget"], f, l)
dropdown(rk, "E", ["1", "2", "3", "4", "5"], f, l)
dropdown(rk, "F", ["1", "2", "3", "4", "5"], f, l)
dropdown(rk, "I", ["Avoid", "Mitigate", "Transfer", "Accept", "Escalate"], f, l)
dropdown(rk, "O", ["Open", "Converted to Issue", "Closed"], f, l)
date_cols(rk, "MN", f, l)
rk.conditional_formatting.add(f"H{f}:H{l}", FormulaRule(formula=[f'H{f}="High"'],
                              font=Font(bold=True, color=WHITE), fill=PatternFill("solid", fgColor=BLACK)))
shade_closed(rk, "O", len(risk_headers), f, l)
rk["E5"].comment = Comment("1 = rare, 3 = possible, 5 = almost certain", "PM")
rk["F5"].comment = Comment("1 = negligible, 3 = slips a milestone, 5 = threatens go-live or payroll accuracy", "PM")

# ---------------------------------------------------------------- Assumptions
asn = wb.create_sheet("Assumptions")
title(asn, "Assumptions", "If an assumption proves false, raise a risk or issue and link it here.")
a_headers = ["ID", "Assumption", "Phase", "Impact if false", "Validation method", "Owner role",
             "Validate by", "Status", "Linked item"]
assumptions = [
    ["A-01", "Payroll provider accepts the standard integration file without custom development.",
     "Explore", "Added build cost and 3-4 weeks of schedule.", "Written confirmation of file spec.",
     "Integration Lead", D(2025, 3, 14), "Validated", "R-04"],
    ["A-02", "HR SMEs are backfilled at 50% from design through UAT.", "Explore",
     "Design and UAT delays.", "Sponsor confirms backfill hires.", "Project Manager", D(2025, 2, 7),
     "Validated", "R-03"],
    ["A-03", "Active headcount at go-live stays near 6,500 (±10%).", "Initiate",
     "Subscription true-up and longer mock loads.", "Monthly headcount check with HR Ops.",
     "HRIS Lead", D(2025, 9, 1), "Open", ""],
    ["A-04", "Legacy HRIS remains available read-only for 12 months after go-live.", "Initiate",
     "Loss of history for audits and reporting.", "IT confirms license and server plan.",
     "Integration Lead", D(2025, 6, 30), "Validated", ""],
    ["A-05", "Pay rules and pay calendars don't change during the project.", "Explore",
     "Rework of mapping and parallel runs.", "Payroll Manager confirms at each gate.",
     "Payroll Manager", D(2025, 8, 29), "Open", "R-02"],
    ["A-06", "Single sign-on is available for HCM by the start of SIT.", "Realize",
     "SIT delayed or run with temporary accounts.", "IT identity team confirms date.",
     "Integration Lead", D(2025, 6, 27), "Invalid", "I-03"],
]
f, l = table(asn, a_headers, [7, 46, 10, 34, 34, 18, 12, 12, 11], assumptions,
             center_cols=(1, 3, 7, 8, 9))
dropdown(asn, "C", PHASES, f, l)
dropdown(asn, "H", ["Open", "Validated", "Invalid"], f, l)
date_cols(asn, "G", f, l)
shade_closed(asn, "H", len(a_headers), f, l)

# ---------------------------------------------------------------- Issues
iss = wb.create_sheet("Issues")
title(iss, "Issues", "Days Open and Overdue calculate from the as-of date on the Summary tab.")
i_headers = ["ID", "Issue", "Phase", "Priority", "Impact", "Action / resolution", "Owner role",
             "Date opened", "Target date", "Date closed", "Status", "Linked risk", "Days open", "Overdue?"]
issues = [
    ["I-01", "Mock load 1 passed validation for only 91% of employee records (missing job codes, "
             "duplicate IDs from rehires).", "Realize", "P1",
     "Threatened G2 build-complete date.",
     "HR Ops cleansed 540 records at source; added duplicate-ID check. Mock 2 passed at 98.7%.",
     "Data Migration Lead", D(2025, 5, 9), D(2025, 6, 13), D(2025, 6, 11), "Closed", "R-01"],
    ["I-02", "UK records mapped NI category to the wrong target field.", "Realize", "P2",
     "UK payroll rejects in SIT.", "Corrected mapping rule; added country-specific SQL check.",
     "Payroll Manager", D(2025, 7, 7), D(2025, 7, 18), D(2025, 7, 16), "Closed", "R-06"],
    ["I-03", "Single sign-on not ready for SIT start.", "Realize", "P2",
     "Testers can't log in with their own accounts.",
     "Temporary test accounts issued; SSO moved to UAT start. Decision D-04.",
     "Integration Lead", D(2025, 6, 30), D(2025, 7, 25), D(2025, 7, 24), "Closed", ""],
    ["I-04", "Parallel run 1 variance at 0.8% of gross pay, above the 0.5% tolerance.", "Realize", "P1",
     "Go / no-go at risk if parallel 2 also fails.",
     "Variance triaged by employee: 3 root causes (overtime rate rounding, annual salary keyed as "
     "hourly, 2 missing pay-group assignments). Fixes in test before parallel 2.",
     "Payroll Manager", D(2025, 8, 4), D(2025, 8, 20), None, "In Progress", "R-02"],
    ["I-05", "UAT execution at 68% of plan at end of week 1.", "Realize", "P2",
     "UAT exit may slip into G3 buffer.",
     "Sponsor freed 2 compensation SMEs for week 2; daily 15-minute UAT stand-up added.",
     "Project Manager", D(2025, 8, 8), D(2025, 8, 22), None, "In Progress", "R-03"],
    ["I-06", "Test environment refresh wiped configured security roles.", "Realize", "P3",
     "1 day of SIT lost.", "Roles restored from transport; refresh checklist now includes security export.",
     "HRIS Lead", D(2025, 7, 21), D(2025, 7, 23), D(2025, 7, 22), "Closed", ""],
    ["I-07", "Org chart in HCM missing 14 cost centers created after data extract.", "Realize", "P3",
     "Reporting lines incomplete in UAT.", "Delta load scheduled; cost-center freeze requested from Finance.",
     "Data Migration Lead", D(2025, 8, 6), D(2025, 8, 13), None, "Open", "R-01"],
    ["I-08", "Canada province-of-employment values not populated for remote workers.", "Realize", "P2",
     "Wrong provincial tax in parallel 2.", "HR Ops confirming work locations; default rule rejected by Payroll.",
     "Payroll Manager", D(2025, 8, 11), D(2025, 8, 19), None, "Open", "R-06"],
]
f, l = table(iss, i_headers, [7, 44, 10, 9, 30, 46, 18, 11, 11, 11, 12, 10, 9, 10], issues,
             formula_cols={
                 13: lambda r: f'=IF(H{r}="","",IF(J{r}<>"",J{r}-H{r},Summary!$B$4-H{r}))',
                 14: lambda r: (f'=IF(OR(I{r}="",K{r}="Closed"),"",'
                                f'IF(Summary!$B$4>I{r},"Overdue",""))')},
             center_cols=(1, 3, 4, 8, 9, 10, 11, 12))
for r in range(f, l + 1):
    for c in (13, 14):
        iss.cell(row=r, column=c).fill = PatternFill("solid", fgColor=GRAY)
dropdown(iss, "C", PHASES, f, l)
dropdown(iss, "D", ["P1", "P2", "P3", "P4"], f, l)
dropdown(iss, "K", ["Open", "In Progress", "Closed"], f, l)
date_cols(iss, "HIJ", f, l)
iss.conditional_formatting.add(f"N{f}:N{l}", FormulaRule(formula=[f'N{f}="Overdue"'],
                               font=Font(bold=True, color=WHITE), fill=PatternFill("solid", fgColor=BLACK)))
shade_closed(iss, "K", len(i_headers), f, l)
iss["D5"].comment = Comment("P1 = blocks a gate or payroll accuracy; P2 = milestone at risk; "
                            "P3 = workaround exists; P4 = cosmetic", "PM")

# ---------------------------------------------------------------- Dependencies
dep = wb.create_sheet("Dependencies")
title(dep, "Dependencies", "What this project needs from others (inbound) or owes them (outbound).")
d_headers = ["ID", "Dependency", "Direction", "Other party", "Needed for", "Need-by date",
             "Owner role", "Status", "Notes"]
deps = [
    ["DP-01", "Payroll provider test environment and file intake for SIT.", "Inbound",
     "Payroll provider", "SIT and parallel runs", D(2025, 6, 30), "Integration Lead", "Met", ""],
    ["DP-02", "SSO configuration by IT identity team.", "Inbound", "IT Identity", "UAT access",
     D(2025, 8, 4), "Integration Lead", "Met", "Moved from SIT to UAT (D-04)."],
    ["DP-03", "Cost-center freeze from Finance through go-live.", "Inbound", "Finance",
     "Final mock load accuracy", D(2025, 8, 15), "Project Manager", "At Risk",
     "Requested 06 Aug; awaiting CFO confirmation."],
    ["DP-04", "Final HCM employee extract to Benefits vendor.", "Outbound", "Benefits vendor",
     "Benefits enrollment feed", D(2025, 9, 19), "Integration Lead", "On Track", ""],
    ["DP-05", "Legacy HRIS read-only access after go-live.", "Inbound", "IT Infrastructure",
     "Audit and history lookups", D(2025, 9, 30), "Integration Lead", "On Track", ""],
    ["DP-06", "Manager training rooms and LMS course setup.", "Inbound", "L&D", "Training delivery",
     D(2025, 9, 1), "Change Lead", "On Track", ""],
]
f, l = table(dep, d_headers, [8, 42, 11, 18, 26, 12, 18, 11, 36], deps, center_cols=(1, 3, 6, 8))
dropdown(dep, "C", ["Inbound", "Outbound"], f, l)
dropdown(dep, "H", ["On Track", "At Risk", "Late", "Met"], f, l)
date_cols(dep, "F", f, l)
shade_closed(dep, "H", len(d_headers), f, l)

# ---------------------------------------------------------------- Decisions
dec = wb.create_sheet("Decisions")
title(dec, "Decisions", "Every scope, schedule, or budget decision and who made it.")
x_headers = ["ID", "Decision", "Options considered", "Rationale", "Decided by", "Date", "Linked item"]
decisions = [
    ["D-01", "Migrate active employees plus 3 years of job history; archive the rest read-only.",
     "Full history / 3 years / active only", "Balances audit needs against data cleansing effort.",
     "Steering committee", D(2025, 2, 24), "R-11"],
    ["D-02", "Use the payroll provider's standard file format; no custom fields.",
     "Standard / custom", "Avoids vendor build cost and keeps upgrades simple.", "Sponsor",
     D(2025, 3, 14), "A-01"],
    ["D-03", "Add a cleanse-at-source step owned by HR Ops before each mock load.",
     "Cleanse in legacy / transform in load", "Fixes root cause; clean data stays clean after go-live.",
     "Project Manager", D(2025, 5, 12), "I-01"],
    ["D-04", "Run SIT with temporary accounts; move SSO to UAT start.",
     "Delay SIT / temporary accounts", "Protects G2 date; security tested again in UAT.",
     "Sponsor", D(2025, 7, 1), "I-03"],
    ["D-05", "Hold a third parallel run only if parallel 2 variance exceeds 0.5%.",
     "Always run 3 / conditional", "Saves 2 weeks if parallel 2 passes; buffer still covers it.",
     "Steering committee", D(2025, 8, 7), "I-04"],
]
f, l = table(dec, x_headers, [7, 46, 30, 40, 18, 11, 11], decisions, center_cols=(1, 6, 7))
date_cols(dec, "F", f, l)

# ---------------------------------------------------------------- Summary (dashboard)
sm = wb.create_sheet("Summary", 1)
title(sm, "RAID Summary", "All counts are formulas. Change the as-of date to re-age issues.")
sm["A4"], sm["B4"] = "As-of date", D(2025, 8, 15)
sm["A4"].font = Font(name=FONT, bold=True, size=10)
sm["B4"].font = Font(name=FONT, bold=True, size=10)
sm["B4"].number_format = "dd-mmm-yyyy"
sm["B4"].border = Border(left=Side("medium"), right=Side("medium"), top=Side("medium"), bottom=Side("medium"))
sm["C4"] = "<- edit this date"
sm["C4"].font = Font(name=FONT, italic=True, size=9, color="595959")


def block(start_row, heading, rows):
    sm.cell(row=start_row, column=1, value=heading)
    sm.cell(row=start_row, column=2, value="Count")
    for c in (1, 2):
        cell = sm.cell(row=start_row, column=c)
        cell.font, cell.fill, cell.border = HEAD_FONT, HEAD_FILL, BORDER
    for i, (label, formula) in enumerate(rows, start_row + 1):
        a = sm.cell(row=i, column=1, value=label)
        b = sm.cell(row=i, column=2, value=formula)
        a.font, b.font = BODY_FONT, Font(name=FONT, bold=True, size=10)
        a.border = b.border = BORDER
        b.alignment = Alignment(horizontal="center")
    return start_row + len(rows) + 2


R = "Risks!"
row = block(6, "Open risks by rating", [
    ("High (15-25)", f'=COUNTIFS({R}$H$5:$H$204,"High",{R}$O$5:$O$204,"Open")'),
    ("Medium (8-14)", f'=COUNTIFS({R}$H$5:$H$204,"Medium",{R}$O$5:$O$204,"Open")'),
    ("Low (1-7)", f'=COUNTIFS({R}$H$5:$H$204,"Low",{R}$O$5:$O$204,"Open")'),
    ("Total open risks", "=SUM(B7:B9)"),
    ("Closed or converted", f'=COUNTIF({R}$O$5:$O$204,"Closed")+COUNTIF({R}$O$5:$O$204,"Converted to Issue")'),
])
I = "Issues!"
row = block(row, "Issues", [
    ("P1 not closed", f'=COUNTIFS({I}$D$5:$D$204,"P1",{I}$K$5:$K$204,"<>Closed")'),
    ("P2 not closed", f'=COUNTIFS({I}$D$5:$D$204,"P2",{I}$K$5:$K$204,"<>Closed")'),
    ("Total not closed", f'=COUNTIFS({I}$A$5:$A$204,"<>",{I}$K$5:$K$204,"<>Closed")'),
    ("Overdue", f'=COUNTIF({I}$N$5:$N$204,"Overdue")'),
    ("Closed", f'=COUNTIF({I}$K$5:$K$204,"Closed")'),
    ("Avg days to close (closed items)",
     f'=IFERROR(AVERAGEIF({I}$K$5:$K$204,"Closed",{I}$M$5:$M$204),0)'),
])
row = block(row, "Assumptions and dependencies", [
    ("Assumptions still open", '=COUNTIF(Assumptions!$H$5:$H$204,"Open")'),
    ("Assumptions proven invalid", '=COUNTIF(Assumptions!$H$5:$H$204,"Invalid")'),
    ("Dependencies at risk or late",
     '=COUNTIF(Dependencies!$H$5:$H$204,"At Risk")+COUNTIF(Dependencies!$H$5:$H$204,"Late")'),
])
row = block(row, "Decisions", [("Decisions logged", '=COUNTA(Decisions!$A$5:$A$204)')])

# Top risks list for the status report: highest open scores, by formula
sm["D6"], sm["E6"], sm["F6"] = "Top open risks", "Score", "Owner role"
for c in ("D6", "E6", "F6"):
    sm[c].font, sm[c].fill, sm[c].border = HEAD_FONT, HEAD_FILL, BORDER
helper = "Risks!$P$5:$P$204"
for r in range(5, 205):  # helper col P on Risks: score for open risks, tie-broken by row
    rk[f"P{r}"] = f'=IF(AND(O{r}="Open",G{r}<>""),G{r}+(1000-ROW())/100000,"")'
    rk[f"P{r}"].font = Font(name=FONT, size=8, color="FFFFFF")
rk.column_dimensions["P"].hidden = True
for i in range(1, 6):
    rr = 6 + i
    key = f"LARGE({helper},{i})"
    sm[f"D{rr}"] = f'=IFERROR(INDEX(Risks!$A$5:$A$204,MATCH({key},{helper},0))&" "&' \
                   f'LEFT(INDEX(Risks!$B$5:$B$204,MATCH({key},{helper},0)),70)&"...","")'
    sm[f"E{rr}"] = f'=IFERROR(INDEX(Risks!$G$5:$G$204,MATCH({key},{helper},0)),"")'
    sm[f"F{rr}"] = f'=IFERROR(INDEX(Risks!$L$5:$L$204,MATCH({key},{helper},0)),"")'
    for c in "DEF":
        sm[f"{c}{rr}"].font = BODY_FONT
        sm[f"{c}{rr}"].border = BORDER
        sm[f"{c}{rr}"].alignment = Alignment(wrap_text=True, vertical="top",
                                             horizontal="center" if c == "E" else "left")
    sm.row_dimensions[rr].height = 28
sm.column_dimensions["A"].width = 34
sm.column_dimensions["B"].width = 14
sm.column_dimensions["C"].width = 4
sm.column_dimensions["D"].width = 62
sm.column_dimensions["E"].width = 8
sm.column_dimensions["F"].width = 20
sm.sheet_view.showGridLines = False

for s in wb.worksheets:
    s.sheet_properties.tabColor = BLACK if s.title in ("Read Me", "Summary") else "808080"
    s.page_setup.orientation = "landscape"
    s.page_setup.fitToWidth = 1
    s.sheet_properties.pageSetUpPr.fitToPage = True
    s.page_setup.fitToHeight = 0

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(OUT)
