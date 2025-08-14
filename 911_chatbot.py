import tkinter as tk
from tkinter import simpledialog
import random

class Chatbot:
    def __init__(self, master):
        self.master = master
        self.master.title("911 Emergency Chatbot")
        self.master.geometry("400x600")

        self.chat_log = tk.Text(master, state='disabled', wrap='word', width=50, height=30)
        self.chat_log.pack(padx=10, pady=10)

        self.input_field = tk.Entry(master, width=50)
        self.input_field.pack(padx=10, pady=5)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.responses = {
            "triangle": "Can you provide more details about the situation?",
            "distressed": "Are there any immediate threats or injuries?",
            "lockdown": "I'm dispatching police and paramedics. Please stay on the line.",
            "en route": "Emergency services are en route. ETA 5-10 minutes.",
            "assist": "Is there anything else we should know?",
            "thank you": "You're welcome. Stay safe."
        }

        self.add_message("Operator", "911, what's your emergency?")

    def add_message(self, speaker, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, f"{speaker}: {message}\n\n")
        self.chat_log.config(state='disabled')
        self.chat_log.see(tk.END)

    def send_message(self, event=None):
        message = self.input_field.get()
        if message:
            self.add_message("You", message)
            self.input_field.delete(0, tk.END)
            self.respond_to_message(message)

    def respond_to_message(self, message):
        for keyword, response in self.responses.items():
            if keyword in message.lower():
                self.add_message("Operator", response)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()
