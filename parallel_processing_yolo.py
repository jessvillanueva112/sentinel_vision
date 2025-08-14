import cv2
import time
import numpy as np
import torch
import os
import subprocess
from multiprocessing import shared_memory
import pygame
from gtts import gTTS
import tempfile
import json
import random

# Initialize pygame mixer
pygame.mixer.init()

# Global variables
detection_status = "Not Started"
emergency_triggered = False
triangle_detection_start_time = None

# Emergency scenarios for random selection
threats = ["active shooter", "armed intruder", "bomb threat", "chemical spill", "hostage situation", "fire", "riot"]
locations = ["elementary school", "high school", "university campus", "school library", "science lab", "school cafeteria", "school gymnasium", "school auditorium", "school playground", "school bus depot"]

def find_available_camera():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            return i
        cap.release()
    return None

def get_triangle_color(roi):
    avg_color = np.mean(roi, axis=(0, 1))
    if avg_color[2] > 150 and avg_color[0] < 100 and avg_color[1] < 100:
        return "red"
    elif avg_color[1] > 150 and avg_color[0] < 100 and avg_color[2] < 100:
        return "green"
    elif avg_color[0] > 150 and avg_color[1] < 100 and avg_color[2] < 100:
        return "blue"
    elif avg_color[0] > 200 and avg_color[1] > 200 and avg_color[2] < 100:
        return "yellow"
    elif avg_color[2] > 150 and avg_color[0] > 150 and avg_color[1] < 100:
        return "pink"
    elif avg_color[2] > 150 and avg_color[1] > 100 and avg_color[0] < 100:
        return "orange"
    else:
        return "unknown"

def get_triangle_size(width, height):
    area = width * height
    if area < 5000:
        return "small"
    elif area < 20000:
        return "medium"
    else:
        return "large"

def update_detection_status(status):
    global detection_status
    detection_status = status
    with open("detection_status.txt", "w") as f:
        f.write(status)

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

def play_siren_sound():
    play_audio("mp3_sounds/siren_sound.mp3")

def trigger_emergency_sequence(color, size):
    global detection_status, emergency_triggered
    if emergency_triggered:
        return  # Prevent duplicate triggering
    print("Triggering emergency sequence...")
    update_detection_status("Emergency Triggered")
    emergency_triggered = True
    
    try:
        # Stage 1: Play alarm sound once
        update_detection_status("Alarm Activated")
        play_audio("mp3_sounds/alarm_sound.mp3")
        time.sleep(3)  # Allow alarm to play for 3 seconds
        
        # Stage 2: PA Announcement
        update_detection_status("PA Announcement In Progress")
        if color == "unknown" and size == "large":
            threat = random.choice(threats)
            location = random.choice(locations)
        else:
            threat = f"{color} {size} triangle"
            location = "school"
        text_to_speech(f"Attention! A {threat} has been detected at the {location}. This is not a drill. Please follow emergency procedures.")
        update_detection_status("PA Announcement Complete")
        time.sleep(2)  # Short pause after announcement
        
        # Stage 3: Play call sound to trigger 911 simulation
        update_detection_status("Initiating 911 Call")
        play_audio("mp3_sounds/call_sound.mp3")  # Make sure this file exists in the mp3_sounds directory
        time.sleep(2)  # Allow call sound to play for 2 seconds
        
        # Stage 4: 911 Simulation
        update_detection_status("911 Simulation In Progress")
        emergency_data = {"color": color, "size": size, "threat": threat, "location": location}
        emergency_data_path = os.path.join(os.getcwd(), "emergency_data.json")
        print(f"Attempting to create emergency_data.json at: {emergency_data_path}")
        with open(emergency_data_path, "w") as f:
            json.dump(emergency_data, f)
        print(f"Created emergency_data.json in {emergency_data_path}")
        time.sleep(1)  # Add a small delay to ensure the file is written
        
        # Run 911_jarvis.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        jarvis_script = os.path.join(script_dir, "911_jarvis.py")
        print(f"Running 911_jarvis.py with emergency data path: {emergency_data_path}")
        subprocess.run(["python", jarvis_script, emergency_data_path], check=True)
        
        # Wait for 911 simulation to complete
        while True:
            if os.path.exists("911_complete.txt"):
                os.remove("911_complete.txt")
                break
            time.sleep(0.1)
        
        # Stage 5: Play siren sound once to indicate emergency services arrival
        update_detection_status("Emergency Services Arriving")
        play_siren_sound()
        time.sleep(5)  # Allow siren to play for 5 seconds
        
        # Stage 6: Update status to completed
        update_detection_status("Emergency Sequence Completed")
    except Exception as e:
        print(f"Unexpected error during emergency sequence: {e}")
        update_detection_status("Emergency Sequence Failed")
    finally:
        emergency_triggered = False  # Reset the trigger

def process_frame(frame, model, shm_name, frame_shape):
    global triangle_detection_start_time, emergency_triggered

    frame = cv2.resize(frame, (frame_shape[1], frame_shape[0]))
    triangles = model(frame).xyxy[0].cpu().numpy()
    detected_triangles = []

    for det in triangles:
        if int(det[5]) == 0:  # Assuming 0 is the class index for triangles
            x1, y1, x2, y2 = map(int, det[:4])
            confidence = float(det[4])
            color = get_triangle_color(frame[y1:y2, x1:x2])
            size = get_triangle_size(x2 - x1, y2 - y1)
            detected_triangles.append((x1, y1, x2, y2, confidence, color, size))

    processed_frame = frame.copy()
    
    if detected_triangles:
        color = detected_triangles[0][5]
        size = detected_triangles[0][6]
        update_detection_status(f"Triangle detected: {color}, {size}")
        print(f"Triangle detected: {color}, {size}")

        current_time = time.time()
        if triangle_detection_start_time is None:
            triangle_detection_start_time = current_time
        elif current_time - triangle_detection_start_time >= 7 and not emergency_triggered:
            trigger_emergency_sequence(color, size)

        for x1, y1, x2, y2, conf, color, size in detected_triangles:
            cv2.rectangle(processed_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(processed_frame, f"{color} {size}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        update_detection_status("No triangle detected")
        print("No triangle detected")
        triangle_detection_start_time = None

    shm = shared_memory.SharedMemory(name=shm_name)
    np_array = np.ndarray(frame_shape, dtype=np.uint8, buffer=shm.buf)
    np_array[:] = processed_frame
    shm.close()

def main():
    model_path = '/Users/jvillanueva112/Downloads/new_tri_yolo_project/yolov5/runs/train/exp2/weights/best.pt'
    print(f"Loading model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return

    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        model = model.to('cuda' if torch.cuda.is_available() else 'cpu').eval()
        print(f"Model loaded successfully. Number of classes: {len(model.names)}")
        print(f"Class names: {model.names}")
    except Exception as e:
        print(f"Error loading the model: {e}")
        return

    camera_index = find_available_camera()
    if camera_index is None:
        print("No camera found")
        return

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    print(f"Camera opened successfully at index {camera_index}")

    frame_shape = (480, 640, 3)
    
    # Check if shared memory exists and unlink it
    try:
        existing_shm = shared_memory.SharedMemory(name="triangle_detection_frame")
        existing_shm.unlink()
    except FileNotFoundError:
        pass

    shm = shared_memory.SharedMemory(create=True, size=frame_shape[0] * frame_shape[1] * frame_shape[2], name="triangle_detection_frame")

    frame_count = 0
    last_frame_time = time.time()
    
    try:
        while True:
            current_time = time.time()
            if current_time - last_frame_time < 0.1:  # Limit to 10 fps
                continue
            last_frame_time = current_time

            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame. Exiting ...")
                break

            frame_count += 1
            if frame_count % 2 == 0:  # Process every other frame
                continue

            process_frame(frame, model, shm.name, frame_shape)

            if cv2.waitKey(1) == ord('q'):  # Quit on 'q' key
                break

    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        shm.close()
        shm.unlink()
        print(f"Processed {frame_count} frames")

if __name__ == "__main__":
    main()
