import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
import google.generativeai as genai
import logging

# Ensure libraries are installed:
# pip install pocketsphinx pyttsx3 speechrecognition requests openai

# Logging setup
logging.basicConfig(level=logging.INFO, filename="jarvis.log", format="%(asctime)s - %(message)s")

# Initialize components
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d1746a451d2543518d651437e82daf9c"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle AI-based commands
def aiProcess(command):
    genai.configure(api_key="AIzaSyBAUP2S02i_aqJ9dJyqvGT1QJzu_XTu0nw")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"you are a person named jarvis who can solve all the command also analyse it and give the answer . He is from India. you analyze and respond like jarvis and give short responses. {command} ")
    return response.text

# Process different commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook.")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song, "Song not found in library.")
        if link.startswith("http"):
            webbrowser.open(link)
            speak(f"Playing {song}.")
        else:
            speak(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        data = r.json()
        articles = data.get('articles', [])
        if articles:
            speak("Here are the top news headlines:")
            for article in articles[:5]:  # Speak only top 5 headlines
                speak(article["title"])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        # Let OpenAI handle unknown commands
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    # Set up the speech engine properties
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Male voice
    engine.setProperty('rate', 150)  # Set speaking rate
    engine.setProperty('volume', 0.9)  # Set volume (0.0 to 1.0)

    speak("Initializing Jarvis...")
    logging.info("Jarvis has been initialized.")

    while True:
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=1)
                # speak("Listening for the wake word...")
                print("Listening for the wake word...")

                # Recognize wake word "Jarvis"
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio).lower()
                if word == "jarvis":
                    speak("Yes, how can I assist you?")
                    logging.info("Wake word detected.")
                    print("Jarvis is active...")

                    # Listen for a command
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    logging.info(f"Command received: {command}")
                    print(f"Command received: {command}")
                    processCommand(command)
        except sr.WaitTimeoutError:
            print("No speech detected, restarting...")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
            logging.warning("UnknownValueError: Speech not recognized.")
        except sr.RequestError as e:
            speak("There was a problem connecting to the speech recognition service.")
            logging.error(f"RequestError: {e}")
        except Exception as e:
            speak("An error occurred. Please try again.")
            logging.error(f"Error: {e}")
