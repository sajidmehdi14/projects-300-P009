---
name: executive-incident-reporter
description: Convert technical incident data into executive-friendly summary reports. Use when users need to generate executive incident reports, create business-focused incident summaries, translate technical incident data for leadership, or convert incident JSON files into non-technical reports. Triggered by requests like "generate an executive report", "create an incident summary for leadership", "convert this incident to a business report", or when working with incident data files (JSON) that need executive communication.
---

# Executive Incident Reporter

## Overview

Convert technical incident data (logs, error codes, stack traces) into concise, executive-friendly reports suitable for non-technical leadership. Automatically translates technical jargon into business language and structures information around business impact, resolution status, and next steps.

**Input:** JSON file containing technical incident data
**Output:** 1-page markdown executive report
**Audience:** Non-technical leadership and executives

## Quick Start

Generate an executive report from incident data:

```bash
python3 scripts/exec_report.py incident.json
```

The script will:
1. Parse technical incident data from JSON
2. Translate technical terms to business language
3. Generate a structured markdown report
4. Save output as `<incident_name>_executive_report.md`

## Usage Workflow

### Step 1: Prepare Incident Data

Collect incident information in JSON format. The script accepts flexible JSON structures and extracts relevant fields automatically.

**Required fields:**
- `incident_id` or `id` - Incident identifier
- `title` - Brief incident title
- `description` or `error_message` - What happened (technical details OK)

**Recommended fields for richer reports:**
- `severity` or `priority` - Critical, high, medium, low, or P1-P4
- `status` - investigating, identified, resolved, monitoring
- `affected_systems` - List of impacted services
- `affected_users` - Number of users impacted
- `revenue_impact` - Financial impact amount
- `start_time`, `end_time` - Incident timeline
- `root_cause` - Technical root cause description
- `actions_taken` - List of remediation steps
- `next_steps` - Planned follow-up actions
- `preventive_measures` - Long-term improvements

**Example minimal incident JSON:**

```json
{
  "incident_id": "INC-2024-001",
  "title": "Database Connection Failure",
  "description": "PostgreSQL connection pool exhausted causing 500 errors",
  "severity": "critical",
  "status": "resolved",
  "affected_users": 5000,
  "root_cause": "Database connection pool size too small for traffic spike"
}
```

See `scripts/example_incident.json` for a comprehensive example with all supported fields.

### Step 2: Generate Report

Run the script with your incident JSON:

```bash
python3 scripts/exec_report.py my_incident.json
```

The script automatically:
- Translates technical terms (e.g., "500 error" → "server error", "connection pool" → "database access capacity")
- Structures information into executive-friendly sections
- Quantifies business impact with metrics
- Summarizes resolution status and next steps

### Step 3: Review and Distribute

The generated markdown report includes:

1. **Executive Summary** - Status, severity, duration at a glance
2. **What Happened** - Non-technical description of the incident
3. **Business Impact** - Customer and revenue effects with metrics
4. **Resolution Status** - Current state, actions taken, root cause
5. **Next Steps** - Immediate actions and preventive measures

Review the output file and distribute to leadership. The report is designed to be consumed in under 2 minutes.

## Report Sections Explained

### Executive Summary
High-level snapshot with status, severity, and duration. Enables leadership to quickly assess incident criticality.

### What Happened
Translates technical incident details into plain language. Removes jargon like "stack traces", "deadlocks", "latency" and replaces with business-friendly terms.

### Business Impact
Focuses on customer and revenue effects. Includes quantifiable metrics:
- Number of affected users
- Revenue impact estimates
- Customer complaint volume

Maps technical severity levels to business impact descriptions automatically.

### Resolution Status
Communicates current state (investigating, resolved, monitoring) and summarizes actions taken. Includes root cause when identified, translated to business language.

### Next Steps
Outlines immediate actions and long-term preventive measures. Helps leadership understand the path forward without technical implementation details.

## Technical Translation

The script automatically converts technical terminology to business language:

**Infrastructure terms:**
- "downtime" → "service unavailability"
- "latency" → "slow response times"
- "5xx error" → "server error"
- "failover" → "automatic backup system activation"

**Database terms:**
- "connection pool" → "database access capacity"
- "deadlock" → "conflicting operations"
- "replication lag" → "data synchronization delay"

**Application terms:**
- "memory leak" → "resource consumption issue"
- "stack trace" → "error details"
- "timeout" → "delayed response"

This ensures the report remains accessible to non-technical audiences.

## Customization

### Adjusting Translation Rules

Edit the `TERM_MAP` dictionary in `scripts/exec_report.py` (lines 20-60) to customize technical-to-business translations:

```python
TERM_MAP = {
    'your_technical_term': 'business-friendly description',
    # Add custom mappings here
}
```

### Modifying Severity Impact

Edit `SEVERITY_IMPACT` dictionary (lines 63-75) to customize how severity levels map to business impact descriptions:

```python
SEVERITY_IMPACT = {
    'critical': 'Your custom critical impact description',
    'high': 'Your custom high impact description',
    # Add custom severity mappings
}
```

### Adjusting Report Structure

The report structure is defined in the `ExecutiveReportGenerator` class. Modify section generation methods:
- `_generate_what_happened()` - Incident description section
- `_generate_business_impact()` - Business impact section
- `_generate_resolution_status()` - Resolution status section
- `_generate_next_steps()` - Next steps section

## Common Scenarios

### Scenario 1: Real-time Incident Communication

During an active incident, generate an initial executive report:

```json
{
  "incident_id": "INC-LIVE-001",
  "title": "Payment API Degradation",
  "status": "investigating",
  "severity": "high",
  "description": "Elevated error rates in payment processing service",
  "affected_users": 1200
}
```

As the incident progresses, update the JSON with new information and regenerate the report.

### Scenario 2: Post-Incident Summary

After resolution, create a comprehensive executive summary:

```json
{
  "incident_id": "INC-2024-042",
  "title": "Service Outage - Checkout",
  "status": "resolved",
  "severity": "critical",
  "start_time": "2024-01-15T10:00:00Z",
  "end_time": "2024-01-15T12:30:00Z",
  "root_cause": "Database deadlock during high traffic",
  "actions_taken": ["Increased connection pool", "Deployed fix"],
  "preventive_measures": ["Add monitoring", "Load testing"],
  "affected_users": 15000,
  "revenue_impact": 50000
}
```

### Scenario 3: Security Incident Reporting

Report security incidents with appropriate sensitivity:

```json
{
  "incident_id": "SEC-2024-005",
  "title": "Authentication Service Vulnerability",
  "severity": "high",
  "status": "mitigated",
  "description": "Vulnerability detected in authentication token validation",
  "actions_taken": ["Deployed security patch", "Rotated credentials"],
  "next_steps": ["Security audit", "Update access policies"]
}
```

## Constraints and Best Practices

**Length:** Reports are designed to fit on 1 page (approximately 500-800 words) for quick executive consumption.

**Tone:** Business-focused, avoiding technical jargon. When technical terms are necessary, they are explained in plain language.

**Audience:** Non-technical leadership who need to understand business impact, not implementation details.

**Frequency:** Generate reports at key incident milestones:
- Initial detection (status: investigating)
- Root cause identified (status: identified)
- Resolution deployed (status: resolved)
- Post-incident review (final report)

**Script Limitations:**
- Maximum 600 lines of code (current: ~440 LOC)
- Requires Python 3.6+
- No external dependencies (uses standard library only)

## Resources

### scripts/exec_report.py
Main Python script that converts incident JSON to executive markdown reports. Can be executed directly or read for customization.

### scripts/example_incident.json
Comprehensive example incident JSON demonstrating all supported fields and realistic technical incident data (database outage with logs, metrics, timeline).

## When NOT to Use This Skill

This skill is specifically for executive incident reporting. Do not use when:
- Users need detailed technical post-mortems (use RCA skill instead)
- Users need real-time incident tracking dashboards
- Users need to generate incident data from logs (use log analysis tools first)
- Users need internal team communication (use standard incident updates)

This skill bridges the gap between technical incident management and executive communication.
