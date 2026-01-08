#!/usr/bin/env python3
"""
Incident Triage and Priority Classifier
Converts raw IT support tickets into structured priority + routing.

Usage:
    python triage_ticket.py <ticket_file>
    cat ticket.txt | python triage_ticket.py
"""

import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class TriageResult:
    """Structured output for ticket triage."""
    severity: str  # P1, P2, P3, P4
    category: str  # Network, Application, Security, Hardware, Access, Other
    resolver_group: str
    business_impact: str  # One-line description
    confidence: str  # High, Medium, Low
    matched_keywords: Dict[str, List[str]]


class IncidentTriageClassifier:
    """Classifies IT support tickets using deterministic rules + LLM reasoning."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize classifier with configuration."""
        if config_path is None:
            # Default to config in skill directory
            script_dir = Path(__file__).parent
            config_path = script_dir.parent / "config" / "severity_criteria.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.severity_rules = self.config['severity_rules']
        self.categories = self.config['categories']

    def normalize_text(self, text: str) -> str:
        """Normalize text for keyword matching."""
        return text.lower().strip()

    def count_keyword_matches(self, text: str, keywords: List[str]) -> Tuple[int, List[str]]:
        """Count keyword matches in text."""
        text = self.normalize_text(text)
        matched = []

        for keyword in keywords:
            keyword = keyword.lower()
            # Use word boundary matching for better accuracy
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                matched.append(keyword)

        return len(matched), matched

    def classify_severity_deterministic(self, ticket_text: str) -> Dict[str, any]:
        """
        Deterministic severity classification based on keyword matching.
        Returns scores for each severity level.
        """
        scores = {}

        for severity, rules in self.severity_rules.items():
            keywords = rules.get('keywords', [])
            count, matched = self.count_keyword_matches(ticket_text, keywords)
            scores[severity] = {
                'score': count,
                'matched_keywords': matched,
                'description': rules['description']
            }

        return scores

    def classify_category_deterministic(self, ticket_text: str) -> Dict[str, any]:
        """
        Deterministic category classification based on keyword matching.
        Returns scores for each category.
        """
        scores = {}

        for category, rules in self.categories.items():
            keywords = rules.get('keywords', [])
            count, matched = self.count_keyword_matches(ticket_text, keywords)
            scores[category] = {
                'score': count,
                'matched_keywords': matched,
                'resolver_group': rules['resolver_group']
            }

        return scores

    def analyze_urgency_signals(self, ticket_text: str) -> Dict[str, any]:
        """Analyze additional urgency signals in the ticket."""
        text = self.normalize_text(ticket_text)

        # Security impact includes active threats
        has_security = bool(re.search(r'\b(breach|hack|compromised|suspicious|malware|virus|ransomware)\b', text))
        has_security_impact = bool(re.search(r'\b(encrypted|encrypting|being encrypted|files being|data loss)\b', text)) if has_security else False

        signals = {
            'has_numbers': bool(re.search(r'\d+\s*(users?|people|employees|customers)', text)),
            'has_urgency': bool(re.search(r'\b(urgent|asap|immediately|critical|emergency)\b', text)),
            # More specific impact detection - must be truly blocking
            'has_impact': bool(re.search(r'\b(cannot access|offline|down|outage|complete|entire|all users|stopped|halted)\b', text)) or has_security_impact,
            'has_security': has_security,
            'has_revenue': bool(re.search(r'\b(sales|revenue|payment|customer|production)\b', text)),
            # Detect informational/how-to requests
            'is_information_request': bool(re.search(r'\b(how to|how do i|question:|information|inquiry|instructions|help me set up)\b', text)),
            # Detect hardware with workaround (less critical)
            'has_workaround': bool(re.search(r'\b(workaround|can send to|other|alternative)\b', text))
        }

        # Extract user count if mentioned
        user_match = re.search(r'(\d+)\s*(users?|people|employees|customers)', text)
        if user_match:
            signals['user_count'] = int(user_match.group(1))
        else:
            signals['user_count'] = None

        return signals

    def determine_severity(self, ticket_text: str, severity_scores: Dict, urgency_signals: Dict) -> Tuple[str, str]:
        """
        Determine final severity using hybrid approach.
        Returns (severity, confidence).
        """
        # Special case: Information requests are always P4
        if urgency_signals.get('is_information_request', False):
            return 'P4', 'High'

        # Sort severities by score
        sorted_severities = sorted(
            severity_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )

        top_severity = sorted_severities[0][0]
        top_score = sorted_severities[0][1]['score']

        # Priority rules (in order of precedence)

        # Rule 1: Critical outages with high user impact
        if urgency_signals['has_security'] and urgency_signals['has_impact']:
            final_severity = 'P1'
            confidence = 'High'
        elif urgency_signals['user_count'] and urgency_signals['user_count'] >= 100:
            final_severity = 'P1'
            confidence = 'High'

        # Rule 2: Major issues affecting teams or with security concerns
        elif urgency_signals['has_security'] and not urgency_signals['has_impact']:
            # Security issue but no active impact (e.g., suspicious logins)
            final_severity = 'P2'
            confidence = 'High'
        elif urgency_signals['user_count'] and urgency_signals['user_count'] >= 10:
            final_severity = 'P2' if top_severity in ['P3', 'P4'] else top_severity
            confidence = 'High'
        elif urgency_signals['has_urgency'] and urgency_signals['has_impact']:
            final_severity = 'P2' if top_severity in ['P3', 'P4'] else top_severity
            confidence = 'Medium'

        # Rule 3: Use keyword-based scoring
        elif top_score >= 3:
            final_severity = top_severity
            confidence = 'High'
        elif top_score >= 1:
            final_severity = top_severity
            confidence = 'Medium'

        # Rule 4: Default fallback
        else:
            # Default to P3 if no clear match
            final_severity = 'P3'
            confidence = 'Low'

        return final_severity, confidence

    def determine_category(self, ticket_text: str, category_scores: Dict) -> Tuple[str, str, str]:
        """
        Determine final category and resolver group.
        Returns (category, resolver_group, confidence).
        """
        # Category priority for tie-breaking (higher index = higher priority)
        category_priority = {
            'Other': 0,
            'Access': 1,
            'Application': 2,
            'Network': 3,
            'Hardware': 4,
            'Security': 5
        }

        # Sort categories by score, then by priority
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: (x[1]['score'], category_priority.get(x[0], 0)),
            reverse=True
        )

        # Filter out "Other" for now
        non_other = [c for c in sorted_categories if c[0] != 'Other']

        if non_other and non_other[0][1]['score'] > 0:
            top_category = non_other[0][0]
            top_score = non_other[0][1]['score']
            resolver_group = non_other[0][1]['resolver_group']

            if top_score >= 2:
                confidence = 'High'
            else:
                confidence = 'Medium'
        else:
            # Default to Other
            top_category = 'Other'
            resolver_group = self.categories['Other']['resolver_group']
            confidence = 'Low'

        return top_category, resolver_group, confidence

    def apply_category_severity_cap(self, severity: str, category: str, urgency_signals: Dict) -> str:
        """
        Apply category-specific severity caps to prevent over-classification.
        Hardware issues with workarounds should typically be P3 max.
        Access requests should typically be P4 max unless urgent.
        """
        severity_order = ['P1', 'P2', 'P3', 'P4']

        # Hardware issues with workarounds and low user impact should be P3 max
        if category == 'Hardware':
            user_count = urgency_signals.get('user_count') or 0
            has_workaround = urgency_signals.get('has_workaround', False)
            if has_workaround and user_count < 10:
                if severity_order.index(severity) < severity_order.index('P3'):
                    return 'P3'

        # Application issues with workaround and low user count should be P3 max
        # (This catches misclassified hardware issues like printers classified as apps)
        if category == 'Application':
            user_count = urgency_signals.get('user_count') or 0
            has_workaround = urgency_signals.get('has_workaround', False)
            # If workaround exists and low user count, cap at P3
            if has_workaround and user_count < 10:
                if severity_order.index(severity) < severity_order.index('P3'):
                    return 'P3'

        # Access requests without urgency should be P4 max
        if category == 'Access':
            if not urgency_signals.get('has_urgency', False) and not urgency_signals.get('has_impact', False):
                if severity_order.index(severity) < severity_order.index('P4'):
                    return 'P4'

        return severity

    def generate_business_impact(self, ticket_text: str, severity: str, category: str, urgency_signals: Dict) -> str:
        """
        Generate a one-line business impact statement.
        This is a simple rule-based approach; could be enhanced with LLM.
        """
        text = self.normalize_text(ticket_text)

        # Extract key impact phrases
        if urgency_signals['user_count']:
            user_impact = f"{urgency_signals['user_count']} users affected"
        elif 'all users' in text or 'entire' in text:
            user_impact = "All users affected"
        elif 'team' in text or 'department' in text:
            user_impact = "Team/department impacted"
        else:
            user_impact = "Individual user impacted"

        # Determine service impact
        if 'down' in text or 'outage' in text or 'offline' in text:
            service_impact = "Service unavailable"
        elif 'slow' in text or 'degraded' in text:
            service_impact = "Performance degraded"
        elif 'cannot' in text or 'unable' in text:
            service_impact = "Functionality blocked"
        else:
            service_impact = "Minor issue"

        # Combine into business impact
        business_impact = f"{service_impact} - {user_impact}"

        # Add urgency for high-priority tickets
        if severity in ['P1', 'P2'] and (urgency_signals['has_revenue'] or urgency_signals['has_security']):
            if urgency_signals['has_revenue']:
                business_impact += " (revenue impact)"
            if urgency_signals['has_security']:
                business_impact += " (security risk)"

        return business_impact

    def triage(self, ticket_text: str) -> TriageResult:
        """
        Main triage function.
        Combines deterministic rules with analytical reasoning.
        """
        if not ticket_text or not ticket_text.strip():
            raise ValueError("Ticket text cannot be empty")

        # Step 1: Deterministic keyword matching
        severity_scores = self.classify_severity_deterministic(ticket_text)
        category_scores = self.classify_category_deterministic(ticket_text)

        # Step 2: Analyze urgency signals
        urgency_signals = self.analyze_urgency_signals(ticket_text)

        # Step 3: Determine final severity
        severity, severity_confidence = self.determine_severity(
            ticket_text, severity_scores, urgency_signals
        )

        # Step 4: Determine final category
        category, resolver_group, category_confidence = self.determine_category(
            ticket_text, category_scores
        )

        # Step 4.5: Apply category-aware severity capping
        severity = self.apply_category_severity_cap(
            severity, category, urgency_signals
        )

        # Overall confidence is minimum of severity and category confidence
        confidence_levels = {'High': 3, 'Medium': 2, 'Low': 1}
        overall_confidence = min(
            confidence_levels[severity_confidence],
            confidence_levels[category_confidence]
        )
        confidence = [k for k, v in confidence_levels.items() if v == overall_confidence][0]

        # Step 5: Generate business impact
        business_impact = self.generate_business_impact(
            ticket_text, severity, category, urgency_signals
        )

        # Collect matched keywords for transparency
        matched_keywords = {
            'severity': severity_scores[severity]['matched_keywords'],
            'category': category_scores[category]['matched_keywords']
        }

        return TriageResult(
            severity=severity,
            category=category,
            resolver_group=resolver_group,
            business_impact=business_impact,
            confidence=confidence,
            matched_keywords=matched_keywords
        )


def main():
    """CLI entry point."""
    # Read ticket text from file or stdin
    if len(sys.argv) > 1:
        ticket_file = sys.argv[1]
        with open(ticket_file, 'r') as f:
            ticket_text = f.read()
    else:
        # Read from stdin
        ticket_text = sys.stdin.read()

    if not ticket_text.strip():
        print("Error: No ticket text provided", file=sys.stderr)
        print("Usage: python triage_ticket.py <ticket_file>", file=sys.stderr)
        print("   or: cat ticket.txt | python triage_ticket.py", file=sys.stderr)
        sys.exit(1)

    # Initialize classifier
    classifier = IncidentTriageClassifier()

    # Triage the ticket
    result = classifier.triage(ticket_text)

    # Output as JSON
    output = asdict(result)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
