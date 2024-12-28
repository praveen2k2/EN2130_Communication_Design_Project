import customtkinter as ctk
import time
import threading
# Set up appearance and mode
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

# Create the main app window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window title and size
        self.title("CustomTkinter App")
        self.geometry("400x300")

        # Login label
        self.label = ctk.CTkLabel(self, text="Login", font=("Arial", 20))
        self.label.pack(pady=20)

        # Username entry
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter your username")
        self.username_entry.pack(pady=5)

        # Password entry
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter your password", show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack(pady=10)


    def run_background_task(self):
        while True:
            # Simulating a background task
            self.label.configure(text=time.strftime("%I:%M:%S %p"), text_color="red")
            time.sleep(0.1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(username)
        
        if username == "admin" and password == "password":
            self.label.configure(text="Login successful!", text_color="green")
        else:
            self.label.configure(text="Invalid credentials.", text_color="red")
        threading.Thread(target=self.run_background_task, daemon=True).start()


# Run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()
