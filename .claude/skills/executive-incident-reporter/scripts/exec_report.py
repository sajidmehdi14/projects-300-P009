#!/usr/bin/env python3
"""
Executive Incident Reporter
Converts technical incident data into executive-friendly markdown reports.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class IncidentTranslator:
    """Translates technical incident data into business language."""

    # Technical to business term mappings
    TERM_MAP = {
        # Infrastructure
        'downtime': 'service unavailability',
        'latency': 'slow response times',
        '5xx error': 'server error',
        '500 error': 'server error',
        '503 error': 'service temporarily unavailable',
        '504 error': 'timeout',
        'timeout': 'delayed response',
        'crashed': 'stopped working',
        'failover': 'automatic backup system activation',
        'load balancer': 'traffic distribution system',

        # Database
        'database': 'data storage system',
        'query': 'data request',
        'connection pool': 'database access capacity',
        'deadlock': 'conflicting operations',
        'replication lag': 'data synchronization delay',

        # Network
        'packet loss': 'data transmission failure',
        'network partition': 'communication disruption',
        'DNS': 'address resolution system',
        'CDN': 'content delivery network',

        # Application
        'memory leak': 'resource consumption issue',
        'stack trace': 'error details',
        'exception': 'error condition',
        'thread': 'processing unit',
        'CPU': 'processing capacity',
        'disk I/O': 'storage access',

        # Security
        'DDoS': 'overwhelming traffic attack',
        'authentication': 'user verification',
        'authorization': 'access permission',
        'vulnerability': 'security weakness',
        'exploit': 'security breach attempt',
    }

    # Severity to business impact mappings
    SEVERITY_IMPACT = {
        'critical': 'Significant business disruption with customer impact',
        'high': 'Notable service degradation affecting operations',
        'medium': 'Limited impact on specific functions',
        'low': 'Minor issue with minimal business effect',
        'p1': 'Critical: Complete service outage',
        'p2': 'High: Major functionality impaired',
        'p3': 'Medium: Partial functionality affected',
        'p4': 'Low: Minor inconvenience',
    }

    @classmethod
    def translate_technical_term(cls, text: str) -> str:
        """Replace technical terms with business-friendly language."""
        result = text.lower()
        for tech_term, business_term in cls.TERM_MAP.items():
            result = result.replace(tech_term.lower(), business_term)
        return result

    @classmethod
    def extract_severity(cls, incident: Dict[str, Any]) -> str:
        """Extract and normalize severity from incident data."""
        severity_fields = ['severity', 'priority', 'level', 'impact']
        for field in severity_fields:
            if field in incident:
                return str(incident[field]).lower()
        return 'unknown'

    @classmethod
    def get_business_impact(cls, incident: Dict[str, Any]) -> str:
        """Derive business impact description from severity and incident data."""
        severity = cls.extract_severity(incident)

        # Check for explicit business impact field
        if 'business_impact' in incident:
            return incident['business_impact']

        # Use severity mapping
        for key, impact in cls.SEVERITY_IMPACT.items():
            if key in severity:
                return impact

        # Infer from affected systems/users
        affected_users = incident.get('affected_users', 0)
        if affected_users:
            if affected_users > 10000:
                return 'Wide-scale customer impact affecting service availability'
            elif affected_users > 1000:
                return 'Moderate customer impact with degraded service quality'
            else:
                return 'Limited customer impact on specific operations'

        return 'Impact assessment in progress'


class ExecutiveReportGenerator:
    """Generates executive-friendly incident reports."""

    def __init__(self, incident_data: Dict[str, Any]):
        self.data = incident_data
        self.translator = IncidentTranslator()

    def generate(self) -> str:
        """Generate complete executive report."""
        sections = [
            self._generate_header(),
            self._generate_summary(),
            self._generate_what_happened(),
            self._generate_business_impact(),
            self._generate_resolution_status(),
            self._generate_next_steps(),
            self._generate_footer()
        ]

        return '\n\n'.join(filter(None, sections))

    def _generate_header(self) -> str:
        """Generate report header with metadata."""
        incident_id = self.data.get('incident_id', 'Unknown')
        title = self.data.get('title', 'Service Incident')
        timestamp = self._format_timestamp(self.data.get('timestamp', datetime.now().isoformat()))

        return f"""# Executive Incident Report

**Incident ID:** {incident_id}
**Title:** {title}
**Report Generated:** {timestamp}"""

    def _generate_summary(self) -> str:
        """Generate executive summary."""
        severity = self.translator.extract_severity(self.data)
        status = self.data.get('status', 'investigating').title()

        duration = self._calculate_duration()

        summary = f"""## Executive Summary

**Status:** {status}
**Severity:** {severity.upper()}"""

        if duration:
            summary += f"  \n**Duration:** {duration}"

        return summary

    def _generate_what_happened(self) -> str:
        """Generate non-technical description of the incident."""
        description = self.data.get('description', '')
        error_message = self.data.get('error_message', '')
        affected_systems = self.data.get('affected_systems', [])

        # Translate technical description
        if description:
            business_desc = self.translator.translate_technical_term(description)
        elif error_message:
            business_desc = self.translator.translate_technical_term(error_message)
        else:
            business_desc = 'Service disruption occurred'

        section = f"""## What Happened

{business_desc.capitalize()}"""

        if affected_systems:
            systems_list = ', '.join(affected_systems[:3])  # Limit to 3 for brevity
            section += f"\n\n**Affected Services:** {systems_list}"

        return section

    def _generate_business_impact(self) -> str:
        """Generate business impact assessment."""
        impact = self.translator.get_business_impact(self.data)

        affected_users = self.data.get('affected_users', None)
        revenue_impact = self.data.get('revenue_impact', None)
        customer_complaints = self.data.get('customer_complaints', None)

        section = f"""## Business Impact

{impact}"""

        # Add quantifiable metrics if available
        metrics = []
        if affected_users:
            metrics.append(f"- **Users Affected:** {affected_users:,}")
        if revenue_impact:
            metrics.append(f"- **Estimated Revenue Impact:** ${revenue_impact:,.2f}")
        if customer_complaints:
            metrics.append(f"- **Customer Reports:** {customer_complaints}")

        if metrics:
            section += '\n\n' + '\n'.join(metrics)

        return section

    def _generate_resolution_status(self) -> str:
        """Generate resolution status and actions taken."""
        status = self.data.get('status', 'investigating').lower()
        resolution_time = self.data.get('resolution_time', None)
        actions_taken = self.data.get('actions_taken', [])
        root_cause = self.data.get('root_cause', None)

        # Status-based messaging
        status_messages = {
            'resolved': 'The incident has been fully resolved and services are operating normally.',
            'investigating': 'Our team is actively investigating the issue and working toward resolution.',
            'identified': 'The root cause has been identified and remediation is underway.',
            'monitoring': 'A fix has been implemented and we are monitoring for stability.',
            'mitigated': 'Immediate impacts have been reduced while we work on a complete resolution.',
        }

        status_msg = status_messages.get(status, 'Teams are actively working to resolve this incident.')

        section = f"""## Resolution Status

{status_msg}"""

        if resolution_time:
            section += f"\n\n**Resolution Time:** {self._format_timestamp(resolution_time)}"

        if root_cause:
            business_cause = self.translator.translate_technical_term(root_cause)
            section += f"\n\n**Root Cause:** {business_cause.capitalize()}"

        if actions_taken:
            section += '\n\n**Actions Taken:**'
            for action in actions_taken[:5]:  # Limit to 5 for brevity
                business_action = self.translator.translate_technical_term(action)
                section += f'\n- {business_action.capitalize()}'

        return section

    def _generate_next_steps(self) -> str:
        """Generate next steps and preventive measures."""
        next_steps = self.data.get('next_steps', [])
        preventive_measures = self.data.get('preventive_measures', [])

        section = "## Next Steps"

        if next_steps:
            section += '\n\n**Immediate Actions:**'
            for step in next_steps[:4]:  # Limit to 4 for brevity
                business_step = self.translator.translate_technical_term(step)
                section += f'\n- {business_step.capitalize()}'

        if preventive_measures:
            section += '\n\n**Preventive Measures:**'
            for measure in preventive_measures[:4]:  # Limit to 4 for brevity
                business_measure = self.translator.translate_technical_term(measure)
                section += f'\n- {business_measure.capitalize()}'

        if not next_steps and not preventive_measures:
            status = self.data.get('status', '').lower()
            if status == 'resolved':
                section += '\n\nPost-incident review will be conducted to identify improvement opportunities.'
            else:
                section += '\n\nContinued monitoring and updates will be provided as the situation evolves.'

        return section

    def _generate_footer(self) -> str:
        """Generate report footer with contact info."""
        contact = self.data.get('contact', 'incident-response@company.com')

        return f"""---

**For Questions:** {contact}
*This report is intended for executive leadership and contains business-focused information.*"""

    def _format_timestamp(self, timestamp_str: str) -> str:
        """Format ISO timestamp to readable format."""
        try:
            if isinstance(timestamp_str, datetime):
                dt = timestamp_str
            else:
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y at %I:%M %p UTC')
        except Exception:
            return str(timestamp_str)

    def _calculate_duration(self) -> Optional[str]:
        """Calculate incident duration if timestamps available."""
        start_time = self.data.get('start_time', None)
        end_time = self.data.get('end_time', self.data.get('resolution_time', None))

        if not start_time:
            return None

        try:
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))

            if end_time:
                end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            else:
                end = datetime.now()

            duration = end - start
            hours = duration.total_seconds() / 3600

            if hours < 1:
                minutes = int(duration.total_seconds() / 60)
                return f"{minutes} minutes"
            elif hours < 24:
                return f"{hours:.1f} hours"
            else:
                days = hours / 24
                return f"{days:.1f} days"
        except Exception:
            return None


def load_incident_data(file_path: str) -> Dict[str, Any]:
    """Load incident data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: exec_report.py <incident.json>", file=sys.stderr)
        print("\nExample: exec_report.py incident_data.json", file=sys.stderr)
        sys.exit(1)

    incident_file = sys.argv[1]

    # Load incident data
    incident_data = load_incident_data(incident_file)

    # Generate report
    generator = ExecutiveReportGenerator(incident_data)
    report = generator.generate()

    # Output report
    print(report)

    # Optionally save to file
    output_file = Path(incident_file).stem + '_executive_report.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Executive report saved to: {output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
