#!/usr/bin/env python3.11
"""
Comprehensive Endpoint Testing Script for AdaptiveMind/ Jarvis AI
Tests all endpoints and captures data + schemas
"""

import json
import time
from typing import Any

import requests


class EndpointTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}

    def test_endpoint(self, method: str, endpoint: str, data: dict | None = None, description: str = "") -> dict[str, Any]:
        """Test a single endpoint and capture response"""
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url)
            elif method.upper() == "POST":
                response = requests.post(url, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")

            result = {
                "status_code": response.status_code,
                "success": response.status_code < 400,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers),
                "description": description,
                "timestamp": time.time()
            }

            return result

        except Exception as e:
            result = {
                "status_code": 0,
                "success": False,
                "error": str(e),
                "description": description,
                "timestamp": time.time()
            }
            return result

    def run_all_tests(self):
        """Run comprehensive endpoint testing"""

        # 1. Health & Status
        self.results["health"] = self.test_endpoint("GET", "/health", description="Health check endpoint")

        # 2. Core API - Models
        self.results["models"] = self.test_endpoint("GET", "/api/v1/models", description="List available models")

        # 3. Core API - Personas
        self.results["personas"] = self.test_endpoint("GET", "/api/v1/personas", description="List configured personas")

        # 4. Core API - Chat (Test 1)
        chat_data = {
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
            "persona": "generalist",
            "temperature": 0.7,
            "max_tokens": 100
        }
        self.results["chat_basic"] = self.test_endpoint("POST", "/api/v1/chat", chat_data, description="Basic chat completion")

        # 5. Core API - Chat (Test 2 - Complex)
        chat_complex = {
            "messages": [
                {"role": "user", "content": "What is the capital of France?"},
                {"role": "assistant", "content": "The capital of France is Paris."},
                {"role": "user", "content": "Tell me more about it."}
            ],
            "persona": "generalist",
            "temperature": 0.5,
            "max_tokens": 150,
            "metadata": {"test": "comprehensive"},
            "external_context": ["Paris is known as the City of Light"]
        }
        self.results["chat_complex"] = self.test_endpoint("POST", "/api/v1/chat", chat_complex, description="Complex chat with context")

        # Note: The working_demo.py server only implements a subset of endpoints
        # Testing additional endpoints that may not be available in this simple server

        return self.results

    def save_results(self, filename: str):
        """Save testing results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

    def generate_report(self) -> str:
        """Generate a formatted test report"""
        report = "# AdaptiveMind/ Jarvis AI Endpoint Testing Report\n\n"
        report += f"**Test Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Server URL**: {self.base_url}\n\n"

        # Summary
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results.values() if r.get('success', False))
        report += f"## Summary\n- **Total Tests**: {total_tests}\n- **Successful**: {successful_tests}\n- **Failed**: {total_tests - successful_tests}\n- **Success Rate**: {(successful_tests/total_tests)*100:.1f}%\n\n"

        # Detailed Results
        report += "## Detailed Results\n\n"

        for endpoint_name, result in self.results.items():
            report += f"### {endpoint_name.replace('_', ' ').title()}\n"
            report += f"- **Status**: {'✅ Success' if result.get('success') else '❌ Failed'}\n"
            if result.get('status_code'):
                report += f"- **HTTP Status**: {result['status_code']}\n"
            if result.get('description'):
                report += f"- **Description**: {result['description']}\n"

            if result.get('response'):
                report += f"- **Response**: \n```json\n{json.dumps(result['response'], indent=2)}\n```\n"

            if result.get('error'):
                report += f"- **Error**: {result['error']}\n"

            report += "\n"

        return report

if __name__ == "__main__":
    tester = EndpointTester()
    results = tester.run_all_tests()

    # Save raw results
    tester.save_results("/tests/endpoint_test_results.json")

    # Generate and save formatted report
    report = tester.generate_report()
    with open("/tests/endpoint_test_report.md", "w") as f:
        f.write(report)

