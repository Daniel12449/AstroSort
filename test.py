import sys

from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.button = QPushButton("Press me for a dialog!")
        self.button.clicked.connect(self.button_clicked)
        self.setCentralWidget(self.button)

    def button_clicked(self, s):
        print("click", s)

        dlg = QDialog(self)
        dlg.setWindowTitle("HELLO!")
        dlg.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()