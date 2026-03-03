import cv2
import os
import time
import pyttsx3
import sqlite3
import threading
import requests
from ultralytics import YOLO

# --- Telegram Settings ---
TELEGRAM_TOKEN="8735495261:AAHazYcz3Cw11_lBbRsDhyguSHO2k2Y4mis"
TELEGRAM_CHAT_ID="1460532958"

def play_audio_warning():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say("Warning. You have entered the Danger Zone without PPE.")
    engine.runAndWait()

def send_telegram_alert(image_path, violation_type):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    message = f"🚨 *Danger Zone Alert*\nViolation: {violation_type}\nWorker entered restricted area without PPE!"
    try:
        with open(image_path, "rb") as img:
            payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": message, "parse_mode": "Markdown"}
            files = {"photo": img}
            requests.post(url, data=payload, files=files)
            print("📱 Telegram alert successfully sent to your phone!")
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

# Database Setup
conn = sqlite3.connect('safesite.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        violation_type TEXT,
        image_path TEXT
    )
''')
conn.commit()

# Load Model
model = YOLO("models/best.pt")

if not os.path.exists("evidence"):
    os.makedirs("evidence")

last_alert_time = 0
cooldown_seconds = 10 

# Start Webcam
cap = cv2.VideoCapture(0)
print("Starting webcam...")

# --- NEW: Interactive Danger Zone Drawing ---
# Read exactly one frame from the camera to draw on
success, first_frame = cap.read()
if success:
    print("\n" + "="*50)
    print("🛑 ACTION REQUIRED:")
    print("1. A new window has opened. Click and drag your mouse to draw the Danger Zone.")
    print("2. Press 'ENTER' or 'SPACE' when you are happy with the box.")
    print("3. Press 'c' to cancel and use the whole screen.")
    print("="*50 + "\n")
    
    # This opens the interactive drawing window
    roi = cv2.selectROI("Draw Danger Zone (Press ENTER to confirm)", first_frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Draw Danger Zone (Press ENTER to confirm)")
    
    # Extract the coordinates from what you drew
    roi_x1 = int(roi[0])
    roi_y1 = int(roi[1])
    roi_w = int(roi[2])
    roi_h = int(roi[3])
    
    # If the user just pressed Enter without drawing, default to the right half of the screen
    if roi_w == 0 or roi_h == 0:
        print("No zone drawn. Defaulting to the right half of the screen.")
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        roi_x1 = int(frame_width / 2)
        roi_y1 = 0
        roi_x2 = frame_width
        roi_y2 = frame_height
    else:
        # Calculate the bottom right corner
        roi_x2 = roi_x1 + roi_w
        roi_y2 = roi_y1 + roi_h
        print(f"Danger Zone set successfully! Tracking area from ({roi_x1}, {roi_y1}) to ({roi_x2}, {roi_y2})")

print("AI Monitoring Active... Press 'q' to quit.")

# Main AI Loop
while True:
    success, frame = cap.read()
    if not success:
        break

    results = model(frame, conf=0.6, verbose=False) 
    annotated_frame = results[0].plot()

    # Draw the custom Danger Zone on the screen
    cv2.rectangle(annotated_frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 0, 255), 2)
    cv2.putText(annotated_frame, "DANGER ZONE", (roi_x1 + 10, roi_y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    in_danger_zone = False
    violation_detected = None

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name in ["NO-Hardhat", "NO-Safety Vest"]:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # Center dot logic
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            cv2.circle(annotated_frame, (center_x, center_y), 8, (255, 0, 0), -1)

            # Check if the center dot is inside the custom box
            if roi_x1 <= center_x <= roi_x2 and roi_y1 <= center_y <= roi_y2:
                in_danger_zone = True
                violation_detected = class_name
                break 

    # Trigger alarm only if inside the custom zone
    if in_danger_zone:
        current_time = time.time()
        
        if current_time - last_alert_time > cooldown_seconds:
            print(f"🚨 DANGER ZONE VIOLATION: Logging and alerting...")

            threading.Thread(target=play_audio_warning).start()
            
            filename = f"evidence/violation_{int(current_time)}.jpg"
            cv2.imwrite(filename, annotated_frame)
            
            cursor.execute('''INSERT INTO incidents (violation_type, image_path) VALUES (?, ?)''', (violation_detected, filename))
            conn.commit()
            
            threading.Thread(target=send_telegram_alert, args=(filename, violation_detected)).start()

            last_alert_time = current_time

    cv2.imshow("SafeSite PPE Monitor", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()