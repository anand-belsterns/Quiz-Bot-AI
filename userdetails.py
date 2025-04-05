import tkinter as tk
from tkinter import messagebox
import re
from db import Database

class UserInfo:
    def __init__(self):
        self.db = Database()
        self.name = ""
        self.email = ""

    def create_input_fields(self, root):
        """Creates user input fields with improved UI."""
        frame = tk.Frame(root, bg="#e3f2fd", padx=20, pady=20)
        frame.pack(pady=20)
        
        tk.Label(root, text="Name:", font=("Arial", 12), bg="#f4f4f4").pack()
        self.name_entry = tk.Entry(root, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        tk.Label(root, text="Email:", font=("Arial", 12), bg="#f4f4f4").pack()
        self.email_entry = tk.Entry(root, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        
        # tk.Label(frame, text="Name:", font=("Arial", 12), bg="#e3f2fd").grid(row=0, column=0, sticky="w")
        # self.name_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        # self.name_entry.grid(row=0, column=1, pady=5)

        # tk.Label(frame, text="Email:", font=("Arial", 12), bg="#e3f2fd").grid(row=1, column=0, sticky="w")
        # self.email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        # self.email_entry.grid(row=1, column=1, pady=5)

    def store_user_data(self, name, email):
        """Validates and stores user input."""
        self.name = name.strip()
        self.email = email.strip()

        # Validate empty fields
        if not all([self.name, self.email]):
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return False

        # Validate email format
        # email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # if not re.match(email_pattern, self.email):
        #     messagebox.showerror("Error", "Invalid email format! Please enter a valid email.")
        #     return False

        # Store user in DB
        self.db.insert_user(self.name, self.email)
        return True
