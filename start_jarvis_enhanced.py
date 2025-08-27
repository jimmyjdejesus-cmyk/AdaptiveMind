#!/usr/bin/env python3
"""
Enhanced Jarvis AI Startup Script
Starts both backend and frontend servers for the enhanced UI system
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import websockets
        import redis
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "websockets", "redis", "pydantic"])
    
    # Check if Node.js is available
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found. Please install Node.js to run the frontend.")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js to run the frontend.")
        return False
    
    # Check if npm dependencies are installed
    frontend_path = Path("src-tauri")
    if frontend_path.exists():
        node_modules = frontend_path / "node_modules"
        if not node_modules.exists():
            print("📦 Installing Node.js dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_path)
        else:
            print("✅ Node.js dependencies found")
    
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    backend_path = Path("app")
    
    if not backend_path.exists():
        print("❌ Backend directory 'app' not found!")
        return None
    
    try:
        # Start the backend server
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=backend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ Backend server started successfully")
            print("📡 API available at: http://localhost:8000")
            print("📚 API docs available at: http://localhost:8000/docs")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the React frontend development server"""
    print("🎨 Starting React frontend development server...")
    frontend_path = Path("src-tauri")
    
    if not frontend_path.exists():
        print("❌ Frontend directory 'src-tauri' not found!")
        return None
    
    try:
        # Start the frontend server
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give it a moment to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Frontend server started successfully")
            print("🌐 Frontend available at: http://localhost:5173")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🤖 Enhanced Jarvis AI Startup Script")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing dependencies.")
        return
    
    print("\n🚀 Starting Enhanced Jarvis AI System...")
    print("=" * 50)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server. Exiting.")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend server. Stopping backend.")
        backend_process.terminate()
        return
    
    print("\n🎉 Enhanced Jarvis AI System Started Successfully!")
    print("=" * 50)
    print("🔗 Access the application:")
    print("   • Frontend UI: http://localhost:5173")
    print("   • Backend API: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    print("\n📋 Features Available:")
    print("   • 🌌 Galaxy View - Workflow visualization")
    print("   • 💬 Enhanced Chat - Customizable chat interface")
    print("   • 💀 Dead-End Shelf - Failed task management")
    print("   • 🤖 Multi-Agent Orchestration - Real-time coordination")
    print("   • ⚡ Real-time Updates - WebSocket communication")
    print("   • 📊 Performance Metrics - Live system monitoring")
    
    print("\n⌨️  Press Ctrl+C to stop all servers")
    
    # Open browser
    try:
        time.sleep(2)
        webbrowser.open("http://localhost:5173")
        print("🌐 Opening browser...")
    except:
        pass
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Enhanced Jarvis AI System...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend server stopped")
        
        print("👋 Enhanced Jarvis AI System stopped successfully!")

if __name__ == "__main__":
    main()
