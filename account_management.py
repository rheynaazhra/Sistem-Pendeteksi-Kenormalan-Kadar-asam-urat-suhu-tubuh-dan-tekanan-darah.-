import tkinter as tk
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk
from main_menu import MainMenuWindow

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=1920, height=1080)
        
        # Load and set background image
        try:
            bg_image = Image.open("assets/user-interface/login-page.png")
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.frame.configure(bg='#f0f0f0')

        # Create login form
        self.create_login_form()

    def create_login_form(self):
        # Login form container
        form_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        form_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=450)

        # Title
        title_label = tk.Label(form_frame, text="Login", font=("Arial", 24, "bold"), bg='white')
        title_label.pack(pady=20)

        # Username
        self.username_var = tk.StringVar()
        username_label = tk.Label(form_frame, text="Username:", font=("Arial", 12), bg='white')
        username_label.pack(pady=5)
        username_entry = tk.Entry(form_frame, textvariable=self.username_var, font=("Arial", 12))
        username_entry.pack(pady=5)

        # Password
        self.password_var = tk.StringVar()
        password_label = tk.Label(form_frame, text="Password:", font=("Arial", 12), bg='white')
        password_label.pack(pady=5)
        password_entry = tk.Entry(form_frame, textvariable=self.password_var, show="*", font=("Arial", 12))
        password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(form_frame, text="Login", command=self.login, 
                               font=("Arial", 12), bg='#4CAF50', fg='white',
                               width=20, height=2)
        login_button.pack(pady=20)

        # Sign up link
        signup_button = tk.Button(form_frame, text="Don't have an account? Sign up", 
                                command=self.show_signup, font=("Arial", 10),
                                bg='white', bd=0, fg='blue')
        signup_button.pack(pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if self.validate_login(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.frame.destroy()
            MainMenuWindow(self.master, username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def validate_login(self, username, password):
        try:
            with open('database/users.json', 'r') as file:
                users = json.load(file)
                if username in users and users[username]['password'] == password:
                    return True
        except FileNotFoundError:
            return False
        return False

    def show_signup(self):
        self.frame.destroy()
        SignupWindow(self.master)

class SignupWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=1920, height=1080)
        
        # Load and set background image
        try:
            bg_image = Image.open("assets/user-interface/login-page.png")
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.frame.configure(bg='#f0f0f0')

        # Create signup form
        self.create_signup_form()

    def create_signup_form(self):
        # Signup form container
        form_frame = tk.Frame(self.frame, bg='white', relief='solid')
        form_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=600)

        # Title
        title_label = tk.Label(form_frame, text="Sign Up", font=("Arial", 24, "bold"), bg='white')
        title_label.pack(pady=20)

        # Full Name
        self.fullname_var = tk.StringVar()
        fullname_label = tk.Label(form_frame, text="Full Name:", font=("Arial", 12), bg='white')
        fullname_label.pack(pady=5)
        fullname_entry = tk.Entry(form_frame, textvariable=self.fullname_var, font=("Arial", 12))
        fullname_entry.pack(pady=5)

        # Email
        self.email_var = tk.StringVar()
        email_label = tk.Label(form_frame, text="Email:", font=("Arial", 12), bg='white')
        email_label.pack(pady=5)
        email_entry = tk.Entry(form_frame, textvariable=self.email_var, font=("Arial", 12))
        email_entry.pack(pady=5)

        # Username
        self.username_var = tk.StringVar()
        username_label = tk.Label(form_frame, text="Username:", font=("Arial", 12), bg='white')
        username_label.pack(pady=5)
        username_entry = tk.Entry(form_frame, textvariable=self.username_var, font=("Arial", 12))
        username_entry.pack(pady=5)

        # Password
        self.password_var = tk.StringVar()
        password_label = tk.Label(form_frame, text="Password:", font=("Arial", 12), bg='white')
        password_label.pack(pady=5)
        password_entry = tk.Entry(form_frame, textvariable=self.password_var, show="*", font=("Arial", 12))
        password_entry.pack(pady=5)

        # Confirm Password
        self.confirm_password_var = tk.StringVar()
        confirm_label = tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg='white')
        confirm_label.pack(pady=5)
        confirm_entry = tk.Entry(form_frame, textvariable=self.confirm_password_var, show="*", font=("Arial", 12))
        confirm_entry.pack(pady=5)

        # Sign up button
        signup_button = tk.Button(form_frame, text="Sign Up", command=self.signup,
                                font=("Arial", 12), bg='#4CAF50', fg='white',
                                width=20, height=2)
        signup_button.pack(pady=20)

        # Login link
        login_button = tk.Button(form_frame, text="Already have an account? Login",
                               command=self.show_login, font=("Arial", 10),
                               bg='white', bd=0, fg='blue')
        login_button.pack(pady=10)

    def signup(self):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        fullname = self.fullname_var.get()
        email = self.email_var.get()

        if not all([username, password, confirm_password, fullname, email]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if self.save_user(username, password, fullname, email):
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists")

    def save_user(self, username, password, fullname, email):
        users = {}
        if os.path.exists('database/users.json'):
            with open('database/users.json', 'r') as file:
                users = json.load(file)
        
        if username in users:
            return False
        
        users[username] = {
            'password': password,
            'fullname': fullname,
            'email': email
        }
        
        with open('database/users.json', 'w') as file:
            json.dump(users, file, indent=4)
        return True

    def show_login(self):
        self.frame.destroy()
        LoginWindow(self.master)