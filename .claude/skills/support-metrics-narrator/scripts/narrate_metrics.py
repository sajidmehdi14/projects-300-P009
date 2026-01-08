#!/usr/bin/env python3
"""
Support Metrics Narrator
Converts weekly support metrics into narrative management summaries.
"""

import json
import csv
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Union


def load_metrics(file_path: str) -> List[Dict[str, Any]]:
    """Load metrics from CSV or JSON file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() == '.json':
        with open(path, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]

    elif path.suffix.lower() == '.csv':
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def calculate_trend(current: Union[int, float], previous: Union[int, float]) -> Dict[str, Any]:
    """Calculate trend percentage and direction."""
    if previous == 0:
        return {"direction": "new", "percentage": 100, "change": current}

    change = current - previous
    percentage = (change / previous) * 100

    if percentage > 0:
        direction = "up"
    elif percentage < 0:
        direction = "down"
    else:
        direction = "flat"

    return {
        "direction": direction,
        "percentage": abs(percentage),
        "change": abs(change)
    }


def analyze_volume_trend(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze ticket volume trends."""
    total_tickets = sum(int(m.get('tickets', 0)) for m in metrics)

    # Get current week and previous week
    current_week = metrics[-1] if metrics else {}
    previous_week = metrics[-2] if len(metrics) > 1 else {}

    current_volume = int(current_week.get('tickets', 0))
    previous_volume = int(previous_week.get('tickets', 0))

    trend = calculate_trend(current_volume, previous_volume)

    return {
        "total": total_tickets,
        "current_week": current_volume,
        "previous_week": previous_volume,
        "trend": trend
    }


def analyze_sla_performance(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze SLA performance."""
    sla_met = sum(int(m.get('sla_met', 0)) for m in metrics)
    sla_breached = sum(int(m.get('sla_breached', 0)) for m in metrics)
    total = sla_met + sla_breached

    compliance_rate = (sla_met / total * 100) if total > 0 else 0

    # Current week performance
    current_week = metrics[-1] if metrics else {}
    current_met = int(current_week.get('sla_met', 0))
    current_breached = int(current_week.get('sla_breached', 0))
    current_total = current_met + current_breached
    current_rate = (current_met / current_total * 100) if current_total > 0 else 0

    return {
        "compliance_rate": round(compliance_rate, 1),
        "current_rate": round(current_rate, 1),
        "sla_met": sla_met,
        "sla_breached": sla_breached,
        "status": "green" if compliance_rate >= 95 else "yellow" if compliance_rate >= 90 else "red"
    }


def analyze_issue_categories(metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze top issue categories."""
    categories = {}

    for metric in metrics:
        category = metric.get('category', 'Unknown')
        count = int(metric.get('count', 1))

        if category in categories:
            categories[category] += count
        else:
            categories[category] = count

    # Sort by count descending
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

    return [
        {"category": cat, "count": count}
        for cat, count in sorted_categories[:5]
    ]


def identify_risks(metrics: List[Dict[str, Any]], sla_analysis: Dict[str, Any],
                   volume_analysis: Dict[str, Any]) -> List[str]:
    """Identify key risks based on metrics."""
    risks = []

    # SLA risk
    if sla_analysis['status'] == 'red':
        risks.append(f"SLA compliance at {sla_analysis['compliance_rate']}% - below 90% threshold")
    elif sla_analysis['status'] == 'yellow':
        risks.append(f"SLA compliance at {sla_analysis['compliance_rate']}% - approaching threshold")

    # Volume risk
    trend = volume_analysis['trend']
    if trend['direction'] == 'up' and trend['percentage'] > 20:
        risks.append(f"Ticket volume increased {trend['percentage']:.0f}% - potential capacity issue")

    # Specific category risks
    for metric in metrics:
        priority = metric.get('priority', '').lower()
        status = metric.get('status', '').lower()

        if priority == 'critical' and status == 'open':
            risks.append(f"Critical priority ticket outstanding: {metric.get('category', 'Unknown')}")

    return risks[:5]  # Top 5 risks


def generate_narrative(volume_analysis: Dict[str, Any], sla_analysis: Dict[str, Any],
                       categories: List[Dict[str, Any]], risks: List[str]) -> str:
    """Generate the narrative markdown summary."""
    output = []

    # Header
    output.append("# Weekly Support Metrics Summary")
    output.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("\n---\n")

    # Ticket Volume Trend
    output.append("## Ticket Volume Trend\n")
    volume = volume_analysis
    trend = volume['trend']

    trend_symbol = "↑" if trend['direction'] == 'up' else "↓" if trend['direction'] == 'down' else "→"
    trend_text = f"{trend_symbol} {trend['percentage']:.1f}%"

    output.append(f"- **Current Week:** {volume['current_week']} tickets")
    output.append(f"- **Previous Week:** {volume['previous_week']} tickets")
    output.append(f"- **Week-over-Week Change:** {trend_text} ({'+' if trend['direction'] == 'up' else '-'}{int(trend['change'])} tickets)")
    output.append(f"- **Period Total:** {volume['total']} tickets")

    if trend['direction'] == 'up' and trend['percentage'] > 10:
        output.append(f"\n**Action:** Volume increased significantly. Review team capacity and prioritization.")
    elif trend['direction'] == 'down' and trend['percentage'] > 10:
        output.append(f"\n**Action:** Volume decreased. Good opportunity for proactive work and technical debt.")

    # SLA Performance
    output.append("\n## SLA Performance\n")
    sla = sla_analysis

    status_emoji = "✅" if sla['status'] == 'green' else "⚠️" if sla['status'] == 'yellow' else "🔴"

    output.append(f"- **Overall Compliance:** {sla['compliance_rate']}% {status_emoji}")
    output.append(f"- **Current Week:** {sla['current_rate']}%")
    output.append(f"- **Tickets Met:** {sla['sla_met']}")
    output.append(f"- **Tickets Breached:** {sla['sla_breached']}")

    if sla['status'] != 'green':
        output.append(f"\n**Action:** SLA compliance below target. Review breach root causes and staffing levels.")
    else:
        output.append(f"\n**Status:** Meeting SLA targets. Continue monitoring.")

    # Top Issue Categories
    output.append("\n## Top Issue Categories\n")

    for i, cat in enumerate(categories, 1):
        output.append(f"{i}. **{cat['category']}** - {cat['count']} tickets")

    if categories:
        top_category = categories[0]
        output.append(f"\n**Insight:** '{top_category['category']}' represents the largest category. Consider root cause analysis or knowledge base updates.")

    # Key Risks
    output.append("\n## Key Risks\n")

    if risks:
        for risk in risks:
            output.append(f"- {risk}")
        output.append("\n**Action:** Address high-priority risks immediately. Schedule risk review with leadership.")
    else:
        output.append("- No significant risks identified this period")
        output.append("\n**Status:** Operations running smoothly. Continue current practices.")

    output.append("\n---")
    output.append("\n*This summary is auto-generated from support metrics data.*")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Convert support metrics into narrative summaries"
    )
    parser.add_argument(
        'input_file',
        help='Path to CSV or JSON metrics file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)',
        default=None
    )

    args = parser.parse_args()

    try:
        # Load metrics
        metrics = load_metrics(args.input_file)

        if not metrics:
            print("Error: No metrics found in file", file=sys.stderr)
            sys.exit(1)

        # Analyze metrics
        volume_analysis = analyze_volume_trend(metrics)
        sla_analysis = analyze_sla_performance(metrics)
        categories = analyze_issue_categories(metrics)
        risks = identify_risks(metrics, sla_analysis, volume_analysis)

        # Generate narrative
        narrative = generate_narrative(volume_analysis, sla_analysis, categories, risks)

        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(narrative)
            print(f"Summary written to: {args.output}")
        else:
            print(narrative)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
