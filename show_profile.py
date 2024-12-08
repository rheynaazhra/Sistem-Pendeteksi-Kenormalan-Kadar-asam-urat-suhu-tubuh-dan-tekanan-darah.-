import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

class ProfileWindow:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=1920, height=1080)
        
        # Load and set background image
        try:
            bg_image = Image.open("assets/user-interface/background.png")
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.frame.configure(bg='#f0f0f0')

        self.load_user_data()
        self.create_profile_view()

    def load_user_data(self):
        try:
            with open('database/users.json', 'r') as file:
                users = json.load(file)
                self.user_data = users.get(self.username, {})
        except FileNotFoundError:
            messagebox.showerror("Error", "User data not found!")
            self.back_to_menu()

    def create_profile_view(self):
        # Profile Container
        profile_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        profile_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=500)

        # Title
        title_label = tk.Label(profile_frame, 
                             text="User Profile",
                             font=("Arial", 24, "bold"),
                             bg='white')
        title_label.pack(pady=20)

        # User Information
        info_frame = tk.Frame(profile_frame, bg='white')
        info_frame.pack(fill='x', padx=40)

        # Full Name
        name_label = tk.Label(info_frame,
                            text=f"Full Name: {self.user_data.get('fullname', 'N/A')}",
                            font=("Arial", 14),
                            bg='white',
                            anchor='w')
        name_label.pack(fill='x', pady=10)

        # Email
        email_label = tk.Label(info_frame,
                             text=f"Email: {self.user_data.get('email', 'N/A')}",
                             font=("Arial", 14),
                             bg='white',
                             anchor='w')
        email_label.pack(fill='x', pady=10)

        # Username
        username_label = tk.Label(info_frame,
                                text=f"Username: {self.username}",
                                font=("Arial", 14),
                                bg='white',
                                anchor='w')
        username_label.pack(fill='x', pady=10)

        # Password Frame
        password_frame = tk.Frame(info_frame, bg='white')
        password_frame.pack(fill='x', pady=10)

        self.password_var = tk.StringVar()
        self.password_var.set("●" * len(self.user_data.get('password', '')))

        password_label = tk.Label(password_frame,
                                text="Password: ",
                                font=("Arial", 14),
                                bg='white')
        password_label.pack(side=tk.LEFT)

        self.password_display = tk.Label(password_frame,
                                       textvariable=self.password_var,
                                       font=("Arial", 14),
                                       bg='white')
        self.password_display.pack(side=tk.LEFT)

        self.show_password_btn = tk.Button(password_frame,
                                         text="Show",
                                         command=self.toggle_password,
                                         font=("Arial", 10),
                                         bg='#4CAF50',
                                         fg='white')
        self.show_password_btn.pack(side=tk.LEFT, padx=10)

        # Back Button
        back_btn = tk.Button(profile_frame,
                           text="Back to Menu",
                           command=self.back_to_menu,
                           font=("Arial", 12, "bold"),
                           bg='#2196F3',
                           fg='white',
                           width=15,
                           height=2)
        back_btn.pack(pady=30)

    def toggle_password(self):
        if self.password_var.get().startswith('●'):
            self.password_var.set(self.user_data.get('password', ''))
            self.show_password_btn.config(text="Hide")
        else:
            self.password_var.set("●" * len(self.user_data.get('password', '')))
            self.show_password_btn.config(text="Show")

    def back_to_menu(self):
        self.frame.destroy()
        from main_menu import MainMenuWindow
        MainMenuWindow(self.master, self.username)