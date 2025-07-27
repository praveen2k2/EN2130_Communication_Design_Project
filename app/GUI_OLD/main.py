import tkinter as tk
from main_menue import MainFrame
from option import OptionsFrame
from Text import TextFrame
from video import VideoFrame
from image import ImageFrame
from Project_ammata_siri.Sound import SoundFrame

root = tk.Tk()
root.title("CDP Group Tele-Link")
root.geometry("500x400")

icon_path = r"C:\\Users\\Bathiya Dissanayake\\Downloads\\signal-tower.ico"  # Example location
try:
    root.iconbitmap(icon_path)  # Use for .ico files
except tk.TclError:
    # Fallback for other image formats if icon.ico is not available
    fallback_icon_path = r"C:\\Users\\Bathiya Dissanayake\\Downloads\\wuY0cA3a_400x400.jpg"  # Replace with a .png file if needed
    root.iconphoto(True, tk.PhotoImage(file=fallback_icon_path))


root.resizable(False, False)  # Disable resizing and full-screen scaling

# Frame instances
main_frame = MainFrame(root, lambda: options_frame.show())
options_frame = OptionsFrame(root, lambda: main_frame.show(),
                             lambda: text_frame.show(),
                             lambda: image_frame.show(),
                             lambda: video_frame.show(),
                             lambda: sound_frame.show())
text_frame = TextFrame(root, lambda: options_frame.show())
image_frame = ImageFrame(root, lambda: options_frame.show())
video_frame = VideoFrame(root, lambda: options_frame.show())
sound_frame = SoundFrame(root, lambda: options_frame.show())


# Show the main frame initially
main_frame.show()

# Run the application
root.mainloop()
