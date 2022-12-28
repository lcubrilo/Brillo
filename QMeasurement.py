from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import valueConversion

class QMeasurement(QWidget):
    unitChanged = pyqtSignal(str, str)
    def __init__(self, measurementName, measurement):
        super().__init__()
        #self.setStyleSheet("font-size: 16pt;")
        self.val = measurement

        # Create the label
        self.label = QLabel(measurementName)

        num, unit = measurement
        measurement = (int(num), unit)
        # Create the line edit
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(str(num))

        # Create the combo box
        self.combo_box = QComboBox(self)
        #self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        self.addUnits(unit)

        # Add the label, line edit, and combo box to the widget layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.combo_box)
        self.setLayout(self.layout)
    
    def addUnits(self, unit):
        baseVal = valueConversion.removePrefix(self.val)
        baseNum, baseUnit = baseVal

        allUnits = []
        larg = list(reversed(valueConversion.largerLetter))
        smal = valueConversion.smallerLetter

        for letter in larg + [""] + smal:
            self.combo_box.addItem(letter+baseUnit)
        
        index = self.combo_box.findText(unit)
        self.combo_box.setCurrentIndex(index)

        self.combo_box.currentIndexChanged.connect(self.changeUnit)
    
    def changeUnit(self, index):
        newUnit = self.combo_box.currentText()
        if newUnit[-1].isdigit(): newUnit = newUnit[:-1]
        newPrefix = newUnit[0] if len(newUnit) > 1 else ""
        
        newVal = valueConversion.convertPrefix(self.val, newPrefix)
        self.line_edit.setText(str(newVal[0]))
        self.unitChanged.emit(self.label.text(), newPrefix)
        

if __name__ == "__main__":
    app = QApplication([])
    widget = QMeasurement("thickness", (1, "m"))
    widget.exec_()