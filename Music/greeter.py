import tkinter as tk
from tkinter import Label, Button, Toplevel
from PIL import Image, ImageTk
from io import BytesIO
from music_suggestion_app import MusicSuggestionApp
import requests
from ttkthemes import ThemedStyle

class Greeter:
    def __init__(self, root, api_key):
        self.root = root
        self.api_key = api_key
        self.dark_mode = False  # Default mode is light mode
        self.style = ThemedStyle(self.root)
        self.show_greeter()

    def show_greeter(self):
        """
        Creates a welcome screen for the Music Suggestion App.
        Displays a welcome message, loads an image from a URL,
        resizes the image, and creates buttons for starting the app,
        accessing settings, and toggling dark mode.
        """
        self.root.title("Welcome to Music Suggestion App")

        # Clear existing widgets if any
        for widget in self.root.winfo_children():
            widget.destroy()

        # Configure the theme
        self.update_theme()

        # Create a welcome message with an image from URL
        welcome_label = Label(self.root, text="Welcome to the Music Suggestion App!", font=("Arial", 14))
        welcome_label.pack(padx=15, pady=15)

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

        # Create buttons for starting the app, accessing settings, and toggling dark mode
        start_button = Button(self.root, text="Start", command=self.start_app)
        start_button.pack(pady=10)

        dark_mode_button = Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        dark_mode_button.pack(pady=10)

    def start_app(self):
        if self.root.winfo_exists():
            self.root.withdraw()
            app = Toplevel() 
            music_app = MusicSuggestionApp(app, self.api_key,dark_mode=self.dark_mode)
            

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        theme_name = "radiance" if not self.dark_mode else "equilux"
        self.style.set_theme(theme_name)
        self.root.configure(bg="#272829" if self.dark_mode else "white")

if __name__ == "__main__":
    root = tk.Tk()
    api_key = "AIzaSyB0ejTmLHUMmtqFUtn6kJmZ4M9CBkxYpO0"
    greeter = Greeter(root, api_key)
    root.mainloop()

    