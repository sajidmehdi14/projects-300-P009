# SLA Breach Prediction Scoring Logic

This document explains how the SLA breach predictor calculates risk levels and recommends actions.

## Overview

The predictor uses a lightweight, rule-based scoring model that considers:

1. **Time consumed** - Percentage of SLA time elapsed
2. **Group workload** - Weighted count of tickets assigned to the group
3. **Priority** - Ticket priority level (P1-P4)
4. **Stagnation** - Time since last update
5. **Status** - Current ticket state

## SLA Thresholds

Default ITIL-standard SLA targets by priority:

- **P1** (Critical): 4 hours
- **P2** (High): 24 hours
- **P3** (Medium): 72 hours (3 days)
- **P4** (Low): 168 hours (7 days)

## Time Consumed Calculation

```
time_consumed = (current_time - created_time) / sla_threshold
```

Example: A P2 ticket created 18 hours ago has consumed 75% of its SLA time (18/24 = 0.75).

## Group Workload Calculation

Each group's workload is calculated as a weighted sum of open tickets:

**Workload Weights:**
- P1: 10 points
- P2: 5 points
- P3: 2 points
- P4: 1 point

**Workload Levels:**
- **HIGH**: Score ≥ 50
- **MEDIUM**: Score ≥ 30
- **LOW**: Score < 30

Example: A group with 2 P1s, 3 P2s, and 5 P3s has a workload score of: (2×10) + (3×5) + (5×2) = 45 (MEDIUM)

## Stagnation Detection

A ticket is considered stagnant if the time since last update exceeds 25% of the SLA threshold.

Examples:
- P1: Stagnant if no update in > 1 hour (25% of 4h)
- P2: Stagnant if no update in > 6 hours (25% of 24h)
- P3: Stagnant if no update in > 18 hours (25% of 72h)

## Risk Level Determination

### Base Risk (by time consumed)

- **HIGH**: ≥ 75% of SLA time consumed
- **MEDIUM**: ≥ 50% of SLA time consumed
- **LOW**: < 50% of SLA time consumed

### Risk Adjustments

The base risk is then adjusted based on other factors:

1. **High workload escalation**: If group workload is HIGH:
   - MEDIUM → HIGH
   - LOW → MEDIUM

2. **High priority attention**: For P1/P2 tickets:
   - LOW → MEDIUM if time consumed ≥ 40%

3. **Stagnation escalation**: If ticket is stagnant and risk is not LOW:
   - Any non-LOW risk → HIGH

### Risk Determination Examples

**Example 1: P1 ticket, 85% consumed, HIGH workload**
- Base: HIGH (85% > 75%)
- No adjustment needed
- Final: **HIGH**

**Example 2: P2 ticket, 60% consumed, LOW workload, not stagnant**
- Base: MEDIUM (60% > 50%)
- No adjustment (workload is LOW, not P1)
- Final: **MEDIUM**

**Example 3: P3 ticket, 45% consumed, HIGH workload, stagnant**
- Base: LOW (45% < 50%)
- Adjusted to MEDIUM (HIGH workload)
- Adjusted to HIGH (stagnant)
- Final: **HIGH**

## Recommended Actions

Actions are recommended based on risk level and contributing factors:

### HIGH Risk Actions

- **Always**: "Escalate to manager"
- **If P1/P2**: Add "Immediate attention required"
- **If high workload**: Add "Consider reassigning to different group"
- **If stagnant**: Add "Send reminder to assignee"
- **If status is 'New'**: Add "Assign to resolver group"

### MEDIUM Risk Actions

- **If high workload**: "Consider reassigning to different group"
- **If P3/P4**: "Increase priority if possible"
- **If stagnant**: "Send reminder to assignee"
- **If status is 'New'**: "Assign to resolver group"

### LOW Risk Actions

- "Monitor" - No immediate action needed

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

## Configuration

All thresholds are configurable via `sla_config.json`:

```json
{
  "sla_thresholds": { ... },      // SLA targets by priority
  "risk_thresholds": { ... },      // Time consumed thresholds
  "workload_weights": { ... },     // Priority weights
  "workload_thresholds": { ... }   // Workload level thresholds
}
```
