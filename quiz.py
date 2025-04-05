import datetime
import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from turtle import pd
from db import Database
from userdetails import UserInfo
from tts import speak_text
from tkinter import Tk, Label, Frame, Entry, Button, StringVar, messagebox, PhotoImage
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import pandas as pd
import os


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizBot")
        self.root.geometry("600x500")
        self.root.config(bg="#f4f4f4")

        self.db = Database()
        self.user_info = UserInfo()
        self.topics = self.get_topics()

        self.create_user_info_page()

    def create_user_info_page(self):
        """Creates the user input form with enhanced UI."""
        self.clear_window()

        # Title Label - Highlighted QuizBot Title
        Label(
            self.root, text="QuizBot", font=("Helvetica", 24, "bold"), fg="white",
            bg="#333", padx=20, pady=10
        ).pack(fill="x")

        # Frame for User Details - Adding a border
        user_frame = Frame(self.root, bg="white", padx=20, pady=20, relief="ridge", bd=3)
        user_frame.pack(pady=20, padx=30, fill="both")

        # User Details Label Inside Bordered Frame
        Label(
            user_frame, text="Enter Your Details", font=("Helvetica", 18, "bold"), fg="#333", bg="white"
        ).pack(pady=10)

        # Input Fields Frame (for better alignment)
        input_frame = Frame(user_frame, bg="white")
        input_frame.pack(pady=10)

        # Load Icons
        self.name_icon = ImageTk.PhotoImage(Image.open("assets/user.png").resize((25, 25)))
        self.email_icon = ImageTk.PhotoImage(Image.open("assets/email.png").resize((25, 25)))

        # Name Input with Icon
        name_icon_label = Label(input_frame, image=self.name_icon, bg="white")
        name_icon_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.name_entry = Entry(
            input_frame, font=("Helvetica", 14), width=28, relief="flat", highlightthickness=2,
            highlightbackground="#ccc", highlightcolor="#4CAF50", bd=0
        )
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, ipady=7)

        # Add spacing between Name and Email
        Label(input_frame, text="", bg="white").grid(row=1, column=0, pady=5)

        # Email Input with Icon
        email_icon_label = Label(input_frame, image=self.email_icon, bg="white")
        email_icon_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.email_entry = Entry(
            input_frame, font=("Helvetica", 14), width=28, relief="flat", highlightthickness=2,
            highlightbackground="#ccc", highlightcolor="#4CAF50", bd=0
        )
        self.email_entry.grid(row=2, column=1, pady=5, padx=5, ipady=7)

        # Next Button - Centered inside the frame
        next_btn = Button(
            user_frame, text="Next", command=self.create_quiz_selection_page,
            font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white",
            activebackground="#45a049", relief="raised", bd=3, padx=15, pady=5
        )
        next_btn.pack(pady=20)

    def create_quiz_selection_page(self):
        """Moves to the quiz selection page after storing user info."""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()

        if not self.user_info.store_user_data(name, email):
            return

        self.clear_window()

        # Title Label
        tk.Label(
            self.root, text="QuizBot", font=("Helvetica", 24, "bold"), fg="white",
            bg="#333", padx=20, pady=10
        ).pack(fill="x")

        # Frame for Quiz Selection
        quiz_frame = tk.Frame(self.root, bg="white", padx=20, pady=20, relief="ridge", bd=3)
        quiz_frame.pack(pady=20, padx=30, fill="both")

        # Select Quiz Label
        tk.Label(
            quiz_frame, text="Select Your Quiz", font=("Helvetica", 18, "bold"), fg="#333", bg="white"
        ).pack(pady=10)

        dropdown_frame = tk.Frame(quiz_frame, bg="white")
        dropdown_frame.pack(pady=10)

        # Load Icons
        self.book_icon = ImageTk.PhotoImage(Image.open("assets/book.png").resize((25, 25)))
        self.target_icon = ImageTk.PhotoImage(Image.open("assets/target.png").resize((25, 25)))

        # Topic Dropdown
        topic_label = tk.Label(dropdown_frame, image=self.book_icon, bg="white")
        topic_label.grid(row=0, column=0, padx=5, pady=5)

        self.topic_var = tk.StringVar(value=self.topics[0] if self.topics else "")
        topic_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.topic_var, values=self.topics, state="readonly", font=("Helvetica", 14))
        topic_dropdown.grid(row=0, column=1, pady=5, padx=5, ipady=5, sticky="ew")

        # Spacing
        tk.Label(dropdown_frame, text="", bg="white").grid(row=1, column=0, pady=5)

        # Difficulty Dropdown
        difficulty_label = tk.Label(dropdown_frame, image=self.target_icon, bg="white")
        difficulty_label.grid(row=2, column=0, padx=5, pady=5)

        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.difficulty_var, values=["Easy", "Medium", "Hard"], state="readonly", font=("Helvetica", 14))
        difficulty_dropdown.grid(row=2, column=1, pady=5, padx=5, ipady=5, sticky="ew")

        # Start Quiz Button
        start_btn = tk.Button(
            quiz_frame, text="Start Quiz", command=self.start_quiz, 
            font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white",
            activebackground="#45a049", relief="raised", bd=3, padx=15, pady=5
        )
        start_btn.pack(pady=20)

        # Hover Effects
        def on_enter(e):
            start_btn.config(bg="#45a049")

        def on_leave(e):
            start_btn.config(bg="#4CAF50")

        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

    def start_quiz(self):
        """Starts the quiz after selecting topic & difficulty."""
        self.selected_topic = self.topic_var.get()
        self.selected_difficulty = self.difficulty_var.get()

        if not self.selected_topic:
            messagebox.showwarning("Warning", "Please select a topic!")
            return

        self.questions = self.load_questions()
        if not self.questions:
            messagebox.showerror("Error", "No questions available for this selection!")
            return

        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.create_quiz_page()

    def get_topics(self):
        """Fetch available topics from the topics folder."""
        topics_folder = os.path.join(os.path.dirname(__file__), "topic")
        if not os.path.exists(topics_folder):
            messagebox.showerror("Error", "Topics folder not found!")
            return []
        return [d for d in os.listdir(topics_folder) if os.path.isdir(os.path.join(topics_folder, d))]

    def load_questions(self):
        """Load quiz questions from the selected topic and difficulty JSON file."""
        file_path = os.path.join(os.path.dirname(__file__), "topic", self.selected_topic, f"{self.selected_difficulty}.json")

        if not os.path.exists(file_path):
            return []

        with open(file_path, "r") as file:
            return json.load(file)

    def create_quiz_page(self):
        """Creates the quiz page with a timer."""
        self.clear_window()

        quiz_frame = tk.Frame(self.root, bg="white", padx=20, pady=20, relief="ridge", bd=3)
        quiz_frame.pack(pady=20, padx=30, fill="both")

        self.question_label = tk.Label(quiz_frame, text="", wraplength=500, font=("Arial", 16, "bold"), bg="white")
        self.question_label.pack(pady=10)

        # Load speaker icon
        self.speaker_icon_img = ImageTk.PhotoImage(Image.open("assets/speaker.png").resize((30, 30)))
        self.speaker_icon = tk.Button(quiz_frame, image=self.speaker_icon_img, command=self.speak_question, bg="#FFD700", bd=1, relief="solid")
        self.speaker_icon.pack(pady=5)

        self.var = tk.StringVar()
        self.options_frame = tk.Frame(quiz_frame, bg="white")
        self.options_frame.pack()
        self.options = []

        for i in range(4):
            btn = tk.Radiobutton(self.options_frame, text="", variable=self.var, value=str(i), font=("Arial", 14), bg="white", indicatoron=0, width=30, pady=5, bd=2, relief="raised")
            btn.pack(pady=5)
            self.options.append(btn)

        self.button_frame = tk.Frame(quiz_frame, bg="white")
        self.button_frame.pack()

        self.submit_btn = tk.Button(self.button_frame, text="Submit", command=self.check_answer, font=("Arial", 14), width=12, bg="#4CAF50", fg="white")
        self.submit_btn.grid(row=0, column=0, padx=10, pady=10)

        self.next_btn = tk.Button(self.button_frame, text="Next", command=self.load_question, font=("Arial", 14), width=12, bg="#008CBA", fg="white")
        self.next_btn.grid(row=0, column=1, padx=10, pady=10)
        self.next_btn.config(state=tk.DISABLED)

        # Timer label
        self.time_left = 600
        self.timer_label = tk.Label(quiz_frame, text=f"Time left: {self.time_left}s", font=("Arial", 14, "bold"), fg="red", bg="white")
        self.timer_label.pack(pady=5)

        self.load_question()
        self.update_timer()

    def update_timer(self):
        """Updates the timer every second."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time Up!", "Time is up! The quiz will now end.")
            self.show_result()

    def load_question(self):
        """Loads the next question with question number."""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            question_text = f"Question {self.current_question + 1}: {q['question']}"
            self.question_label.config(text=question_text)

            for i in range(4):
                self.options[i].config(text=q["options"][i])
                self.options[i].deselect()

            self.var.set("-1")
            self.submit_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.DISABLED)
        else:
            self.show_result()

    def check_answer(self):
        """Checks the selected answer."""
        selected = self.var.get()
        if selected == "-1":
            messagebox.showwarning("Warning", "Please select an option!")
            return

        correct_answer = self.questions[self.current_question]["answer"]
        if int(selected) == correct_answer:
            self.score += 1

        self.user_answers.append(int(selected))
        self.submit_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL)
        self.current_question += 1

    def speak_question(self):
        """Reads the current question aloud, including question number."""
        question_text = f"{self.questions[self.current_question]['question']}"
        speak_text(question_text)

    def show_result(self):
        """Displays the quiz result & saves it to DB."""
        result_text = f"Name: {self.user_info.name}\nEmail: {self.user_info.email}\n\nYour Score: {self.score}/{len(self.questions)}\n\n"
        messagebox.showinfo("Quiz Completed", result_text)

        file_path = "quiz_results.xlsx"

        # Save results to Excel
        data = {
            "Name": [self.user_info.name],
            "Email": [self.user_info.email],
            "Topic": [self.selected_topic],
            "Difficulty": [self.selected_difficulty],
            "Score": [self.score],
            "Datetime": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        df = pd.DataFrame(data)

        # Check if the file exists
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path, engine="openpyxl")  # Read existing data
            df = pd.concat([existing_df, df], ignore_index=True)  # Append new data

        # Save updated DataFrame to the same Excel file
        df.to_excel(file_path, index=False, engine="openpyxl")

        # Store quiz result in DB
        self.db.insert_quiz_result(self.user_info.name, self.user_info.email, self.selected_topic, self.selected_difficulty, self.score)
        self.root.quit()

    def clear_window(self):
        """Clears all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
