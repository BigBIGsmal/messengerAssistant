from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
import time 


class Worker(QThread):
    finished = pyqtSignal()
    recording_stopped = pyqtSignal()

    def __init__(self, back_end):
        super().__init__()
        self.back_end = back_end

    def run(self):
        self.back_end.start_recording()
        self.finished.emit()

    def stop_recording(self):
        self.back_end.stop_recording()
        self.recording_stopped.emit()

class MessageUpdater(QObject):
    messages_updated = pyqtSignal(list)

    def __init__(self, back_end):
        super().__init__()
        self.back_end = back_end
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_messages)
        self.timer.start(5000)  # Update every 5 seconds

    def fetch_messages(self):
        updates = self.back_end.get_updates()
        messages = []
        if updates and 'result' in updates:
            for result in updates['result']:
                if 'message' in result and 'text' in result['message']:
                    messages.append(result['message']['text'])
        if messages:
            self.messages_updated.emit(messages)

class MainWindow(QMainWindow):
    def __init__(self, back_end):
        super().__init__()

        self.back_end = back_end

        self.setWindowTitle("Speech to Text App")

        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        self.text_edit = QTextEdit()
        self.telegram_text_edit = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.record_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.telegram_text_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.worker = Worker(self.back_end)
        self.worker.finished.connect(self.display_text)
        self.worker.recording_stopped.connect(self.stop_recording)

        self.message_updater = MessageUpdater(back_end)
        self.message_updater.messages_updated.connect(self.update_messages)

    def stop_recording(self):
        print("Front: Recording Stopped")

    def start_recording(self):
        print("Front: Record button clicked")  # Print statement for record button
        self.worker.start()

    def display_text(self):
        text = self.back_end.stop_recording()
        self.text_edit.setPlainText(text)

    def display_telegram_text(self, telegram_text):
        self.telegram_text_edit.append(telegram_text)

    def update_messages(self, messages):
        # Update GUI with new messages
        for message in messages:
            self.telegram_text_edit.append(message)