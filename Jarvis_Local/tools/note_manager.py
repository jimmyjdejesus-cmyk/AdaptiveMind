# tools/note_manager.py
import os

NOTES_DIR = "notes"
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

def save_note(filename: str, content: str) -> str:
    """Saves content to a note with the given filename."""
    try:
        with open(os.path.join(NOTES_DIR, filename), "w") as f:
            f.write(content)
        return f"Successfully saved note to {filename}."
    except Exception as e:
        return f"Error saving note: {e}"