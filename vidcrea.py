import tkinter as tk
from tkinter import filedialog
from moviepy.editor import *
from PIL import Image, ImageTk
import os

class SlideshowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio + Slideshow Creator")
        self.images = []
        self.audio_file = None

        self.label = tk.Label(root, text="Sleep je muziek (MP3/WAV) en afbeeldingen hier", width=60, height=4)
        self.label.pack(pady=10)

        self.text_overlay = tk.Entry(root, width=50)
        self.text_overlay.insert(0, "Je eigen tekst hier")
        self.text_overlay.pack(pady=5)

        self.generate_button = tk.Button(root, text="Maak Video", command=self.create_video)
        self.generate_button.pack(pady=10)

        self.root.bind("<Drag>", lambda e: "break")
        self.root.bind("<Drop>", self.drop)

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                self.images.append(f)
            elif f.lower().endswith((".mp3", ".wav")):
                self.audio_file = f

        self.label.config(text=f"{len(self.images)} afbeeldingen geladen\nAudio: {'Ja' if self.audio_file else 'Nee'}")

    def create_video(self):
        if not self.audio_file or not self.images:
            self.label.config(text="Laad zowel audio als afbeeldingen eerst!")
            return

        duration = AudioFileClip(self.audio_file).duration
        img_duration = duration / len(self.images)

        clips = []
        for img_path in self.images:
            img_clip = ImageClip(img_path).set_duration(img_duration).fadein(1).fadeout(1)
            img_clip = img_clip.resize(height=720)  # Schaal naar HD hoogte
            clips.append(img_clip)

        slideshow = concatenate_videoclips(clips, method="compose")
        audio = AudioFileClip(self.audio_file)
        final = slideshow.set_audio(audio)

        # Voeg tekstoverlay toe
        if self.text_overlay.get():
            txt = TextClip(self.text_overlay.get(), fontsize=40, color='white', bg_color='black')
            txt = txt.set_duration(duration).set_position(("center", "bottom")).margin(bottom=30, opacity=0)
            final = CompositeVideoClip([final, txt])

        output_file = "output_video.mp4"
        final.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")

        self.label.config(text=f"Video opgeslagen als {output_file}")

# Start de GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SlideshowApp(root)
    root.mainloop()
