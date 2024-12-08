import tkinter as tk
from PIL import Image, ImageTk
import json
from datetime import datetime

class ResultWindow:
    def __init__(self, master, username, test_type, result):
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

        self.save_result(test_type, result)
        self.create_result_view(test_type, result)

    def create_result_view(self, test_type, result):
        # Result Container
        result_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        result_frame.place(relx=0.5, rely=0.3, anchor='n', width=800, height=500)

        title_label = tk.Label(result_frame, 
                             text="Hasil Pemeriksaan",
                             font=("Arial", 24, "bold"),
                             bg='white')
        title_label.pack(pady=20)

        # Result Text
        result_text = tk.Text(result_frame,
                            font=("Arial", 12),
                            bg='white',
                            wrap=tk.WORD,
                            width=60,
                            height=15)
        result_text.insert('1.0', result)
        result_text.configure(state='disabled')
        result_text.pack(padx=40, pady=20)

        # Buttons Frame
        buttons_frame = tk.Frame(result_frame, bg='white')
        buttons_frame.pack(pady=20)

        # New Test Button
        new_test_btn = tk.Button(buttons_frame,
                               text="New Test",
                               command=self.new_test,
                               font=("Arial", 12, "bold"),
                               bg='#4CAF50',
                               fg='white',
                               width=15,
                               height=2)
        new_test_btn.pack(side=tk.LEFT, padx=10)

        # Back to Menu Button
        back_btn = tk.Button(buttons_frame,
                           text="Back to Menu",
                           command=self.back_to_menu,
                           font=("Arial", 12, "bold"),
                           bg='#2196F3',
                           fg='white',
                           width=15,
                           height=2)
        back_btn.pack(side=tk.LEFT, padx=10)

    def save_result(self, test_type, result):
        try:
            with open('database/health_check.json', 'r') as file:
                health_records = json.load(file)
        except FileNotFoundError:
            health_records = []

        new_record = {
            'username': self.username,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'test_type': test_type,
            'result': result
        }

        health_records.append(new_record)

        with open('database/health_check.json', 'w') as file:
            json.dump(health_records, file, indent=4)

    def new_test(self):
        self.frame.destroy()
        from tes_kesehatan import HealthTestWindow
        HealthTestWindow(self.master, self.username)

    def back_to_menu(self):
        self.frame.destroy()
        from main_menu import MainMenuWindow
        MainMenuWindow(self.master, self.username)