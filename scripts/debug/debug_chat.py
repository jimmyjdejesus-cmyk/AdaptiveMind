#!/usr/bin/env python3.11
"""
Debug script to identify the exact error in chat functionality
"""

from adaptivemind_core.config import load_config
from adaptivemind_core.app import AdaptiveMindApplication

def debug_chat():
    print("🔧 Debugging Chat Functionality...")
    print("=" * 50)
    
    try:
        # Load configuration
        config = load_config()
        print(f"✅ Configuration loaded")
        
        # Create application
        app = AdaptiveMindApplication(config=config)
        print(f"✅ Application created")
        
        # Check personas
        personas = app.personas()
        print(f"✅ Available personas: {[p['name'] for p in personas]}")
        
        # Check routing config
        routing_config = app.get_routing_config()
        print(f"✅ Routing config: {routing_config}")
        
        # Check backends
        backends = app.list_backends()
        print(f"✅ Available backends: {[b['name'] for b in backends if b['is_available']]}")
        
        # Test backend availability
        for backend in app.backends:
            available = backend.is_available()
            print(f"✅ Backend '{backend.name}' available: {available}")
            if hasattr(backend, 'get_available_models'):
                models = backend.get_available_models()
                print(f"  📋 Available models: {models}")
        
        # Try to test a simple chat
        print(f"\n🧪 Testing chat with 'generalist' persona...")
        try:
            result = app.chat(
                persona="generalist",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
                temperature=0.7,
                max_tokens=100
            )
            print(f"✅ Chat successful!")
            print(f"Response: {result}")
            
        except Exception as e:
            print(f"❌ Chat failed with error: {e}")
            import traceback
            traceback.print_exc()
        
        # Cleanup
        app.shutdown()
        print(f"✅ Application shutdown complete")
        
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_chat()
