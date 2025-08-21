"""
Tests for the Unified Jarvis Agent

This test suite covers the functionality of the new, unified JarvisAgent,
ensuring that all its capabilities (simple chat, MCP, multi-agent, etc.)
work as expected.
"""
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import pytest

import jarvis
from jarvis.core.agent import JarvisAgent

class TestUnifiedAgent(unittest.TestCase):

    def test_agent_initialization(self):
        """
        Test that the unified agent can be initialized correctly.
        """
        agent = jarvis.get_jarvis_agent()
        self.assertIsInstance(agent, JarvisAgent)

    def test_simple_mode(self):
        """
        Test that the agent can be configured to run in simple mode.
        """
        agent = jarvis.get_simple_jarvis()
        self.assertFalse(agent.enable_mcp)
        self.assertFalse(agent.enable_multi_agent)
        self.assertFalse(agent.enable_workflows)

    def test_smart_mode(self):
        """
        Test that the agent can be configured to run in smart (MCP) mode.
        """
        agent = jarvis.get_smart_jarvis()
        self.assertTrue(agent.enable_mcp)
        self.assertFalse(agent.enable_multi_agent)
        self.assertFalse(agent.enable_workflows)

    def test_super_mode(self):
        """
        Test that the agent can be configured to run in super (multi-agent) mode.
        """
        agent = jarvis.get_super_jarvis()
        self.assertTrue(agent.enable_mcp)
        self.assertTrue(agent.enable_multi_agent)
        self.assertFalse(agent.enable_workflows)

    def test_ultimate_mode(self):
        """
        Test that the agent can be configured to run in ultimate (workflow) mode.
        """
        agent = jarvis.get_ultimate_jarvis()
        self.assertTrue(agent.enable_mcp)
        self.assertTrue(agent.enable_multi_agent)
        self.assertTrue(agent.enable_workflows)

    @patch('jarvis.core.agent.JarvisAgent._simple_chat')
    def test_simple_chat(self, mock_simple_chat):
        """
        Test that the agent correctly uses the simple chat functionality.
        """
        mock_simple_chat.return_value = "This is a simple response."

        agent = jarvis.get_simple_jarvis()
        response = agent.chat("Hello, world!")

        mock_simple_chat.assert_called_once_with("Hello, world!")
        self.assertIn("This is a simple response.", response)

    @pytest.mark.asyncio
    async def test_mcp_chat(self):
        """
        Test that the agent correctly uses the MCP routing functionality.
        """
        with patch('jarvis.core.agent.JarvisAgent._execute_mcp', new_callable=AsyncMock) as mock_execute_mcp:
            mock_execute_mcp.return_value = "This is an MCP response."

            agent = jarvis.get_smart_jarvis()
            response = await agent.chat_async("Analyze this complex query.")

            mock_execute_mcp.assert_called_once_with("Analyze this complex query.")
            self.assertIn("This is an MCP response.", response)

    @pytest.mark.asyncio
    async def test_multi_agent_chat(self):
        """
        Test that the agent correctly uses the multi-agent orchestration functionality.
        """
        with patch('jarvis.core.agent.JarvisAgent._execute_multi_agent', new_callable=AsyncMock) as mock_execute_multi_agent:
            mock_execute_multi_agent.return_value = "This is a multi-agent response."

            agent = jarvis.get_super_jarvis()
            response = await agent.chat_async("Review this code for security issues.", code="print('hello')")

            mock_execute_multi_agent.assert_called_once_with("Review this code for security issues.", code="print('hello')")
            self.assertIn("This is a multi-agent response.", response)

if __name__ == '__main__':
    unittest.main()
