import speech_recognition as sr
import requests
import json

BOT_TOKEN = '6774777905:AAGtrkDcqrGFTBK-XN4qzE23m53y0YlQG0Y'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

class SpeechToTextEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def start_recording(self):
        print("Back: Recording started")  # Print statement for recording start
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.audio = self.recognizer.listen(source)

    def stop_recording(self):
        print("Back: Recording stopped")  # Print statement for recording stop
        try:
            text = self.recognizer.recognize_google(self.audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Error: {0}".format(e)

    def get_updates(self, offset=None):
        print("getUpdates is running")
        url = BASE_URL + 'getUpdates'
        params = {'timeout': 100, 'offset': offset}
        try:
            response = requests.get(url, params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return json.loads(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching updates: {e}")
            return None

