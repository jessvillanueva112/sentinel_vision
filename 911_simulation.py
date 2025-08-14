import time
import random
import subprocess
import os
import pygame
from twilio.rest import Client

# Twilio credentials (replace with your own)
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
client = Client(account_sid, auth_token)

# Your phone numbers
twilio_number = ''  # Your Twilio number
your_number = ''  # Your personal number

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def send_text_message():
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

def simulate_conversation():
    conversation = [
        "911 Operator: 911, what's your emergency?",
        "Caller: A triangle has been detected at the location I just reported.",
        "911 Operator: Understood. Can you provide more details about the situation?",
        "Caller: Our AI system detected a triangle. The subject appears distressed.",
        "911 Operator: Are there any immediate threats or injuries?",
        "Caller: No immediate injuries, but the situation is tense. We've initiated lockdown.",
        "911 Operator: I'm dispatching police and paramedics. Please stay on the line.",
        "Caller: We'll maintain the lockdown until help arrives.",
        "911 Operator: Emergency services are en route. ETA 5-10 minutes.",
        "Caller: Understood. We're ready to assist when they arrive.",
        "911 Operator: Is there anything else we should know?",
        "Caller: No, that's all the information we have now.",
        "911 Operator: Okay. Call back if anything changes. Help is coming.",
        "Caller: Thank you for your assistance.",
        "911 Operator: You're welcome. Stay safe."
    ]

    for line in conversation:
        print(line)
        time.sleep(2)  # Pause between lines to simulate conversation timing

def main():
    print("Starting 911 Call Simulation")
    
    # Play calling sound
    print("Simulating phone call...")
    play_audio("mp3_sounds/calling_sound.mp3")
    
    # Play 911 emergency sound
    print("911 operator answering...")
    play_audio("mp3_sounds/911_emergency.mp3")
    
    # Send text message
    print("Sending emergency text message...")
    send_text_message()
    
    # Simulate conversation
    print("\nSimulating 911 conversation:")
    simulate_conversation()
    
    print("\nParamedics and police have arrived on site. Simulation complete.")

if __name__ == "__main__":
    main()
