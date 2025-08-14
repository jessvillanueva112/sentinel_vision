import customtkinter as ctk
import threading
import time
import os
from PIL import Image
import numpy as np
import cv2
from multiprocessing import shared_memory
from tkinter import messagebox
import pygame
import json
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ControlBoard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.attributes('-fullscreen', True)
        self.root.title("Sentinel Vision Control Board")

        self.create_widgets()
        self.process_thread = None
        self.running = False
        self.update_thread = None
        pygame.mixer.init()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(main_frame, text="Sentinel Vision Control Board", font=ctk.CTkFont(size=36, weight="bold"))
        title_label.pack(pady=20)

        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_process, width=150, height=50, font=ctk.CTkFont(size=18))
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_process, width=150, height=50, font=ctk.CTkFont(size=18))
        self.stop_button.pack(side="left", padx=10)

        self.refresh_button = ctk.CTkButton(button_frame, text="Refresh", command=self.refresh_status, width=150, height=50, font=ctk.CTkFont(size=18))
        self.refresh_button.pack(side="left", padx=10)

        self.restart_button = ctk.CTkButton(button_frame, text="Restart", command=self.restart_process, width=150, height=50, font=ctk.CTkFont(size=18))
        self.restart_button.pack(side="left", padx=10)

        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(pady=20, fill="x", padx=20)

        self.detection_status_label = self.create_status_label(status_frame, "Detection Status:")
        self.alarm_status_label = self.create_status_label(status_frame, "Alarm Status:")
        self.pa_status_label = self.create_status_label(status_frame, "PA Announcement:")
        self.simulation_status_label = self.create_status_label(status_frame, "911 Simulation:")

        self.progress_bar = ctk.CTkProgressBar(main_frame, height=20)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.set(0)

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.video_frame = ctk.CTkLabel(content_frame)
        self.video_frame.pack(side="left", padx=10, fill="both", expand=True)

        self.conversation_log = ctk.CTkTextbox(content_frame, height=400, width=400)
        self.conversation_log.pack(side="right", padx=10, fill="both", expand=True)

    def create_status_label(self, parent, text):
        frame = ctk.CTkFrame(parent)
        frame.pack(pady=10, fill="x")
        
        label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(side="left", padx=10)
        
        status = ctk.CTkLabel(frame, text="Not Started", font=ctk.CTkFont(size=20))
        status.pack(side="right", padx=10)
        
        return status

    def start_process(self):
        if self.process_thread is None or not self.process_thread.is_alive():
            self.running = True
            self.clear_previous_data()
            self.process_thread = threading.Thread(target=self.run_detection_process)
            self.process_thread.start()
            self.update_status("Running", "Not Triggered", "Not Triggered", "Not Triggered")
            self.start_status_update()
        else:
            messagebox.showinfo("Info", "Process is already running")

    def stop_process(self):
        self.running = False
        self.update_status("Stopped", "Not Triggered", "Not Triggered", "Not Triggered")
        self.progress_bar.set(0)
        if self.update_thread:
            self.update_thread.join()
        if self.process_thread:
            self.process_thread.join(timeout=5)  # Wait for up to 5 seconds
        self.clear_shared_memory()

    def refresh_status(self):
        self.clear_previous_data()
        self.update_status("Simulation Complete", "Not Triggered", "Not Triggered", "Not Triggered")
        self.progress_bar.set(0)
        self.clear_shared_memory()

    def restart_process(self):
        self.stop_process()
        time.sleep(1)  # Wait for processes to stop
        self.start_process()

    def start_status_update(self):
        self.update_thread = threading.Thread(target=self.update_status_loop)
        self.update_thread.start()

    def update_status_loop(self):
        while self.running:
            self.read_detection_status()
            self.update_video_frame()
            self.update_conversation_log()
            time.sleep(0.1)  # Update more frequently for smoother video

    def read_detection_status(self):
        try:
            with open("detection_status.txt", "r") as f:
                status = f.read().strip()
            self.parse_and_update_status(status)
        except FileNotFoundError:
            self.update_status("Status Unknown", "Not Triggered", "Not Triggered", "Not Triggered")

    def parse_and_update_status(self, status):
        if "Triangle detected:" in status:
            self.update_status(status, "Not Triggered", "Not Triggered", "Not Triggered")
            self.progress_bar.set(0.25)
        elif "Emergency Triggered" in status:
            self.update_status("Emergency Triggered", "Activated", "Not Triggered", "Not Triggered")
            self.progress_bar.set(0.5)
        elif "PA Announcement Complete" in status:
            self.update_status("Emergency Triggered", "Activated", "Completed", "In Progress")
            self.progress_bar.set(0.75)
        elif "Emergency Sequence Completed" in status:
            self.update_status("Emergency Triggered", "Activated", "Completed", "Completed")
            self.progress_bar.set(1.0)
        else:
            self.update_status(status, "Not Triggered", "Not Triggered", "Not Triggered")
            self.progress_bar.set(0)

    def update_status(self, detection_status, alarm_status, pa_status, simulation_status):
        self.detection_status_label.configure(text=detection_status)
        self.alarm_status_label.configure(text=alarm_status)
        self.pa_status_label.configure(text=pa_status)
        self.simulation_status_label.configure(text=simulation_status)

    def update_video_frame(self):
        try:
            shm = shared_memory.SharedMemory(name="triangle_detection_frame")
            frame_shape = (480, 640, 3)
            np_array = np.ndarray(frame_shape, dtype=np.uint8, buffer=shm.buf)
            frame = np_array.copy()
            shm.close()
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
            self.video_frame.configure(image=img)
            self.video_frame.image = img
        except FileNotFoundError:
            pass

    def update_conversation_log(self):
        try:
            with open("conversation_log.txt", "r") as f:
                conversation_log = f.read()
            self.conversation_log.delete("1.0", ctk.END)
            self.conversation_log.insert(ctk.END, conversation_log)
        except FileNotFoundError:
            pass

    def clear_previous_data(self):
        open("detection_status.txt", "w").close()
        open("conversation_log.txt", "w").close()
        open("911_status.txt", "w").close()
        if os.path.exists("emergency_data.json"):
            os.remove("emergency_data.json")
        if os.path.exists("911_complete.txt"):
            os.remove("911_complete.txt")

    def clear_shared_memory(self):
        try:
            shm = shared_memory.SharedMemory(name="triangle_detection_frame")
            shm.close()
            shm.unlink()
        except FileNotFoundError:
            pass

    def run_detection_process(self):
        try:
            self.update_status("Running", "Not Triggered", "Not Triggered", "Not Triggered")
            while self.running:
                time.sleep(0.1)  # Sleep to prevent high CPU usage
                if os.path.exists("emergency_data.json"):
                    with open("emergency_data.json", "r") as f:
                        data = json.load(f)
                    os.remove("emergency_data.json")
                    self.run_911_simulation(data["color"], data["size"], data["threat"], data["location"])
        except Exception as e:
            print(f"Error in detection process: {e}")
            self.update_status("Error", "Error", "Error", "Error")
        finally:
            self.running = False
            self.progress_bar.set(0)
            self.clear_shared_memory()

    def run_911_simulation(self, color, size, threat, location):
        try:
            self.update_status("Emergency Triggered", "Activated", "Completed", "In Progress")
            subprocess.run(["python", "911_jarvis.py"], check=True)
            self.update_status("Emergency Triggered", "Activated", "Completed", "Completed")
            with open("911_complete.txt", "w") as f:
                f.write("complete")
        except subprocess.CalledProcessError:
            self.update_status("Error", "Error", "Error", "Error")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Sentinel Vision Control Board Initializing...")
    app = ControlBoard()
    app.run()
