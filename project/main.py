from ui  import front
from back import back
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    back_end = back.SpeechToTextEngine()
    window = front.MainWindow(back_end)
    window.show()
    sys.exit(app.exec_())
