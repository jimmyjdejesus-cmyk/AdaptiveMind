#!/usr/bin/env python3
"""
Debug script to test Ollama backend issues
"""

def test_ollama_endpoints():
    """Test different Ollama endpoints to identify the issue"""
    
    import requests
    
    print("🔍 Testing Ollama Backend Issues")
    print("=" * 50)
    
    # Test 1: Check if /api/generate works
    print("\n1. Testing /api/generate endpoint:")
    try:
        response = requests.post("http://localhost:11434/api/generate", 
                               json={
                                   "model": "qwen3:0.6b",
                                   "prompt": "Hello! How are you?",
                                   "stream": False,
                                   "options": {
                                       "temperature": 0.7,
                                       "num_predict": 100
                                   }
                               },
                               timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /api/generate works: {data.get('response', '')[:50]}...")
        else:
            print(f"❌ /api/generate failed: {response.text}")
    except Exception as e:
        print(f"❌ /api/generate error: {e}")
    
    # Test 2: Check if /api/chat works (we know this works)
    print("\n2. Testing /api/chat endpoint:")
    try:
        response = requests.post("http://localhost:11434/api/chat",
                               json={
                                   "model": "qwen3:0.6b",
                                   "messages": [
                                       {"role": "user", "content": "Hello! How are you?"}
                                   ],
                                   "stream": False
                               },
                               timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /api/chat works: {data.get('message', {}).get('content', '')[:50]}...")
        else:
            print(f"❌ /api/chat failed: {response.text}")
    except Exception as e:
        print(f"❌ /api/chat error: {e}")
    
    # Test 3: Test with default model "llama3"
    print("\n3. Testing with default model 'llama3':")
    try:
        response = requests.post("http://localhost:11434/api/chat",
                               json={
                                   "model": "llama3",
                                   "messages": [
                                       {"role": "user", "content": "Hello!"}
                                   ],
                                   "stream": False
                               },
                               timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ llama3 model works: {data.get('message', {}).get('content', '')[:50]}...")
        else:
            print(f"❌ llama3 model failed: {response.text}")
    except Exception as e:
        print(f"❌ llama3 model error: {e}")

def test_adaptivemind_backend():
    """Test the AdaptiveMind backend directly"""
    print("\n\n🧪 Testing AdaptiveMind Backend")
    print("=" * 50)
    
    try:
        from adaptivemind_core.llm.ollama import OllamaBackend
        
        # Test with default config
        backend = OllamaBackend(
            host="http://127.0.0.1:11434",
            model="llama3",  # Default model
            timeout=30.0
        )
        
        print(f"Backend name: {backend.name}")
        print(f"Is available: {backend.is_available()}")
        
        if backend.is_available():
            print(f"Available models: {backend.get_available_models()}")
            
            # Test generate method
            from adaptivemind_core.llm.base import GenerationRequest
            
            request = GenerationRequest(
                messages=[{"role": "user", "content": "Hello!"}],
                persona="generalist",
                context="Hello!",
                temperature=0.7,
                max_tokens=100
            )
            
            print("\nTesting generate method...")
            response = backend.generate(request)
            print(f"✅ Generation successful!")
            print(f"Content: {response.content[:50]}...")
            print(f"Tokens: {response.tokens}")
            print(f"Backend: {response.backend}")
        else:
            print("❌ Backend not available")
            
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        import traceback
        traceback.print_exc()

def main():
    test_ollama_endpoints()
    test_adaptivemind_backend()

if __name__ == "__main__":
    main()
