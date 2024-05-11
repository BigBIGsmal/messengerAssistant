# back.py

import keyboard
import time
import string
import speech_recognition as sr
import threading

should_respond = False
stop_event = threading.Event()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your command.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

def send_message(message):
    # Simulate typing delay
    for char in message:
        keyboard.write(char)
        time.sleep(0.05)
    keyboard.press_and_release('enter')

def add_punctuation(text):
    if text[-1] not in string.punctuation:
        text += "."

    if text.endswith(("who", "what", "where", "when", "why", "how", "?")):
        text += "?"
    return text

def start_listening():
    global should_respond
    while not stop_event.is_set():
        if should_respond:
            command = listen_for_command()
            if command:
                if "mary" in command:
                    command = command.replace("mary", "", 1)
                    response = add_punctuation(command.strip())
                    send_message(response)
                else:
                    response = add_punctuation(command)
                    print("Response:", response)

    print("Recording stopped.")

def start_listening_thread():
    global should_respond
    should_respond = True
    t = threading.Thread(target=start_listening)
    t.start()

def stop_listening_thread():
    global should_respond
    should_respond = False
    stop_event.set()
