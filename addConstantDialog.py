from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout

class addConstantDialog(QDialog):

    constantLoaded = pyqtSignal(str, str, str)
    def __init__(self, file):
        super().__init__()
        self.setStyleSheet("font-size: 16pt;")

        self.constName = QLineEdit()
        self.constName.setPlaceholderText("Constant name")

        self.numVal = QLineEdit()
        self.numVal.setPlaceholderText("Numerical value")

        self.unit = QLineEdit()
        self.unit.setPlaceholderText("Unit")

        self.button = QPushButton("Add this constant to file {}".format(file))
        self.button.clicked.connect(self.emit_signal)

        layout = QVBoxLayout()
        layout.addWidget(self.constName);layout.addWidget(self.numVal);layout.addWidget(self.unit);layout.addWidget(self.button);
        self.setLayout(layout)
    
    def emit_signal(self):
        c = self.constName.text()
        n = self.numVal.text()
        u = self.unit.text()
        self.constantLoaded.emit(c, n, u)

        