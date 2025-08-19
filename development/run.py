#!/usr/bin/env python3
"""
Main entry point for Jarvis AI V2
"""

import os
import sys
from development.agent.core.agent import JarvisAgentV2
from development.config.config import DEFAULT_CONFIG

def main():
    """Initialize and run the Jarvis AI V2 system."""
    print("🚀 Starting Jarvis AI V2")
    
    # Initialize the agent
    agent = JarvisAgentV2(config=DEFAULT_CONFIG)
    
    # Set up the workflow
    agent.setup_workflow()
    
    # Example query
    result = agent.run_workflow("Help me understand LangGraph architecture")
    
    print(f"✅ Result: {result}")
    
if __name__ == "__main__":
    main()
