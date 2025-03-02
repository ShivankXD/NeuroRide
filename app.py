import streamlit as st
from ultralytics import YOLO
import pandas as pd
import matplotlib.pyplot as plt
import torch
import cv2
import numpy as np
from PIL import Image

st.title("NeuroRide-BETA")
st.write("Upload an image/video and let the model detect helmets and number plates.")

# Load the trained model
model = YOLO(r"D:\AIML Projects\Trainedweights\NeuroRide\train\weights\best.pt")  # Use best.pt or last.pt
#best.pt has the highest performance (best mAP-mean Average Precision).
#Use last.pt only if you want to continue training or test the latest checkpoint.


# Image Video Upload Feature 
# File uploader for image/video
uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4"])

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

        st.image(img, caption="Detected Objects", use_column_width=True)

    elif uploaded_file.type == "video/mp4":
        st.video(uploaded_file)


# Display Visualizations (Loss Curves, Precision, Recall, mAP)


# Load results CSV
csv_path = "D:\\AIML Projects\\Trainedweights\\NeuroRide\\train\\results.csv"  # Update this path
df = pd.read_csv(csv_path)

# Plot Loss Curves
st.subheader("Loss Curves")
fig, ax = plt.subplots()
ax.plot(df["epoch"], df["train/box_loss"], label="Train Box Loss", color='blue')
ax.plot(df["epoch"], df["val/box_loss"], label="Validation Box Loss", color='red')
ax.legend()
st.pyplot(fig)

# Plot Performance Metrics
st.subheader("Performance Metrics")
fig, ax = plt.subplots()
ax.plot(df["epoch"], df["metrics/precision(B)"], label="Precision", color='green')
ax.plot(df["epoch"], df["metrics/recall(B)"], label="Recall", color='orange')
ax.plot(df["epoch"], df["metrics/mAP50(B)"], label="mAP@50", color='purple')
ax.plot(df["epoch"], df["metrics/mAP50-95(B)"], label="mAP@50-95", color='brown')
ax.legend()
st.pyplot(fig)
