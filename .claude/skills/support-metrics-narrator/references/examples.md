# Support Metrics Narrator - Examples

## Input Format Examples

### CSV Format

The script accepts CSV files with the following columns:

```csv
week,tickets,sla_met,sla_breached,category,count,priority,status
2026-W01,45,40,5,Network Issues,15,normal,closed
2026-W01,45,40,5,Software Bugs,12,normal,closed
2026-W01,45,40,5,Access Requests,10,normal,closed
2026-W01,45,40,5,Hardware Failures,8,critical,open
2026-W02,52,45,7,Network Issues,18,normal,closed
2026-W02,52,45,7,Software Bugs,14,normal,closed
2026-W02,52,45,7,Access Requests,12,normal,closed
2026-W02,52,45,7,Password Resets,8,normal,closed
```

**Required columns:**
- `tickets`: Total ticket count for the period
- `sla_met`: Number of tickets that met SLA
- `sla_breached`: Number of tickets that breached SLA
- `category`: Issue category name
- `count`: Count for this specific category

**Optional columns:**
- `week`: Week identifier
- `priority`: Ticket priority (critical, high, normal, low)
- `status`: Ticket status (open, closed, pending)

### JSON Format

The script also accepts JSON files in two formats:

**Array format:**

```json
[
  {
    "week": "2026-W01",
    "tickets": 45,
    "sla_met": 40,
    "sla_breached": 5,
    "category": "Network Issues",
    "count": 15,
    "priority": "normal",
    "status": "closed"
  },
  {
    "week": "2026-W01",
    "tickets": 45,
    "sla_met": 40,
    "sla_breached": 5,
    "category": "Software Bugs",
    "count": 12,
    "priority": "normal",
    "status": "closed"
  }
]
```

**Single object format:**

```json
{
  "week": "2026-W02",
  "tickets": 52,
  "sla_met": 45,
  "sla_breached": 7,
  "category": "Network Issues",
  "count": 18
}
```

## Output Example

```markdown
# Weekly Support Metrics Summary

**Generated:** 2026-01-08 14:30

---

## Ticket Volume Trend

- **Current Week:** 52 tickets
- **Previous Week:** 45 tickets
- **Week-over-Week Change:** ↑ 15.6% (+7 tickets)
- **Period Total:** 97 tickets

**Action:** Volume increased significantly. Review team capacity and prioritization.

## SLA Performance

- **Overall Compliance:** 91.8% ⚠️
- **Current Week:** 86.5%
- **Tickets Met:** 85
- **Tickets Breached:** 12

**Action:** SLA compliance below target. Review breach root causes and staffing levels.

## Top Issue Categories

1. **Network Issues** - 33 tickets
2. **Software Bugs** - 26 tickets
3. **Access Requests** - 22 tickets
4. **Password Resets** - 8 tickets
5. **Hardware Failures** - 8 tickets

**Insight:** 'Network Issues' represents the largest category. Consider root cause analysis or knowledge base updates.

## Key Risks

- SLA compliance at 91.8% - approaching threshold
- Ticket volume increased 16% - potential capacity issue
- Critical priority ticket outstanding: Hardware Failures

**Action:** Address high-priority risks immediately. Schedule risk review with leadership.

---

*This summary is auto-generated from support metrics data.*
```

## Usage Examples

### Basic usage (output to stdout):

```bash
python scripts/narrate_metrics.py data/weekly_metrics.csv
```

### Save to file:

```bash
python scripts/narrate_metrics.py data/weekly_metrics.csv -o reports/weekly_summary.md
```

### Using JSON input:

```bash
python scripts/narrate_metrics.py data/metrics.json -o summary.md
```

## Common Patterns

### Weekly Report Generation

Create a weekly report from your ticketing system export:

```bash
# Export from ticketing system to CSV
# Run the narrator
python scripts/narrate_metrics.py exports/week_52_2025.csv -o reports/week_52_summary.md

# Review and share with leadership
cat reports/week_52_summary.md
```

### Automated Reporting Pipeline

Integrate into a scheduled job:

```bash
#!/bin/bash
# weekly_report.sh

DATE=$(date +%Y-%m-%d)
METRICS_FILE="exports/metrics_$DATE.csv"
OUTPUT_FILE="reports/summary_$DATE.md"

# Generate the narrative
python scripts/narrate_metrics.py "$METRICS_FILE" -o "$OUTPUT_FILE"

# Email or post to Slack
# mail -s "Weekly Support Summary" team@company.com < "$OUTPUT_FILE"
```

## Interpreting the Output

### Ticket Volume Trend

- **Green signals:** Stable or decreasing volume with maintained quality
- **Yellow signals:** Moderate increases (10-20%) - monitor closely
- **Red signals:** Sharp increases (>20%) - immediate capacity review needed

### SLA Performance

- **Green (≥95%):** Meeting targets consistently
- **Yellow (90-95%):** Approaching threshold - investigate causes
- **Red (<90%):** Immediate action required - review processes and staffing

### Top Issue Categories

Use category analysis to:
- Identify recurring problems requiring permanent fixes
- Update knowledge base articles
- Plan training for common issues
- Allocate specialist resources

### Key Risks

Risk indicators include:
- SLA compliance trending downward
- Sudden volume spikes
- Critical priority tickets remaining open
- Single category dominating ticket volume
