from ui import front
from back import back
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot

class App(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.back_end = back.SpeechToTextEngine()
        self.window = front.MainWindow(self.back_end)
        self.window.show()
        self.app.aboutToQuit.connect(self.cleanup)
        sys.exit(self.app.exec_())

    @pyqtSlot()
    def cleanup(self):
        """Perform cleanup when the application is about to quit."""
        self.back_end.cleanup()

if __name__ == "__main__":
    my_app = App()
