# 🧠 NeuroDrive – Drowsiness Reversal via Stimuli

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-red.svg)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 The Problem
Driver drowsiness is a leading cause of road accidents worldwide. Most existing systems detect drowsiness too late or trigger annoying false alarms on every squint, slow blink, or glare.

## 🚀 Our Solution
**NeuroDrive** uses the **Eye Aspect Ratio (EAR)** via MediaPipe's 468 facial landmarks to detect micro-sleeps with high accuracy. Instead of just beeping, it applies **graduated stimuli** to actively wake the driver:

| Duration | Stimulus |
| :--- | :--- |
| 🟡 **2 seconds** | Yellow border – Mild alert |
| 🔴 **4 seconds** | Red border + Loud beep – Severe alert |
| ⚪ **6 seconds** | Full-screen white flash + Emergency text |

Natural blinks (under 0.4 seconds) are automatically ignored to prevent false alarms.

---

## ✨ Key Features
- **Automatic Calibration** – Adapts to your eye shape in 3 seconds at startup.
- **Blink Filtering** – Distinguishes natural blinks from dangerous micro-sleeps.
- **Real-Time Feedback** – Displays live EAR value and threshold on screen.
- **CSV Logging** – Automatically logs every drowsy episode for safety analysis.
- **Privacy First** – All processing runs locally on your machine. No cloud uploads.

---

## 🎮 Controls
| Key | Action |
| :--- | :--- |
| `Q` | Quit the application. |

---

## 🛠️ How to Run

1. **Install Python 3.8+**.
2. **Install dependencies** (run this in your terminal):
   ```bash
   pip install -r requirements.txt
