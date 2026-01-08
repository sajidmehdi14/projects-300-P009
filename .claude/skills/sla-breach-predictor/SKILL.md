---
name: sla-breach-predictor
description: "Predict which support tickets will breach SLA based on ticket metadata (priority, age, status, last update, group workload). Outputs breach risk (LOW/MEDIUM/HIGH) with explainable reasons and recommended actions. Use when users need to: (1) Analyze tickets for SLA breach risk, (2) Prioritize which tickets need immediate attention, (3) Monitor SLA compliance, (4) Generate SLA breach reports, or (5) Automate SLA monitoring workflows. Accepts CSV or JSON ticket data."
---

# SLA Breach Predictor

## Overview

Predict SLA breach risk for support tickets using a lightweight, explainable scoring model. No ML training required—uses configurable rules based on time consumed, group workload, priority, and ticket stagnation.

## Quick Start

Basic usage:

```bash
python scripts/sla_predict.py tickets.json
```

With custom configuration:

```bash
python scripts/sla_predict.py tickets.json --config custom_sla_config.json
```

Save output to file:

```bash
python scripts/sla_predict.py tickets.json --output results.json
```

Get summary instead of full JSON:

```bash
python scripts/sla_predict.py tickets.json --format summary
```

## Input Format

### Required Fields

Tickets must include:

- **id** or **ticket_id**: Unique identifier
- **priority**: P1, P2, P3, or P4
- **status**: Ticket state (e.g., "New", "In Progress", "Resolved")
- **created** or **age**: When the ticket was created (ISO format or various datetime formats)
- **last_update**: When the ticket was last updated
- **assigned_group**: Group or team handling the ticket

### Supported Formats

**JSON:**
```json
[
  {
    "id": "INC001234",
    "priority": "P1",
    "status": "In Progress",
    "created": "2026-01-08 10:00:00",
    "last_update": "2026-01-08 12:30:00",
    "assigned_group": "Infrastructure"
  }
]
```

**CSV:**
```csv
id,priority,status,created,last_update,assigned_group
INC001234,P1,In Progress,2026-01-08 10:00:00,2026-01-08 12:30:00,Infrastructure
```

See `assets/example_tickets.json` and `assets/example_tickets.csv` for complete examples.

## Output Format

Each prediction includes:

```json
{
  "ticket_id": "INC001234",
  "priority": "P1",
  "status": "In Progress",
  "assigned_group": "Infrastructure",
  "breach_risk": "HIGH",
  "reason": "85% of SLA time consumed; assigned group has high workload (score: 65); high priority (P1)",
  "recommended_action": "Escalate to manager; Immediate attention required; Consider reassigning to different group",
  "time_consumed_pct": 85,
  "group_workload_score": 65
}
```

**Fields:**

- **breach_risk**: LOW, MEDIUM, HIGH, or N/A (for closed tickets)
- **reason**: Human-readable explanation of the risk assessment
- **recommended_action**: Suggested actions to prevent breach
- **time_consumed_pct**: Percentage of SLA time elapsed (0-100+)
- **group_workload_score**: Weighted workload score for the assigned group

## Configuration

### Default SLA Thresholds

Uses standard ITIL targets:

- **P1** (Critical): 4 hours
- **P2** (High): 24 hours
- **P3** (Medium): 72 hours
- **P4** (Low): 168 hours (7 days)

### Custom Configuration

Create a JSON config file to override defaults:

```json
{
  "sla_thresholds": {
    "P1": 2,
    "P2": 12,
    "P3": 48,
    "P4": 120
  },
  "risk_thresholds": {
    "high": 0.80,
    "medium": 0.60
  },
  "workload_weights": {
    "P1": 10,
    "P2": 5,
    "P3": 2,
    "P4": 1
  },
  "workload_thresholds": {
    "high": 50,
    "medium": 30
  }
}
```

See `assets/sla_config.json` for the full default configuration.

## Scoring Logic

### Risk Levels

**HIGH** - Immediate action required:
- ≥75% of SLA time consumed, OR
- MEDIUM risk with high group workload, OR
- Any non-LOW risk with stagnant ticket

**MEDIUM** - Attention needed soon:
- ≥50% of SLA time consumed, OR
- LOW risk with high group workload, OR
- P1/P2 tickets at ≥40% time consumed

**LOW** - Monitor:
- <50% of SLA time consumed
- Normal workload conditions

### Factors Considered

1. **Time Consumed**: Percentage of SLA time elapsed since ticket creation
2. **Group Workload**: Weighted sum of open tickets (P1=10pts, P2=5pts, P3=2pts, P4=1pt)
3. **Priority**: Higher priorities get stricter thresholds
4. **Stagnation**: Tickets with no updates in >25% of SLA time are escalated
5. **Status**: Closed/resolved tickets are marked N/A

For detailed scoring algorithms, see `references/scoring_logic.md`.

## Recommended Actions

Actions are suggested based on risk factors:

- **Escalate to manager** - HIGH risk tickets
- **Immediate attention required** - HIGH risk P1/P2 tickets
- **Consider reassigning to different group** - HIGH workload teams
- **Send reminder to assignee** - Stagnant tickets
- **Increase priority if possible** - MEDIUM risk P3/P4 tickets
- **Assign to resolver group** - Tickets still in "New" status
- **Monitor** - LOW risk tickets

## Common Workflows

### Daily SLA Monitoring

```bash
# Generate daily report
python scripts/sla_predict.py daily_tickets.json --format summary > daily_report.txt

# Email high-risk tickets
python scripts/sla_predict.py daily_tickets.json | jq '[.[] | select(.breach_risk=="HIGH")]'
```

### Integration with Ticketing Systems

```python
# Export from ticketing system
tickets = export_tickets_to_json()

# Run prediction
from scripts.sla_predict import SLAPredictor
predictor = SLAPredictor()
predictions = predictor.predict_all(tickets)

# Take automated actions
for pred in predictions:
    if pred['breach_risk'] == 'HIGH':
        escalate_ticket(pred['ticket_id'])
```

### Custom Thresholds by Customer Tier

Create different config files per customer tier:

```bash
# Premium customers (stricter SLAs)
python scripts/sla_predict.py premium_tickets.json --config premium_sla.json

# Standard customers
python scripts/sla_predict.py standard_tickets.json --config standard_sla.json
```

## Resources

- **scripts/sla_predict.py** - Main prediction script
- **references/scoring_logic.md** - Detailed explanation of risk calculation algorithms
- **assets/sla_config.json** - Default configuration template
- **assets/example_tickets.json** - Sample ticket data (JSON format)
- **assets/example_tickets.csv** - Sample ticket data (CSV format)
