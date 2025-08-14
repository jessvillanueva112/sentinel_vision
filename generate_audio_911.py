import subprocess

def generate_audio(text, filename, voice="Siri"):
    subprocess.run(['say', '-v', voice, '-o', filename, text])

emergency_text = "911, what's your emergency?"
generate_audio(emergency_text, "911_emergency.aiff", voice="Siri")

print("Audio file generated: 911_emergency.aiff")
