import speech_recognition as sr

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
