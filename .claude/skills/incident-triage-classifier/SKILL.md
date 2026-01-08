---
name: incident-triage-classifier
description: Convert raw IT support tickets into structured triage output with priority (P1-P4), category, resolver group, and business impact. Use when analyzing support tickets, automating ticket routing, classifying incident severity for IT operations, or building ticket triage workflows. Accepts plain text tickets from email, chat, or portal submissions.
---

# Incident Triage and Priority Classifier

## Overview

Automates IT support ticket triage by analyzing raw ticket text and outputting structured classification including severity (P1-P4), category (Network, Application, Security, Hardware, Access, Other), suggested resolver group, and business impact statement. Combines deterministic keyword matching with rule-based reasoning for accurate, explainable results.

**Value proposition:** Saves IT support managers ~3 minutes per ticket by eliminating manual triage decisions.

## Quick Start

### Basic Usage

```bash
# Triage a ticket from a file
python3 scripts/triage_ticket.py path/to/ticket.txt

# Or pipe ticket content
cat ticket.txt | python3 scripts/triage_ticket.py
```

### Example Input

```
Subject: URGENT - Main Office Internet Down

The entire main office internet connection is down. All 500+ employees
cannot access any cloud services, email, or external resources. This is
blocking all work. We need immediate assistance.

Reported by: John Smith (IT Manager)
Time: 9:15 AM
```

### Example Output

```json
{
  "severity": "P1",
  "category": "Network",
  "resolver_group": "Network Team",
  "business_impact": "Service unavailable - All users affected",
  "confidence": "High",
  "matched_keywords": {
    "severity": ["down", "urgent", "entire", "cannot access"],
    "category": ["internet"]
  }
}
```

## Classification Logic

### Severity Levels (P1-P4)

**P1 - Critical:**
- Complete service outages affecting many users (100+)
- Active security breaches with data exposure
- Revenue-impacting system failures
- Keywords: down, outage, all users, ransomware, compromised, offline

**P2 - High:**
- Major functionality degraded (10-99 users)
- Performance issues affecting departments
- Security threats without confirmed breach
- Keywords: slow, degraded, intermittent, team, suspicious, urgent

**P3 - Medium:**
- Minor issues with workarounds (1-9 users)
- Localized problems
- Non-critical errors
- Keywords: minor, few users, error, issue, problem, workaround

**P4 - Low:**
- Information requests
- Password resets
- Access provisioning
- How-to questions
- Keywords: request, password, reset, access, how to, question

### Categories

- **Network:** Internet, WiFi, VPN, connectivity issues → Network Team
- **Security:** Breaches, malware, suspicious activity → Security Team
- **Application:** Software errors, performance, crashes → Application Support
- **Hardware:** Computers, printers, devices → Infrastructure Team
- **Access:** Password resets, permissions → Service Desk
- **Other:** Unclassified tickets → Service Desk

### Special Rules

1. **Information requests** (containing "how to", "question", "instructions") are always P4
2. **Hardware/Application issues with workarounds** and low user count (<10) are capped at P3
3. **Security issues with active impact** (ransomware, data loss) are elevated to P1
4. **Category tie-breaking:** Security > Hardware > Network > Application > Access > Other

## Configuration

The classifier uses `config/severity_criteria.yaml` for customizable rules.

### Customizing Severity Criteria

Edit `config/severity_criteria.yaml` to adjust:

```yaml
severity_rules:
  P1:
    keywords:
      - "down"
      - "outage"
      - "critical"
      # Add custom keywords
    user_impact:
      min_users: 100  # Adjust threshold
```

### Customizing Categories

```yaml
categories:
  Hardware:
    keywords:
      - "printer"
      - "laptop"
      # Add org-specific hardware
    resolver_group: "Infrastructure Team"
```

### Customizing Resolver Groups

```yaml
resolver_groups:
  - name: "Network Team"
    escalation_path: "Network Manager"
  # Add custom groups
```

## Testing

Run the test suite to verify classification accuracy:

```bash
cd /path/to/skill
python3 tests/test_triage.py
```

The test suite includes 12 realistic ticket samples covering all severity levels and categories.

### Test Coverage

- 3 × P1 tickets (network outage, security breach, payment system down)
- 3 × P2 tickets (VPN issues, slow CRM, suspicious logins)
- 3 × P3 tickets (printer issue, report error, WiFi issue)
- 3 × P4 tickets (password reset, access request, how-to question)

All tests validate:
- Correct severity classification
- Appropriate category assignment
- Proper resolver group routing
- JSON output format

## Integration Examples

### CLI Workflow

```bash
# Batch process tickets
for ticket in tickets/*.txt; do
  echo "Processing: $ticket"
  python3 scripts/triage_ticket.py "$ticket" >> results.jsonl
done
```

### Python Integration

```python
from scripts.triage_ticket import IncidentTriageClassifier

classifier = IncidentTriageClassifier()
ticket_text = """
VPN connection dropping for remote team...
"""

result = classifier.triage(ticket_text)
print(f"Severity: {result.severity}")
print(f"Route to: {result.resolver_group}")
print(f"Impact: {result.business_impact}")
```

### CI/CD Integration

Use JSON output for automated ticket routing:

```bash
#!/bin/bash
RESULT=$(python3 scripts/triage_ticket.py ticket.txt)
SEVERITY=$(echo $RESULT | jq -r '.severity')
GROUP=$(echo $RESULT | jq -r '.resolver_group')

if [ "$SEVERITY" == "P1" ]; then
  # Page on-call engineer
  ./page_oncall.sh "$GROUP"
fi
```

## Output Schema

The classifier outputs strict JSON with these fields:

```typescript
{
  severity: "P1" | "P2" | "P3" | "P4",
  category: "Network" | "Application" | "Security" | "Hardware" | "Access" | "Other",
  resolver_group: string,
  business_impact: string,  // One-line impact statement
  confidence: "High" | "Medium" | "Low",
  matched_keywords: {
    severity: string[],
    category: string[]
  }
}
```

## Advanced Features

### Business Impact Generation

The classifier automatically generates business impact statements:

- **Service status:** "Service unavailable", "Performance degraded", "Functionality blocked", "Minor issue"
- **User impact:** "All users affected", "N users affected", "Team/department impacted", "Individual user impacted"
- **Risk flags:** "(revenue impact)", "(security risk)" for high-priority tickets

### Confidence Scoring

Confidence reflects classification certainty:

- **High:** Strong keyword matches, clear user impact, or definitive signals
- **Medium:** Moderate keyword matches, some ambiguity
- **Low:** Weak matches, defaulted classification

### Explainability

The `matched_keywords` field shows which keywords triggered the classification, enabling auditability and refinement.

## Limitations and Best Practices

**Current limitations:**
- English language only
- Keyword-based matching (no ML)
- User count extraction limited to numeric patterns ("50 users", "30 people")
- Context-free analysis (no ticket history or relationships)

**Best practices:**
- **Customize keywords** for your organization's terminology
- **Review misclassifications** and adjust severity_criteria.yaml
- **Set appropriate user thresholds** for P1/P2 boundaries
- **Use confidence scores** to flag uncertain classifications for human review
- **Test regularly** with representative ticket samples

## Resources

### scripts/triage_ticket.py
Main classification script (320 LOC). Can be executed directly or imported as a Python module. Implements hybrid classification combining deterministic rules and analytical reasoning.

### config/severity_criteria.yaml
Configurable classification rules defining severity levels, categories, keywords, and resolver groups. Edit this file to customize the classifier for your organization.

### tests/test_triage.py
Comprehensive test suite with 14 test cases covering all severity levels, categories, and edge cases. Run before/after configuration changes to verify behavior.

### tests/fixtures/
12 realistic ticket samples for testing and development.
