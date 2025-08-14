import sys
import pygame
import time
from gtts import gTTS
import os
import tempfile

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Emergency announcements based on triangle color and size
announcements = {
    "red": {
        "small": "Attention all students and staff. We have an active shooter situation. Implement lockdown procedures immediately. This is not a drill.",
        "medium": "Emergency alert. An armed intruder has been detected on campus. Secure your location and await further instructions from authorities.",
        "large": "Critical emergency. A potential terrorist threat has been identified. Evacuate the premises immediately following designated routes."
    },
    "blue": {
        "small": "Attention. A student with a weapon has been reported. Stay in your classrooms and lock the doors. Wait for further instructions.",
        "medium": "Alert. We have a hostage situation in progress. Avoid the affected area and follow staff directions for your safety.",
        "large": "Warning. A bomb threat has been received. Calmly evacuate the building using the nearest exit. Do not use elevators."
    },
    "yellow": {
        "small": "Caution. A chemical spill has occurred in the science lab. Avoid the area. Ventilation systems are being shut down.",
        "medium": "Alert. A gas leak has been detected. Evacuate the building immediately. Do not use any electrical devices or open flames.",
        "large": "Warning. A hazardous material incident is in progress. Shelter in place and seal all windows and doors. Wait for further instructions."
    },
    "green": {
        "small": "Attention. A suspicious package has been found. Do not approach or touch any unattended items. Report any suspicious objects to staff.",
        "medium": "Notice. A student protest is occurring on campus. Please avoid the area and continue with your regular activities.",
        "large": "Weather alert. Severe weather is approaching. Move to designated shelter areas within the building immediately."
    },
    "pink": {
        "small": "Medical emergency in progress. Please clear hallways for medical personnel. Avoid the affected area.",
        "medium": "Attention. We have a missing student. All staff please implement search protocols. Students, return to your classrooms.",
        "large": "Fire alert. The fire alarm is not a drill. Evacuate the building calmly using the nearest exit. Do not use elevators."
    },
    "orange": {
        "small": "Attention students. Bullying is not tolerated. If you see something, say something. Report incidents to staff immediately.",
        "medium": "Security alert. A fight has broken out. All students clear the area. Teachers, implement de-escalation procedures.",
        "large": "Emergency. Civil disturbance on campus. All students and staff, lock down in place. Close and secure all doors and windows."
    }
}

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        play_audio(fp.name)
    os.unlink(fp.name)

def update_status(status):
    with open("detection_status.txt", "w") as f:
        f.write(status)

def make_announcement(color, size):
    announcement = announcements.get(color, {}).get(size, "Attention. An unspecified emergency has been detected. Please stand by for further instructions.")
    
    update_status("PA Announcement In Progress")
    print("Playing alarm sound...")
    play_audio("mp3_sounds/alarm_sound.mp3")
    time.sleep(3)  # Allow alarm to play for 3 seconds
    
    print("Playing PA announcement...")
    text_to_speech(announcement)
    
    print("PA announcement complete.")
    update_status("PA Announcement Complete")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        make_announcement(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pa_announcement.py <color> <size>")
