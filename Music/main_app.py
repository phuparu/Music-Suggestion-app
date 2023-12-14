import tkinter as tk
from greeter import Greeter

if __name__ == "__main__":
    root = tk.Tk()
    api_key = "AIzaSyB0ejTmLHUMmtqFUtn6kJmZ4M9CBkxYpO0"  # Replace with your actual API key

    # Create an instance of the Greeter class
    greeter = Greeter(root, api_key)

    # Show the greeter window
    greeter.show_greeter()

    # Start the Tkinter main loop
    root.mainloop()