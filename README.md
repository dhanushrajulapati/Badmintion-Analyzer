<div align="center">
  <h1 align="center">GAMESENSE ADOBE</h1>
  <p align="center">
    An advanced sports tracking system for real-time badminton data analysis and performance insights.
    <br />
    <br />
    <br />
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## 🌟 Overview

**GAMESENSE** is an advanced sports tracking system designed to provide real-time data analysis, event detection, and performance insights during live gameplay. It currently supports **Badminton** and uses cutting-edge machine learning and computer vision technologies to monitor and enhance the gameplay experience for players, coaches, and spectators.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Next.js-14-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/YOLO-v8-blue.svg" alt="YOLOv8">
  <img src="https://img.shields.io/badge/OpenCV-brightgreen.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/Deployment-Vercel-black.svg" alt="Vercel">
</p>

---

## 📑 Table of Contents

- [Features](#-features)
- [Technologies & Algorithms](#-technologies--algorithms)
- [How It Works](#-how-it-works)
- [Installation Guide](#%EF%B8%8F-installation-guide)
  - [Backend Setup](#backend)
  - [Frontend Setup](#frontend)
- [Usage](#-usage)
- [License](#-license)

---

## 🚀 Features

### 1. 🏸 Game Selection
- **Supported Games:** Currently tailored exclusively for **Badminton**.

### 2. 📏 Play Area Marking
- **Precision Marking:** Automatically detects and marks key areas on the court (boundaries, nets, service lines, etc.) using YOLO object detection.
- **Valid Angles:** It is valid only for a single, fixed camera angle.

### 3. 🎾 Shuttle Tracking
- **Advanced Tracking:** Continuously tracks the shuttlecock's position, speed, and trajectory using specific machine learning algorithms.
- **Real-Time Analysis:** Offers instant feedback on shot speed, angles, and potential outcomes.
- **Event Detection:** Identifies key events like the shuttle hitting the net, out-of-bounds shots, and faults.

### 4. 🏃 Player Tracking
- **Movement Monitoring:** Tracks players' positions and movements on the court using YOLO and DeepSORT algorithms.
- **Player Mapping:** Visualizes player activity zones and movement patterns on a court map.
- **Player Movement Metrics:** Provides detailed statistics on distance covered, time spent in active zones, and player fatigue.

### 5. 🎯 Automated Scoring
- **Real-Time Scoring:** Automatically updates scores based on gameplay events (points, fouls, etc.).
- **Scoreboard Integration:** Syncs seamlessly with digital scoreboards to ensure real-time accuracy.

### 6. ⏱️ Rally Length Calculation
- **Rally Metrics:** Tracks and calculates the length of each rally by time, number of shots, and distance covered by players.
- **Detailed Breakdown:** Provides insights into successful rallies, unforced errors, and overall trends.

### 7. 🚨 Event Detection
- **Key Event Alerts:** Detects critical events such as game points, fouls, faults, and out-of-bounds shots, triggering alerts for immediate action.
- **Highlight Generation:** Automatically compiles key moments for post-game review.

### 8. 🎙️ Real-Time Commentary (Bonus)
- **Automated Commentary:** Uses the Gemini API to generate live commentary for the game, including player performance highlights and key events.
- **Text-to-Speech Conversion:** Converts generated commentary into real-time audio for an enhanced spectator experience.

### 9. 📈 Real-Time Graph Analysis
- **Score Tracking:** Displays a real-time graph showing the current score progression of both players.
- **Shuttlecock Hit Distance:** Visualizes the distance covered by the shuttlecock during each hit.
- **Player Speed Analysis:** Continuously monitors and graphs the speeds of both players, offering insights into their relative movements.

---

## 🛠️ Technologies & Algorithms

| Technology/Algorithm | Description / Role |
| ------------------- | ----------------- |
| **YOLOv8**          | Used for spotting players and other objects in real-time. |
| **TrackNet v3**     | Used specifically for shuttlecock tracking and trajectory estimating. |
| **DeepSORT**        | Employed for robust multi-object tracking (players and shuttlecock). |
| **OpenCV**          | Extensively utilized for computer vision and image processing tasks. |
| **NumPy**           | Matrix operations and array calculations. |
| **Python / Flask**  | Provides the backend framework and ML inference environments. |
| **Next.js & Node**  | Used to build the reactive frontend dashboard. |
| **Socket.io**       | Ensures low-latency, real-time bi-directional communication between backend and frontend. |

---

## ⚙️ Installation Guide

### Backend

1. **Clone the Repository**
   ```bash
   git clone https://github.com/harshitnitjsr/Adobe-GenSolve-Team-Neuron
   cd Adobe-GenSolve-Team-Neuron/Backend
   ```

2. **Install Dependencies**
   It's recommended to create a virtual environment first.
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Model Checkpoints**
   - Download the required model weights via this [[Google Drive Link]](https://drive.google.com/drive/u/3/folders/18HJsCZ6piwOD5maKC2z2_RFGYDPjGG4T?usp=sharing).
   - Move `.pt` model files to the `Models/` folder.
   - Move TrackNet weights to `TrackNetV3/ckpts/`.
   - Place any `.mp4` test footage in `TestVideos/`.

4. **Setup and Run**
   ```bash
   python setup.py install
   python app.py
   ```

### Frontend

You can access the live version at [adobe-gen-solve-team-neuron.vercel.app](https://adobe-gen-solve-team-neuron.vercel.app/), or run it locally:

1. **Navigate to the Client Directory**
   ```bash
   cd ../myapp
   ```

2. **Install Dependencies**
   ```bash
   npm i
   ```

3. **Environment Setup (Gemini API)**
   - Get a Gemini API key from Google AI Studio.
   - Create a `.env` file in the `myapp` directory.
   - Add the following line:
     ```env
     NEXT_PUBLIC_GEMINI_KEY=your_gemini_api_key_here
     ```

4. **Run the Development Server**
   ```bash
   npm run dev
   ```

---

## 💡 Usage

1. Launch both the backend (`python app.py`) and frontend (`npm run dev`).
2. Open your browser and navigate to `http://localhost:3000`.
3. Select an existing video from your `TestVideos/` folder or upload a new one.
4. Let the models process the frame (ensure you have optimal hardware/GPU capability if doing real-time processing locally).
5. View the dashboard to see analytics, active bounding boxes, commentary, and tracked real-time graphs.

---
S
<p align="center">
  Built with ❤️ by Team Neuron for Adobe GenSolve 
</p>
