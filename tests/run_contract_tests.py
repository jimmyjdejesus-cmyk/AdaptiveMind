#!/usr/bin/env python3

# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/



"""
Contract Testing Runner

This script runs all contract tests and generates comprehensive reports.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.contract_tests.test_api_contracts import run_contract_tests
from tests.contract_tests.test_integration_contracts import run_integration_tests
from tests.contract_tests.test_performance_contracts import run_performance_tests


async def run_all_contract_tests():
    """Run all contract test suites and generate unified report."""

    test_results = {
        'api_contracts': {'status': 'pending', 'details': {}},
        'performance_contracts': {'status': 'pending', 'details': {}},
        'integration_contracts': {'status': 'pending', 'details': {}}
    }

    try:
        # Run API Contract Tests
        try:
            await run_contract_tests()
            test_results['api_contracts']['status'] = 'passed'
        except Exception as e:
            test_results['api_contracts']['status'] = 'failed'
            test_results['api_contracts']['details']['error'] = str(e)

        # Run Performance Contract Tests
        try:
            await run_performance_tests()
            test_results['performance_contracts']['status'] = 'passed'
        except Exception as e:
            test_results['performance_contracts']['status'] = 'failed'
            test_results['performance_contracts']['details']['error'] = str(e)

        # Run Integration Contract Tests
        try:
            await run_integration_tests()
            test_results['integration_contracts']['status'] = 'passed'
        except Exception as e:
            test_results['integration_contracts']['status'] = 'failed'
            test_results['integration_contracts']['details']['error'] = str(e)

    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:
        sys.exit(1)

    # Generate final summary

    passed_tests = sum(1 for result in test_results.values() if result['status'] == 'passed')
    total_tests = len(test_results)
    overall_success_rate = passed_tests / total_tests

    for _test_type, result in test_results.items():
        "✅" if result['status'] == 'passed' else "❌"
        "PASSED" if result['status'] == 'passed' else "FAILED"

        if result['status'] == 'failed' and 'error' in result['details']:
            pass


    # Save test results
    results_file = project_root / "contract_test_results.json"
    import json
    from datetime import datetime

    final_report = {
        'timestamp': datetime.now().isoformat(),
        'overall_success_rate': overall_success_rate,
        'passed_tests': passed_tests,
        'total_tests': total_tests,
        'test_results': test_results
    }

    with open(results_file, 'w') as f:
        json.dump(final_report, f, indent=2)


    # Exit with appropriate code
    if overall_success_rate < 1.0:
        total_tests - passed_tests
        sys.exit(1)
    else:
        sys.exit(0)


def main():
    """Main entry point."""
    try:
        asyncio.run(run_all_contract_tests())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
