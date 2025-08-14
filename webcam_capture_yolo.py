import cv2
import sys
import time
import torch
import multiprocessing

def find_available_camera():
    for i in range(10):  # Check first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            return i
        cap.release()
    return None

def process_frame_from_queue(input_queue, output_queue):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='results/triangle_detection_run19/weights/best.pt')
        model.eval()  # Set the model to evaluation mode
        while True:
            frame = input_queue.get()
            if frame is None:  # Signal to stop
                break
            # Perform detection
            results = model(frame)
            # Render results on frame
            rendered_frame = results.render()[0]
            output_queue.put(rendered_frame)
    except Exception as e:
        print(f"Error in worker process: {e}")
    finally:
        output_queue.put(None)  # Signal that this process is done

def main():
    print(f"Python version: {sys.version}")
    print(f"OpenCV version: {cv2.__version__}")
    print(f"PyTorch version: {torch.__version__}")

    print("Initializing webcam...")
    camera_index = find_available_camera()
    if camera_index is None:
        print("No camera found")
        sys.exit(1)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Cannot open camera")
        sys.exit(1)

    print(f"Camera opened successfully at index {camera_index}")

    num_processes = 2  # Reduced from multiprocessing.cpu_count()
    input_queue = multiprocessing.Queue(maxsize=1)
    output_queue = multiprocessing.Queue()

    # Start worker processes
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=process_frame_from_queue, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    frame_count = 0
    last_frame_time = time.time()
    while True:
        current_time = time.time()
        if current_time - last_frame_time < 0.1:  # Limit to 10 fps
            continue
        last_frame_time = current_time

        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        if input_queue.empty():
            try:
                input_queue.put_nowait(frame)
                frame_count += 1
            except multiprocessing.queues.Full:
                pass  # Skip frame if queue is full

        if not output_queue.empty():
            rendered_frame = output_queue.get()
            if rendered_frame is not None:
                cv2.imshow('Triangle Detection', rendered_frame)

        if cv2.waitKey(1) == ord('q'):  # Quit on 'q' key
            break

    # Signal processes to stop
    for _ in range(num_processes):
        input_queue.put(None)

    # Wait for all processes to finish
    for p in processes:
        p.join()

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processed {frame_count} frames")
    print("Script completed")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")
