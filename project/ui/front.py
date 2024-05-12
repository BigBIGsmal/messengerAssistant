from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QObject
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

class MainWindow(QMainWindow):
    def __init__(self, back_end):
        super().__init__()

        self.back_end = back_end

        self.setWindowTitle("Speech to Text App")

        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        self.text_edit = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.record_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.text_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.worker = Worker(self.back_end)
        self.worker.finished.connect(self.display_text)
        self.worker.recording_stopped.connect(self.stop_recording)

    def stop_recording(self):
        print("Front: Recording Stopped")

    def start_recording(self):
        print("Front: Record button clicked")  # Print statement for record button
        self.worker.start()

    def display_text(self):
        text = self.back_end.stop_recording()
        self.text_edit.setPlainText(text)
