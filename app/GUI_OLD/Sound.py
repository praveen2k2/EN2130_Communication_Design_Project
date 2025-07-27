import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os


class SoundFrame:
    def __init__(self, root, switch_back_callback):
        self.display_thumbnail = None
        self.root = root
        self.switch_back_callback = switch_back_callback
        self.selected_audio_path = None
        self.thumbnail_canvas = None  # To display the selected thumbnail

    def show(self):
        # Clear the existing window content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Heading
        heading = tk.Label(self.root, text="Select a Audio", font=("Arial", 15))
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

        # Function to display a thumbnail of the selected video
        def browse_video():
            file_path = filedialog.askopenfilename(
                filetypes=[("Audio Files", "*.mp3;*.wav")]
            )
            if file_path:
                self.selected_video_path = file_path
                self.display_thumbnail(file_path)
                send_button.config(state=tk.NORMAL)

        # Display the selected video icon and name on the canvas
        def display_thumbnail(file_path):
            if self.thumbnail_canvas:
                self.thumbnail_canvas.destroy()

            self.thumbnail_canvas = tk.Canvas(self.root, width=300, height=100, bg="white", highlightthickness=1, highlightbackground="black")
            self.thumbnail_canvas.pack(pady=10, before=button_frame)

            # Placeholder for video thumbnail: an icon and filename
            audio_icon_path = r"C:\\Users\\Bathiya Dissanayake\\Pictures\\istockphoto-1244097573-612x612.jpg"  # Provide the path to a placeholder video icon
            try:
                img = Image.open(audio_icon_path)
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

        browse_button = ttk.Button(text="Browse", command=browse_video, width=20, style="Custom.TButton")
        browse_button.pack()

        # Send button
        def send_video():
            if self.selected_audio_path:
                messagebox.showinfo("Video Selected", f"Video sent: {self.selected_audio_path}")
                self.switch_back_callback()

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        send_button = ttk.Button(button_frame, text="Send", command=send_video, state=tk.DISABLED, width=20, style="Custom.TButton")
        send_button.grid(row=0, column=0, padx=10)

        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.switch_back_callback, width=20, style="Custom.TButton")
        cancel_button.grid(row=0, column=1, padx=10)

