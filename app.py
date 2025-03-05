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

# Sidebar for Mode Selection
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Mode", ["Home", "Upload & Detect", "Visualizations"])

st.title("🚀 NeuroRide-BETA")
st.write("A smart helmet & number plate detection system.")

# Load Model
model = YOLO(r"D:\AIML Projects\Trainedweights\NeuroRide\train\weights\best.pt")  # Update path

if page == "Home":
    st.subheader("Welcome to NeuroRide!")
    st.write("""
        ![](NeuroRide.png)
        - **Upload images/videos** for helmet & number plate detection.  
        - **Check visualizations** of model performance.  
        - **Download processed outputs**.  
        - ### Note : **This is not a final product but a Beta Version**
    """)
    st.image("https://source.unsplash.com/800x400/?motorbike,helmet", use_container_width=True)

elif page == "Upload & Detect":
    st.subheader("Upload Image/Video for Detection")

    uploaded_file = st.file_uploader("Choose an image/video", type=["jpg", "jpeg", "png", "mp4"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

        if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            st.image(img, caption="Uploaded Image", use_container_width=True)

            # Perform YOLO inference
            results = model(img)

            # Draw bounding boxes
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
                    conf = box.conf[0]  # Confidence score

                    # Draw on image
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, f"Conf: {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            st.image(img, caption="Detected Objects", use_container_width=True)
            st.download_button(label="📥 Download Processed Image", data=cv2.imencode('.jpg', img)[1].tobytes(),
                               file_name="output.jpg", mime="image/jpeg")

        elif uploaded_file.type == "video/mp4":
            st.video(uploaded_file)

elif page == "Visualizations":
    st.subheader("📊 Model Performance Visualizations")

    # Load results CSV
    csv_path = "D:\\AIML Projects\\Trainedweights\\NeuroRide\\train\\results.csv"  # Update this path
    df = pd.read_csv(csv_path)

    # Button to show/hide visualizations
    if st.button("🔍 Show Detailed Analysis"):
        st.subheader("1️⃣ Loss Curves")
        fig = px.line(df, x="epoch", y=["train/box_loss", "val/box_loss"], title="Train vs Validation Box Loss")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("2️⃣ Performance Metrics")
        fig = px.line(df, x="epoch", y=["metrics/precision(B)", "metrics/recall(B)", "metrics/mAP50(B)", "metrics/mAP50-95(B)"],
                      title="Precision, Recall, and mAP over Epochs")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("3️⃣ Learning Rate Scheduler")
        fig = px.line(df, x="epoch", y="lr/pg0", title="Learning Rate Progression")
        st.plotly_chart(fig, use_container_width=True)