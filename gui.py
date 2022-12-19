from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import QSize, Qt
import sys

class prviProzor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OVo je naslov")
        button = QPushButton("klikni")

        self.setCentralWidget(button)
        self.setFixedSize(QSize(500,100))
        #minimumSize, MaximumSize


app = QApplication(sys.argv)

window = prviProzor()
#window = QPushButton("yooo")
window.show()

app.exec()