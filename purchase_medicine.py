import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime
import os

class PurchaseMedicineWindow:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=1920, height=1080)
        
        # Medicine categories and their corresponding medicines
        self.medicine_categories = {
            'tekanan_darah_tinggi': [
                'Amlodipine', 
                'Nifedipine', 
                'Bisoprolol'
            ],
            'tekanan_darah_rendah': [
                'Fludrocortisone', 
                'Midodrine'
            ],
            'asam_urat_tinggi': [
                'Allopurinol', 
                'Febuxostat'
            ],
            'kolesterol_tinggi': [
                'Simvastatin', 
                'Rosuvastatin'
            ],
            'vitamin': [
                'Imboost', 
                'Esterc'
            ]
        }

        self.category_names = {
            'tekanan_darah_tinggi': 'Tekanan Darah Tinggi',
            'tekanan_darah_rendah': 'Tekanan Darah Rendah',
            'asam_urat_tinggi': 'Asam Urat Tinggi',
            'kolesterol_tinggi': 'Kolesterol Tinggi',
            'vitamin' : 'vitamin'
        }

        try:
            bg_image = Image.open("assets/user-interface/background.png")
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.frame.configure(bg='#f0f0f0')

        self.create_purchase_form()

    def create_purchase_form(self):
        # Main container
        main_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        main_frame.place(relx=0.5, rely=0.15, anchor='n', width=800, height=700)

        title_label = tk.Label(main_frame, 
                             text="Pembelian Obat",
                             font=("Arial", 24, "bold"),
                             bg='white')
        title_label.pack(pady=20)

        # Category selection
        category_frame = tk.Frame(main_frame, bg='white')
        category_frame.pack(fill='x', padx=40, pady=10)

        category_label = tk.Label(category_frame,
                                text="Select Category:",
                                font=("Arial", 12),
                                bg='white')
        category_label.pack(anchor='w')

        self.category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(category_frame,
                                       textvariable=self.category_var,
                                       values=list(self.category_names.values()),
                                       font=("Arial", 12),
                                       state="readonly")
        category_dropdown.pack(fill='x', pady=5)
        category_dropdown.bind('<<ComboboxSelected>>', self.on_category_select)

        # Medicine display frame
        self.medicine_frame = tk.Frame(main_frame, bg='white')
        self.medicine_frame.pack(fill='both', expand=True, padx=40, pady=10)

        # Bottom Buttons Frame
        bottom_buttons_frame = tk.Frame(self.frame)
        bottom_buttons_frame.place(x=1520, y=980)

        # History Button
        history_btn = tk.Button(bottom_buttons_frame,
                              text="Purchase History",
                              command=self.show_history,
                              font=("Arial", 12, "bold"),
                              bg='#FFA500',
                              fg='white',
                              width=15,
                              height=2)
        history_btn.pack(side=tk.LEFT, padx=5)

        # Back Button
        back_btn = tk.Button(bottom_buttons_frame,
                           text="Back to Menu",
                           command=self.back_to_menu,
                           font=("Arial", 12, "bold"),
                           bg='#2196F3',
                           fg='white',
                           width=15,
                           height=2)
        back_btn.pack(side=tk.LEFT, padx=5)

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Purchase History")
        history_window.geometry("800x600")

        # Create main frame
        main_frame = tk.Frame(history_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add title
        title_label = tk.Label(main_frame, 
                             text="Your Purchase History",
                             font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Create text widget for history display
        history_text = tk.Text(main_frame, 
                             wrap=tk.WORD,
                             font=("Arial", 12),
                             width=70,
                             height=25)
        history_text.pack(pady=10)

        # Add scrollbar
        scrollbar = tk.Scrollbar(main_frame, command=history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_text.config(yscrollcommand=scrollbar.set)

        try:
            with open('database/purchasing.json', 'r') as file:
                purchases = json.load(file)
                
            # Filter purchases for current user and sort by timestamp
            user_purchases = [record for record in purchases if record['username'] == self.username]
            user_purchases.sort(key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"), 
                              reverse=True)

            if user_purchases:
                for purchase in user_purchases:
                    history_text.insert(tk.END, f"\nDate: {purchase['timestamp']}\n")
                    history_text.insert(tk.END, f"Medicine: {purchase['medicine']}\n")
                    history_text.insert(tk.END, f"Price: Rp {purchase['price']:,}\n")
                    history_text.insert(tk.END, "-" * 50 + "\n")
            else:
                history_text.insert(tk.END, "No purchase history found.")

            history_text.config(state='disabled')

        except FileNotFoundError:
            history_text.insert(tk.END, "No purchase history found.")
            history_text.config(state='disabled')

    def on_category_select(self, event=None):
        # Clear previous medicines
        for widget in self.medicine_frame.winfo_children():
            widget.destroy()

        selected_category_name = self.category_var.get()
        selected_category = next(key for key, value in self.category_names.items() 
                               if value == selected_category_name)
        
        medicines = self.medicine_categories[selected_category]

        # Create a canvas for scrolling
        canvas = tk.Canvas(self.medicine_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.medicine_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display medicines in a grid
        for i, medicine in enumerate(medicines):
            medicine_frame = tk.Frame(scrollable_frame, bg='white', bd=1, relief='solid')
            medicine_frame.grid(row=i, column=0, padx=10, pady=5, sticky='ew')

            try:
                img_path = f"assets/obat/{medicine}.png"
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(medicine_frame, image=photo, bg='white')
                    img_label.image = photo
                    img_label.grid(row=0, column=0, padx=10, pady=5)
                else:
                    placeholder = tk.Label(medicine_frame, 
                                         text="No Image",
                                         width=15,
                                         height=5,
                                         bg='gray90')
                    placeholder.grid(row=0, column=0, padx=10, pady=5)
            except Exception as e:
                print(f"Error loading image for {medicine}: {e}")
                placeholder = tk.Label(medicine_frame, 
                                     text="No Image",
                                     width=15,
                                     height=5,
                                     bg='gray90')
                placeholder.grid(row=0, column=0, padx=10, pady=5)

            info_frame = tk.Frame(medicine_frame, bg='white')
            info_frame.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')

            name_label = tk.Label(info_frame,
                                text=medicine,
                                font=("Arial", 12, "bold"),
                                bg='white')
            name_label.pack(anchor='w')

            price = self.generate_price()  # Generate a random price
            price_label = tk.Label(info_frame,
                                 text=f"Price: Rp {price:,}",
                                 font=("Arial", 10),
                                 bg='white')
            price_label.pack(anchor='w')

            buy_btn = tk.Button(info_frame,
                              text="Buy",
                              command=lambda m=medicine, p=price: self.purchase_medicine(m, p),
                              bg='#4CAF50',
                              fg='white')
            buy_btn.pack(anchor='w', pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generate_price(self):
        # Generate a random price between 50,000 and 200,000
        import random
        return random.randint(50000, 200000)

    def purchase_medicine(self, medicine_name, price):
        if messagebox.askyesno("Confirm Purchase", 
                              f"Do you want to purchase {medicine_name} for Rp {price:,}?"):
            # Record the purchase
            purchase_record = {
                "username": self.username,
                "medicine": medicine_name,
                "price": price,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            try:
                with open('database/purchasing.json', 'r') as file:
                    purchases = json.load(file)
            except FileNotFoundError:
                purchases = []

            purchases.append(purchase_record)

            with open('database/purchasing.json', 'w') as file:
                json.dump(purchases, file, indent=4)

            messagebox.showinfo("Success", 
                              f"Successfully purchased {medicine_name}!")

    def back_to_menu(self):
        self.frame.destroy()
        from main_menu import MainMenuWindow
        MainMenuWindow(self.master, self.username)