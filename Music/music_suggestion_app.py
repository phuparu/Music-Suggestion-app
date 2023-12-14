import tkinter as tk
from tkinter import ttk, Canvas, Label, Toplevel
from ttkthemes import ThemedStyle
import random
import webbrowser
import googleapiclient.discovery
import googleapiclient.errors
import requests
from PIL import Image, ImageTk

class MusicSuggestionApp:
    def __init__(self, root, DEVELOPER_KEY, dark_mode=False):
        self.root = root
        self.DEVELOPER_KEY = DEVELOPER_KEY
        self.dark_mode = dark_mode

        self.song_label = Label(self.root, text="")
        self.song_label.pack(pady=10)

        self.root.title("Music Suggestion App")
        self.create_gradient_background()
        self.root.resizable(False, False)

        window_width = 500
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.style = ThemedStyle(self.root)
        self.update_theme()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=35, pady=35)

        center_frame = ttk.Frame(main_frame)
        center_frame.pack(expand=True, pady=20)

        ttk.Label(center_frame, text="Select Genre:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.genre_combobox = ttk.Combobox(center_frame, values=["-", "Pop", "Rock", "Hip Hop", "Electronic", "R&B", "Country", "Jazz", "Indie"])
        self.genre_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.genre_combobox.set("-")

        ttk.Label(center_frame, text="Select Language:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.language_combobox = ttk.Combobox(center_frame, values=["-", "Thai", "Korean", "Japan", "Italian", "English", "Spanish", "French", "German", "Portuguese"])
        self.language_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.language_combobox.set("-")

        suggest_button = ttk.Button(center_frame, text="Suggest Music", command=self.suggest_music)
        suggest_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.video_data = []
        self.thumbnail_cache = {}
        api_service_name = "youtube"
        api_version = "v3"
        self.DEVELOPER_KEY = DEVELOPER_KEY
        
        self.youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=self.DEVELOPER_KEY)
        
        self.liked_songs = []
        self.disliked_songs = []
        style = ThemedStyle(self.root)
        self.style = style
        
        mode_button = ttk.Button(main_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        mode_button.pack(pady=10)

        self.update_theme()

    def create_gradient_background(self):
        start_color = "#A0C3FF"  # Pastel Blue
        end_color = "#FFC3A0"    # Pastel Pink

        gradient_canvas = Canvas(self.root, width=800, height=600)
        gradient_canvas.place(relx=0, rely=0, anchor=tk.NW)

        for i in range(600):
            r = int(int(start_color[1:3], 16) + (int(end_color[1:3], 16) - int(start_color[1:3], 16)) * (i / 600))
            g = int(int(start_color[3:5], 16) + (int(end_color[3:5], 16) - int(start_color[3:5], 16)) * (i / 600))
            b = int(int(start_color[5:7], 16) + (int(end_color[5:7], 16) - int(start_color[5:7], 16)) * (i / 600))

            color = f"#{r:02X}{g:02X}{b:02X}"
            gradient_canvas.create_line(0, i, 800, i, fill=color)

    def suggest_music(self):
        genre = self.genre_combobox.get()
        language = self.language_combobox.get()

        if genre == "-" or language == "-":
            self.show_error("Error", "Please select a valid genre and language")
            return

        search_query = f"{genre} {language} music playlist"
        search_params = {
            'q': search_query,
            'type': 'playlist',
            'part': 'snippet',
            'maxResults': 3
        }

        try:
            if search_query in self.thumbnail_cache:
                playlist_data = self.thumbnail_cache[search_query]
            else:
                search_response = self.youtube.search().list(**search_params).execute()
                playlists = search_response.get('items', [])
                playlist_data = [(playlist['id']['playlistId'], playlist['snippet']['title']) for playlist in playlists]
                self.thumbnail_cache[search_query] = playlist_data

            playlist_data = [playlist for playlist in playlist_data if playlist[0] not in self.liked_songs and playlist[0] not in self.disliked_songs]

            if not playlist_data:
                self.show_error("Error", "No more suggestions available.")
                return

            random.shuffle(playlist_data)
            self.video_data = []

            playlist_id, playlist_title = playlist_data[0]
            playlist_items_params = {
                'playlistId': playlist_id,
                'part': 'snippet',
                'maxResults': 20
            }

            playlist_items_response = self.youtube.playlistItems().list(**playlist_items_params).execute()
            videos = playlist_items_response.get('items', [])
            self.video_data = [
                (
                    video['snippet']['resourceId']['videoId'],
                    video['snippet']['title'],
                    video['snippet']['thumbnails'].get('default', {}).get('url', 'default_url_placeholder')
                ) 
                for video in videos
            ]

            random.shuffle(self.video_data)

            self.open_suggestions_window()

        except googleapiclient.errors.HttpError as e:
            error_message = f"An HTTP error occurred: {str(e)}"
            print("Error:", error_message)
            self.show_error("Error", error_message)
        except googleapiclient.errors.Error as e:
            error_message = f"An error occurred: {str(e)}"
            print("Error:", error_message)
            self.show_error("Error", error_message)

    def show_error(self, title, message):
        error_window = Toplevel(self.root)
        error_window.title(title)
        label = ttk.Label(error_window, text=message, font=("Arial", 12), foreground="red")
        label.pack(padx=20, pady=20)
        button = ttk.Button(error_window, text="Close", command=error_window.destroy)
        button.pack(pady=10)

    def open_suggestions_window(self):
        suggestions_window = Toplevel(self.root)
        suggestions_window.title("Music Suggestions")
        suggestions_window.configure(bg="#272829")
        suggestions_window.resizable(False, False)

        suggestions_frame = ttk.Frame(suggestions_window)
        suggestions_frame.pack(padx=10, pady=10)

        for i in range(3):
            video_title = self.video_data[i][1]
            video_thumbnail_url = self.video_data[i][2]

            play_button = ttk.Button(suggestions_frame, text=f"Play : {video_title}", command=lambda i=i: self.play_video(i))
            play_button.grid(row=1, column=i, padx=10, pady=5)

            open_playlist_button = ttk.Button(suggestions_frame, text=f"Open Playlist : {video_title}", command=lambda i=i: self.open_playlist(i))
            open_playlist_button.grid(row=2, column=i, padx=10, pady=5)

            image = Image.open(requests.get(video_thumbnail_url, stream=True).raw)
            thumbnail_image = ImageTk.PhotoImage(image)

            thumbnail_label = Label(suggestions_frame, image=thumbnail_image)
            thumbnail_label.grid(row=0, column=i, padx=10, pady=5)
            thumbnail_label.image = thumbnail_image

            dislike_button = ttk.Button(suggestions_frame, text="Dislike", command=lambda i=i: self.dislike_song(i))
            dislike_button.grid(row=3, column=i, padx=10, pady=5)

            exit_button = ttk.Button(suggestions_frame, text="Exit", command=suggestions_window.destroy)
            exit_button.grid(row=5, column=1, padx=10, pady=10)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        theme_name = "radiance" if not self.dark_mode else "equilux"
        self.style.set_theme(theme_name)
        self.root.configure(bg="#272829" if self.dark_mode else "white")

    def dislike_song(self, index):
        if 0 <= index < len(self.video_data):
            disliked_song = self.video_data.pop(index)
            self.open_disliked_song_window(disliked_song)
            self.suggest_random_song()

    def open_disliked_song_window(self, song):
        disliked_window = Toplevel(self.root)
        disliked_window.title("Disliked Song")
        disliked_window.configure(bg="#272829")

        image = Image.open(requests.get(song[2], stream=True).raw)
        thumbnail_image = ImageTk.PhotoImage(image)

        thumbnail_label = Label(disliked_window, image=thumbnail_image)
        thumbnail_label.pack(pady=10)

        title_label = ttk.Label(disliked_window, text=song[1], font=("Arial", 12), foreground="white", background="#272829")
        title_label.pack(pady=10)

        dislike_message = ttk.Label(disliked_window, text="You disliked this song.", font=("Arial", 12), foreground="red", background="#272829")
        dislike_message.pack(pady=10)

        close_button = ttk.Button(disliked_window, text="Close", command=disliked_window.destroy)
        close_button.pack(pady=10)

    def play_video(self, index):
        if 0 <= index < len(self.video_data):
            webbrowser.open(f"https://www.youtube.com/watch?v={self.video_data[index][0]}")

    def open_playlist(self, index):
        if 0 <= index < len(self.video_data):
            video_id = self.video_data[index][0]
            playlist_id = self.get_playlist_id_for_video(video_id)

            if playlist_id:
                webbrowser.open(f"https://www.youtube.com/playlist?list={playlist_id}")
            else:
                self.show_error("Error", "Unable to find the playlist for this video.")

    def get_playlist_id_for_video(self, video_id):
        for video in self.video_data:
            if video[0] == video_id:
                search_query = f"{video[1]} playlist"
                search_params = {
                    'q': search_query,
                    'type': 'playlist',
                    'part': 'snippet',
                    'maxResults': 1
                }

                try:
                    search_response = self.youtube.search().list(**search_params).execute()
                    playlists = search_response.get('items', [])
                    if playlists:
                        return playlists[0]['id']['playlistId']
                    else:
                        return None
                except googleapiclient.errors.HttpError as e:
                    print("Error:", str(e))
                    return None

if __name__ == "__main__":
    root = tk.Tk()
    api_key = "AIzaSyB0ejTmLHUMmtqFUtn6kJmZ4M9CBkxYpO0"  # Replace with your actual API key
    app = MusicSuggestionApp(root, api_key)
    root.mainloop()