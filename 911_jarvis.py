import os
import tempfile
import pygame
import time
from gtts import gTTS
import random
import json
import sys

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def speak(text, is_caller=True):
    tts = gTTS(text=text, lang='en', tld='com' if is_caller else 'co.uk', slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        play_audio(fp.name)
    os.unlink(fp.name)

def update_status(status):
    with open("911_status.txt", "w") as f:
        f.write(status)

def log_conversation(speaker, text):
    with open("conversation_log.txt", "a") as f:
        f.write(f"{speaker}: {text}\n")

def generate_caller_response(context):
    locations = ['exit', "principal's office", 'crowded hallway']
    responses = [
        f"We're hiding in the {context['location']}. What should we do?",
        f"I can see the {context['threat']} from here. They're {random.choice(['armed', 'acting erratically', 'threatening students'])}.",
        f"There are about {random.randint(5, 30)} students near me. We're all very scared.",
        f"The {context['threat']} is moving towards the {random.choice(locations)}.",
        f"I think I heard {random.choice(['gunshots', 'screaming', 'explosions'])}. Please hurry!",
        f"There are {random.choice(['young children', 'special needs students', 'injured students'])} here. We need help fast!",
        f"The {context['threat']} is {random.choice(['making demands', 'becoming more aggressive', 'trying to break into classrooms'])}.",
        f"I can see {random.choice(['police cars', 'an ambulance', 'a SWAT team'])} arriving at the school. Are they here for us?",
        "What's taking so long? The situation in the school is getting worse!",
        f"I think there might be multiple {context['threat']}s in the school. What should we do?"
    ]
    return random.choice(responses)

def generate_operator_response(context):
    responses = [
        f"Stay calm. Can you give me more details about the {context['threat']} in the {context['location']}?",
        f"Are you in a safe place within the {context['location']}? Try to stay hidden and quiet.",
        "How many students are with you? Is anyone injured?",
        "Emergency services are on their way to the school. Can you see any safe exits?",
        f"Do not approach the {context['threat']}. Stay hidden and wait for help to arrive at the school.",
        "Can you describe the current situation in the school? Has anything changed?",
        "If it's safe to do so, try to lock the doors or barricade the entrances to your location.",
        "Are there any teachers or school staff members who can help?",
        "Remember, your safety is the top priority. Follow any instructions from school authorities or emergency responders when they arrive.",
        f"Can you see or hear where the {context['threat']} is now in the school? Don't put yourself at risk to find out."
    ]
    return random.choice(responses)

def handle_conversation(context):
    update_status("911 Simulation In Progress")
    print("Operator: 911, what's your emergency?")
    speak("911, what's your emergency?", is_caller=False)
    log_conversation("Operator", "911, what's your emergency?")
    
    initial_report = f"There's {context['threat']} at {context['location']}!"
    print(f"Caller: {initial_report}")
    speak(initial_report, is_caller=True)
    log_conversation("Caller", initial_report)
    
    for _ in range(5):  # 5 exchanges
        operator_response = generate_operator_response(context)
        print(f"Operator: {operator_response}")
        speak(operator_response, is_caller=False)
        log_conversation("Operator", operator_response)
        
        time.sleep(1)
        
        caller_response = generate_caller_response(context)
        print(f"Caller: {caller_response}")
        speak(caller_response, is_caller=True)
        log_conversation("Caller", caller_response)
        
        time.sleep(1)
    
    final_message = f"Emergency services have arrived at the {context['location']}. Stay where you are and wait for help. You're going to be okay."
    print(f"Operator: {final_message}")
    speak(final_message, is_caller=False)
    log_conversation("Operator", final_message)

def run_911_simulation():
    print("911 Simulation Started")
    update_status("911 Simulation Started")
    
    try:
        emergency_data_path = sys.argv[1] if len(sys.argv) > 1 else "emergency_data.json"
        print(f"Attempting to read emergency data from: {emergency_data_path}")
        
        if not os.path.exists(emergency_data_path):
            print(f"Error: File not found at {emergency_data_path}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Files in current directory: {os.listdir()}")
            raise FileNotFoundError(f"emergency_data.json not found at {emergency_data_path}")

        with open(emergency_data_path, "r") as f:
            context = json.load(f)
        
        handle_conversation(context)
        
        print("911 Simulation Completed")
        update_status("911 Simulation Completed")
        with open("911_complete.txt", "w") as f:
            f.write("complete")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print(f"Error: {emergency_data_path} is not a valid JSON file.")
    except Exception as e:
        print(f"Unexpected error in 911 simulation: {e}")

if __name__ == "__main__":
    run_911_simulation()
