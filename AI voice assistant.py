import speech_recognition as sr
import cv2
import pyttsx3
import requests
import smtplib
import datetime
import wikipedia
import webbrowser
from twilio.rest import Client





recognizer = sr.Recognizer()


engine = pyttsx3.init()


account_sid = "ACbdadadf551ad32a15b587bd25c87109f"
auth_token = "f2f0645b75268af0237ed83c9b78946d"
client = Client(account_sid, auth_token)


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
    server.login('voiceai24@gmail.com', 'a1b2c3d4@')
    server.sendmail('voiceai@gmail.com', to, content)
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
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def make_call(phone_number):
    call = client.calls.create(
        to=phone_number,
        from_="+14432216537",
        url="http://demo.twilio.com/docs/voice.xml",
    )
    print("Calling...")

def search_wikipedia(query): 
    try: 
        result = wikipedia.summary(query, sentences=2) 
        return result 
    except wikipedia.exceptions.DisambiguationError as e: 
        options = e.options[:3]  # Get the first three options
        return f"Can you please specify? I found multiple options: {', '.join(options)}" 
    except wikipedia.exceptions.PageError as e: 
        return "Sorry, I couldn't find any relevant information."


def main():
    speak("Hello I am Jaison Sir! How can I assist you today?")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()

                if "good morning" in command:
                    if int(get_time()) < 12:
                        speak("Good morning!")
                    else:
                        speak("Good morning! It seems it's already past morning.")
                elif "good afternoon" in command:
                    if 12 <= int(get_time()) < 18:
                        speak("Good afternoon!")
                    else:
                        speak("Good afternoon! It seems it's already past afternoon.")
                elif "good evening" in command:
                    if int(get_time()) >= 18:
                        speak("Good evening!")
                    else:
                        speak("Good evening! It seems it's still afternoon.")
                elif "weather" in command:
                    speak(get_weather())
                    print(get_weather())
                elif "search" in command: 
                    query = command.split("for")[-1].strip() 
                    speak(search_wikipedia(query))
                    print(search_wikipedia(query))

                elif 'open youtube' in command:
                    webbrowser.open("https://www.youtube.com/")

                elif 'open google' in command:
                    webbrowser.open("google.com")

                elif 'open stackoverflow' in command:
                    webbrowser.open("stackoverflow.com")
                elif "camera" in command:
                    speak(take_photo())
                elif "news" in command:
                    speak(get_news())
                    print(get_news())
                elif 'email' in command:
                    try:
                        speak("What should I say?")
                        print("What should I say?")
                        content = takeCommand()
                        to = "dhurbojyoti73@gmail.com"    
                        sendEmail(to, content)
                        speak("Email has been sent!")
                    except Exception as e:
                        print(e)
                        speak("Sorry my friend . I am not able to send this email")
                elif "call" in command:
                    make_call("phone number of that person you want to call")
                elif "exit" in command:
                    speak("Goodbye!")
                    break
                else:
                    speak("Sorry, I didn't understand that. Can you repeat?")
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said. Can you please repeat?")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == "__main__":
    main()
