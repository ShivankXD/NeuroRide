import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
import os
from datetime import datetime
import pandas as pd  # Replaced xlwings with pandas for Excel operations

# Initialize PaddleOCR
ocr = PaddleOCR()

# Function to perform OCR on an image array
def perform_ocr(image_array):
    if image_array is None:
        raise ValueError("Image is None")
    
    # Perform OCR on the image array
    results = ocr.ocr(image_array, rec=True)  # rec=True enables text recognition
    detected_text = []

    # Process OCR results
    if results[0] is not None:
        for result in results[0]:
            text = result[1][0]
            detected_text.append(text)

    # Join all detected texts into a single string
    return ''.join(detected_text)

# Load YOLOv8 model
model = YOLO("best.pt")
names = model.names

# Define polygon area
area = [(1, 173), (62, 468), (608, 431), (364, 155)]

# Function to process an image or video file
def process_file(file_path):
    """
    Processes the uploaded file (image or video) and detects helmets and number plates.
    Returns the detected number plate and other results.
    """
    # Check if the file is an image or video
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Process image
        frame = cv2.imread(file_path)
        if frame is None:
            raise ValueError("Could not read image file")
        
        # Resize the frame
        frame = cv2.resize(frame, (1020, 500))
        
        # Run YOLOv8 tracking on the frame
        results = model.track(frame, persist=True)
        
        # Initialize flags and variables
        no_helmet_detected = False
        numberplate_box = None
        numberplate_track_id = None
        
        # Check if there are any boxes in the results
        if results[0].boxes is not None and results[0].boxes.id is not None:
            # Get the boxes, class IDs, track IDs, and confidences
            boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
            class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
            track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
            confidences = results[0].boxes.conf.cpu().tolist()  # Confidence scores
            
            for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                c = names[class_id]
                x1, y1, x2, y2 = box
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                
                result = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
                if result >= 0:
                    if c == 'no-helmet':
                        no_helmet_detected = True  # Mark that no-helmet is detected
                    elif c == 'numberplate':
                        numberplate_box = box  # Store the numberplate bounding box
                        numberplate_track_id = track_id  # Store the track ID for the numberplate
            
            # If both no-helmet and numberplate are detected
            if no_helmet_detected and numberplate_box is not None:
                x1, y1, x2, y2 = numberplate_box
                crop = frame[y1:y2, x1:x2]
                crop = cv2.resize(crop, (120, 85))
                
                # Perform OCR on the cropped image
                text = perform_ocr(crop)
                print(f"Detected Number Plate: {text}")
                
                # Save the cropped image with current time as filename
                current_date = datetime.now().strftime('%Y-%m-%d')
                current_time = datetime.now().strftime('%H-%M-%S-%f')[:12]
                if not os.path.exists(current_date):
                    os.makedirs(current_date)
                crop_image_path = os.path.join(current_date, f"{text}_{current_time}.jpg")
                cv2.imwrite(crop_image_path, crop)
                
                # Return the detected number plate
                return text
        
        return None  # No number plate detected

    elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
        # Process video
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file")
        
        # Create directory for current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        if not os.path.exists(current_date):
            os.makedirs(current_date)

        # Excel file path
        excel_file_path = os.path.join(current_date, f"{current_date}.xlsx")
        
        # Create or load DataFrame
        if os.path.exists(excel_file_path):
            df = pd.read_excel(excel_file_path)
        else:
            df = pd.DataFrame(columns=["Number Plate", "Date", "Time"])

        processed_track_ids = set()

        while True:
            # Read a frame from the video
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.resize(frame, (1020, 500))
            
            # Run YOLOv8 tracking on the frame
            results = model.track(frame, persist=True)
            
            # Initialize flags and variables
            no_helmet_detected = False
            numberplate_box = None
            numberplate_track_id = None
            
            # Check if there are any boxes in the results
            if results[0].boxes is not None and results[0].boxes.id is not None:
                # Get the boxes, class IDs, track IDs, and confidences
                boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
                class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
                track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
                confidences = results[0].boxes.conf.cpu().tolist()  # Confidence scores
                
                for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                    c = names[class_id]
                    x1, y1, x2, y2 = box
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                    result = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
                    if result >= 0:
                        if c == 'no-helmet':
                            no_helmet_detected = True  # Mark that no-helmet is detected
                        elif c == 'numberplate':
                            numberplate_box = box  # Store the numberplate bounding box
                            numberplate_track_id = track_id  # Store the track ID for the numberplate
            
                # If both no-helmet and numberplate are detected and the track ID is not already processed
                if no_helmet_detected and numberplate_box is not None and numberplate_track_id not in processed_track_ids:
                    x1, y1, x2, y2 = numberplate_box
                    crop = frame[y1:y2, x1:x2]
                    crop = cv2.resize(crop, (120, 85))
                    
                    # Perform OCR on the cropped image
                    text = perform_ocr(crop)
                    print(f"Detected Number Plate: {text}")
                    
                    # Save the cropped image with current time as filename
                    current_time = datetime.now().strftime('%H-%M-%S-%f')[:12]
                    crop_image_path = os.path.join(current_date, f"{text}_{current_time}.jpg")
                    cv2.imwrite(crop_image_path, crop)
                    
                    # Add data to DataFrame
                    new_entry = pd.DataFrame({
                        "Number Plate": [text],
                        "Date": [current_date],
                        "Time": [current_time]
                    })
                    df = pd.concat([df, new_entry], ignore_index=True)
                    
                    # Add the track ID to the processed set
                    processed_track_ids.add(numberplate_track_id)
        
        # Release the video capture object
        cap.release()

        # Save DataFrame to Excel
        df.to_excel(excel_file_path, index=False)
        return "Video processing completed. Check the Excel file for results."
    
    else:
        raise ValueError("Unsupported file type. Only images and videos are supported.")