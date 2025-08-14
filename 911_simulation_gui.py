import tkinter as tk
import time
import random
from twilio.rest import Client

# Twilio credentials (replace with your own)
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
client = Client(account_sid, auth_token)

# Your phone numbers
twilio_number = 'YOUR_TWILIO_NUMBER'
your_number = 'YOUR_PERSONAL_NUMBER'

class EmergencyCallSimulator:
    def __init__(self, master):
        self.master = master
        master.title("911 Emergency Call")
        master.geometry("400x600")

        self.chat_log = tk.Text(master, state='disabled', wrap='word', width=50, height=30)
        self.chat_log.pack(padx=10, pady=10)

        self.input_field = tk.Entry(master, width=50)
        self.input_field.pack(padx=10, pady=5)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.conversation = [
            ("Operator", "911, what's your emergency?"),
            ("Caller", "A triangle has been detected at our location."),
            ("Operator", "Can you provide more details about the situation?"),
            ("Caller", "Our AI system detected a triangle. The subject appears distressed."),
            ("Operator", "Are there any immediate threats or injuries?"),
            ("Caller", "No immediate injuries, but the situation is tense. We've initiated lockdown."),
            ("Operator", "I'm dispatching police and paramedics. Please stay on the line."),
            ("Caller", "We'll maintain the lockdown until help arrives."),
            ("Operator", "Emergency services are en route. ETA 5-10 minutes."),
            ("Caller", "Understood. We're ready to assist when they arrive."),
            ("Operator", "Is there anything else we should know?"),
            ("Caller", "No, that's all the information we have now."),
            ("Operator", "Okay. Call back if anything changes. Help is coming."),
            ("Caller", "Thank you for your assistance."),
            ("Operator", "You're welcome. Stay safe.")
        ]

        self.current_message = 0
        self.master.after(1000, self.simulate_conversation)

    def simulate_conversation(self):
        if self.current_message < len(self.conversation):
            speaker, message = self.conversation[self.current_message]
            self.add_message(speaker, message)
            self.current_message += 1
            self.master.after(random.randint(2000, 4000), self.simulate_conversation)
        else:
            self.send_text_message()

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

    def send_text_message(self):
        scenarios = [
            "Triangle detected at Forest Hill High School, 123 10th Avenue, 2nd floor. Subject appears distressed.",
            "Triangle sighting at Central Park, 456 5th Avenue, near the fountain. Lockdown initiated.",
            "Triangle alert at Downtown Mall, 789 Main Street, food court area. Security notified.",
            "Triangle observed at City Library, 321 Book Lane, reference section. Staff evacuating.",
            "Triangle reported at Riverside Park, 654 Water Way, near playground. Park rangers alerted."
        ]

        message_body = f"EMERGENCY ALERT: {random.choice(scenarios)} Requesting immediate police and paramedic response."
        
        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=your_number
            )
            print(f"Text message sent: {message.sid}")
        except Exception as e:
            print(f"Error sending text message: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencyCallSimulator(root)
    root.mainloop()
