---
name: support-metrics-narrator
description: Convert weekly support metrics into human-readable narrative summaries for IT support managers. Use when users need to transform raw support ticket data (CSV/JSON format) into management-friendly markdown reports covering ticket volume trends, SLA performance, top issue categories, and key risks. Triggered by requests like "generate weekly support summary", "create support metrics report", "analyze support ticket data", or when working with support metrics files that need narrative explanation for leadership.
---

# Support Metrics Narrator

## Overview

This skill transforms raw support metrics data into actionable narrative summaries for IT support management. Instead of manually interpreting CSV exports or JSON data from ticketing systems, the skill generates markdown reports with clear insights about ticket trends, SLA compliance, issue categories, and operational risks.

**Primary use case:** Weekly support reporting for IT managers and leadership.

## Quick Start

Generate a narrative summary from metrics data:

```bash
python scripts/narrate_metrics.py metrics.csv
```

Save to a file:

```bash
python scripts/narrate_metrics.py metrics.csv -o weekly_summary.md
```

The script accepts both CSV and JSON formats. See [examples.md](references/examples.md) for detailed format specifications.

## What Gets Analyzed

The narrative summary includes four key sections:

### 1. Ticket Volume Trend
- Current vs previous week comparison
- Week-over-week percentage change
- Total ticket count for the period
- Action recommendations for significant changes

### 2. SLA Performance
- Overall compliance rate with status indicator (✅/⚠️/🔴)
- Current week performance
- Tickets met vs breached counts
- Compliance thresholds: Green (≥95%), Yellow (90-95%), Red (<90%)

### 3. Top Issue Categories
- Top 5 issue categories by volume
- Ticket counts per category
- Insights on dominant categories

### 4. Key Risks
- SLA compliance risks
- Volume spike warnings
- Outstanding critical tickets
- Capacity concerns

## Input Requirements

**Minimum required fields:**
- `tickets`: Total ticket count
- `sla_met`: Tickets meeting SLA
- `sla_breached`: Tickets breaching SLA
- `category`: Issue category name
- `count`: Count per category

**Optional fields:**
- `week`: Week identifier
- `priority`: Ticket priority level
- `status`: Current status

For complete format examples and sample data, see [examples.md](references/examples.md).

## Output Format

The skill generates markdown output with:
- Clear section headers
- Bullet point narratives (no charts/graphs)
- Action-oriented insights
- Status indicators (emojis for quick scanning)
- Timestamp for report generation

## Common Workflows

### Weekly Management Report

When a user provides weekly metrics:

1. Load the metrics file (CSV or JSON)
2. Run the narrator script
3. Review the generated summary
4. Save to a report file or share directly

Example:
```bash
python scripts/narrate_metrics.py exports/week_52_metrics.csv -o reports/week_52_summary.md
```

### Ad-hoc Analysis

For quick metric reviews during the week:

1. Export current data from ticketing system
2. Run the script to stdout
3. Review insights immediately

Example:
```bash
python scripts/narrate_metrics.py current_metrics.json
```

### Automated Reporting

Integrate into scheduled jobs for automatic report generation:

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
python scripts/narrate_metrics.py "metrics_$DATE.csv" -o "summary_$DATE.md"
```

## Script Details

**Location:** `scripts/narrate_metrics.py`

**Command line options:**
- `input_file` (required): Path to CSV or JSON metrics file
- `-o, --output` (optional): Output file path (defaults to stdout)

**Exit codes:**
- `0`: Success
- `1`: Error (file not found, invalid format, no metrics)

## Interpreting Results

The narrative includes action recommendations based on:
- **Volume changes >20%**: Capacity review recommended
- **SLA <95%**: Process and staffing review needed
- **Critical tickets open**: Immediate escalation required

Review the [examples.md](references/examples.md) file for detailed interpretation guidance and output examples.

## Notes

- Script is designed for weekly reporting but works with any time period
- Handles both single-week and multi-week data
- Generates consistent markdown format for easy integration with docs/wikis
- LOC count: ~290 (well under 500 LOC requirement)
