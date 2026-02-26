import cv2
import os
import time
import sqlite3
from ultralytics import YOLO

conn = sqlite3.connect('safesite.db')
cursor = conn.cursor()
cursor.execute('''
create table if not exists incidents(
               id integer primary key autoincrement,
               timestamp datetime default current_timestamp,
               violation_type text,
               image_path text
               )               
''')
conn.commit()

# 1. Load the model
model = YOLO("models/best.pt")

# --- NEW: Setup the Evidence Folder ---
if not os.path.exists("evidence"):
    os.makedirs("evidence")
    print("Created 'evidence' folder.")

# --- NEW: Alert Cooldown (Debounce) ---
last_alert_time = 0
cooldown_seconds = 10  # Wait 10 seconds between taking pictures

# 2. Start Webcam
cap = cv2.VideoCapture(0)
print("Starting webcam... Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    # 3. Run AI (Increased conf to 0.6 to ignore background clothes!)
    results = model(frame, conf=0.6, verbose=False) # Added verbose=False
    annotated_frame = results[0].plot()

    # --- NEW: Business Logic ---
    # Extract the names of what the AI found in this exact frame
    detected_classes = [model.names[int(c)] for c in results[0].boxes.cls]

    # Check if a violation is happening
    if "NO-Hardhat" in detected_classes or "NO-Safety Vest" in detected_classes:
        
        current_time = time.time()
        
        # Check if our cooldown timer is up
        if current_time - last_alert_time > cooldown_seconds:
            print(f"🚨 VIOLATION DETECTED: Saving evidence to Database ...")
            
            # Save the image with a unique timestamp name
            filename = f"evidence/violation_{int(current_time)}.jpg"
            cv2.imwrite(filename, annotated_frame)
            
            violation_type = "Multiple Violations"

            if "NO-Hardhat" in detected_classes and "NO-Safety Vest" not in detected_classes:
                violation_type = "Missing Hardhat"
            elif "NO-Safety Vest" in detected_classes and "NO-Hardhat" not in detected_classes:
                violation_type = "Missing Vest"

            cursor.execute('''
                          insert into incidents (violation_type,image_path) values(?,?) ''',(violation_type,filename))
            conn.commit()
            # Reset the timer
            last_alert_time = current_time

    # 4. Show the video
    cv2.imshow("SafeSite PPE Monitor", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()