import os
import subprocess
import threading

def run_parallel_processing():
    subprocess.run(["python", "parallel_processing_yolo.py"])

def run_control_board():
    subprocess.run(["python", "control_board.py"])

if __name__ == "__main__":
    # Set the working directory to the script's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start parallel processing in a separate thread
    processing_thread = threading.Thread(target=run_parallel_processing)
    processing_thread.start()

    # Run control board in the main thread
    run_control_board()

    # Wait for the processing thread to finish
    processing_thread.join()
