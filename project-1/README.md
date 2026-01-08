# Notes:
```text
We created 3 Claude Code Skills for IT Management with following details.

1- incident-triage-classifier
2- rca-summary-writer
3- sla-breach-predictor
```
# URLs for skills
- https://github.com/sajidmehdi14/projects-300-P009/tree/main/.claude/skills/incident-triage-classifier

- https://github.com/sajidmehdi14/projects-300-P009/tree/main/.claude/skills/rca-summary-writer

- https://github.com/sajidmehdi14/projects-300-P009/tree/main/.claude/skills/sla-breach-predictor

# Prompt Skill 1:
```text
Create Skill using skill-creator skill standards 

# Skill Name: Incident-Triage-and-Priority-Classifier

Outcome: Convert messy tickets into structured priority + routing.

Claude Code Prompt

Build a Claude Code skill named incident_triage_classifier.

Purpose: Take raw IT support tickets (email, chat, portal text) and output:

Severity (P1–P4)

Category (Network, App, Security, Hardware, Access, Other)

Suggested resolver group

1-line business impact

Inputs: plain text ticket content
Output: strict JSON schema

Requirements:

Deterministic rules + LLM reasoning combined

Configurable severity criteria in a YAML file

Unit tests for at least 10 ticket samples

CLI usage: triage_ticket.py ticket.txt

Keep code under 600 LOC.

This skill replaces manual triage by IT support managers and saves ~3 minutes per ticket.
```

# Prompt 2
```text
Create Skill using skill-creator skill standards 

# Skill Name: Root-Cause-Summary-Generator

Outcome: Auto-write RCA summaries from logs + notes.

Claude Code Prompt

Build a Claude Code skill named rca_summary_writer.

Purpose: Generate a professional Root Cause Analysis summary from:

Incident description

Timeline

Logs or engineer notes

Output:

Root cause

Contributing factors

Resolution

Preventive actions

Output must be in markdown report format.

Constraints:

No hallucinated facts

If data is missing, explicitly state assumptions

Deterministic formatting template

CLI:
python rca_writer.py incident.json > rca.md

Keep implementation under 700 LOC.

This replaces manual RCA writing and improves report quality.

```

# Prompt 3
```text
Create Skill using skill-creator skill standards 

# Skill Name: SLA-Breach-Predictor

Outcome: Predict which tickets will breach SLA.

Claude Code Prompt

Build a Claude Code skill named sla_breach_predictor.

Purpose: Given ticket metadata (priority, age, status, last update, group workload), predict:

Breach risk: LOW / MEDIUM / HIGH

Reason

Recommended next action

Inputs: CSV or JSON tickets
Output: annotated JSON

Requirements:

Lightweight scoring model (no ML training required)

Explainable decision logic

Configurable SLA thresholds

CLI:
python sla_predict.py tickets.json

Target LOC: under 500.

This replaces manual SLA monitoring by managers.

```

# Prompt 4
```text
Create Skill using skill-creator skill standards 

# Skill Name: Executive-Incident-Report-Generator

Outcome: Convert technical chaos into executive-friendly summary.

Claude Code Prompt

Build a Claude Code skill named executive_incident_reporter.

Purpose: Convert technical incident data into an executive report containing:

What happened

Business impact

Resolution status

Next steps

Audience: non-technical leadership.

Input: JSON incident data
Output: 1-page markdown report.

Constraints:

No jargon

Business language only

Consistent tone template

CLI:
python exec_report.py incident.json

Keep under 600 LOC.

This replaces manual executive communication drafting.

```

# Prompt 5
```text
Create Skill using skill-creator skill standards 

# Skill Name: Weekly-Support-Metrics-Narrator

Outcome: Turn metrics into human explanation.

Claude Code Prompt

Build a Claude Code skill named support_metrics_narrator.

Purpose: Convert weekly support metrics into a narrative summary:

Ticket volume trend

SLA performance

Top issue categories

Key risks

Input: CSV or JSON metrics
Output: markdown management summary.

Constraints:

No charts

Clear bullet narrative

Action-oriented insights

CLI:
python narrate_metrics.py metrics.csv

Keep LOC under 500.

This replaces weekly report writing by IT support managers.
```