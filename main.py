import cv2
from ultralytics import YOLO

# 1. Load your custom-trained model
model = YOLO("models/best.pt")

# 2. Turn on the webcam (0 is usually the default laptop camera)
cap = cv2.VideoCapture(0)

print("Starting webcam... Press 'q' to quit.")

while True:
    # Read a single frame from the webcam
    success, frame = cap.read()
    
    if not success:
        print("Failed to grab frame from webcam. Is it being used by another app?")
        break
        
    # 3. Run the AI on that frame
    # conf=0.4 means it will only draw a box if it is at least 40% sure
    results = model(frame, conf=0.4)

    # 4. Tell the model to draw the bounding boxes on the frame
    annotated_frame = results[0].plot()

    # 5. Display the frame in a window
    cv2.imshow("SafeSite PPE Monitor", annotated_frame)

    # 6. Wait for the 'q' key to be pressed to stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Clean up and turn off the camera
cap.release()
cv2.destroyAllWindows()