#!/usr/bin/env python3
"""
Jarvis AI Desktop Application
Simple desktop UI for agentic workflows with LangSmith monitoring.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
from pathlib import Path
import asyncio

from config.config_loader import load_config
from v2.agent.core.agent import JarvisAgentV2

# Load environment variables
def load_env():
    env_file = Path('.env')
    if env_file.exists():
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

# Load configuration profile and apply environment overrides
CONFIG = load_config()
os.environ.setdefault(
    "OLLAMA_BASE_URL",
    CONFIG.get("integrations", {}).get("ollama", {}).get("base_url", "http://localhost:11434"),
)

class JarvisDesktopApp:
    def __init__(self, root):
        self.root = root
        app_name = CONFIG.get("app_name", "Jarvis AI")
        self.root.title(f"{app_name} - Agentic Workflows")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize the agent
        self.agent = JarvisAgentV2()
        self.models = []
        
        # Create main interface
        self.create_widgets()
        
        # Configure style
        self.setup_styles()
        
        # Initialize connections
        self.check_connections()

        # Prompt for API key if missing
        self.prompt_for_api_key()
    
    def setup_styles(self):
        """Setup modern dark theme styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('TButton', background='#4a4a4a', foreground='#ffffff')
        style.map('TButton', background=[('active', '#5a5a5a')])

        # Chat history text styles
        self.chat_history.tag_configure("user", foreground="#a9d1ff", font=('Arial', 10, 'bold'))
        self.chat_history.tag_configure("agent", foreground="#ffffff", font=('Arial', 10, 'bold'))
        self.chat_history.tag_configure("agent_stream", foreground="#ffffff")
        self.chat_history.tag_configure("warning", foreground="#ffaa00")
        self.chat_history.tag_configure("error", foreground="#ff4444", font=('Arial', 10, 'italic'))
    
    def create_widgets(self):
        """Create the main UI components."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header
        header_label = ttk.Label(main_frame, text="🤖 Jarvis AI - Agentic Workflows", 
                                font=('Arial', 16, 'bold'))
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Model selection
        model_frame = ttk.Frame(main_frame)
        model_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(model_frame, text="Model:").grid(row=0, column=0, sticky=tk.W)
        self.model_selector = ttk.Combobox(model_frame, state="readonly")
        self.model_selector.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        model_frame.columnconfigure(1, weight=1)

        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, text="Initializing...", foreground='#ffaa00')
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Chat history
        self.chat_history = scrolledtext.ScrolledText(main_frame,
                                                      bg='#1e1e1e', fg='#ffffff',
                                                      font=('Arial', 10),
                                                      wrap=tk.WORD,
                                                      state='disabled')
        self.chat_history.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input frame
        input_frame = ttk.Frame(main_frame, padding=(0, 10))
        input_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)

        self.query_text = tk.Text(input_frame, height=2, bg='#3b3b3b', fg='#ffffff',
                                  insertbackground='#ffffff', font=('Arial', 10))
        self.query_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.query_text.bind("<Return>", self.run_workflow_on_enter)

        self.run_button = ttk.Button(input_frame, text="Send", command=self.run_workflow)
        self.run_button.grid(row=0, column=1, padx=(10, 0))

        # Bottom button bar
        bottom_bar = ttk.Frame(main_frame)
        bottom_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(bottom_bar, text="🔄 New Chat",
                  command=self.clear_output).pack(side=tk.LEFT)
        ttk.Button(bottom_bar, text="📊 Open LangSmith", 
                  command=self.open_langsmith).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(bottom_bar, text="⚙️ Settings",
                  command=self.open_settings_window).pack(side=tk.LEFT, padx=(10, 0))

        # Configure additional row weights
        main_frame.rowconfigure(3, weight=1)
    
    def check_connections(self):
        """Check LangSmith and Ollama connections."""
        def check():
            self.log_output("🔍 Checking connections...\n")
            
            # Test LangSmith
            langsmith_ok = self.test_langsmith()
            
            # Test Ollama
            ollama_ok = self.test_ollama()
            
            if langsmith_ok and ollama_ok:
                self.status_label.config(text="✅ All systems ready", foreground='#00ff00')
            elif langsmith_ok:
                self.status_label.config(text="⚠️ LangSmith only", foreground='#ffaa00')
            elif ollama_ok:
                self.status_label.config(text="⚠️ Ollama only", foreground='#ffaa00')
            else:
                self.status_label.config(text="❌ Connection issues", foreground='#ff4444')
        
        threading.Thread(target=check, daemon=True).start()
    
    def test_langsmith(self):
        """Test LangSmith connection."""
        try:
            from langsmith import Client
            client = Client()
            projects = list(client.list_projects(limit=1))
            self.log_output(f"✅ LangSmith: Connected ({len(projects)} projects)\n")
            return True
        except Exception as e:
            self.log_output(f"❌ LangSmith: {str(e)}\n")
            return False
    
    def test_ollama(self):
        """Test Ollama connection."""
        try:
            import requests
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.models = [m['name'] for m in response.json().get('models', [])]
                self.log_output(f"✅ Ollama: Connected ({len(self.models)} models)\n")
                self.root.after(0, self.update_model_selector)
                return True
            else:
                self.log_output("❌ Ollama: Not responding\n")
                return False
        except Exception as e:
            self.log_output(f"❌ Ollama: {str(e)}\n")
            return False
    
    def log_output(self, text, tag=None):
        """Add text to the chat history with an optional tag for styling."""
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, text, tag)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)
        self.root.update_idletasks()

    def prompt_for_api_key(self):
        """Check for LangSmith API key and prompt if missing."""
        if not os.getenv('LANGSMITH_API_KEY'):
            self.open_settings_window(prompt_message="LangSmith API Key is not set. Please enter it to enable tracing.")

    def open_settings_window(self, prompt_message=None):
        """Open a window to configure settings like API keys."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x200")
        settings_window.configure(bg='#2b2b2b')
        settings_window.transient(self.root)
        settings_window.grab_set()

        frame = ttk.Frame(settings_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        if prompt_message:
            ttk.Label(frame, text=prompt_message, foreground="#ffaa00", wraplength=380).pack(pady=(0, 10))

        ttk.Label(frame, text="LangSmith API Key:").pack(pady=(10, 5))
        
        api_key_entry = ttk.Entry(frame, width=50)
        api_key_entry.pack()
        current_key = os.getenv('LANGSMITH_API_KEY', '')
        api_key_entry.insert(0, current_key)

        def save_key():
            new_key = api_key_entry.get().strip()
            if new_key:
                # Update .env file
                env_file = Path('.env')
                lines = []
                key_found = False
                if env_file.exists():
                    with open(env_file, 'r') as f:
                        lines = f.readlines()
                
                with open(env_file, 'w') as f:
                    for line in lines:
                        if line.strip().startswith('LANGSMITH_API_KEY='):
                            f.write(f'LANGSMITH_API_KEY={new_key}\n')
                            key_found = True
                        else:
                            f.write(line)
                    if not key_found:
                        f.write(f'LANGSMITH_API_KEY={new_key}\n')
                
                os.environ['LANGSMITH_API_KEY'] = new_key
                self.log_output("✅ LangSmith API Key saved.\n")
                settings_window.destroy()
                self.check_connections() # Re-check connections
            else:
                messagebox.showwarning("Warning", "API Key cannot be empty.", parent=settings_window)

        save_button = ttk.Button(frame, text="Save", command=save_key)
        save_button.pack(pady=(10, 0))

    def update_model_selector(self):
        """Update the model selector combobox with available models."""
        if self.models:
            self.model_selector['values'] = self.models
            self.model_selector.set(self.models[0])
        else:
            self.model_selector['values'] = []
            self.model_selector.set("No models found")
    
    def clear_output(self):
        """Clear the chat history."""
        self.chat_history.config(state='normal')
        self.chat_history.delete('1.0', tk.END)
        self.chat_history.config(state='disabled')
    
    def open_langsmith(self):
        """Open LangSmith dashboard."""
        import webbrowser
        webbrowser.open('https://smith.langchain.com/')
    
    def run_workflow_on_enter(self, event):
        """Handle the Enter key press to run the workflow."""
        self.run_workflow()
        return "break"  # Prevents the default newline character

    def run_workflow(self, event=None):
        """Run the agentic workflow."""
        query = self.query_text.get('1.0', tk.END).strip()
        model = self.model_selector.get()

        if not query:
            return
        
        if not model or model == "No models found":
            messagebox.showwarning("Warning", "Please select a model!")
            return

        self.log_output(f"You: {query}\n\n", "user")
        self.query_text.delete('1.0', tk.END)

        # Disable button and start progress
        self.run_button.config(state='disabled')
        
        def workflow_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.execute_agentic_workflow(query, model))
            loop.close()

        threading.Thread(target=workflow_thread, daemon=True).start()
    
    async def execute_agentic_workflow(self, query: str, model: str):
        """Execute the agentic workflow using JarvisAgentV2 and stream results to the UI."""
        try:
            # Pass the selected model to the agent
            self.agent.llm.model = model

            # Setup environment for LangSmith tracing
            if os.getenv('LANGSMITH_API_KEY'):
                os.environ['LANGCHAIN_TRACING_V2'] = 'true'
                os.environ['LANGCHAIN_PROJECT'] = 'jarvis-ai-desktop'

            self.log_output("Jarvis: ", "agent")
            final_result = ""
            async for event in self.agent.stream_workflow(query):
                event_type = event.get("type")
                content = event.get("content")

                if event_type == "step":
                    self.status_label.config(text=f"Working: {content.capitalize()}...")
                elif event_type == "token":
                    final_result += content + " "
                    self.log_output(content + " ", "agent_stream")
                elif event_type == "hitl":
                    self.log_output(f"\n\n[USER CONFIRMATION REQUIRED]\n{content}\n\n", "warning")
                elif event_type == "done":
                    self.log_output("\n\n", "agent") # Add spacing after response

        except Exception as e:
            self.log_output(f"\n\nAn error occurred: {str(e)}\n\n", "error")
        
        finally:
            # Re-enable button and reset status in the main thread
            self.root.after(0, lambda: [
                self.run_button.config(state='normal'),
                self.check_connections() # Reset status to connection health
            ])
    
    def show_result_window(self, result):
        """Show the final result in a new window."""
        result_window = tk.Toplevel(self.root)
        result_window.title("Workflow Result")
        result_window.geometry("600x400")
        result_window.configure(bg='#2b2b2b')
        
        result_text = scrolledtext.ScrolledText(result_window, 
                                              bg='#1e1e1e', fg='#ffffff',
                                              font=('Consolas', 10),
                                              wrap=tk.WORD)
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        result_text.insert('1.0', result)
        result_text.config(state='disabled')

def main():
    """Main function to start the desktop application."""
    root = tk.Tk()
    app = JarvisDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
