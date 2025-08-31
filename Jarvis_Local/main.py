"""Tkinter-based chat UI for the local J.A.R.V.I.S. Meta-Agent."""

import tkinter as tk
from ui.chat.app import ChatApplication
from logger_config import log


if __name__ == "__main__":
    log.info("Starting J.A.R.V.I.S. application...")
    root = tk.Tk()
    app = ChatApplication(master=root)
    app.mainloop()
    log.info("J.A.R.V.I.S. application closed.")
