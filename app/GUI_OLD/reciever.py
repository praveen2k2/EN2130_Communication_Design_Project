import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading


class Reciever:
    def __init__(self, root, switch_back_callback):
        self.display_thumbnail = None
        self.root = root
        self.switch_back_callback = switch_back_callback
        self.selected_file_path = None # Tempory file
        self.thumbnail_canvas = None  # To display the selected thumbnail

    def show(self):
        # Clear the existing window content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Heading
        heading = tk.Label(self.root, text="Receive", font=("Arial", 15))
        heading.pack(pady=10)

        style = ttk.Style()
        style.configure("Custom.TButton", font=('calibri', 12, 'bold'))

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

        # Display the selected video icon and name on the canvas
        def display_thumbnail(file_path):
            if self.thumbnail_canvas:
                self.thumbnail_canvas.destroy()

            self.thumbnail_canvas = tk.Canvas(self.root, width=300, height=100, bg="white", highlightthickness=1, highlightbackground="black")
            self.thumbnail_canvas.pack(pady=10)

            # Placeholder for video thumbnail: an icon and filename
            video_icon_path = r"C:\\Users\\Bathiya Dissanayake\\Pictures\\free-video-icon-831-thumb.png"  # Provide the path to a placeholder video icon
            try:
                img = Image.open(video_icon_path)
                img.thumbnail((50, 50))
                img_tk = ImageTk.PhotoImage(img)

                self.thumbnail_canvas.create_image(30, 50, image=img_tk)
                self.thumbnail_canvas.image = img_tk  # Keep a reference

                # Display video filename
                video_name = os.path.basename(file_path)
                self.thumbnail_canvas.create_text(120, 50, text=video_name, font=("Arial", 10), anchor=tk.W)

            except Exception as e:
                print(f"Error displaying video icon: {e}")

        self.display_thumbnail = display_thumbnail  # Bind method to self

        # Send button
        close_button = ttk.Button(text="Close", command=self.switch_back_callback, width=20, style="Custom.TButton")
        close_button.pack()
