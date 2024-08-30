from flask import Flask, request, render_template
import torch
from PIL import Image
import io
import os

# Initialize Flask app
app = Flask(__name__)

# Load your custom YOLOv5 model
model = torch.hub.load('/Users/priyanshubehere/Desktop/yolov5', 'custom', path='/Users/priyanshubehere/Desktop/yolov5-fastapi/best (3).pt', source='local')

# Set the base path for saving output images
BASE_OUTPUT_FOLDER = 'static'
if not os.path.exists(BASE_OUTPUT_FOLDER):
    os.makedirs(BASE_OUTPUT_FOLDER)

# Variable to keep track of the folder number
folder_counter = 0

@app.route('/', methods=['GET'])
def home():
    global folder_counter
    folder_counter = (folder_counter + 1) % 1000  # Ensure folder_counter stays within bounds (e.g., 0-999)
    current_folder = f"{BASE_OUTPUT_FOLDER}{folder_counter}"
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)
    return render_template('index.html', current_folder=folder_counter)

@app.route('/predict', methods=['POST'])
def predict():
    global folder_counter
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No file selected"

    if file:
        # Read image
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        # Perform inference with custom save directory
        current_folder = f"{BASE_OUTPUT_FOLDER}{folder_counter}"
        results = model(img)
        results.save(save_dir=current_folder)  # Save in the current folder

        # Get the output file path (assume single output file)
        output_image = [f for f in os.listdir(current_folder) if f.endswith('.jpg')][0]
        output_image_path = os.path.join(current_folder, output_image)

        return render_template('index.html', output_image=os.path.join(f"{folder_counter}", output_image))

if __name__ == '__main__':
    app.run(debug=True)
