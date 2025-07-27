import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw


class TextFrame:
    def __init__(self, root, switch_back_callback):
        self.root = root
        self.switch_back_callback = switch_back_callback

    def show(self):
        # Clear the existing window content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Heading
        heading = tk.Label(self.root, text="Write Your Text Message", font=("Arial", 15))
        heading.pack(pady=20)

        # Text entry widget
        text_entry = tk.Text(self.root, width=30, height=10, font=("Arial", 11))
        text_entry.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        try:
            # Load the image
            image_path = r"C:\\Users\\Bathiya Dissanayake\\Downloads\\tele-removebg-preview.png"  # Replace with your image path
            img = Image.open(image_path)
            img.thumbnail((100, 100))  # Resize the image to fit better (optional)
            img_tk = ImageTk.PhotoImage(img)

            # Create an image label
            image_label = tk.Label(self.root, image=img_tk)
            image_label.image = img_tk  # Keep a reference to avoid garbage collection

            # Use the `place()` method to position at bottom-right
            # x=width - image_width, y=height - image_height
            self.root.update_idletasks()  # Update the window to get its dimensions
            x_position = self.root.winfo_width() - 110  # Adjust for image size and padding
            y_position = self.root.winfo_height() - 90
            image_label.place(x=x_position, y=y_position)
        except Exception as e:
            print(f"Failed to load image: {e}")

        # Save button
        def save_to_file():
            text_content = text_entry.get("1.0", tk.END).strip()
            if not text_content:
                messagebox.showwarning("Warning", "Text message cannot be empty!")
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Text Message",
                filetypes=[("Text files", "*.txt")],
                defaultextension=".txt"
            )
            style = ttk.Style()
            style.configure("Custom.TButton",
                            font=('calibri', 12, 'bold'))

            if file_path:
                try:
                    with open(file_path, "w") as file:
                        file.write(text_content)
                    messagebox.showinfo("Success", "Text message saved successfully!")
                    self.switch_back_callback()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")

        save_button = ttk.Button(button_frame, text="Send", command=save_to_file, width=20, style="Custom.TButton")
        save_button.grid(row=0, column=0, padx=10)

        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.switch_back_callback, width=20, style="Custom.TButton")
        cancel_button.grid(row=0, column=1, padx=10)
