import speech_recognition as sr
import cv2
import pyttsx3
import requests
import smtplib
import datetime
import wikipedia
import webbrowser
import os
import numpy as np
import mediapipe as mp
import pyautogui
from twilio.rest import Client
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys
from PIL import Image, ImageTk
import os
import time
import ollama
import random
import nltk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.sentiment import SentimentIntensityAnalyzer
from ollama import chat
from tkinter import simpledialog


class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jaison Voice Assistant")
        self.root.geometry("700x500")
        self.setup_ui()
        
       
        self.assistant_thread = threading.Thread(target=main, daemon=True)
        self.assistant_thread.start()

    def setup_ui(self):
        
        bg_color = "#0a1f3d"  
        text_color = "#00ff00"  
        console_bg = "#001a33" 
        
      
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
            self.root.iconbitmap(icon_path)
        except:
            pass
        
        main_frame = tk.Frame(self.root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
     
        header_frame = tk.Frame(main_frame, bg=bg_color)
        header_frame.pack(fill=tk.X, pady=10)
        
        try:
            img = Image.open("android-chrome-192x192.png").resize((50, 50))
            self.logo = ImageTk.PhotoImage(img)
            tk.Label(header_frame, image=self.logo, bg=bg_color).pack(side=tk.LEFT, padx=10)
        except:
            pass
        
        tk.Label(header_frame, 
                text="Jaison Voice Assistant", 
                font=("Helvetica", 16, "bold"),
                fg=text_color,
                bg=bg_color).pack(side=tk.LEFT)
        
       
        console_frame = tk.Frame(main_frame, bg=bg_color)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(console_frame, 
                text="Activity Log:", 
                font=("Helvetica", 10),
                fg=text_color,
                bg=bg_color).pack(anchor=tk.W)
        
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=20,
            wrap=tk.WORD,
            bg=console_bg,
            fg=text_color,
            insertbackground=text_color,
            font=("Consolas", 9)
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
      
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame,
                    text="Exit",
                    command=self.root.quit,
                    bg="#ff0000",  
                    fg="white",
                    activebackground="#cc0000",
                    activeforeground="white",
                    relief=tk.RAISED,
                    font=("Helvetica", 14, "bold"),  
                    width=15,  
                    height=2,  
                    borderwidth=4  
                    ).pack(side=tk.RIGHT, padx=10, pady=10)
        
      
        import sys
        sys.stdout = TextRedirector(self.console, "stdout")

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
        
    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.widget.update()
        
    def flush(self):
        pass


recognizer = sr.Recognizer()
engine = pyttsx3.init()
account_sid = "ACdf7742cc5b5ac7228353a059eb3c9791"
auth_token = "dead390107afa126de7e5b23490d0447"
client = Client(account_sid, auth_token)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
mouse_active = False
cap = None

alpha = 0.2  
prev_x, prev_y = 0, 0
last_click_time = 0  
click_cooldown = 0.5 

recognizer = sr.Recognizer()


engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%H")


def get_weather():

    api_key = 'f76752c6b8dd4ace8a16916a0b87fd64'
    city = 'Kolkata'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f"The weather today is {weather_description}. The temperature is {temperature} degrees Celsius."

def take_photo():
    
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    camera.release()
    cv2.imwrite("captured_photo.jpg", image)
    print("Photo captured successfully!")

def get_news():

    api_key = '6cfe3ffa84a84af3b8f63697a893b038'
    url = f'http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    headlines = [article['title'] for article in data['articles']]
    return "Here are the top headlines: " + ", ".join(headlines[:5])


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('nijer_email24@gmail.com', 'a1b2c3d4@')
    server.sendmail('jake _send_korbi_tar_email@gmail.com', to, content)
    server.close()

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:    
        print("Say that again please...")  
        return "None"
    return query

def make_call(phone_number):
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+917980347474",
        from_="+16313141326"
        )

    print("Calling...")

def search_wikipedia(query): 
    try: 
        result = wikipedia.summary(query, sentences=2) 
        return result 
    except wikipedia.exceptions.DisambiguationError as e: 
        options = e.options[:3] 
        return f"Can you please specify? I found multiple options: {', '.join(options)}" 
    except wikipedia.exceptions.PageError as e: 
        return "Sorry, I couldn't find any relevant information."

def open_application(app_name):
    app_mappings = {
        "chrome": "start chrome",
        "notepad": "start notepad",
        "calculator": "start calc",
        "command prompt": "start cmd",
        "paint": "start mspaint",
        "telegram": "start telegram",
        "whatsapp": "start whatsapp",
        "file explorer": "start explorer",
        "downloads": "start explorer C:\\Users\\Dhrubojyoti\\Downloads",
        "this pc": "start explorer",
        "browser": "start chrome"
    }
    app_m2={
        "youtube" : "https://www.youtube.com/",
        "google":"https://www.google.com/",
        "stackoverflow":"stackoverflow.com"
    }
    if app_name in app_mappings:
        os.system(app_mappings[app_name])
        speak(f"Opening {app_name}")
    elif app_name in app_m2:
        webbrowser.open(app_m2[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I don't recognize {app_name}. Try another name.")

def close_application(app_name):
    close_mappings = {
        "chrome": "taskkill /IM chrome.exe /F",
        "notepad": "taskkill /IM notepad.exe /F",
        "calculator": "taskkill /IM calculator.exe /F",
        "command prompt": "taskkill /IM cmd.exe /F",
        "paint": "taskkill /IM mspaint.exe /F",
        "telegram": "taskkill /IM Telegram.exe /F",
        "whatsapp": "taskkill /IM WhatsApp.exe /F",
        "file explorer": "taskkill /IM explorer.exe /F",
        "spotify":"taskkill /IM spotify.exe /F"
    }
    if app_name in close_mappings:
        os.system(close_mappings[app_name])
        speak(f"Closing {app_name}")
    else:
        speak(f"Sorry, I couldn't find {app_name} running.")
        

def smooth_cursor_movement(x, y):
    global prev_x, prev_y
    smoothed_x = alpha * x + (1 - alpha) * prev_x
    smoothed_y = alpha * y + (1 - alpha) * prev_y
    prev_x, prev_y = smoothed_x, smoothed_y
    return int(smoothed_x), int(smoothed_y)

def detect_gestures(hand_landmarks):
    global last_click_time
    
    landmarks = hand_landmarks.landmark
    
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    thumb_tip = landmarks[4]
    
    fingers = [index_tip, middle_tip, ring_tip, pinky_tip, thumb_tip]
    extended_fingers = sum(1 for finger in fingers if finger.y < landmarks[5].y)
    
    current_time = time.time()
    
    if extended_fingers == 1:  
        if current_time - last_click_time > click_cooldown:
            pyautogui.rightClick()
            last_click_time = current_time
    
    elif extended_fingers == 2:  
        if current_time - last_click_time > click_cooldown:
            pyautogui.click()
            last_click_time = current_time
    
    elif extended_fingers == 5:  
        x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
        x, y = smooth_cursor_movement(x, y)
        pyautogui.moveTo(x, y)

def activate_mouse_gesture():
    global mouse_active, cap
    if mouse_active:
        return
    
    mouse_active = True
    cap = cv2.VideoCapture(0)
    print("Mouse gesture activated. Show your hand to control the mouse.")
    
    while mouse_active and cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                detect_gestures(hand_landmarks)
                
        cv2.imshow('Mouse Control', frame)
        if cv2.waitKey(5) & 0xFF == 27: 
            break
    
    deactivate_mouse_gesture()

def deactivate_mouse_gesture():
    global mouse_active, cap
    mouse_active = False
    if cap and cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    print("Mouse gesture deactivated.")

email_directory = {
    "john": "john.doe@gmail.com",
    "alice": "alice.smith@yahoo.com",
    "bob": "bob.jones@outlook.com",
    "somnath": "roysomnath2002@gmail.com",
    "soumili":"trina13soumilighosh@gmail.com"
}
def get_email_input():
    recipient_name, recipient_email = None, None
    def on_submit():
        nonlocal recipient_name,recipient_email
        recipient_name = name_entry.get().strip()
        recipient_email = email_entry.get().strip()
        
        if recipient_name and recipient_email:
            email_directory[recipient_name] = recipient_email
            root.destroy() 

    root = tk.Tk()
    root.title("Enter Email Details")
    root.geometry("300x150")
    
    tk.Label(root, text="Recipient Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()
    
    tk.Label(root, text="Recipient Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()
    
    submit_btn = tk.Button(root, text="Submit", command=on_submit)
    submit_btn.pack()
    
   
    root.bind('<Return>', lambda event: on_submit(recipient_name,recipient_email))

    
    root.mainloop()  

    return recipient_name, recipient_email
    
def send_email_automation():
    speak("Whom should I send the email to?")
    recipient_name = takeCommand().lower()
    
    if recipient_name in email_directory:
        recipient_email = email_directory[recipient_name]
    else:
        speak("I couldn't find the email address. Please enter it.")
        recipient_name, recipient_email = get_email_input()
        email_directory.update({recipient_name:recipient_email})
        
        if not recipient_name or not recipient_email:
            speak("Email address was not provided. Canceling email sending.")
            return
    speak("Opening Gmail to send an email.")
    webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")
    time.sleep(5)
    pyautogui.write(recipient_email.strip())
    pyautogui.press('tab')
    pyautogui.press('tab')
    
    speak("What is the subject of the email?")
    subject = takeCommand()
    pyautogui.write(subject)
    pyautogui.press('tab')  
    
    speak("What should I write in the email?")
    body = takeCommand()
    pyautogui.write(body)
    
    speak("Say send to send the email.")
    while True:
        command = takeCommand().lower()
        if "send" in command:
            pyautogui.hotkey('ctrl', 'enter') 
            speak("Email sent successfully.")
            break
        elif "cancel" in command:
            speak("Email sending canceled.")
            break

def chat_with_ollama(user_input, conversation_history):
    model = "llama2"  
    conversation_history.append({"role": "user", "content": user_input})

    response = ollama.chat(model=model, messages=conversation_history)
    reply = response['message']['content']

    conversation_history.append({"role": "assistant", "content": reply})
    return reply, conversation_history

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

SPOTIFY_CLIENT_ID = "a6607b65ded843798254c2742136e332"
SPOTIFY_CLIENT_SECRET = "8420b0869a9443f0b0ad01e317bd59d5"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET))


def detect_mood(user_input):
    
    sentiment_score = sia.polarity_scores(user_input)["compound"]
    
    if sentiment_score >= 0.5:
        return "happy"
    elif sentiment_score <= -0.3:
        return "sad"
    elif 0.1 < sentiment_score < 0.5:
        return "energetic"
    else:
        return "calm"

def get_song_from_spotify(query):
    results = sp.search(q=query, type="track", limit=1)
    
    if results["tracks"]["items"]:
        song = results["tracks"]["items"][0]
        return song["name"], song["external_urls"]["spotify"]
    return None

def get_song_from_ollama(user_input):
    response = chat("Suggest a song based on this input: " + user_input)
    return response  

def listen_to_user():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        speak("What song would you like to play, or how are you feeling today?")
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        return None
    except sr.RequestError:
        print("There was an issue with the speech recognition service.")
        return None
def take_photo():
    
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    camera.release()
    cv2.imwrite("captured_photo.jpg", image)
    print("Photo captured successfully!")
    
def suggest_music():
    user_input = listen_to_user()
    
    if not user_input:
        return
    
    song_info = get_song_from_spotify(user_input)
    
    if song_info:
        song_name, song_url = song_info
        speak(f"Playing {song_name} for you.")
        webbrowser.open(song_url)
        return
    
    
    mood = detect_mood(user_input)
    speak(f"I think you're feeling {mood}. Let me find a song for you.")
    suggested_song = get_song_from_ollama(user_input)
    
    if suggested_song:
        song_info = get_song_from_spotify(suggested_song)
        if song_info:
            song_name, song_url = song_info
            speak(f"Playing {song_name} for you.")
            webbrowser.open(song_url)
        else:
            speak("Sorry, I couldn't find that song on Spotify.")
    else:
        speak("Sorry, I couldn't find a suitable song for you right now.")

call_hist={
    "jeet":"8697691238",
    "dhrubo":"+917980347474"
}        
def main():
    speak("Hello I am Jaison Sir! How can I assist you today?")
    print("Hello I am Jaison Sir! How can I assist you today?")
    
    while True:
        
        command = takeCommand().lower()
        conversation_history=[]
        if "open" in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)
        elif "close" in command:
            app_name = command.replace("close", "").strip()
            close_application(app_name)
        elif "get news" in command:
            news = get_news()
            speak(news)
            print(news)
        elif "get weather" in command:
            weather = get_weather()
            speak(weather)
            print(weather)
        elif "take photo" in command:
            take_photo()
        elif "call" in command:
            number = command.replace("call", "").strip()
            make_call(call_hist[number])
        elif "search" in command: 
                query = command.split("for")[-1].strip() 
                speak(search_wikipedia(query))
                print(search_wikipedia(query))
        elif "activate mouse" in command or "start mouse" in command:
            threading.Thread(target=activate_mouse_gesture, daemon=True).start()
        elif "deactivate mouse" in command or "stop mouse" in command:
            deactivate_mouse_gesture()
        elif "send email" in command:
            send_email_automation()
        elif "play song" in command:
            suggest_music()
        elif "exit" in command or "quit" in command:
            deactivate_mouse_gesture() 
            speak("Goodbye!")
            break
        else:
            reply, conversation_history = chat_with_ollama(command, conversation_history)
            speak(reply)
            print("Jaison : ",reply)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
