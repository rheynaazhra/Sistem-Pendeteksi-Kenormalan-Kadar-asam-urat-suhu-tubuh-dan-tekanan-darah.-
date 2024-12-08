import tkinter as tk
from account_management import LoginWindow

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login System")
        
        # Set window size and position it at center of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"1920x1080+{(screen_width-1920)//2}+{(screen_height-1080)//2}")
        
        # Initialize with login window
        self.current_window = LoginWindow(self.root)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()