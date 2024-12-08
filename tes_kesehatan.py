import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from hasil_pemeriksaan import ResultWindow
import json
from datetime import datetime

class HealthTestWindow:
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

        self.create_test_form()
        
    def create_test_form(self):
        form_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        form_frame.place(relx=0.505, rely=0.25, anchor='n', width=590, height=600)

        title_label = tk.Label(form_frame, 
                             text="Tes Kesehatan",
                             font=("Arial", 24, "bold"),
                             bg='white')
        title_label.pack(pady=20)

        # Test Type Dropdown
        test_frame = tk.Frame(form_frame, bg='white')
        test_frame.pack(fill='x', padx=40, pady=15)
        
        test_label = tk.Label(test_frame,
                            text="Select Test Type:",
                            font=("Arial", 12),
                            bg='white')
        test_label.pack(anchor='w')
        
        self.test_type = ttk.Combobox(test_frame,
                                     values=["Cek Tekanan Darah",
                                            "Cek Kolestrol",
                                            "Cek Asam Urat"],
                                     font=("Arial", 12),
                                     state="readonly")
        self.test_type.pack(fill='x', pady=5)
        self.test_type.bind('<<ComboboxSelected>>', self.on_test_type_change)

        # Gender Dropdown
        gender_frame = tk.Frame(form_frame, bg='white')
        gender_frame.pack(fill='x', padx=40, pady=10)
        
        gender_label = tk.Label(gender_frame,
                              text="Gender:",
                              font=("Arial", 12),
                              bg='white')
        gender_label.pack(anchor='w')
        
        self.gender = ttk.Combobox(gender_frame,
                                  values=["Pria", "Wanita"],
                                  font=("Arial", 12),
                                  state="readonly")
        self.gender.pack(fill='x', pady=5)

        # Age Input
        age_frame = tk.Frame(form_frame, bg='white')
        age_frame.pack(fill='x', padx=40, pady=10)
        
        age_label = tk.Label(age_frame,
                           text="Age:",
                           font=("Arial", 12),
                           bg='white')
        age_label.pack(anchor='w')
        
        self.age = tk.Entry(age_frame, font=("Arial", 12))
        self.age.pack(fill='x', pady=5)

        # Dynamic Form Container
        self.dynamic_frame = tk.Frame(form_frame, bg='white')
        self.dynamic_frame.pack(fill='x', padx=40, pady=10)

        # Check Button
        self.check_btn = tk.Button(form_frame,
                                 text="Check",
                                 command=self.check_health,
                                 font=("Arial", 14, "bold"),
                                 bg='#4CAF50',
                                 fg='white',
                                 width=15,
                                 height=2)
        self.check_btn.pack(pady=20)

        # Bottom Buttons Frame
        bottom_buttons_frame = tk.Frame(self.frame)
        bottom_buttons_frame.place(x=1520, y=980)

        # History Button
        history_btn = tk.Button(bottom_buttons_frame,
                              text="History",
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
        history_window.title("Test History")
        history_window.geometry("800x600")

        # Create main frame
        main_frame = tk.Frame(history_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add title
        title_label = tk.Label(main_frame, 
                             text="Your Health Test History",
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
            with open('database/health_check.json', 'r') as file:
                history = json.load(file)
                
            # Filter history for current user and sort by timestamp
            user_history = [record for record in history if record['username'] == self.username]
            user_history.sort(key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"), 
                            reverse=True)

            if user_history:
                for record in user_history:
                    history_text.insert(tk.END, f"\nDate: {record['timestamp']}\n")
                    history_text.insert(tk.END, f"Test Type: {record['test_type']}\n")
                    history_text.insert(tk.END, f"Result: {record['result']}\n")
                    history_text.insert(tk.END, "-" * 50 + "\n")
            else:
                history_text.insert(tk.END, "No test history found.")

            history_text.config(state='disabled')

        except FileNotFoundError:
            history_text.insert(tk.END, "No test history found.")
            history_text.config(state='disabled')

    def on_test_type_change(self, event=None):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        test_type = self.test_type.get()
        
        if test_type == "Cek Tekanan Darah":
            systolic_label = tk.Label(self.dynamic_frame,
                                    text="Systolic (mmHg):",
                                    font=("Arial", 12),
                                    bg='white')
            systolic_label.pack(anchor='w')
            
            self.systolic = tk.Entry(self.dynamic_frame, font=("Arial", 12))
            self.systolic.pack(fill='x', pady=5)

            diastolic_label = tk.Label(self.dynamic_frame,
                                     text="Diastolic (mmHg):",
                                     font=("Arial", 12),
                                     bg='white')
            diastolic_label.pack(anchor='w')
            
            self.diastolic = tk.Entry(self.dynamic_frame, font=("Arial", 12))
            self.diastolic.pack(fill='x', pady=5)

        elif test_type in ["Cek Kolestrol", "Cek Asam Urat"]:
            level_label = tk.Label(self.dynamic_frame,
                                 text="Kadar:",
                                 font=("Arial", 12),
                                 bg='white')
            level_label.pack(anchor='w')
            
            self.level = tk.Entry(self.dynamic_frame, font=("Arial", 12))
            self.level.pack(fill='x', pady=5)

    def check_health(self):
        try:
            test_type = self.test_type.get()
            age = int(self.age.get())
            gender = self.gender.get()

            if not all([test_type, age, gender]):
                messagebox.showerror("Error", "Please fill all fields")
                return

            result = ""
            
            if test_type == "Cek Tekanan Darah":
                systolic = int(self.systolic.get())
                diastolic = int(self.diastolic.get())
                result = self.check_blood_pressure(age, systolic, diastolic)
                
            elif test_type == "Cek Asam Urat":
                level = float(self.level.get())
                result = self.check_uric_acid(age, gender, level)
                
            elif test_type == "Cek Kolestrol":
                level = float(self.level.get())
                result = self.check_cholesterol(age, level)

            if result:
                self.frame.destroy()
                ResultWindow(self.master, self.username, test_type, result)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_blood_pressure(self, age, systolic, diastolic):
        if age <= 20:
            if 95 <= systolic <= 110 and 55 <= diastolic <= 70:
                return "Tekanan darah Anda normal."
            elif systolic > 110 or diastolic > 70:
                return (
                    f"Tekanan darah tinggi. Rentang normal untuk anak-anak: 95-110 sistolik dan 55-70 diastolik.\n"
                    f"Sistolik Anda: {systolic}, Diastolik Anda: {diastolic}.\n"
                    "Rekomendasi obat: Amlodipine, Nifedipine, Bisoprolol.\n"
                    "Pesan:\n1. Olahraga rutin.\n2. Perbanyak konsumsi sayur, buah, dan makanan tidak berlemak."
                )
            else:
                return (
                    f"Tekanan darah rendah. Rentang normal untuk anak-anak: 95-110 sistolik dan 55-70 diastolik.\n"
                    f"Sistolik Anda: {systolic}, Diastolik Anda: {diastolic}.\n"
                    "Rekomendasi obat: Fludrocortisone, Midodrine.\n"
                    "Pesan:\n1. Perbanyak konsumsi air putih.\n2. Hindari berdiri terlalu lama dan ubah posisi."
                )
        else:
            if 90 <= systolic <= 120 and 60 <= diastolic <= 80:
                return "Tekanan darah Anda normal."
            elif systolic > 120 or diastolic > 80:
                return (
                    f"Tekanan darah tinggi. Rentang normal untuk dewasa: 90-120 sistolik dan 60-80 diastolik.\n"
                    f"Sistolik Anda: {systolic}, Diastolik Anda: {diastolic}.\n"
                    "Rekomendasi obat: Amlodipine, Nifedipine, Bisoprolol.\n"
                    "Pesan:\n1. Olahraga rutin.\n2. Perbanyak konsumsi sayur, buah, dan makanan tidak berlemak."
                )
            else:
                return (
                    f"Tekanan darah rendah. Rentang normal untuk dewasa: 90-120 sistolik dan 60-80 diastolik.\n"
                    f"Sistolik Anda: {systolic}, Diastolik Anda: {diastolic}.\n"
                    "Rekomendasi obat: Fludrocortisone, Midodrine.\n"
                    "Pesan:\n1. Perbanyak konsumsi air putih.\n2. Hindari berdiri terlalu lama dan ubah posisi."
                )

    def check_uric_acid(self, age, gender, level):
        if age <= 20:
            if 2.0 <= level <= 5.5:
                return "Kadar asam urat Anda normal."
            else:
                if level > 5.5:
                    return (
                        f"Asam urat tinggi. Rentang normal: 2.0 <= kadar <= 5.5.\n"
                        f"Kadar Anda: {level}.\n"
                        "Rekomendasi obat: Allopurinol, Febuxostat, Colchicine.\n"
                        "Pesan: Hindari makanan tinggi purin seperti jeroan, seafood, dan daging merah."
                    )
                else:
                    return (
                        f"Asam urat rendah. Rentang normal: 2.0 <= kadar <= 5.5.\n"
                        f"Kadar Anda: {level}.\n"
                        "Pesan: Tingkatkan konsumsi protein sehat seperti telur, ikan, dan daging."
                    )
        else:
            if gender == "Pria":
                if 3.1 <= level <= 7.0:
                    return "Kadar asam urat Anda normal."
                else:
                    if level > 7.0:
                        return (
                            f"Asam urat tinggi. Rentang normal: 3.1 <= kadar <= 7.0.\n"
                            f"Kadar Anda: {level}.\n"
                            "Rekomendasi obat: Allopurinol, Febuxostat, Colchicine.\n"
                            "Pesan: Hindari makanan tinggi purin seperti jeroan, seafood, dan daging merah."
                        )
                    else:
                        return (
                            f"Asam urat rendah. Rentang normal: 3.1 <= kadar <= 7.0.\n"
                            f"Kadar Anda: {level}.\n"
                            "Pesan: Tingkatkan konsumsi protein sehat seperti telur, ikan, dan daging."
                        )
            elif gender == "Wanita":
                if 2.4 <= level <= 6.0:
                    return "Kadar asam urat Anda normal."
                else:
                    if level > 6.0:
                        return (
                            f"Asam urat tinggi. Rentang normal: 2.4 <= kadar <= 6.0.\n"
                            f"Kadar Anda: {level}.\n"
                            "Rekomendasi obat: Allopurinol, Febuxostat, Colchicine.\n"
                            "Pesan: Hindari makanan tinggi purin seperti jeroan, seafood, dan daging merah."
                        )
                    else:
                        return (
                            f"Asam urat rendah. Rentang normal: 2.4 <= kadar <= 6.0.\n"
                            f"Kadar Anda: {level}.\n"
                            "Pesan: Tingkatkan konsumsi protein sehat seperti telur, ikan, dan daging."
                        )

    def check_cholesterol(self, age, level):
        if age <= 20:
            if level < 170:
                return "Kadar kolesterol Anda normal."
            else:
                return (
                    f"Kolesterol tinggi. Rentang normal untuk anak/remaja: <170 mg/dL.\n"
                    f"Kadar Anda: {level} mg/dL.\n"
                    "Rekomendasi obat: Simvastatin, Atorvastatin, Rosuvastatin.\n"
                    "Pesan:\n1. Perbanyak konsumsi serat, seperti gandum utuh, buah, dan sayur.\n"
                    "2. Olahraga aerobik rutin, minimal 30 menit sehari.\n"
                    "3. Hindari makanan tinggi lemak jenuh, seperti gorengan dan makanan cepat saji."
                )
        else:
            if level < 200:
                return "Kadar kolesterol Anda normal."
            else:
                return (
                    f"Kolesterol tinggi. Rentang normal untuk dewasa: <200 mg/dL.\n"
                    f"Kadar Anda: {level} mg/dL.\n"
                    "Rekomendasi obat: Simvastatin, Atorvastatin, Rosuvastatin.\n"
                    "Pesan:\n1. Konsumsi makanan rendah lemak dan tinggi serat, seperti oatmeal dan sayur.\n"
                    "2. Olahraga secara teratur, minimal 5 hari seminggu.\n"
                    "3. Kurangi konsumsi alkohol dan hentikan merokok."
                )

    def back_to_menu(self):
        self.frame.destroy()
        from main_menu import MainMenuWindow
        MainMenuWindow(self.master, self.username)