# Root Cause Analysis Report

**Incident ID:** INC-YYYY-NNN
**Title:** Brief incident title
**Severity:** P0/P1/P2/P3/P4

**Start Time:** YYYY-MM-DD HH:MM:SS UTC
**End Time:** YYYY-MM-DD HH:MM:SS UTC
**Duration:** X hours, Y minutes

**Affected Services:** service1, service2, service3

## Impact

Description of business and technical impact, including:
- Number of affected users
- Affected functionality
- Revenue or SLA impact

## Incident Description

Detailed description of what happened, including:
- Initial symptoms
- How the incident was detected
- Initial assessment

## Timeline

- **YYYY-MM-DD HH:MM:SS UTC**: Incident first detected
- **YYYY-MM-DD HH:MM:SS UTC**: Investigation started
- **YYYY-MM-DD HH:MM:SS UTC**: Root cause identified
- **YYYY-MM-DD HH:MM:SS UTC**: Fix deployed
- **YYYY-MM-DD HH:MM:SS UTC**: Services restored
- **YYYY-MM-DD HH:MM:SS UTC**: Incident closed

## Logs Summary

**Log Level Distribution:**

- ERROR: X entries
- WARN: Y entries
- INFO: Z entries

**Sample Error Logs:**

- **YYYY-MM-DD HH:MM:SS UTC**: Error message 1
- **YYYY-MM-DD HH:MM:SS UTC**: Error message 2
- **YYYY-MM-DD HH:MM:SS UTC**: Error message 3

## Engineer Notes

Notes from investigating engineers, including:
- Debugging steps taken
- Hypotheses tested
- Relevant observations

## Root Cause Analysis

### Root Cause

The primary cause of the incident. This should be specific and actionable.

Example: "Database connection pool exhaustion due to unclosed connections in the payment processing service after the v2.3.1 deployment."

### Contributing Factors

Secondary factors that enabled or amplified the incident:

- Factor 1: Description
- Factor 2: Description
- Factor 3: Description

## Resolution

Description of how the incident was resolved:

**Actions Taken:**

- Action 1: What was done to stop the immediate issue
- Action 2: How normal operation was restored
- Action 3: Any temporary mitigations applied

## Preventive Actions

Concrete actions to prevent recurrence:

- [ ] Action 1: Specific improvement with owner and timeline
- [ ] Action 2: Process or tooling enhancement
- [ ] Action 3: Documentation or training update
- [ ] Action 4: Monitoring or alerting improvements

---

## Assumptions and Notes

If any data was missing during analysis, state assumptions here:

- Assumption 1: What was assumed and why
- Assumption 2: What needs to be verified
