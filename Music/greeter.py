import tkinter as tk
from tkinter import Label, Button, Toplevel
from PIL import Image, ImageTk
from io import BytesIO
from music_suggestion_app import MusicSuggestionApp
import requests

class Greeter:
    def __init__(self, root, api_key):
        self.root = root
        self.api_key = api_key
        self.show_greeter()

    def show_greeter(self):
        """
        Creates a welcome screen for the Music Suggestion App.
        Displays a welcome message, loads an image from a URL,
        resizes the image, and creates buttons for starting the app
        and accessing settings.
        """
        self.root.title("Welcome to Music Suggestion App")

        # Clear existing widgets if any
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a welcome message with an image from URL
        welcome_label = Label(self.root, text="Welcome to the Music Suggestion App!", font=("Arial", 14))
        welcome_label.pack(padx=20, pady=20)

        # Load image from URL
        image_url = "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/9/94/Spider-Man_Red_and_Blue.jpg/revision/latest?cb=20220417141216"  # Replace with your actual image URL
        response = requests.get(image_url)
        image_data = response.content
        img = Image.open(BytesIO(image_data))
        img = img.resize((200, 200))  # Adjust the size as needed

        # Convert Image to PhotoImage
        tk_img = ImageTk.PhotoImage(img)

        # Create label to display the image
        image_label = Label(self.root, image=tk_img)
        image_label.photo = tk_img  # to prevent garbage collection
        image_label.pack(pady=10)

        # Create buttons for starting the app and accessing settings
        start_button = Button(self.root, text="Start", command=self.start_app)
        start_button.pack(pady=10)

        settings_button = Button(self.root, text="Settings", command=self.open_settings)
        settings_button.pack(pady=10)

    def start_app(self):
        if self.root.winfo_exists():  # Check if the root window is still alive
            self.root.destroy()  # Close the Greeter window
            music_app_root = tk.Tk()
            music_app = MusicSuggestionApp(music_app_root, self.api_key)
            music_app_root.mainloop()


    def open_settings(self):
        settings_window = SettingsWindow(self.root)
class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.settings_window = Toplevel(parent)
        self.settings_window.title("Settings")
        self.create_widgets()

    def create_widgets(self):
        # Add toggle dark mode button
        toggle_dark_mode_button = Button(self.settings_window, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        toggle_dark_mode_button.pack(pady=10)

    def toggle_dark_mode(self):
        # Implement toggle dark mode logic here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    api_key = "AIzaSyB0ejTmLHUMmtqFUtn6kJmZ4M9CBkxYpO0"  # Replace with your actual YouTube API key
    greeter = Greeter(root, api_key)
    root.mainloop()

    