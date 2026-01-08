---
name: rca-summary-writer
description: Generate professional Root Cause Analysis (RCA) summary reports from incident data. Use when users need to create RCA documentation from incidents, outages, or post-mortem analysis. Accepts JSON incident data with logs, timelines, and engineer notes, and produces markdown-formatted RCA reports with root cause, contributing factors, resolution steps, and preventive actions. Triggered by requests like "generate an RCA", "write a root cause analysis", "create a post-mortem report", or "analyze this incident".
---

# RCA Summary Writer

## Overview

Generate comprehensive, professional Root Cause Analysis (RCA) reports from structured incident data. The skill provides a deterministic Python script that transforms incident JSON files into well-formatted markdown reports following industry-standard RCA structure.

## Quick Start

```bash
python scripts/rca_writer.py incident.json > rca.md
```

Or via stdin:

```bash
cat incident.json | python scripts/rca_writer.py - > rca.md
```

## Input Format

The script expects a JSON file with incident data. Required and optional fields:

**Core Fields:**
- `incident_id` (string): Unique incident identifier (e.g., "INC-2026-001")
- `title` (string): Brief incident title
- `description` (string): Detailed incident description
- `severity` (string): Incident severity (P0/P1/P2/P3/P4, Critical/High/Medium/Low)

**Timing:**
- `start_time` (ISO 8601 timestamp): When incident began
- `end_time` (ISO 8601 timestamp): When incident resolved
- `timeline` (array): List of timestamped events
  - Each event: `{"timestamp": "...", "description": "..."}`

**Technical Data:**
- `logs` (array): Log entries from affected systems
  - Each log: `{"timestamp": "...", "level": "ERROR|WARN|INFO", "message": "..."}`
- `affected_services` (array of strings): List of impacted services
- `engineer_notes` (string): Investigation notes from engineers

**Analysis Fields:**
- `impact` (string): Business and technical impact description
- `root_cause` (string): Identified root cause (if known)
- `contributing_factors` (array of strings): Secondary factors
- `resolution` (string): How the incident was resolved
- `preventive_actions` (array of strings): Actions to prevent recurrence

**Example Input:**

```json
{
  "incident_id": "INC-2026-042",
  "title": "API Gateway Timeout - Payment Service",
  "severity": "P1",
  "description": "Payment API experiencing timeouts affecting checkout",
  "start_time": "2026-01-08T14:30:00Z",
  "end_time": "2026-01-08T16:15:00Z",
  "affected_services": ["payment-api", "checkout-service"],
  "impact": "30% of checkout attempts failed. Estimated revenue impact: $50k",
  "timeline": [
    {"timestamp": "2026-01-08T14:30:00Z", "description": "First timeout alerts"},
    {"timestamp": "2026-01-08T14:45:00Z", "description": "On-call engineer paged"},
    {"timestamp": "2026-01-08T15:20:00Z", "description": "Root cause identified"},
    {"timestamp": "2026-01-08T15:45:00Z", "description": "Fix deployed"},
    {"timestamp": "2026-01-08T16:15:00Z", "description": "Services fully restored"}
  ],
  "logs": [
    {"timestamp": "2026-01-08T14:30:15Z", "level": "ERROR", "message": "Connection timeout to database"},
    {"timestamp": "2026-01-08T14:30:22Z", "level": "ERROR", "message": "Connection pool exhausted"}
  ],
  "engineer_notes": "Database connection pool was undersized after traffic spike from marketing campaign",
  "root_cause": "Database connection pool exhaustion due to 3x traffic increase without capacity adjustment",
  "contributing_factors": [
    "Marketing campaign launched without capacity planning review",
    "No auto-scaling configured for connection pools",
    "Alerting threshold set too high to catch gradual degradation"
  ],
  "resolution": "Increased database connection pool size from 50 to 200 connections and restarted payment service",
  "preventive_actions": [
    "Implement auto-scaling for database connection pools",
    "Require capacity review for marketing campaigns",
    "Lower alerting thresholds for connection pool saturation"
  ]
}
```

## Running the Script

The `rca_writer.py` script is located in `scripts/` and requires Python 3.6+. No external dependencies needed.

**From file:**
```bash
python scripts/rca_writer.py path/to/incident.json > output.md
```

**From stdin:**
```bash
echo '{"incident_id": "INC-001", "title": "Test"}' | python scripts/rca_writer.py - > output.md
```

**Direct execution:**
```bash
chmod +x scripts/rca_writer.py
./scripts/rca_writer.py incident.json > rca.md
```

## Output Format

The script generates a structured markdown report with these sections:

1. **Executive Summary**: Incident ID, title, severity, timing, affected services, impact
2. **Incident Description**: Detailed description of what occurred
3. **Timeline**: Chronological sequence of events
4. **Logs Summary**: Log level distribution and sample error logs
5. **Engineer Notes**: Investigation notes and observations
6. **Root Cause Analysis**: Primary root cause identified
7. **Contributing Factors**: Secondary factors that enabled or amplified the issue
8. **Resolution**: Actions taken to resolve the incident
9. **Preventive Actions**: Checkbox list of actions to prevent recurrence
10. **Assumptions and Notes**: Documents any assumptions made due to missing data

See `assets/rca_template.md` for the complete output template structure.

## Analysis Guidelines

### No Hallucinated Facts

The script adheres to strict data integrity:

- Only uses information present in the input JSON
- Never invents times, metrics, or technical details
- If a field is missing, explicitly notes it in the report

### Explicit Assumptions

When data is incomplete, the script:

- Documents each assumption in the "Assumptions and Notes" section
- Uses phrases like "inferred from", "appears to be", "based on available data"
- Tracks all assumptions in a dedicated section at the report end

Examples of documented assumptions:
- "Root cause inferred from incident data; may require validation"
- "Timeline events not provided; incident progression is not documented"
- "Preventive actions suggested based on incident patterns"

### Intelligent Analysis

When explicit fields aren't provided, the script performs limited inference:

- Extracts root cause indicators from logs and descriptions (timeouts, errors, etc.)
- Identifies contributing factors from incident context (deployments, load spikes)
- Suggests preventive actions based on incident patterns
- All inferences are clearly marked as such in the assumptions section

### Deterministic Formatting

The output format is consistent across all reports:

- Same section ordering every time
- Standardized timestamp format (YYYY-MM-DD HH:MM:SS UTC)
- Consistent markdown styling
- Checkbox format for preventive actions (`- [ ] Action item`)

## Best Practices

**When creating incident JSON:**

1. **Be comprehensive**: Include all available fields. More data = better analysis.
2. **Use ISO 8601 timestamps**: Format as `YYYY-MM-DDTHH:MM:SSZ` for proper parsing.
3. **Structure timeline chronologically**: Order events from earliest to latest.
4. **Include log context**: Don't just include errors; include surrounding logs.
5. **Document resolution steps**: Capture what actually fixed the issue.

**When reviewing generated RCAs:**

1. **Check assumptions section**: Review and validate any inferred information.
2. **Add missing context**: If the script noted missing fields, add them and regenerate.
3. **Validate preventive actions**: Suggested actions are generic; customize to your context.
4. **Review with stakeholders**: Use the report as a starting point for team discussion.

## Resources

### scripts/rca_writer.py

Python script (643 LOC) that generates RCA reports. Key features:

- Zero external dependencies (uses only Python stdlib)
- Handles missing data gracefully with explicit assumption tracking
- Performs intelligent inference while staying grounded in provided data
- Generates consistent, deterministic markdown output
- Supports both file input and stdin piping

### assets/rca_template.md

Reference template showing the complete structure and format of generated RCA reports. Use this to understand the expected output format before running the script.
