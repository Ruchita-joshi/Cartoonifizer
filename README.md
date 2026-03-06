# Cartoonifizer
# 🎨 Cartoonifizer - Image & Live Webcam Cartoon Generator

Cartoonifizer is a web-based application built using Flask and OpenCV that converts normal images and live webcam video into cartoon-style visuals.

The application allows users to upload images and apply different cartoon effects or view a real-time cartoonified video stream from their webcam.

---

## 🚀 Features

• Upload an image and convert it into a cartoon version  
• Multiple cartoon styles available  
• Classic Cartoon Effect  
• Pencil Sketch Effect  
• Live webcam cartoonification  
• Real-time image processing using OpenCV  
• Simple and interactive web interface  

---

## 🛠 Technologies Used

Python

Flask – Web framework used to build the web application

OpenCV – Image processing and computer vision

NumPy – Numerical operations for image processing

Werkzeug – Secure file upload handling

HTML + CSS – Frontend user interface

---

## 📂 Project Structure
Cartoonifizer<br>
│
├── uploads/ # Uploaded images<br>
├── output/ # Processed cartoon images<br>
├── static/ # Background images for UI<br>
│
├── cartoonfizer.py # Main Flask application<br>
├── requirements.txt # Project dependencies<br>
└── README.md # Project documentation


---

## 🎯 How It Works

### Image Cartoonification

1. User uploads an image
2. User selects a cartoon style
3. The image is processed using OpenCV
4. The cartoonified image is returned and displayed

### Live Webcam Cartoonification

1. Webcam is accessed using OpenCV
2. Frames are captured continuously
3. Cartoon filter is applied to each frame
4. Frames are streamed through Flask as a live video feed

---

## 🖼 Cartoon Effects Implemented

### 1️⃣ Classic Cartoon Effect

Steps:<br>
• Convert image to grayscale  
• Apply Gaussian Blur  
• Detect edges using Adaptive Threshold  
• Apply Bilateral Filtering to smooth colors  
• Combine edges with color image  

---

### 2️⃣ Enhanced Cartoon (Webcam)

Improved parameters for stronger cartoon effect:
• Stronger bilateral filtering
• Larger edge detection block size

---

### 3️⃣ Pencil Sketch Effect

Steps:<br>
• Convert image to grayscale  
• Invert grayscale image  
• Apply Gaussian blur  
• Blend images using divide operation to create sketch effect  

---

## ⚙ Installation

### 1️⃣ Clone the repository
https://github.com/Ruchita-joshi/Cartoonifizer


### 2️⃣ Navigate to project folder
cd Cartoonifizer


### 3️⃣ Install dependencies
pip install -r requirements.txt


---

## ▶ Running the Application

Run the Flask server:
python cartoonfizer.py


Then open your browser and go to:
http://127.0.0.1:5000


---

## 📸 Application Interface

Home Page Options:

• Upload Image  
• Live Webcam Cartoonify  

---

## 📈 Future Improvements

• More cartoon styles  
• Anime style filter  
• Download cartoon images option  
• Deploy the project online  
• Add deep learning based cartoon filters  

---

## 🎓 Educational Purpose

This project demonstrates concepts of:

• Image Processing  
• Computer Vision  
• Real-time video processing  
• Flask Web Development  
• File Upload Handling  

---

## 👩‍💻 Author

Developed by **Ruchita Joshi**

MCA Student 

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

