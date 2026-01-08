#!/usr/bin/env python3
"""
SLA Breach Predictor

Predicts which tickets will breach SLA based on:
- Priority and associated SLA targets
- Ticket age and time to SLA breach
- Current status
- Time since last update
- Group workload (weighted by priority)

Output: Annotated JSON with breach risk (LOW/MEDIUM/HIGH), reason, and recommended action.
"""

import json
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


class SLAPredictor:
    """Predicts SLA breach risk for support tickets."""

    def __init__(self, config_path: str = None):
        """Initialize predictor with configuration."""
        self.config = self._load_config(config_path)
        self.sla_thresholds = self.config['sla_thresholds']
        self.risk_thresholds = self.config['risk_thresholds']
        self.workload_weights = self.config['workload_weights']

    def _load_config(self, config_path: str = None) -> Dict:
        """Load SLA configuration from file or use defaults."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            "sla_thresholds": {
                "P1": 4,    # hours
                "P2": 24,   # hours
                "P3": 72,   # hours
                "P4": 168   # hours (7 days)
            },
            "risk_thresholds": {
                "high": 0.75,    # >75% of SLA time consumed
                "medium": 0.50   # >50% of SLA time consumed
            },
            "workload_weights": {
                "P1": 10,
                "P2": 5,
                "P3": 2,
                "P4": 1
            },
            "workload_thresholds": {
                "high": 50,
                "medium": 30
            }
        }

    def load_tickets(self, file_path: str) -> List[Dict[str, Any]]:
        """Load tickets from JSON or CSV file."""
        file_path = Path(file_path)

        if file_path.suffix == '.json':
            with open(file_path, 'r') as f:
                return json.load(f)

        elif file_path.suffix == '.csv':
            tickets = []
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tickets.append(row)
            return tickets

        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def calculate_group_workload(self, tickets: List[Dict]) -> Dict[str, float]:
        """Calculate weighted workload score for each group."""
        workload = defaultdict(float)

        for ticket in tickets:
            group = ticket.get('assigned_group', 'Unassigned')
            priority = ticket.get('priority', 'P4')
            status = ticket.get('status', '').lower()

            # Only count open/in-progress tickets
            if status not in ['closed', 'resolved', 'cancelled']:
                weight = self.workload_weights.get(priority, 1)
                workload[group] += weight

        return dict(workload)

    def parse_datetime(self, dt_str: str) -> datetime:
        """Parse datetime string in various formats."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%f',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue

        raise ValueError(f"Unable to parse datetime: {dt_str}")

    def calculate_time_consumed(self, ticket: Dict, now: datetime) -> float:
        """Calculate percentage of SLA time consumed (0.0 to 1.0+)."""
        priority = ticket.get('priority', 'P4')
        sla_hours = self.sla_thresholds.get(priority, 168)

        # Parse created timestamp
        created_str = ticket.get('created', ticket.get('age'))
        if not created_str:
            return 0.0

        created = self.parse_datetime(created_str)
        elapsed = (now - created).total_seconds() / 3600  # hours

        return elapsed / sla_hours

    def predict_breach_risk(self, ticket: Dict, group_workload: Dict[str, float], now: datetime) -> Dict[str, Any]:
        """Predict SLA breach risk for a single ticket."""
        ticket_id = ticket.get('id', ticket.get('ticket_id', 'UNKNOWN'))
        priority = ticket.get('priority', 'P4')
        status = ticket.get('status', '').lower()
        group = ticket.get('assigned_group', 'Unassigned')

        # Skip closed tickets
        if status in ['closed', 'resolved', 'cancelled']:
            return {
                'ticket_id': ticket_id,
                'breach_risk': 'N/A',
                'reason': f'Ticket is {status}',
                'recommended_action': 'None',
                'time_consumed_pct': 0,
                'group_workload_score': 0
            }

        # Calculate time consumed
        time_consumed = self.calculate_time_consumed(ticket, now)
        time_consumed_pct = int(time_consumed * 100)

        # Get group workload
        workload_score = group_workload.get(group, 0)
        workload_level = self._classify_workload(workload_score)

        # Calculate stagnation (time since last update)
        stagnant = self._is_stagnant(ticket, now)

        # Determine breach risk
        risk_level = self._determine_risk_level(
            time_consumed,
            workload_level,
            priority,
            stagnant
        )

        # Generate reason
        reason = self._generate_reason(
            time_consumed_pct,
            priority,
            workload_level,
            workload_score,
            stagnant
        )

        # Recommend action
        action = self._recommend_action(
            risk_level,
            priority,
            workload_level,
            stagnant,
            status
        )

        return {
            'ticket_id': ticket_id,
            'priority': priority,
            'status': status,
            'assigned_group': group,
            'breach_risk': risk_level,
            'reason': reason,
            'recommended_action': action,
            'time_consumed_pct': time_consumed_pct,
            'group_workload_score': workload_score
        }

    def _classify_workload(self, workload_score: float) -> str:
        """Classify workload level."""
        if workload_score >= self.config['workload_thresholds']['high']:
            return 'HIGH'
        elif workload_score >= self.config['workload_thresholds']['medium']:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _is_stagnant(self, ticket: Dict, now: datetime) -> bool:
        """Check if ticket hasn't been updated recently."""
        last_update_str = ticket.get('last_update')
        if not last_update_str:
            return False

        try:
            last_update = self.parse_datetime(last_update_str)
            hours_since_update = (now - last_update).total_seconds() / 3600

            priority = ticket.get('priority', 'P4')
            # Stagnation threshold: 25% of SLA time
            sla_hours = self.sla_thresholds.get(priority, 168)
            stagnation_threshold = sla_hours * 0.25

            return hours_since_update > stagnation_threshold
        except:
            return False

    def _determine_risk_level(self, time_consumed: float, workload_level: str,
                             priority: str, stagnant: bool) -> str:
        """Determine breach risk level."""
        high_threshold = self.risk_thresholds['high']
        medium_threshold = self.risk_thresholds['medium']

        # Base risk on time consumed
        if time_consumed >= high_threshold:
            base_risk = 'HIGH'
        elif time_consumed >= medium_threshold:
            base_risk = 'MEDIUM'
        else:
            base_risk = 'LOW'

        # Adjust for workload
        if workload_level == 'HIGH':
            if base_risk == 'MEDIUM':
                base_risk = 'HIGH'
            elif base_risk == 'LOW':
                base_risk = 'MEDIUM'

        # Adjust for high priority tickets
        if priority in ['P1', 'P2']:
            if base_risk == 'LOW' and time_consumed >= 0.40:
                base_risk = 'MEDIUM'

        # Adjust for stagnation
        if stagnant and base_risk != 'LOW':
            base_risk = 'HIGH'

        return base_risk

    def _generate_reason(self, time_consumed_pct: int, priority: str,
                        workload_level: str, workload_score: float,
                        stagnant: bool) -> str:
        """Generate human-readable reason for risk assessment."""
        reasons = []

        reasons.append(f"{time_consumed_pct}% of SLA time consumed")

        if workload_level in ['HIGH', 'MEDIUM']:
            reasons.append(f"assigned group has {workload_level.lower()} workload (score: {workload_score:.0f})")

        if stagnant:
            reasons.append("no recent updates")

        if priority in ['P1', 'P2']:
            reasons.append(f"high priority ({priority})")

        return '; '.join(reasons)

    def _recommend_action(self, risk_level: str, priority: str,
                         workload_level: str, stagnant: bool,
                         status: str) -> str:
        """Recommend action based on risk factors."""
        if risk_level == 'LOW':
            return "Monitor"

        actions = []

        if risk_level == 'HIGH':
            actions.append("Escalate to manager")

            if priority in ['P1', 'P2']:
                actions.append("Immediate attention required")

        if workload_level == 'HIGH':
            actions.append("Consider reassigning to different group")

        if stagnant:
            actions.append("Send reminder to assignee")

        if risk_level == 'MEDIUM' and priority in ['P3', 'P4']:
            actions.append("Increase priority if possible")

        if status.lower() == 'new':
            actions.append("Assign to resolver group")

        return '; '.join(actions) if actions else "Take action to prevent breach"

    def predict_all(self, tickets: List[Dict]) -> List[Dict[str, Any]]:
        """Predict breach risk for all tickets."""
        now = datetime.now()
        group_workload = self.calculate_group_workload(tickets)

        predictions = []
        for ticket in tickets:
            prediction = self.predict_breach_risk(ticket, group_workload, now)
            predictions.append(prediction)

        return predictions


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Predict SLA breach risk for support tickets'
    )
    parser.add_argument(
        'tickets_file',
        help='Path to tickets file (JSON or CSV)'
    )
    parser.add_argument(
        '-c', '--config',
        help='Path to SLA configuration file (JSON)',
        default=None
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)',
        default=None
    )
    parser.add_argument(
        '--format',
        choices=['json', 'summary'],
        default='json',
        help='Output format (default: json)'
    )

    args = parser.parse_args()

    # Initialize predictor
    predictor = SLAPredictor(config_path=args.config)

    # Load tickets
    tickets = predictor.load_tickets(args.tickets_file)

    # Predict breach risks
    predictions = predictor.predict_all(tickets)

    # Output results
    if args.format == 'json':
        output = json.dumps(predictions, indent=2)
    else:
        # Summary format
        high_risk = [p for p in predictions if p['breach_risk'] == 'HIGH']
        medium_risk = [p for p in predictions if p['breach_risk'] == 'MEDIUM']
        low_risk = [p for p in predictions if p['breach_risk'] == 'LOW']

        output = f"""SLA Breach Risk Summary
========================
Total tickets analyzed: {len(predictions)}
High risk: {len(high_risk)}
Medium risk: {len(medium_risk)}
Low risk: {len(low_risk)}

High Risk Tickets:
"""
        for p in high_risk:
            output += f"\n  {p['ticket_id']} ({p['priority']}) - {p['reason']}\n  → {p['recommended_action']}\n"

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results written to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
