import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Main app class
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Player 🎵")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Track variables
        self.playlist = []
        self.current_index = 0
        self.paused = False

        # Playlist box
        self.playlist_box = tk.Listbox(self.root, bg="black", fg="white", width=60, height=12)
        self.playlist_box.pack(pady=15)

        # Control buttons
        controls_frame = tk.Frame(self.root)
        controls_frame.pack()

        self.play_btn = tk.Button(controls_frame, text="▶ Play", width=10, command=self.play_song)
        self.pause_btn = tk.Button(controls_frame, text="⏸ Pause", width=10, command=self.pause_song)
        self.resume_btn = tk.Button(controls_frame, text="⏯ Resume", width=10, command=self.resume_song)
        self.stop_btn = tk.Button(controls_frame, text="⏹ Stop", width=10, command=self.stop_song)

        self.play_btn.grid(row=0, column=0, padx=5)
        self.pause_btn.grid(row=0, column=1, padx=5)
        self.resume_btn.grid(row=0, column=2, padx=5)
        self.stop_btn.grid(row=0, column=3, padx=5)

        # Next/Prev buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack()

        self.prev_btn = tk.Button(nav_frame, text="⏮ Prev", width=10, command=self.prev_song)
        self.next_btn = tk.Button(nav_frame, text="⏭ Next", width=10, command=self.next_song)

        self.prev_btn.grid(row=0, column=0, padx=5, pady=10)
        self.next_btn.grid(row=0, column=1, padx=5, pady=10)

        # Volume control
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient="horizontal",
                                      label="Volume", command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=10)

        # Menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Songs", command=self.add_songs)
        file_menu.add_command(label="Exit", command=self.root.quit)

    # Add songs
    def add_songs(self):
        files = filedialog.askopenfilenames(initialdir="~/Music", title="Choose Songs",
                                            filetypes=(("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")))
        for file in files:
            self.playlist.append(file)
            self.playlist_box.insert(tk.END, os.path.basename(file))

    # Play selected or current song
    def play_song(self):
        if not self.playlist:
            messagebox.showwarning("No songs", "Please add songs to playlist!")
            return

        self.current_index = self.playlist_box.curselection()[0] if self.playlist_box.curselection() else 0
        song = self.playlist[self.current_index]

        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.paused = False

    # Pause
    def pause_song(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    # Resume
    def resume_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    # Stop
    def stop_song(self):
        pygame.mixer.music.stop()

    # Next song
    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(self.current_index)
        self.play_song()

    # Previous song
    def prev_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(self.current_index)
        self.play_song()

    # Set volume
    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()