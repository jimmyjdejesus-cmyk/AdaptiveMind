#!/usr/bin/env python3.11
"""
Debug script to check configuration loading
"""

from adaptivemind_core.config import load_config, AppConfig

def debug_config():
    print("🔧 Debugging Configuration Loading...")
    print("=" * 50)
    
    try:
        # Test direct config creation
        print("🧪 Testing direct AppConfig creation...")
        config = AppConfig()
        print(f"✅ Direct config - personas: {list(config.personas.keys())}")
        print(f"✅ Direct config - allowed_personas: {config.allowed_personas}")
        
        # Test load_config
        print("\n🧪 Testing load_config...")
        loaded_config = load_config()
        print(f"✅ Loaded config - personas: {list(loaded_config.personas.keys())}")
        print(f"✅ Loaded config - allowed_personas: {loaded_config.allowed_personas}")
        
        # Check environment variables
        import os
        print(f"\n🔧 Environment variables:")
        print(f"ADAPTIVEMIND_DEFAULT_PERSONA: {os.getenv('ADAPTIVEMIND_DEFAULT_PERSONA', 'Not set')}")
        
    except Exception as e:
        print(f"❌ Configuration debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_config()
