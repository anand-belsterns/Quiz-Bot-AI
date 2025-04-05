import json

def load_questions():
    """Loads quiz questions from JSON file."""
    with open("questions.json", "r") as file:
        return json.load(file)
