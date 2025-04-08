import tkinter as tk
from quiz import QuizApp


def test_quiz_app_initialization():
    root = tk.Tk()
    app = QuizApp(root)
    assert isinstance(app, QuizApp)
    root.destroy()  # Clean up the Tkinter instance
