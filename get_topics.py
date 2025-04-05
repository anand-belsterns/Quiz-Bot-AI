import os
from tkinter import messagebox


def get_topics(self):
    """Fetch available topics from the topics folder."""
    topics_folder = os.path.join(os.path.dirname(__file__), "topic")
    if not os.path.exists(topics_folder):
        messagebox.showerror("Error", f"Topics folder not found: {topics_folder}")
        return []
    return [d for d in os.listdir(topics_folder) if os.path.isdir(os.path.join(topics_folder, d))]
