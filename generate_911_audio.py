# generate_911_audio.py

import pyttsx3

def generate_911_audio(text, filename, voice_id=None):
    engine = pyttsx3.init()
    if voice_id:
        engine.setProperty('voice', voice_id)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"Audio saved as {filename}")

def main():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # List available voices
    for idx, voice in enumerate(voices):
        print(f"Voice {idx}: {voice.name}")

    # Select a female voice (adjust the index as needed)
    female_voice_id = voices[1].id  # This is usually a female voice, but check the list

    # 911 emergency text
    emergency_text = "911, what's your emergency?"

    # Generate and save the 911 emergency audio file
    generate_911_audio(emergency_text, '911_emergency.mp3', female_voice_id)

if __name__ == "__main__":
    main()
