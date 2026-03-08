# 🚧 SafeSite: Real-Time AI PPE Monitoring System

An enterprise-grade, full-stack AI application designed to monitor industrial and construction environments in real-time. SafeSite uses custom-trained YOLOv8 computer vision to detect missing Personal Protective Equipment (PPE) such as hardhats and safety vests. 

When a safety violation occurs inside a user-defined "Danger Zone," the system instantly logs the incident, streams the evidence to a React web dashboard, and fires a real-time photo alert to a mobile device via Telegram.

## ✨ Key Features
* **Real-Time AI Detection:** Utilizes Ultralytics YOLOv8 for high-speed, accurate object detection of workers and safety gear.
* **Interactive Danger Zone Mapping:** Features a dynamic OpenCV GUI (`cv2.selectROI`) allowing safety managers to draw custom restricted areas on the camera feed before monitoring begins.
* **Live Video Streaming:** Uses `Multipart/x-mixed-replace` to stream the AI-annotated video feed seamlessly from a Python backend directly into a React web interface.
* **Automated Incident Logging:** Logs all violations, timestamps, and image paths into a local SQLite database for historical tracking.
* **Instant Mobile Alerts:** Integrates with the Telegram Bot API to push real-time photo evidence and violation details directly to a safety officer's phone.
* **Wireless Camera Support:** Capable of processing RTSP/IP camera streams (e.g., using a mobile phone as a wireless surveillance camera).

## 🛠️ Technology Stack
* **Computer Vision:** Python, OpenCV, YOLOv8 (`best.pt`)
* **Backend API & Streaming:** FastAPI, Uvicorn
* **Database:** SQLite3
* **Frontend Web Dashboard:** React, Vite, CSS Grid
* **Cloud & Notifications:** Telegram Bot API, Pyttsx3 (Audio generation)

## 📸 Dashboard Preview
*(Add your screenshots here! Replace the links with your actual image paths once uploaded to GitHub)*
* `![Live Dashboard](path/to/your/react_dashboard_screenshot.png)`
* `![Telegram Alert](path/to/your/telegram_alert_screenshot.png)`

## 🚀 Installation & Setup

### 1. Prerequisites
* Python 3.9+
* Node.js & npm
* A Telegram Bot Token and Chat ID (for mobile alerts)

### 2. Backend Setup (AI & FastAPI)
Clone the repository and install the Python dependencies:
```bash
git clone [https://github.com/yourusername/safesite-ppe-monitor.git](https://github.com/yourusername/safesite-ppe-monitor.git)
cd safesite-ppe-monitor
pip install opencv-python ultralytics pyttsx3 requests fastapi uvicorn

```

*Note: Open `app.py` and replace `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` with your actual credentials.*

### 3. Frontend Setup (React)

Open a second terminal to start the web dashboard:

```bash
cd client
npm install
npm run dev

```

## 🎮 How to Use the System

1. Run the super-server from your backend directory:
```bash
python app.py

```


2. **Draw the Danger Zone:** A static image from your webcam will pop up. Click and drag your mouse to draw a blue box over the restricted area. Press **ENTER** to confirm.
3. **Monitor:** Open your browser to `http://localhost:5173`. You will see the live AI video feed.
4. **Test it:** Walk into the camera's view (inside the area you boxed) without a helmet. The system will log the incident on the dashboard and send a photo to your Telegram!

## 🧠 Technical Architecture

The application resolves the bottleneck of running synchronous AI loops alongside a web server by utilizing Python multithreading. The YOLOv8 inference loop runs on a daemon thread, constantly updating a global frame buffer, while the FastAPI server runs on the main thread, continuously yielding that buffer to the React frontend as a JPEG byte stream.

## 👨‍💻 Author

**MD Nadeemuddin**

* Computer Science Engineering @ MSRIT
