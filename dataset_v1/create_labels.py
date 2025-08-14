import os
from PIL import Image

def create_label(image_path, label_path):
    with Image.open(image_path) as img:
        width, height = img.size
    
    # Create a default bounding box in the center of the image
    # covering 50% of the image width and height
    x_center = 0.5
    y_center = 0.5
    box_width = 0.5
    box_height = 0.5

    with open(label_path, 'w') as f:
        f.write(f"0 {x_center} {y_center} {box_width} {box_height}\n")

image_dir = 'images'
label_dir = 'labels'

for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_dir, filename)
        label_path = os.path.join(label_dir, os.path.splitext(filename)[0] + '.txt')
        
        if not os.path.exists(label_path):
            print(f"Creating label for {filename}")
            create_label(image_path, label_path)

print("Finished creating labels.")
