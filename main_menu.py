import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MainMenuWindow:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=1920, height=1080)
        
        try:
            bg_image = Image.open("assets/user-interface/background.png")
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.frame.configure(bg='#f0f0f0')

        self.create_main_menu()

    def create_main_menu(self):
        # Welcome Title
        welcome_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        welcome_frame.place(relx=0.505, rely=0.1, anchor='n', width=590, height=100)
        
        welcome_label = tk.Label(welcome_frame, 
                               text=f"Welcome, {self.username}!",
                               font=("Arial", 24, "bold"),
                               bg='white')
        welcome_label.pack(pady=25)

        # Main Buttons Container
        buttons_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        buttons_frame.place(relx=0.505, rely=0.3, anchor='n', width=590, height=400)

        # Health Test Button
        health_test_btn = tk.Button(buttons_frame,
                                  text="Health Test",
                                  font=("Arial", 16, "bold"),
                                  bg='#4CAF50',
                                  fg='white',
                                  width=20,
                                  height=2,
                                  command=self.health_test)
        health_test_btn.pack(pady=30)

        # Medicine Purchase Button
        medicine_btn = tk.Button(buttons_frame,
                               text="Purchase Medicine",
                               font=("Arial", 16, "bold"),
                               bg='#2196F3',
                               fg='white',
                               width=20,
                               height=2,
                               command=self.purchase_medicine)
        medicine_btn.pack(pady=30)

        # Bottom Right Buttons Frame
        bottom_frame = tk.Frame(self.frame)
        bottom_frame.place(x=1620, y=980)

        # Profile Button
        profile_btn = tk.Button(bottom_frame,
                              text="Profile",
                              font=("Arial", 12, "bold"),
                              bg='#FFA500',
                              fg='white',
                              width=10,
                              height=2,
                              command=self.show_profile)
        profile_btn.pack(side=tk.LEFT, padx=5)

        # Logout Button
        logout_btn = tk.Button(bottom_frame,
                             text="Logout",
                             font=("Arial", 12, "bold"),
                             bg='#FF0000',
                             fg='white',
                             width=10,
                             height=2,
                             command=self.logout)
        logout_btn.pack(side=tk.LEFT, padx=5)

    def health_test(self):
        self.frame.destroy()
        from tes_kesehatan import HealthTestWindow
        HealthTestWindow(self.master, self.username)

    def purchase_medicine(self):
        self.frame.destroy()
        from purchase_medicine import PurchaseMedicineWindow
        PurchaseMedicineWindow(self.master, self.username)

    def show_profile(self):
        self.frame.destroy()
        from show_profile import ProfileWindow
        ProfileWindow(self.master, self.username)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.frame.destroy()
            from account_management import LoginWindow
            LoginWindow(self.master)