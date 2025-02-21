import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np


chatStr = ""
def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...") # Added print statement for clarity
        r.pause_threshold = 1 # Adjust as needed
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            say("I didn't understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            say("There was an error with the speech recognition service.")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred during speech recognition: {e}")
            say("An unexpected error occurred.")
            return ""

def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Harry: {query}\nJarvis: "

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Jarvis."},
                {"role": "user", "content": chatStr}
            ],
            temperature=0.7,
            max_tokens=256,
        )
        jarvis_response = response.choices[0].message.content.strip() # Extract and clean the response
        say(jarvis_response)
        chatStr += f"{jarvis_response}\n"
        return jarvis_response
    except openai.error.OpenAIError as e:  # Handle OpenAI errors
        print(f"OpenAI Error: {e}")
        error_message = "I encountered an error with the OpenAI API."
        say(error_message)
        chatStr += f"{error_message}\n"
        return error_message  # Or return None, depending on how you want to handle errors



def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.chat.completions.create(  # Use chat completions
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}], # No system message needed here
            temperature=0.7,
            max_tokens=256,
        )

        ai_response = response.choices[0].message.content.strip()
        text += ai_response

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except openai.error.OpenAIError as e:  # Handle OpenAI errors
        print(f"OpenAI Error: {e}")
        say("I encountered an error with the OpenAI API.")

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "the time" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)





        # say(query)