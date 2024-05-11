# front.py

import tkinter as tk
from back import start_listening_thread, stop_listening_thread

should_respond = False

def start_recording():
    start_listening_thread()

def stop_recording():
    stop_listening_thread()

root = tk.Tk()
root.title("Speech Recognition")

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)
stop_button.config(state=tk.DISABLED)

root.mainloop()
