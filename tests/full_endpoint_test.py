#!/usr/bin/env python3.11
"""
Full Comprehensive Endpoint Testing Script for AdaptiveMind/ Jarvis AI
Tests ALL endpoints from the OpenAPI specification
"""

import requests
import json
import time
from typing import Dict, Any

class FullEndpointTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, description: str = "", headers: Dict = None) -> Dict[str, Any]:
        """Test a single endpoint and capture response"""
        url = f"{self.base_url}{endpoint}"
        request_headers = headers or {}
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=request_headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=request_headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = response.text
                
            result = {
                "status_code": response.status_code,
                "success": response.status_code < 400,
                "response": response_data,
                "headers": dict(response.headers),
                "description": description,
                "timestamp": time.time(),
                "method": method,
                "endpoint": endpoint
            }
            
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            return result
            
        except Exception as e:
            result = {
                "status_code": 0,
                "success": False,
                "error": str(e),
                "description": description,
                "timestamp": time.time(),
                "method": method,
                "endpoint": endpoint
            }
            print(f"❌ {method} {endpoint} - Error: {e}")
            return result
    
    def run_full_test_suite(self):
        """Run comprehensive endpoint testing for all OpenAPI endpoints"""
        print("🧪 Starting Full Comprehensive Endpoint Testing...")
        print("=" * 80)
        
        # 1. Health & Status Endpoints
        print("\n📊 Testing Health & Status Endpoints...")
        self.results["health"] = self.test_endpoint("GET", "/health", description="Health check endpoint")
        
        # 2. Core API - Models
        print("\n🤖 Testing Core API - Models...")
        self.results["models"] = self.test_endpoint("GET", "/api/v1/models", description="List available models")
        
        # 3. Core API - Personas
        print("\n🎭 Testing Core API - Personas...")
        self.results["personas"] = self.test_endpoint("GET", "/api/v1/personas", description="List configured personas")
        
        # 4. Core API - Chat (Basic)
        print("\n💬 Testing Core API - Chat (Basic)...")
        chat_data = {
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
            "persona": "generalist",
            "temperature": 0.7,
            "max_tokens": 100
        }
        self.results["chat_basic"] = self.test_endpoint("POST", "/api/v1/chat", chat_data, description="Basic chat completion")
        
        # 5. Core API - Chat (Complex)
        print("\n💬 Testing Core API - Chat (Complex)...")
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
        
        # 6. Monitoring Endpoints
        print("\n📈 Testing Monitoring Endpoints...")
        self.results["monitoring_metrics"] = self.test_endpoint("GET", "/api/v1/monitoring/metrics", description="Get metrics history")
        self.results["monitoring_traces"] = self.test_endpoint("GET", "/api/v1/monitoring/traces", description="Get request traces")
        
        # 7. Management API - System
        print("\n⚙️  Testing Management API - System...")
        self.results["system_status"] = self.test_endpoint("GET", "/api/v1/management/system/status", description="Get system status")
        
        # 8. Management API - Routing
        print("\n🎯 Testing Management API - Routing...")
        self.results["routing_config_get"] = self.test_endpoint("GET", "/api/v1/management/routing/config", description="Get routing configuration")
        
        # Test routing config update
        routing_update_data = {
            "allowed_personas": ["generalist", "test-persona"],
            "enable_adaptive_routing": True
        }
        self.results["routing_config_put"] = self.test_endpoint("PUT", "/api/v1/management/config/routing", routing_update_data, description="Update routing configuration")
        
        # 9. Management API - Backends
        print("\n🔧 Testing Management API - Backends...")
        self.results["backends_list"] = self.test_endpoint("GET", "/api/v1/management/backends", description="List backends")
        self.results["backend_test"] = self.test_endpoint("POST", "/api/v1/management/backends/ollama/test", description="Test backend connectivity")
        
        # 10. Management API - Context
        print("\n📚 Testing Management API - Context...")
        self.results["context_config_get"] = self.test_endpoint("GET", "/api/v1/management/context/config", description="Get context configuration")
        
        context_update_data = {
            "enable_semantic_chunking": True,
            "max_combined_context_tokens": 8192
        }
        self.results["context_config_put"] = self.test_endpoint("PUT", "/api/v1/management/config/context", context_update_data, description="Update context configuration")
        
        # 11. Management API - Security
        print("\n🔒 Testing Management API - Security...")
        self.results["security_status"] = self.test_endpoint("GET", "/api/v1/management/security/status", description="Get security status")
        
        # 12. Management API - Personas CRUD
        print("\n👤 Testing Management API - Personas CRUD...")
        
        # Create persona
        persona_create_data = {
            "name": "test-persona",
            "description": "Test persona for endpoint testing",
            "system_prompt": "You are a helpful test assistant.",
            "max_context_window": 2048,
            "routing_hint": "test"
        }
        self.results["persona_create"] = self.test_endpoint("POST", "/api/v1/management/personas", persona_create_data, description="Create new persona")
        
        # Update persona
        persona_update_data = {
            "description": "Updated test persona description",
            "system_prompt": "You are a helpful test assistant with updated instructions."
        }
        self.results["persona_update"] = self.test_endpoint("PUT", "/api/v1/management/personas/test-persona", persona_update_data, description="Update persona")
        
        # 13. OpenAI-Compatible Endpoints
        print("\n🤝 Testing OpenAI-Compatible Endpoints...")
        openai_chat_data = {
            "model": "generalist",
            "messages": [{"role": "user", "content": "Hello from OpenAI-compatible API!"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        self.results["openai_chat"] = self.test_endpoint("POST", "/v1/chat/completions", openai_chat_data, description="OpenAI-compatible chat completions")
        self.results["openai_models"] = self.test_endpoint("GET", "/v1/models", description="OpenAI-compatible models list")
        
        # 14. Configuration Management
        print("\n💾 Testing Configuration Management...")
        self.results["config_save"] = self.test_endpoint("POST", "/api/v1/management/config/save", description="Save configuration")
        
        # 15. Persona Deletion (cleanup)
        print("\n🗑️  Testing Persona Deletion...")
        self.results["persona_delete"] = self.test_endpoint("DELETE", "/api/v1/management/personas/test-persona", description="Delete test persona")
        
        return self.results
    
    def save_results(self, filename: str):
        """Save testing results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Results saved to {filename}")
    
    def generate_full_report(self) -> str:
        """Generate a comprehensive formatted test report"""
        report = "# AdaptiveMind/ Jarvis AI Full Endpoint Testing Report\n\n"
        report += f"**Test Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Server URL**: {self.base_url}\n"
        report += f"**OpenAPI Specification**: Complete endpoint coverage\n\n"
        
        # Summary
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results.values() if r.get('success', False))
        report += f"## Summary\n- **Total Tests**: {total_tests}\n- **Successful**: {successful_tests}\n- **Failed**: {total_tests - successful_tests}\n- **Success Rate**: {(successful_tests/total_tests)*100:.1f}%\n\n"
        
        # Group by categories
        categories = {
            "Health & Status": ["health"],
            "Core API": ["models", "personas", "chat_basic", "chat_complex"],
            "Monitoring": ["monitoring_metrics", "monitoring_traces"],
            "Management - System": ["system_status"],
            "Management - Routing": ["routing_config_get", "routing_config_put"],
            "Management - Backends": ["backends_list", "backend_test"],
            "Management - Context": ["context_config_get", "context_config_put"],
            "Management - Security": ["security_status"],
            "Management - Personas CRUD": ["persona_create", "persona_update", "persona_delete"],
            "OpenAI-Compatible": ["openai_chat", "openai_models"],
            "Configuration": ["config_save"]
        }
        
        for category, endpoints in categories.items():
            report += f"## {category}\n"
            category_success = 0
            category_total = len([e for e in endpoints if e in self.results])
            
            for endpoint_name in endpoints:
                if endpoint_name in self.results:
                    result = self.results[endpoint_name]
                    status_icon = "✅" if result.get('success') else "❌"
                    report += f"- **{endpoint_name.replace('_', ' ').title()}**: {status_icon}\n"
                    if result.get('success'):
                        category_success += 1
                        
                    # Add response details for successful requests
                    if result.get('success') and result.get('response'):
                        report += f"  - Response Preview: `{str(result['response'])[:100]}{'...' if len(str(result['response'])) > 100 else ''}`\n"
            
            if category_total > 0:
                category_rate = (category_success / category_total) * 100
                report += f"  - **Category Success Rate**: {category_rate:.1f}%\n"
            report += "\n"
        
        # Detailed Results
        report += "## Detailed Results\n\n"
        
        for endpoint_name, result in self.results.items():
            report += f"### {endpoint_name.replace('_', ' ').title()}\n"
            report += f"- **Status**: {'✅ Success' if result.get('success') else '❌ Failed'}\n"
            report += f"- **Method**: {result.get('method', 'N/A')}\n"
            report += f"- **Endpoint**: {result.get('endpoint', 'N/A')}\n"
            if result.get('status_code'):
                report += f"- **HTTP Status**: {result['status_code']}\n"
            if result.get('description'):
                report += f"- **Description**: {result['description']}\n"
            
            if result.get('response'):
                report += f"- **Response**: \n```json\n{json.dumps(result['response'], indent=2, default=str)}\n```\n"
            
            if result.get('error'):
                report += f"- **Error**: {result['error']}\n"
                
            report += "\n"
        
        # Schema Analysis
        report += "## Response Schema Analysis\n\n"
        successful_responses = [r for r in self.results.values() if r.get('success') and r.get('response')]
        
        if successful_responses:
            report += "### Successful Response Schemas\n\n"
            for i, result in enumerate(successful_responses[:5], 1):  # Show first 5
                endpoint = result.get('endpoint', 'Unknown')
                response = result.get('response', {})
                report += f"#### {i}. {endpoint}\n"
                if isinstance(response, dict):
                    report += f"```json\n{json.dumps(response, indent=2, default=str)}\n```\n\n"
                else:
                    report += f"**Response**: {response}\n\n"
        
        return report

if __name__ == "__main__":
    tester = FullEndpointTester()
    results = tester.run_full_test_suite()
    
    # Save raw results
    tester.save_results("/tests/full_endpoint_test_results.json")
    
    # Generate and save formatted report
    report = tester.generate_full_report()
    with open("/tests/full_endpoint_test_report.md", "w") as f:
        f.write(report)
    
    print("\n" + "=" * 80)
    print("🎉 Full Endpoint Testing Complete!")
    print(f"📄 Full Report saved to: /tests/full_endpoint_test_report.md")
    print("=" * 80)
