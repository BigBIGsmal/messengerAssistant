import requests
from datetime import datetime
import time
import os
import pyautogui
import time
import random

BOT_TOKEN = '6774777905:AAGtrkDcqrGFTBK-XN4qzE23m53y0YlQG0Y'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

class Controller:
    def open_telegram(self):
        # Click on the search bar
        pyautogui.press('win')
        time.sleep(1)
        # Type "Telegram" in the search bar and press Enter
        pyautogui.write("Telegram")
        time.sleep(1)  # Wait for the search results to appear
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.click(100, 100, duration=1)
        pyautogui.write("Expert")
        time.sleep(2)
        pyautogui.press('enter')

    
    def type_message(self, message):
        pyautogui.click(400, 840, duration=1)
        time.sleep(2)
        pyautogui.write(message)
        time.sleep(2)
        pyautogui.press('enter')
    
class TelegramReceiver:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f'https://api.telegram.org/bot{self.bot_token}/'
        self.last_update_id = None

    def get_updates(self):
        method = 'getUpdates'
        params = {'offset': self.last_update_id + 1 if self.last_update_id else None}
        response = requests.get(self.base_url + method, params=params)
        if response.status_code == 200:
            updates = response.json()['result']
            if updates:
                self.last_update_id = updates[-1]['update_id']
            return updates
        return []

    def get_messages(self):
        updates = self.get_updates()
        messages = []
        for update in updates:
            message = update.get('message')
            if message:
                text = message.get('text')
                sender_name = message.get('from').get('first_name')
                time = datetime.fromtimestamp(message.get('date')).strftime('%Y-%m-%d %H:%M:%S')
                messages.append({'text': text, 'sender_name': sender_name, 'time': time})
        return messages
    
    def wait_message(self):
        telegram_receiver = TelegramReceiver(BOT_TOKEN)
        telegram_sender = TelegramSender()
        controller = Controller()
        while True:
            messages = telegram_receiver.get_messages()
            for message in messages:
                print(f"Message from {message['sender_name']} at {message['time']}: {message['text']}")
                reply = telegram_sender.check_message(message['text'])
                if reply:
                    controller.type_message(f"@{message['sender_name']} {reply}")  # Mention the sender in the reply
            time.sleep(1)

class TelegramSender:

    def __init__(self):
        self.general_replies = [
            "Please be respectful in your language. Personal attacks are not allowed.",
            "Let's keep the chat positive and welcoming for everyone.",
            "Remember to treat others with kindness and respect.",
            "We encourage constructive and respectful conversations. Please avoid using offensive language.",
            "Let's keep the conversation friendly and respectful.",
            "Please refrain from using language that could be considered offensive or harmful to others."
        ]

    def check_message(self, message):
        offensive_keywords = [
            "kill yourself",
            "you're a failure",
            "nobody cares about you",
            "you're not welcome",
            "potang ina mo",
            "gago ka ba",
            "gago",
            "fuck",
            "hayop ka",
            "mamatay na magulang mo"
        ]
        for keyword in offensive_keywords:
            if keyword.lower() in message.lower():
                return random.choice(self.general_replies)
        return None


class Main: 
    def run(self):
        controller = Controller()
        controller.open_telegram()
        
        telegram_receiver = TelegramReceiver(BOT_TOKEN)
        message = telegram_receiver.wait_message()
        print(f"Received message: {message}")


if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()