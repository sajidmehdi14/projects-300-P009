#!/usr/bin/env python3
"""
Unit tests for Incident Triage Classifier.
Tests classification accuracy on sample tickets.
"""

import sys
import json
from pathlib import Path

# Add parent scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from triage_ticket import IncidentTriageClassifier, TriageResult


class TestIncidentTriage:
    """Test cases for incident triage classifier."""

    @classmethod
    def setup_class(cls):
        """Initialize classifier for all tests."""
        cls.classifier = IncidentTriageClassifier()
        cls.fixtures_dir = Path(__file__).parent / "fixtures"

    def load_ticket(self, filename):
        """Load a ticket from fixtures directory."""
        filepath = self.fixtures_dir / filename
        with open(filepath, 'r') as f:
            return f.read()

    def test_p1_network_outage(self):
        """Test P1 classification for complete network outage."""
        ticket = self.load_ticket("ticket_01_p1_network.txt")
        result = self.classifier.triage(ticket)

        assert result.severity == "P1", f"Expected P1, got {result.severity}"
        assert result.category == "Network", f"Expected Network, got {result.category}"
        assert result.resolver_group == "Network Team"
        assert "users affected" in result.business_impact.lower() or "all users" in result.business_impact.lower()
        print(f"✓ P1 Network Outage: {result.severity} - {result.category} - {result.business_impact}")

    def test_p1_security_breach(self):
        """Test P1 classification for security breach."""
        ticket = self.load_ticket("ticket_02_p1_security.txt")
        result = self.classifier.triage(ticket)

        assert result.severity == "P1", f"Expected P1, got {result.severity}"
        assert result.category == "Security", f"Expected Security, got {result.category}"
        assert result.resolver_group == "Security Team"
        assert "security" in result.business_impact.lower() or "unavailable" in result.business_impact.lower()
        print(f"✓ P1 Security Breach: {result.severity} - {result.category} - {result.business_impact}")

    def test_p1_payment_system_down(self):
        """Test P1 classification for revenue-impacting outage."""
        ticket = self.load_ticket("ticket_03_p1_application.txt")
        result = self.classifier.triage(ticket)

        assert result.severity == "P1", f"Expected P1, got {result.severity}"
        assert result.category == "Application", f"Expected Application, got {result.category}"
        assert result.resolver_group == "Application Support"
        print(f"✓ P1 Payment System: {result.severity} - {result.category} - {result.business_impact}")

    def test_p2_vpn_issues(self):
        """Test P2 classification for VPN disconnections."""
        ticket = self.load_ticket("ticket_04_p2_network.txt")
        result = self.classifier.triage(ticket)

        assert result.severity in ["P2", "P1"], f"Expected P2 or P1, got {result.severity}"
        assert result.category == "Network", f"Expected Network, got {result.category}"
        assert result.resolver_group == "Network Team"
        print(f"✓ P2 VPN Issues: {result.severity} - {result.category} - {result.business_impact}")

    def test_p2_slow_crm(self):
        """Test P2 classification for performance degradation."""
        ticket = self.load_ticket("ticket_05_p2_application.txt")
        result = self.classifier.triage(ticket)

        assert result.severity in ["P2", "P3"], f"Expected P2 or P3, got {result.severity}"
        assert result.category == "Application", f"Expected Application, got {result.category}"
        assert result.resolver_group == "Application Support"
        print(f"✓ P2 Slow CRM: {result.severity} - {result.category} - {result.business_impact}")

    def test_p2_security_suspicious_login(self):
        """Test P2 classification for suspicious login attempts."""
        ticket = self.load_ticket("ticket_06_p2_security.txt")
        result = self.classifier.triage(ticket)

        assert result.severity in ["P1", "P2"], f"Expected P1 or P2, got {result.severity}"
        assert result.category == "Security", f"Expected Security, got {result.category}"
        assert result.resolver_group == "Security Team"
        print(f"✓ P2 Suspicious Logins: {result.severity} - {result.category} - {result.business_impact}")

    def test_p3_printer_issue(self):
        """Test P3 classification for printer malfunction."""
        ticket = self.load_ticket("ticket_07_p3_hardware.txt")
        result = self.classifier.triage(ticket)

        assert result.severity in ["P3", "P4"], f"Expected P3 or P4, got {result.severity}"
        assert result.category == "Hardware", f"Expected Hardware, got {result.category}"
        assert result.resolver_group == "Infrastructure Team"
        print(f"✓ P3 Printer Issue: {result.severity} - {result.category} - {result.business_impact}")

    def test_p3_report_error(self):
        """Test P3 classification for application error with workaround."""
        ticket = self.load_ticket("ticket_08_p3_application.txt")
        result = self.classifier.triage(ticket)

        assert result.severity in ["P3", "P4"], f"Expected P3 or P4, got {result.severity}"
        assert result.category == "Application", f"Expected Application, got {result.category}"
        assert result.resolver_group == "Application Support"
        print(f"✓ P3 Report Error: {result.severity} - {result.category} - {result.business_impact}")

    def test_p3_wifi_weak_signal(self):
        """Test P3 classification for localized WiFi issue."""
        ticket = self.load_ticket("ticket_09_p3_network.txt")
        result = self.classifier.triage(ticket)

        assert result.severity in ["P3", "P4"], f"Expected P3 or P4, got {result.severity}"
        assert result.category == "Network", f"Expected Network, got {result.category}"
        assert result.resolver_group == "Network Team"
        print(f"✓ P3 WiFi Issue: {result.severity} - {result.category} - {result.business_impact}")

    def test_p4_password_reset(self):
        """Test P4 classification for password reset request."""
        ticket = self.load_ticket("ticket_10_p4_access.txt")
        result = self.classifier.triage(ticket)

        assert result.severity == "P4", f"Expected P4, got {result.severity}"
        assert result.category == "Access", f"Expected Access, got {result.category}"
        assert result.resolver_group == "Service Desk"
        print(f"✓ P4 Password Reset: {result.severity} - {result.category} - {result.business_impact}")

    def test_p4_access_request(self):
        """Test P4 classification for access request."""
        ticket = self.load_ticket("ticket_11_p4_access.txt")
        result = self.classifier.triage(ticket)

        assert result.severity == "P4", f"Expected P4, got {result.severity}"
        assert result.category == "Access", f"Expected Access, got {result.category}"
        assert result.resolver_group == "Service Desk"
        print(f"✓ P4 Access Request: {result.severity} - {result.category} - {result.business_impact}")

    def test_p4_how_to_question(self):
        """Test P4 classification for informational request."""
        ticket = self.load_ticket("ticket_12_p4_other.txt")
        result = self.classifier.triage(ticket)

        assert result.severity == "P4", f"Expected P4, got {result.severity}"
        # Category could be Other or Access
        assert result.category in ["Other", "Access"], f"Expected Other or Access, got {result.category}"
        print(f"✓ P4 How-To Question: {result.severity} - {result.category} - {result.business_impact}")

    def test_json_output_format(self):
        """Test that result can be serialized to JSON."""
        ticket = self.load_ticket("ticket_01_p1_network.txt")
        result = self.classifier.triage(ticket)

        # Convert to dict and then to JSON
        from dataclasses import asdict
        result_dict = asdict(result)
        json_output = json.dumps(result_dict, indent=2)

        # Verify JSON structure
        parsed = json.loads(json_output)
        assert "severity" in parsed
        assert "category" in parsed
        assert "resolver_group" in parsed
        assert "business_impact" in parsed
        assert "confidence" in parsed
        assert "matched_keywords" in parsed
        print(f"✓ JSON Output Format: Valid")

    def test_empty_ticket_error(self):
        """Test that empty ticket raises error."""
        try:
            result = self.classifier.triage("")
            assert False, "Expected ValueError for empty ticket"
        except ValueError as e:
            assert "empty" in str(e).lower()
            print(f"✓ Empty Ticket Error: Handled correctly")


def run_tests():
    """Run all tests."""
    import pytest

    # Run pytest on this file
    test_file = Path(__file__)
    exit_code = pytest.main([str(test_file), "-v", "--tb=short"])

    return exit_code


if __name__ == "__main__":
    # If pytest is not available, run tests manually
    try:
        import pytest
        exit_code = run_tests()
        sys.exit(exit_code)
    except ImportError:
        print("pytest not found, running tests manually...\n")

        test = TestIncidentTriage()
        test.setup_class()

        tests = [
            test.test_p1_network_outage,
            test.test_p1_security_breach,
            test.test_p1_payment_system_down,
            test.test_p2_vpn_issues,
            test.test_p2_slow_crm,
            test.test_p2_security_suspicious_login,
            test.test_p3_printer_issue,
            test.test_p3_report_error,
            test.test_p3_wifi_weak_signal,
            test.test_p4_password_reset,
            test.test_p4_access_request,
            test.test_p4_how_to_question,
            test.test_json_output_format,
            test.test_empty_ticket_error,
        ]

        passed = 0
        failed = 0

        for test_func in tests:
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                print(f"✗ {test_func.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test_func.__name__}: Unexpected error: {e}")
                failed += 1

        print(f"\n{'='*60}")
        print(f"Tests run: {passed + failed}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"{'='*60}")

        sys.exit(0 if failed == 0 else 1)
