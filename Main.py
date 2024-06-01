import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import pydirectinput
import time
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

SAVE_INTERVAL_FILE = "save_interval.txt"
BACKGROUND_IMAGE = "background_image.jpg" 


class AutoSaveApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1280x720")
        self.master.resizable(False, False)
        self.master.title("Baldur's Gate 3 - Custom Auto Save")

        self.load_save_interval()

        self.running = False
        self.countdown_seconds = 0

        image = Image.open(BACKGROUND_IMAGE)
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(self.master, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_status = ttk.Label(self.master, text="Program is not running", foreground="red", font=("Arial", 16))
        self.label_status.grid(row=0, columnspan=2, padx=10, pady=10)

        self.label_countdown = ttk.Label(self.master, text="Time until save: 0 seconds", font=("Arial", 16))
        self.label_countdown.grid(row=1, columnspan=2, padx=10, pady=10)

        self.label_interval = ttk.Label(self.master, text="Enter save interval in minutes:", font=("Arial", 16))
        self.label_interval.grid(row=2, column=0, padx=10, pady=10)

        self.entry_interval = ttk.Entry(self.master, font=("Arial", 16))
        self.entry_interval.grid(row=2, column=1, padx=10, pady=10)
        self.entry_interval.insert(0, str(self.save_interval))

        self.button_start_stop = ttk.Button(self.master, text="Start", command=self.start_stop_autosave, style='Large.TButton')
        self.button_start_stop.grid(row=3, columnspan=2, padx=10, pady=10)

        if hasattr(self, 'label_countdown'):
            self.update_countdown()

    def load_save_interval(self):
        try:
            with open(SAVE_INTERVAL_FILE, "r") as file:
                self.save_interval = int(file.read())
        except FileNotFoundError:
            self.save_interval = 0

    def save_save_interval(self):
        with open(SAVE_INTERVAL_FILE, "w") as file:
            file.write(str(self.save_interval))

    def start_stop_autosave(self):
        if self.running:
            self.running = False
            self.label_status.config(text="Program is not running", foreground="red")
            self.button_start_stop.config(text="Start")
        else:
            interval_minutes = self.entry_interval.get()
            if interval_minutes.strip():
                try:
                    interval_minutes = int(interval_minutes)
                    if interval_minutes <= 0:
                        messagebox.showwarning("Warning", "Please enter a value greater than zero for the save interval.")
                    else:
                        self.save_interval = interval_minutes
                        self.save_save_interval()
                        self.running = True
                        self.label_status.config(text="Program is running", foreground="green")
                        threading.Thread(target=self.perform_autosave, args=(self.save_interval,)).start()
                        self.button_start_stop.config(text="Stop")
                except ValueError:
                    messagebox.showwarning("Warning", "Please enter a valid integer value for the save interval.")
            else:
                messagebox.showwarning("Warning", "Please enter a value for the save interval.")

    def perform_autosave(self, interval_minutes):
        self.countdown_seconds = interval_minutes * 60
        while self.running:
            time.sleep(1)
            self.countdown_seconds -= 1
            self.update_countdown()
            if self.countdown_seconds <= 0:
                pydirectinput.keyDown('f5')
                pydirectinput.keyUp('f5')
                self.countdown_seconds = interval_minutes * 60

    def update_countdown(self):
        minutes = self.countdown_seconds // 60
        seconds = self.countdown_seconds % 60
        self.label_countdown.config(text=f"Time until save: {minutes} minutes {seconds} seconds")

def main():
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure('Large.TButton', font=('Arial', 16))
    app = AutoSaveApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
