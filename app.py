# x1
import streamlit as st
from ultralytics import YOLO
import pandas as pd
import matplotlib.pyplot as plt
import torch
import cv2
import numpy as np
import plotly.express as px
from PIL import Image

# Set Page Configuration
st.set_page_config(page_title="NeuroRide-BETA", layout="wide")

# Sidebar for Mode Selection (Will be replaced with buttons in Part 2)
st.sidebar.title("Navigation")

st.title("🚀 NeuroRide")
st.write("A smart helmet & number plate detection system.")

# Load Model
model = YOLO(r"D:\AIML Projects\Trainedweights\NeuroRide\train\weights\best.pt")  # Update path

# Define state variables for file and settings
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "confidence_threshold" not in st.session_state:
    st.session_state.confidence_threshold = 0.5

if "show_bboxes" not in st.session_state:
    st.session_state.show_bboxes = True

# Function to Process Image
def process_image(image):
    results = model(image)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            conf = box.conf[0]  # Confidence score
            
            if conf >= st.session_state.confidence_threshold:  # Apply confidence filter
                if st.session_state.show_bboxes:
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(image, f"Conf: {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# Upload & Detect Section
st.subheader("Upload Image/Video for Detection")
st.session_state.uploaded_file = st.file_uploader("Choose an image/video", type=["jpg", "jpeg", "png", "mp4"])

if st.session_state.uploaded_file is not None:
    file_bytes = np.asarray(bytearray(st.session_state.uploaded_file.read()), dtype=np.uint8)

    if st.session_state.uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        processed_img = process_image(img)
        st.image(processed_img, caption="Processed Image", use_container_width=True)

        st.download_button(label="📥 Download Processed Image", data=cv2.imencode('.jpg', processed_img)[1].tobytes(),
                           file_name="output.jpg", mime="image/jpeg")

    elif st.session_state.uploaded_file.type == "video/mp4":
        st.video(st.session_state.uploaded_file)

# x2
# x2

# NeuroRide Logo & Header Enhancements
logo_url = "https://raw.githubusercontent.com/ShivankXD/ShivankXD/main/NeuroRidedet.png"
st.markdown(
    f"""
    <style>
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #1e1e1e;
            border-radius: 10px;
        }}
        .header-left {{
            display: flex;
            align-items: center;
        }}
        .header-right {{
            display: flex;
            gap: 20px;
        }}
        .header-button {{
            background-color: #3c3c3c;
            padding: 8px 15px;
            border-radius: 5px;
            text-decoration: none;
            color: white;
            font-weight: bold;
        }}
        .header-button:hover {{
            background-color: #565656;
        }}
        .neural-symbol {{
            width: 40px;
            height: 40px;
            cursor: pointer;
        }}
        .neural-symbol:hover {{
            filter: drop-shadow(0px 0px 8px #00ffcc);
        }}
        .neuro-title {{
            font-size: 32px;
            font-weight: bold;
            color: white;
        }}
        .beta {{
            font-size: 12px;
            vertical-align: super;
            opacity: 0.7;
        }}
    </style>
    <div class="header-container">
        <div class="header-left">
            <img src="{logo_url}" width="60px" alt="NeuroRide Logo">
            <span class="neuro-title">NeuroRide<span class="beta">Beta</span></span>
        </div>
        <div class="header-right">
            <a href="#" id="home-btn" class="header-button">Home</a>
            <a href="#" id="detect-btn" class="header-button">Upload & Detect</a>
            <a href="#" id="visual-btn" class="header-button">Visualizations</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Bike Animation (Moving on a Mountain Road)
st.markdown(
    """
    <style>
        @keyframes moveBike {
            0% { transform: translateX(-20px); }
            50% { transform: translateX(20px); }
            100% { transform: translateX(-20px); }
        }
        .bike-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .bike-img {
            width: 120px;
            animation: moveBike 3s infinite alternate ease-in-out;
        }
    </style>
    <div class="bike-container">
        <img src="https://source.unsplash.com/120x120/?motorbike" class="bike-img" alt="Moving Bike">
    </div>
    """,
    unsafe_allow_html=True
)

# Handling Button Clicks in Streamlit
selected_page = st.session_state.get("page", "Home")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"

with col2:
    if st.button("📤 Upload & Detect"):
        st.session_state.page = "Upload & Detect"

with col3:
    if st.button("📊 Visualizations"):
        st.session_state.page = "Visualizations"

# Render the selected page
if st.session_state.page == "Home":
    st.subheader("Welcome to NeuroRide!")
    st.write("""
        - **Upload images/videos** for helmet & number plate detection.  
        - **Check visualizations** of model performance.  
        - **Download processed outputs**.  
    """)
elif st.session_state.page == "Upload & Detect":
    st.subheader("Upload & Detect Page")  # This part will continue in Part 3.
elif st.session_state.page == "Visualizations":
    st.subheader("Visualizations Page")  # Widget implementation in Part 3.

# x3
# x3

# Sliding Detection Settings Panel
st.markdown(
    """
    <style>
        .settings-panel {
            position: fixed;
            top: 0;
            left: -300px;
            width: 280px;
            height: 100%;
            background-color: #222;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
            padding: 20px;
            transition: left 0.4s ease-in-out;
        }
        .settings-panel.open {
            left: 0;
        }
        .close-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 20px;
            color: white;
        }
    </style>
    <div id="settingsPanel" class="settings-panel">
        <span class="close-btn" onclick="closePanel()">×</span>
        <h3 style="color: white;">Detection Settings</h3>
        <label style="color: white;"><input type="checkbox"> Enable Helmet Detection</label><br>
        <label style="color: white;"><input type="checkbox"> Enable Number Plate Recognition</label><br>
        <label style="color: white;"><input type="checkbox"> Highlight Violations</label><br>
    </div>
    <script>
        function openPanel() {
            document.getElementById("settingsPanel").classList.add("open");
        }
        function closePanel() {
            document.getElementById("settingsPanel").classList.remove("open");
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Neural Symbol (Click to Open Panel)
st.markdown(
    """
    <style>
        .neural-symbol-container {
            position: fixed;
            top: 20px;
            left: 20px;
            cursor: pointer;
        }
    </style>
    <div class="neural-symbol-container" onclick="openPanel()">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Neural_Network.svg/120px-Neural_Network.svg.png" width="40">
    </div>
    """,
    unsafe_allow_html=True
)

# Visualization Widget
st.markdown(
    """
    <style>
        .visual-widget {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 300px;
            background-color: white;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            display: none;
        }
        .close-visual {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 18px;
        }
    </style>
    <div id="visualWidget" class="visual-widget">
        <span class="close-visual" onclick="closeVisual()">×</span>
        <h3>Visualization Panel</h3>
        <p>Graph-based insights will be displayed here.</p>
    </div>
    <script>
        function openVisual() {
            document.getElementById("visualWidget").style.display = "block";
        }
        function closeVisual() {
            document.getElementById("visualWidget").style.display = "none";
        }
        document.addEventListener("keydown", function(event) {
            if (event.key === "Escape") {
                closeVisual();
            }
        });
    </script>
    """,
    unsafe_allow_html=True
)

# Visualization Button (Opens Widget)
if st.button("📊 Open Visualizations"):
    st.markdown('<script>openVisual();</script>', unsafe_allow_html=True)

# x4
# x4

# Fix: Ensure uploaded_file is defined before use
uploaded_file = None  

# File Upload Section
st.subheader("Upload Image/Video for Detection")
uploaded_file = st.file_uploader("Choose an image/video", type=["jpg", "jpeg", "png", "mp4"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

    if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        # Perform YOLO inference
        results = model(img)

        # Draw bounding boxes (if enabled)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
                conf = box.conf[0]  # Confidence score
                
                if conf >= confidence_threshold:  # Apply confidence filter
                    if show_bboxes:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, f"Conf: {conf:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        st.image(img, caption="Processed Image", use_container_width=True)

        # Download Button for Processed Image
        st.download_button(label="📥 Download Processed Image", data=cv2.imencode('.jpg', img)[1].tobytes(),
                           file_name="output.jpg", mime="image/jpeg")

elif uploaded_file and uploaded_file.type == "video/mp4":
    st.video(uploaded_file)

# x5
