# ⚡ Morse Vision

A modern assistive tool that translates **eye blinks** into **Morse code**, inspired by history and built for accessibility and innovation.

---

## 🚀 Overview

**Morse Vision** uses real-time video processing to detect eye blinks, classify them based on duration (short or long), and convert them into text using the Morse code system. This hands-free communication system is designed to assist people with disabilities, or serve as a secure communication layer in high-risk or silent environments.

---

## 🔍 Inspiration

> “During World War II, soldiers used Morse code to silently transmit critical information. That legacy inspired me to build a system that turns something as subtle as a blink into meaningful communication.”

---

## 🧠 Features

- 👁️ Blink detection using **OpenCV**
- ⏱️ Classifies blinks into **short** or **long**
- 🔡 Translates blinks to **text** via Morse code
- 🎥 Real-time **video feed**
- 🌐 Lightweight front-end with **HTML/CSS**
- 🧪 Backend logic handled with **Python + Flask**

---

## 🛠️ Tech Stack

| Layer         | Tech                |
|---------------|---------------------|
| Frontend      | HTML, CSS           |
| Backend       | Python, Flask       |
| Computer Vision | OpenCV             |
| Other         | Morse Code Logic    |

---

## 🎯 Use Cases

- Assistive communication for people with motor or speech impairments
- Hands-free secure messaging
- Experimental HCI (Human-Computer Interaction)

---

## ✅ Project Status

- [x] Blink Detection
- [x] Duration Classification
- [x] Morse Code Mapping
- [x] Text Output

---

## 📥 Download Required Model File

To run blink detection, you'll need the **dlib facial landmark predictor file**:

🔗 [Download `shape_predictor_68_face_landmarks.dat`](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2)

### Steps:
1. Download the file from the link above.
2. Extract the `.bz2` file to get `shape_predictor_68_face_landmarks.dat`.
3. Place the `.dat` file in the root folder of the project or update the path in your code accordingly.

---

