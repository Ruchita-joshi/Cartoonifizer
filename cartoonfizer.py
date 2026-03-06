from flask import Flask, request, send_file, Response
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cartoonify_image(image_path, style):
    """Applies a selected cartoon style to an image."""
    img = cv2.imread(image_path)
    if img is None:
        return None
    if style == "classic":
        return classic_cartoon(img)
    elif style == "sketch":
        return sketch_style(img)
    else:
        return img  # Default to normal image if invalid style

def cartoonify_frame(frame):
    """Applies only classic cartoon effect to webcam frames."""
    return enhanced_cartoon(frame)

def classic_cartoon(img):
    """Applies a classic cartoon effect."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3),0)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
    color = cv2.bilateralFilter(img, 9, 150, 150)
    return cv2.bitwise_and(color, color, mask=edges)

def enhanced_cartoon(img):
    """Enhances the cartoon effect for webcam frames."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3),0)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 350, 350)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def sketch_style(img):
    """Applies a pencil sketch effect."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    return cv2.divide(gray, 255 - blur, scale=256)

@app.route('/')
def home():
    return HOME_HTML

@app.route('/image_upload')
def image_upload():
    return IMAGE_UPLOAD_HTML

@app.route('/cartoonify', methods=['POST'])
def cartoonify():
    """Handles image upload and applies selected cartoon style."""
    if 'image' not in request.files:
        return "No file selected", 400
    file = request.files['image']
    style = request.form.get("style", "classic")  # Default to "classic" if not selected
    if file.filename == '':
        return "No selected file", 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    cartoon = cartoonify_image(filepath, style)
    if cartoon is None:
        return "Invalid image", 400
    output_path = os.path.join(OUTPUT_FOLDER, f'cartoon_{filename}')
    cv2.imwrite(output_path, cartoon)
    return send_file(output_path, mimetype='image/png')

def generate_frames():
    """Generates enhanced cartoonified webcam frames."""
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            cartoon = cartoonify_frame(frame)
            _, buffer = cv2.imencode('.jpg', cartoon)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    """Streams enhanced cartoonified webcam video."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cartoonify App</title>
    <style>
        body {
            background-image: url('/static/cartoon.jpg');
            background-size:cover;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
            padding: 50px;
        }
        h1, h2 {
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
        }
        .button {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            margin: 20px;
            transition: 0.3s ease-in-out;
        }
        .button:hover {
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <h1>Cartoonify Your Images</h1>
    <h2>Select an Option</h2>
    <button class="button" onclick="window.location.href='/image_upload'">Upload Image</button>
    <button class="button" onclick="window.location.href='/video_feed'">Live Cartoonify (Webcam)</button>
</body>
</html>
"""

IMAGE_UPLOAD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Upload Image</title>
    <style>
        body {
            background-image: url('/static/Images.png');
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
            padding: 50px;
        }
        select, input {
            margin: 10px;
            font-size: 1.2em;
            padding: 10px;
        }
        .button {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.2rem;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease-in-out;
        }
        .button:hover {
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <h2>Upload an Image to Cartoonify</h2>
    <form action="/cartoonify" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <br>
        <label>Select Style:</label>
        <select name="style">
            <option value="classic">Classic Cartoon</option>
            <option value="sketch">Sketch Effect</option>
        </select>
        <br>
        <button class="button" type="submit">Cartoonify</button>
    </form>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
