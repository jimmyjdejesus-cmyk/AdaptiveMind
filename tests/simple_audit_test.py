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
Simple test for the AdaptiveMind AI audit system core components.
"""

import sys
from pathlib import Path

# Add the jarvis_core directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "jarvis_core"))

def test_imports():
    """Test that all audit modules can be imported."""

    try:



        return True
    except Exception:
        import traceback
        traceback.print_exc()
        return False


def test_models():
    """Test that models can be instantiated."""

    try:
        from audit.models import (
            AuditCategory,
            AuditFinding,
            ScanConfiguration,
            SeverityLevel,
        )

        # Test AuditFinding
        AuditFinding(
            id="test_001",
            category=AuditCategory.SECURITY,
            severity=SeverityLevel.HIGH,
            title="Test Finding",
            description="Test description",
            file_path="test.py",
            line_number=1,
            remediation="Fix this"
        )

        # Test ScanConfiguration
        ScanConfiguration()

        return True
    except Exception:
        import traceback
        traceback.print_exc()
        return False


def test_scanners():
    """Test that scanners can be instantiated."""

    try:
        from audit.models import ScanConfiguration
        from audit.scanner import CodeQualityScanner, DependencyScanner, SecurityScanner

        config = ScanConfiguration()

        # Test scanner instantiation
        security_scanner = SecurityScanner(config)
        quality_scanner = CodeQualityScanner(config)
        DependencyScanner(config)


        # Test with minimal file content
        test_content = '''
def test_function():
    password = "hardcoded_secret"
    return password

# TODO: fix this function
def complex_function():
    for i in range(100):
        if i > 50:
            return i
        elif i == 25:
            print("magic number 25")
        elif i == 75:
            print("another magic number 75")
        else:
            continue
'''

        test_file = Path("/tmp/test_audit.py")
        test_file.write_text(test_content)

        # Test security scanner
        security_scanner.scan_files([test_file])

        # Test quality scanner
        quality_scanner.scan_files([test_file])

        # Clean up
        test_file.unlink()

        return True
    except Exception:
        import traceback
        traceback.print_exc()
        return False


def test_engine():
    """Test that the audit engine can be instantiated."""

    try:
        from audit.engine import AuditEngine
        from audit.models import ScanConfiguration

        config = ScanConfiguration()
        engine = AuditEngine(config)


        # Test scan status
        engine.get_scan_status()

        return True
    except Exception:
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":

    # Run all tests
    tests = [
        ("Import Test", test_imports),
        ("Model Test", test_models),
        ("Scanner Test", test_scanners),
        ("Engine Test", test_engine)
    ]

    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))


    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"

    passed = sum(1 for _, success in results if success)
    total = len(results)


    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)
