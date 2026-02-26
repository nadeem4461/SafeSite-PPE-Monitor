# 🚧 SafeSite PPE Monitor (Full-Stack AI System)

A real-time computer vision application that detects Personal Protective Equipment (PPE) compliance on construction sites. This system uses a custom-trained YOLOv8 object detection model to identify missing hardhats, masks, and safety vests, logs violations to a local database, and displays the evidence on a modern React web dashboard.

## ✨ Features
* **Real-Time AI Inference:** Processes live webcam feeds using a custom YOLOv8 Nano model.
* **Automated Violation Logging:** Captures screenshot evidence when compliance rules are broken.
* **Smart Debouncing:** Implements cooldown logic to prevent database spamming during sustained violations.
* **RESTful API:** Serves database logs and static image files via FastAPI.
* **Modern Web Dashboard:** A Vite-powered React front-end to review incident reports.

## 🛠️ Tech Stack
* **Machine Learning:** Ultralytics YOLOv8, OpenCV, Python
* **Backend API:** FastAPI, Uvicorn, SQLite
* **Frontend:** React.js, Vite
* **Dataset & Training:** Roboflow, Google Colab (NVIDIA T4 GPU)

## 🚀 How to Run Locally

### 1. Setup the Environment
Clone the repository and install the Python dependencies:
```bash
git clone [https://github.com/nadeem4461/SafeSite-PPE-Monitor.git](https://github.com/nadeem4461/SafeSite-PPE-Monitor.git)
cd SafeSite-PPE-Monitor
pip install ultralytics opencv-python fastapi uvicorn

```

### 2. Add the AI Model

Since the trained weights are ignored in Git due to file size limits, download the custom model here:

> **[best.pth]**

Place the downloaded `best.pt` file inside the `models/` directory exactly like this:

```text
SafeSite-PPE-Monitor/
└── models/
    └── best.pt

```

### 3. Start the Backend API & Database

Open a terminal and start the FastAPI server to serve the SQLite database:

```bash
uvicorn api:app --reload

```

### 4. Start the React Dashboard

Open a second terminal, install the Node modules, and start Vite:

```bash
cd client
npm install
npm run dev

```

### 5. Launch the AI Security Camera

Open a third terminal and run the main inference script to turn on your webcam:

```bash
python main.py

```

## 👤 Author

**MD Nadeemuddin**

```

Once you paste and save that, just run your Git commands to push it to your repository:
```bash
git add README.md
git commit -m "Added professional README"
git push

```
