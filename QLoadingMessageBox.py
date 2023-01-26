from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QProgressBar,QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
import time
import sys

class QLoadingMessageBox(QDialog):
    def __init__(self, callingWindow, message, load=False, coef=5, parent=None):
        super().__init__(parent)

        self.coef = coef
        self.load = load
        self.callingWindow = callingWindow
        
        layout = QVBoxLayout()
        
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font: 16pt")
        layout.addWidget(self.label)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        #layout.addWidget(self.progressBar)

        self.showProgressButton = QPushButton("Show progress")
        self.showProgressButton.clicked.connect(self.update_progress)
        if load:
            #layout.addWidget(self.showProgressButton)
            print()
            
        self.setLayout(layout)

        timer = QTimer()
        timer.timeout.connect(self.update_progress)
        timer.start(1000)

        self.show()
        self.exec_()

        
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_progress()


    def showEvent(self, event):
        self.progressBar.setValue(1)
        super().showEvent(event)

    def update_progress(self):
        step = int(self.progressBar.maximum()/1.4**self.coef)

        while self.progressBar.value() < self.progressBar.maximum() - 2*step:
            self.progressBar.setValue(self.progressBar.value() + step)
            time.sleep(0.05)
        """else:
            self.close()
            if self.callingWindow.killThread == False:
                try:
                    QLoadingMessageBox(self.callingWindow, self.label.text(), self.load, self.coef + 1)
                except:
                    print("jbg brt")"""
        self.progressBar.setValue(10)
        self.coef += 1

class random:
    def __init__(self):
        self.killThread = False

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = QLoadingMessageBox(random(), "Proba", True)
    #widget.exec_()
    
        
