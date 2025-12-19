# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/




# Copyright (c) 2025 Jimmy De Jesus (Bravetto)

# Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).
# See https://creativecommons.org/licenses/by/4.0/ for license terms.

#!/usr/bin/env python3
"""
Test script for the AdaptiveMind AI audit system.

This script tests the basic functionality of the audit system.
"""

import sys
from pathlib import Path

# Add the jarvis_core directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "jarvis_core"))

from audit.engine import AuditEngine
from audit.models import ScanConfiguration, ScanDepth


def test_audit_system():
    """Test the basic audit system functionality."""

    # Create a minimal scan configuration
    config = ScanConfiguration(
        scan_depth=ScanDepth.BASIC,
        include_tests=False,
        exclude_patterns=["__pycache__", "*.pyc", ".git", "venv", ".venv"]
    )

    # Initialize the audit engine
    engine = AuditEngine(config)

    # Test the current directory
    current_dir = Path(__file__).parent

    try:
        # Run the audit
        report = engine.run_audit(current_dir)

        # Display results


        # Risk level

        # Findings by category
        if report.findings_by_category:
            for _category, findings in report.findings_by_category.items():
                if findings:
                    severity_counts = {}
                    for finding in findings:
                        severity = finding.severity.value
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1

                    for severity, _count in severity_counts.items():
                        {"CRITICAL": "🚨", "HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "INFO": "ℹ️"}.get(severity, "•")

        # Recommendations
        if report.recommendations:
            for _i, _recommendation in enumerate(report.recommendations[:5], 1):
                pass


        return True

    except Exception:
        import traceback
        traceback.print_exc()
        return False


def test_scanner_individual():
    """Test individual scanners."""

    config = ScanConfiguration()
    current_dir = Path(__file__).parent

    # Collect files to scan
    files_to_scan = []
    for file_path in current_dir.rglob("*.py"):
        if "test_audit_system.py" not in str(file_path) and "audit" not in str(file_path):
            files_to_scan.append(file_path)


    # Test security scanner
    try:
        from audit.scanner import SecurityScanner
        security_scanner = SecurityScanner(config)
        security_scanner.scan_files(files_to_scan[:5])  # Test first 5 files

        # Test code quality scanner
        from audit.scanner import CodeQualityScanner
        quality_scanner = CodeQualityScanner(config)
        quality_scanner.scan_files(files_to_scan[:5])

        # Test dependency scanner
        from audit.scanner import DependencyScanner
        dep_scanner = DependencyScanner(config)
        dep_scanner.scan_files(files_to_scan[:5])

        return True

    except Exception:
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":

    # Test the complete audit system
    audit_success = test_audit_system()

    # Test individual components
    scanner_success = test_scanner_individual()


    if audit_success and scanner_success:
        sys.exit(0)
    else:
        sys.exit(1)
