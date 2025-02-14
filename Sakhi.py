import os
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3
import openai

# Initialize OpenAI API
openai.api_key=""  # Replace with your own account made OpenAI API key

# Initialize text-to-speech engine
engine=pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use a female voice (if available)

# Function to speak text
def speak(text):
    print(f"Lilith: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input
def listen():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query=recognizer.recognize_google(audio, language="en-US")
        print(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None

# Function to open files
def open_file(file_path):
    try:
        os.startfile(file_path)  # For Windows
        # os.system(f'open {file_path}')  # For macOS
        # os.system(f'xdg-open {file_path}')  # For Linux
        return f"Opened {file_path}"
    except Exception as e:
        return f"Error opening file: {e}"

# Function to search the web
def search_web(query):
    try:
        url=f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching the web for {query}"
    except Exception as e:
        return f"Error searching the web: {e}"

# Function to get weather
def get_weather(city):
    try:
        api_key=""  # Replace with your own/your account made OpenWeatherMap API key
        url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response=requests.get(url)
        weather_data=response.json()
        weather=weather_data['weather'][0]['description']
        return f"The weather in {city} is {weather}"
    except Exception as e:
        return f"Error fetching weather: {e}"

# Function to handle general conversation using OpenAI's GPT-3.5
def chat_with_gpt(prompt):
    try:
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Lilith."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key. Please check your API key."
    except openai.error.RateLimitError:
        return "Error: You've exceeded your API usage limit. Please check your billing."
    except Exception as e:
        return f"Error communicating with OpenAI: {e}"

# Main function to process queries
def process_query(query):
    if query is None:
        return
    elif "open file" in query:
        file_path=query.split("open file")[1].strip()
        speak(open_file(file_path))
    elif "search" in query:
        search_query=query.split("search")[1].strip()
        speak(search_web(search_query))
    elif "weather" in query:
        city=query.split("weather")[1].strip()
        speak(get_weather(city))
    elif "exit" in query or "bye" in query or "goodbye" in query:
        speak("Goodbye! Have a great day!")
        exit()
    else:
        response=chat_with_gpt(query)
        speak(response)

# Main loop
if __name__=="__main__":
    speak("Hello, I am Lilith. How can I assist you today?")
    while True:
        query=listen()
        process_query(query)