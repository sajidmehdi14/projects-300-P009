#!/usr/bin/env python3
"""
Root Cause Analysis (RCA) Summary Generator

Generates professional RCA reports from incident data in JSON format.
Outputs markdown-formatted reports to stdout.

Usage:
    python rca_writer.py incident.json > rca.md
    cat incident.json | python rca_writer.py - > rca.md
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class RCAGenerator:
    """Generates Root Cause Analysis reports from incident data."""

    def __init__(self, incident_data: Dict[str, Any]):
        """
        Initialize RCA generator with incident data.

        Args:
            incident_data: Dictionary containing incident information
        """
        self.data = incident_data
        self.assumptions = []

    def _get_field(self, field: str, default: Any = None, required: bool = False) -> Any:
        """
        Safely retrieve a field from incident data.

        Args:
            field: Field name to retrieve
            default: Default value if field is missing
            required: If True, adds assumption note when field is missing

        Returns:
            Field value or default
        """
        value = self.data.get(field, default)
        if required and (value is None or value == default):
            self.assumptions.append(f"Field '{field}' was not provided in incident data")
        return value

    def _format_timestamp(self, timestamp: str) -> str:
        """Format timestamp for display."""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except (ValueError, AttributeError):
            return str(timestamp) if timestamp else "Unknown time"

    def _generate_executive_summary(self) -> str:
        """Generate executive summary section."""
        lines = ["# Root Cause Analysis Report", ""]

        incident_id = self._get_field('incident_id', 'Unknown')
        title = self._get_field('title', 'Untitled Incident')
        severity = self._get_field('severity', 'Unknown')

        lines.append(f"**Incident ID:** {incident_id}")
        lines.append(f"**Title:** {title}")
        lines.append(f"**Severity:** {severity}")
        lines.append("")

        start_time = self._get_field('start_time')
        end_time = self._get_field('end_time')

        if start_time:
            lines.append(f"**Start Time:** {self._format_timestamp(start_time)}")
        if end_time:
            lines.append(f"**End Time:** {self._format_timestamp(end_time)}")
            if start_time:
                lines.append(f"**Duration:** {self._calculate_duration(start_time, end_time)}")

        lines.append("")

        affected_services = self._get_field('affected_services', [])
        if affected_services:
            lines.append(f"**Affected Services:** {', '.join(affected_services)}")
            lines.append("")

        impact = self._get_field('impact')
        if impact:
            lines.append("## Impact")
            lines.append("")
            lines.append(impact)
            lines.append("")

        return "\n".join(lines)

    def _calculate_duration(self, start: str, end: str) -> str:
        """Calculate duration between timestamps."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            duration = end_dt - start_dt

            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            if duration.days > 0:
                return f"{duration.days} days, {hours} hours, {minutes} minutes"
            elif hours > 0:
                return f"{hours} hours, {minutes} minutes"
            else:
                return f"{minutes} minutes"
        except (ValueError, AttributeError):
            return "Unable to calculate"

    def _generate_timeline(self) -> str:
        """Generate timeline section."""
        lines = ["## Timeline", ""]

        timeline = self._get_field('timeline', [])

        if not timeline:
            self.assumptions.append("No timeline data provided; incident progression is not documented")
            lines.append("*No timeline data available*")
            lines.append("")
            return "\n".join(lines)

        for event in timeline:
            timestamp = event.get('timestamp', 'Unknown time')
            description = event.get('description', 'No description')

            formatted_time = self._format_timestamp(timestamp)
            lines.append(f"- **{formatted_time}**: {description}")

        lines.append("")
        return "\n".join(lines)

    def _generate_description(self) -> str:
        """Generate incident description section."""
        lines = ["## Incident Description", ""]

        description = self._get_field('description', required=True)

        if not description:
            lines.append("*No detailed description provided*")
        else:
            lines.append(description)

        lines.append("")
        return "\n".join(lines)

    def _generate_root_cause(self) -> str:
        """Analyze and generate root cause section."""
        lines = ["## Root Cause Analysis", ""]

        # Check if root cause is explicitly provided
        root_cause = self._get_field('root_cause')

        if root_cause:
            lines.append("### Root Cause")
            lines.append("")
            lines.append(root_cause)
            lines.append("")
        else:
            # Analyze from available data
            lines.append("### Root Cause")
            lines.append("")

            description = self._get_field('description', '')
            logs = self._get_field('logs', [])
            engineer_notes = self._get_field('engineer_notes', '')

            # Attempt to extract root cause indicators
            indicators = self._extract_root_cause_indicators(description, logs, engineer_notes)

            if indicators:
                lines.append("Based on available data, the root cause appears to be:")
                lines.append("")
                for indicator in indicators:
                    lines.append(f"- {indicator}")
                lines.append("")
                self.assumptions.append("Root cause inferred from incident data; may require validation")
            else:
                lines.append("*Root cause not explicitly documented in incident data*")
                lines.append("")
                self.assumptions.append("Root cause analysis requires additional investigation")

        return "\n".join(lines)

    def _extract_root_cause_indicators(
        self,
        description: str,
        logs: List[Any],
        notes: str
    ) -> List[str]:
        """
        Extract potential root cause indicators from data.

        Returns list of observed issues/errors.
        """
        indicators = []

        # Common error patterns
        error_keywords = [
            'timeout', 'connection refused', 'out of memory', 'disk full',
            'permission denied', 'null pointer', 'deadlock', 'rate limit',
            'authentication failed', 'certificate expired', 'dns resolution'
        ]

        # Check description
        desc_lower = description.lower()
        for keyword in error_keywords:
            if keyword in desc_lower:
                indicators.append(f"Incident involved {keyword}")

        # Check logs for errors
        if logs:
            error_count = sum(1 for log in logs if isinstance(log, dict) and
                            log.get('level', '').upper() in ['ERROR', 'CRITICAL', 'FATAL'])
            if error_count > 0:
                indicators.append(f"Found {error_count} error-level log entries")

        # Check engineer notes
        if notes:
            notes_lower = notes.lower()
            for keyword in error_keywords:
                if keyword in notes_lower:
                    indicators.append(f"Engineer noted {keyword} in investigation")

        return indicators

    def _generate_contributing_factors(self) -> str:
        """Generate contributing factors section."""
        lines = ["### Contributing Factors", ""]

        contributing_factors = self._get_field('contributing_factors', [])

        if contributing_factors:
            for factor in contributing_factors:
                lines.append(f"- {factor}")
            lines.append("")
        else:
            # Try to identify from available data
            factors = self._identify_contributing_factors()

            if factors:
                for factor in factors:
                    lines.append(f"- {factor}")
                lines.append("")
                self.assumptions.append("Contributing factors inferred from incident context")
            else:
                lines.append("*No contributing factors documented*")
                lines.append("")

        return "\n".join(lines)

    def _identify_contributing_factors(self) -> List[str]:
        """Identify potential contributing factors from incident data."""
        factors = []

        # Check for deployment-related incidents
        description = self._get_field('description', '').lower()
        timeline = self._get_field('timeline', [])

        if 'deploy' in description or any('deploy' in str(e.get('description', '')).lower()
                                          for e in timeline if isinstance(e, dict)):
            factors.append("Recent deployment may have introduced changes")

        # Check for load/traffic spikes
        if 'spike' in description or 'load' in description or 'traffic' in description:
            factors.append("Traffic or load increase may have contributed")

        # Check for configuration changes
        if 'config' in description or 'configuration' in description:
            factors.append("Configuration changes may have played a role")

        # Check for dependency issues
        if 'dependency' in description or 'downstream' in description or 'upstream' in description:
            factors.append("Dependency or service interaction issues")

        return factors

    def _generate_resolution(self) -> str:
        """Generate resolution section."""
        lines = ["## Resolution", ""]

        resolution = self._get_field('resolution')

        if resolution:
            lines.append(resolution)
            lines.append("")
        else:
            # Extract from timeline or notes
            timeline = self._get_field('timeline', [])
            resolution_events = [
                e.get('description', '') for e in timeline
                if isinstance(e, dict) and any(
                    keyword in str(e.get('description', '')).lower()
                    for keyword in ['fix', 'resolve', 'restore', 'recover', 'rollback']
                )
            ]

            if resolution_events:
                lines.append("**Actions Taken:**")
                lines.append("")
                for event in resolution_events:
                    lines.append(f"- {event}")
                lines.append("")
                self.assumptions.append("Resolution steps extracted from incident timeline")
            else:
                lines.append("*Resolution steps not documented*")
                lines.append("")
                self.assumptions.append("Resolution details require documentation")

        return "\n".join(lines)

    def _generate_preventive_actions(self) -> str:
        """Generate preventive actions section."""
        lines = ["## Preventive Actions", ""]

        preventive_actions = self._get_field('preventive_actions', [])

        if preventive_actions:
            for action in preventive_actions:
                lines.append(f"- [ ] {action}")
            lines.append("")
        else:
            # Generate generic preventive actions based on incident type
            actions = self._suggest_preventive_actions()

            if actions:
                lines.append("**Recommended Actions:**")
                lines.append("")
                for action in actions:
                    lines.append(f"- [ ] {action}")
                lines.append("")
                self.assumptions.append("Preventive actions suggested based on incident patterns")
            else:
                lines.append("*No preventive actions documented*")
                lines.append("")

        return "\n".join(lines)

    def _suggest_preventive_actions(self) -> List[str]:
        """Suggest preventive actions based on incident characteristics."""
        actions = []

        description = self._get_field('description', '').lower()
        severity = self._get_field('severity', '').upper()

        # High severity incidents
        if severity in ['P0', 'P1', 'CRITICAL', 'HIGH']:
            actions.append("Conduct post-incident review with stakeholders")
            actions.append("Update runbooks with lessons learned")

        # Monitoring-related
        if 'monitor' in description or 'alert' in description:
            actions.append("Review and enhance monitoring coverage")
            actions.append("Tune alerting thresholds to reduce noise")

        # Deployment-related
        if 'deploy' in description:
            actions.append("Enhance deployment validation and testing procedures")
            actions.append("Consider implementing gradual rollout strategies")

        # Performance-related
        if any(keyword in description for keyword in ['timeout', 'slow', 'latency', 'performance']):
            actions.append("Implement performance testing in CI/CD pipeline")
            actions.append("Set up performance benchmarking and tracking")

        # Capacity-related
        if any(keyword in description for keyword in ['capacity', 'memory', 'disk', 'cpu']):
            actions.append("Review and adjust capacity planning")
            actions.append("Implement auto-scaling if not already in place")

        # Generic actions
        actions.append("Document incident in knowledge base")
        actions.append("Share findings with relevant teams")

        return actions

    def _generate_logs_summary(self) -> str:
        """Generate logs summary section."""
        lines = ["## Logs Summary", ""]

        logs = self._get_field('logs', [])

        if not logs:
            lines.append("*No logs provided*")
            lines.append("")
            return "\n".join(lines)

        # Summarize log levels
        log_levels = {}
        for log in logs:
            if isinstance(log, dict):
                level = log.get('level', 'INFO').upper()
                log_levels[level] = log_levels.get(level, 0) + 1

        if log_levels:
            lines.append("**Log Level Distribution:**")
            lines.append("")
            for level, count in sorted(log_levels.items()):
                lines.append(f"- {level}: {count} entries")
            lines.append("")

        # Show sample error logs
        error_logs = [
            log for log in logs
            if isinstance(log, dict) and log.get('level', '').upper() in ['ERROR', 'CRITICAL', 'FATAL']
        ]

        if error_logs:
            lines.append("**Sample Error Logs:**")
            lines.append("")
            for log in error_logs[:5]:  # Show first 5 errors
                timestamp = self._format_timestamp(log.get('timestamp', ''))
                message = log.get('message', 'No message')
                lines.append(f"- **{timestamp}**: {message}")

            if len(error_logs) > 5:
                lines.append(f"- *(... and {len(error_logs) - 5} more error entries)*")
            lines.append("")

        return "\n".join(lines)

    def _generate_engineer_notes(self) -> str:
        """Generate engineer notes section."""
        lines = ["## Engineer Notes", ""]

        engineer_notes = self._get_field('engineer_notes')

        if engineer_notes:
            lines.append(engineer_notes)
            lines.append("")
        else:
            lines.append("*No engineer notes provided*")
            lines.append("")

        return "\n".join(lines)

    def _generate_assumptions(self) -> str:
        """Generate assumptions section if any assumptions were made."""
        if not self.assumptions:
            return ""

        lines = ["---", "", "## Assumptions and Notes", ""]
        lines.append("The following assumptions were made during this analysis due to missing or incomplete data:")
        lines.append("")

        for assumption in self.assumptions:
            lines.append(f"- {assumption}")

        lines.append("")
        return "\n".join(lines)

    def generate_report(self) -> str:
        """
        Generate complete RCA report.

        Returns:
            Markdown-formatted RCA report
        """
        sections = [
            self._generate_executive_summary(),
            self._generate_description(),
            self._generate_timeline(),
            self._generate_logs_summary(),
            self._generate_engineer_notes(),
            self._generate_root_cause(),
            self._generate_contributing_factors(),
            self._generate_resolution(),
            self._generate_preventive_actions(),
            self._generate_assumptions(),
        ]

        return "\n".join(sections)


def load_incident_data(file_path: str) -> Dict[str, Any]:
    """
    Load incident data from JSON file or stdin.

    Args:
        file_path: Path to JSON file or '-' for stdin

    Returns:
        Parsed incident data dictionary

    Raises:
        ValueError: If JSON is invalid
        FileNotFoundError: If file doesn't exist
    """
    try:
        if file_path == '-':
            data = json.load(sys.stdin)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def main():
    """Main entry point for RCA generator."""
    if len(sys.argv) < 2:
        print("Usage: python rca_writer.py <incident.json|->", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python rca_writer.py incident.json > rca.md", file=sys.stderr)
        print("  cat incident.json | python rca_writer.py - > rca.md", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        incident_data = load_incident_data(file_path)
        generator = RCAGenerator(incident_data)
        report = generator.generate_report()
        print(report)
    except Exception as e:
        print(f"Error generating RCA report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
