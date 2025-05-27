# 🏹 Hand Archery Game

A real-time hand-tracking archery game built with Python, OpenCV, and MediaPipe.  
The game uses your webcam to detect hand gestures to draw and release arrows, aiming to hit randomly generated targets on screen.

---

## 🎯 Overview

This game leverages MediaPipe’s hand tracking to detect when you “draw” the bow by closing your pinching your index finger and thumb and release the arrow by opening your hand. The goal is to hit a randomly generated target that appears on the screen and score points.

---

## 🚀 Features

- Real-time hand tracking using MediaPipe Hands  
- Intuitive gesture controls for drawing and releasing arrows  
- Moving targets with random repositioning every few seconds  
- Scoring system that increments when hitting targets  
- Calibration mode to adjust for different hand sizes and distances  
- Simple and lightweight — runs on local webcam input  

---

## 📋 How to Run

1. Make sure you have Python 3.7+ installed.  
2. Install dependencies:  
   ```bash
   pip install opencv-python mediapipe numpy
Run the game:

bash

python hand_archery_game.py

Use the following keys during gameplay:

  c to calibrate your hand distance (recommended before playing)

  q to quit the game

---

🕹 Gameplay Controls
Bring your index finger tip and thumb tip close together to draw the arrow.

Open your hand to release the arrow towards the target.

Hit the moving green target to increase your score.

---

📁 Folder Structure
hand-archery-game/
├── README.md
├── .gitignore
├── LICENSE
├── archery.py

---

🎯 Future Improvements
  Add different game modes (e.g., moving arrows, timed challenges)
  
  Enhance arrow trajectory with vertical aiming
  
  Add sound effects and visual feedback
  
  Track high scores and store session stats

---

⚠️ Disclaimer
This project is intended for educational and personal use. Performance may vary based on webcam quality and lighting conditions.

---

🧾 License
MIT License — feel free to use, modify, and share with attribution.
