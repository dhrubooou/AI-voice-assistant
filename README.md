# 🎙️ Jaison Voice Assistant

**Jaison Voice Assistant** is an AI-powered desktop assistant that integrates **speech recognition, computer vision, sentiment analysis, and automation** to perform various user tasks.  
It can listen to voice commands, recognize gestures, automate applications, send emails, make phone calls, fetch weather/news, suggest music based on mood, and even engage in chatbot conversations using **Ollama (Llama 2 model)**.

---

## 🧠 Overview

Jaison is designed to act as an all-in-one **intelligent personal assistant**.  
It combines:
- **Voice Interaction** using SpeechRecognition and pyttsx3
- **Computer Vision (Hand Gestures)** using MediaPipe
- **Music Recommendation** using Spotify API + Sentiment Analysis (VADER)
- **Automation** for emails, app control, calling, and browsing
- **Conversational AI** using Ollama and Llama 2
- **Graphical User Interface (GUI)** using Tkinter

---

## 🖥️ Features

### 🎧 Voice Interaction
- Jaison listens and responds to commands using **Google Speech Recognition**.
- Uses **pyttsx3** for offline speech synthesis.

### 🖱️ Hand Gesture Control
- Control the mouse using your hand via webcam.
- Move cursor, perform clicks, and right-click using **MediaPipe Hand Tracking**.

### 📬 Email Automation
- Automatically send emails through Gmail using **speech-to-text** input.
- Stores frequently used email addresses in an internal dictionary.
- GUI prompt to add new contacts dynamically.

### 📞 Twilio Calling Integration
- Make phone calls programmatically using the **Twilio API**.

### 🌦️ Weather and 📰 News Fetching
- Fetch live **weather updates** (OpenWeatherMap API).
- Get the latest **news headlines** (NewsAPI).

### 🎶 Sentiment-Based Music Suggestions
- Detect user **mood** using NLTK’s **VADER Sentiment Analyzer**.
- Suggest and play songs via **Spotify API**.
- If no match found, it queries **Ollama (Llama 2)** for personalized recommendations.

### 🤖 Chatbot Mode
- When no command matches predefined actions, Jaison automatically switches to **chat mode** using Ollama (local AI model).

### 📷 Camera & Photo Capture
- Capture photos using webcam via OpenCV.

### 🧠 Wikipedia Integration
- Fetch summarized information from **Wikipedia** using speech queries.

### 💻 GUI Interface
- Modern Tkinter GUI with an activity log, voice assistant console, and interactive design.

---

## 🧩 Technologies Used

| Category | Technologies |
|-----------|--------------|
| **Programming Language** | Python 3.x |
| **GUI Framework** | Tkinter |
| **Speech Recognition** | SpeechRecognition, pyttsx3 |
| **Computer Vision** | OpenCV, MediaPipe |
| **Automation** | pyautogui, webbrowser, smtplib |
| **AI / NLP** | NLTK (VADER), Ollama (Llama 2 model) |
| **APIs** | Spotify API, OpenWeatherMap API, NewsAPI, Twilio |
| **Data Handling** | JSON, Requests |
| **System Integration** | os, subprocess, threading |

---
![UI](Screenshot%20(382).png)
