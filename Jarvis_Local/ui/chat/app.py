import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame
from threading import Thread
from orchestrator import Orchestrator
from tools.autotune import find_optimal_threshold  # Ensure this path is correct
from logger_config import log

class ChatApplication(Frame):
    """Simple Tkinter chat interface for interacting with the Meta-Agent."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("J.A.R.V.I.S. Local Console")
        self.pack(pady=10, padx=10)

        self.create_widgets()

        # Initialize the backend orchestrator
        self.orchestrator = Orchestrator()
        self.add_message("J.A.R.V.I.S.: Meta-Agent online. How can I help you?")

    def create_widgets(self):
        """Create all UI elements for the application."""
        self.chat_log = scrolledtext.ScrolledText(self, state='disabled', height=25, width=80, wrap=tk.WORD)
        self.chat_log.pack(pady=5)

        self.entry_box = Entry(self, width=80)
        self.entry_box.pack(pady=5)
        self.entry_box.bind("<Return>", self.send_message_event)

        button_frame = Frame(self)
        button_frame.pack(pady=5)

        self.send_button = Button(button_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.autotune_button = Button(button_frame, text="Auto-Tune Confidence", command=self.start_autotune)
        self.autotune_button.pack(side=tk.LEFT, padx=5)

    def start_autotune(self):
        """Launches the auto-tuner in a background thread."""
        self.add_message("J.A.R.V.I.S.: Starting auto-tuner in the background...")
        autotune_thread = Thread(target=find_optimal_threshold, args=(self.add_message,))
        autotune_thread.start()

    def send_message_event(self, event):
        """Handle Enter key press events to send messages."""
        self.send_message()

    def send_message(self):
        """Send user input to the orchestrator and display the response."""
        user_input = self.entry_box.get()
        if user_input:
            self.add_message(f"You: {user_input}")
            self.entry_box.delete(0, tk.END)

            # Disable UI while the agent is thinking
            self.toggle_ui_elements(enabled=False)

            # Run agent processing in a separate thread to keep UI responsive
            thread = Thread(target=self.get_agent_response, args=(user_input,))
            thread.start()

    def get_agent_response(self, user_input):
        """Fetch response from the orchestrator in a background thread."""
        response_text, tokens_used = self.orchestrator.handle_request(user_input)
        self.add_message(f"J.A.R.V.I.S.: {response_text} (Tokens used: {tokens_used})", re_enable_ui=True)

    def toggle_ui_elements(self, enabled=True):
        """Enables or disables UI elements to prevent interaction during processing."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.send_button.config(state=state)
        self.autotune_button.config(state=state)
        self.entry_box.config(state=state)

    def add_message(self, message, re_enable_ui=False):
        """Safely adds a message to the chat log from any thread."""
        def append():
            self.chat_log.config(state='normal')
            self.chat_log.insert(tk.END, message + "\n\n")
            self.chat_log.config(state='disabled')
            self.chat_log.yview(tk.END)

            # If this message is the final response from an agent, re-enable the UI
            if re_enable_ui:
                self.toggle_ui_elements(enabled=True)

        # This ensures the UI update happens on the main thread
        self.master.after(0, append)