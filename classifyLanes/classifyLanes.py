from PIL import Image
import matplotlib.pyplot as plt
import os
import csv

# Global variable to store response
user_response = None

# Key press event handler
def on_key(event):
    global user_response
    key_map = {
        'q': 'hardL',
        'w': 'smoothL',
        'e': 'straight',
        'r': 'smoothR',
        't': 'hardR'
    }
    if event.key.lower() in key_map:
        user_response = key_map[event.key.lower()]
        plt.close()

# Function to open and display image, then get input via key press
def classify_lane(image_path, image_index):
    global user_response
    user_response = None
    try:
        # Open image
        img = Image.open(image_path)

        # Display image
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.axis('off')
        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.title("Press 'q'=hardL, 'w'=smoothL, 'e'=straight, 'r'=smoothR, 't'=hardR")
        plt.show()

        if user_response:
            print(f"Image {image_index}: {os.path.basename(image_path)} classified as: {user_response}.")
        else:
            print(f"Image {image_index}: {os.path.basename(image_path)} - No valid key pressed.")

        return user_response

    except Exception as e:
        print(f"Error opening or processing image: {e}")
        return None

# Example usage
# Replace 'path/to/your/images' with the actual directory path
image_directory = 'data/IMG'
output_file = 'lane_classification_2.csv'

# Open CSV file to write results
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Image Filename', 'Classification'])

    # Loop through all files in the directory that start with 'center' in alphabetical order
    for index, filename in enumerate(sorted(os.listdir(image_directory)), start=1):
        if filename.lower().startswith('center'):
            image_path = os.path.join(image_directory, filename)
            label = classify_lane(image_path, index)
            if label:
                writer.writerow([filename, label])
