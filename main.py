#!/usr/bin/env python
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QPoint, QFile, QTextStream
from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtGui import QFont
from QMeasurement import QMeasurement
import importlib
from qt_material import apply_stylesheet

# Custom packages
from PandasModelClass import PandasModel
import brlopack
import arrayConversion
from addConstantDialog import addConstantDialog
from QLoadingMessageBox import QLoadingMessageBox
killThread = False
# TODO: Constants can become zero after too many conversions due to huge precision loss
# Solution: do not ever change units in brlopack. only in the gui. then add a getter in the brlopack that says unit in the function name! so it only converts for the output

"""class ProgressValue(QObject):
    valueChanged = pyqtSignal(int)
    def __init__(self, value=0):
        super().__init__()
        self._value = value

    #@pyqtProperty(int)
    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            self.valueChanged.emit(value)"""

class MyApplicationMainWindow(QMainWindow):
    def splitData(self):
        importlib.reload(brlopack)
        columnName = self.splittingColumnCombo.currentText()
        try:
            self.paket.separateData(columnName)
            self.browseFiles(dontBrowse=True, dontLoad=True)
        except:
            QLoadingMessageBox(self, "Splitting failed.")

    def update_progress(self):
        step = int(self.progressBar.maximum()/1.4**self.coef)

        if self.progressBar.value() <= self.progressBar.maximum() - 2*step:
            self.progressBar.setValue(self.progressBar.value() + step)
        else:
            self.progressBar.setValue(1)
            self.coef +=1

        if self.progressBar.value() <= self.progressBar.maximum():
            step = int(self.progressBar.maximum()/1.4**self.coef)
            self.progressBar.setValue(self.progressBar.value() + step)
            #time.sleep(0.05)

    def overrideText(self, inputQSS, new_value):
        i = 0
        while i < len(inputQSS):
            try:
                start_index = inputQSS.index("font-size:", i) + len("font-size:")
                end_index = inputQSS.index("px;", start_index)
                old_value = inputQSS[start_index:end_index].strip()
                inputQSS = inputQSS.replace(f"font-size: {old_value}px", f"font-size: {new_value}px")
                i = start_index + len(f"{new_value}px")
            except:
                break

        i = 0  
        while i < len(inputQSS):
            try:
                start_index = inputQSS.index("padding:", i) + len("padding:")
                end_index = inputQSS.index("px;", start_index)
                old_value = inputQSS[start_index:end_index].strip()
                new_value = int(old_value) + 1
                inputQSS = inputQSS.replace(f"padding: {old_value}px", f"padding: {new_value}px")
                i = start_index + len(f"{new_value}px")
            except:
                return inputQSS

    def keyPressEvent(self, event):
        # Check for the Ctrl + key
        if event.modifiers() and Qt.ControlModifier:
            if (event.key() == Qt.Key_Plus or event.key() ==  Qt.Key_Equal):
                self.font_size += 2
            elif event.key() == Qt.Key_Minus:
                if self.font_size > 3: #don't go into negative
                    self.font_size -= 2
            else: return
        self.setFont(QFont('Arial', self.font_size))

        stylesheet = self.app.styleSheet()
        self.app.setStyleSheet(self.overrideText(stylesheet, self.font_size))
            
            
        super().keyPressEvent(event)

    def getCurrentFileTable(self, notText = False):
        items = self.treeWidget.selectedItems()

        if type(items) != list or len(items) == 0:
            point = QPoint(10, 10)
            table = self.treeWidget.itemAt(point).child(0)
            file = self.treeWidget.itemAt(point)
        else:
            file = items[0].parent()
            table = items[0]
        
        if notText:
            return file, table
        else:
            return file.text(0), table.text(0)

    def openAddConstantDialog(self):
        items = self.treeWidget.selectedItems()
        if not items: return
        file, table = self.getCurrentFileTable()
        self.dialog = addConstantDialog(file)
        self.dialog.constantLoaded.connect(self.addingTheConstant)
        self.dialog.exec_()
        
    def addingTheConstant(self, constName, value, unit):
        items = self.treeWidget.selectedItems()
        if not items: return
        file, table = self.getCurrentFileTable()
        for t in self.paket.tellMeTablesInFile(file):
            self.paket.constants[file][t][constName] = (float(value), unit)
        self.constCombo.addItem(constName)
        self.dialog.done(0)
        self.updateConstants()
    
    def loadCode(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", "macros")[0]
        file = QFile(fileName)
        file.open(QFile.ReadOnly | QFile.Text)
        text = file.readAll()
        text = bytearray(text.data()).decode("ISO-8859-1")
        file.close()
        self.codePlainEdit.setPlainText(str(text))
        self.filenameLineEdit.setText(fileName)
    
    def saveCode(self):
        fileName = self.filenameLineEdit.text()
        try:
            with open("macros/"+fileName, "w") as f:
                for line in self.codePlainEdit.toPlainText():
                    f.write(line)
        except:
            QLoadingMessageBox(self, "You need to specify a file name")

    """def plotStateChanged(self):
        if self.showCheckbox.isChecked():
            self.plotButton.setText("Display the final plot")
        else:
            self.plotButton.setText("Add this to the final plot")"""

    def exportFromPlot(self, columnNames):

        x_axis = self.xAxisCombo.currentText()
        checkBoxes = [item for item in self.yColumnsScrollArea.widget().children() if type(item) == type(QCheckBox())]
        y_axes = [item.text() for item in checkBoxes if item.isChecked()]
        columnsToExport = [x_axis] + y_axes 

        tablesToExport = [item for item in self.yColumnsScrollArea.widget().children() if type(item) == type(QCheckBox())]
        y_axes = [item.text() for item in checkBoxes if item.isChecked()]

        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "")


        self.paket.exportToExcel(directory, columnsToExport, self.filesToPlot, self.tablesToPlot)

    def setupUI(self):
        # Load UI from .ui file
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mainwindow_tabs.ui")
        uic.loadUi(path, self)
        self.font_size = 12
        self.plotButton.setEnabled(True) # I really dont know why this is necessary... but it is.
        self.exportButton.setEnabled(True) # I really dont know why this is necessary... but it is.
        
        # Slot-signal connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotData)  
        self.deleteButton.clicked.connect(self.deleteColumns)
        self.reloadButton.clicked.connect(self.reloadFiles)
        self.editButton.clicked.connect(self.editColumn)
        self.runCodeButton.clicked.connect(self.parseCode)
        self.loadCodeButton.clicked.connect(self.loadCode)
        self.saveCodeButton.clicked.connect(self.saveCode)
        self.addConstantButton.clicked.connect(self.openAddConstantDialog)
        self.splitDataButton.clicked.connect(self.splitData)
        
        #self.showCheckbox.stateChanged.connect(self.plotStateChanged)
        

        self.operationCombo.currentIndexChanged.connect(self.checkIfConstantNeeded)

        

        
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update_progress)

    def setupUI2(self):
        self.setEnabled(True)
        # treeWidget connections
        self.treeWidget.itemClicked.connect(self.showData)
        self.treeWidget.itemChanged.connect(self.updateFilesToPlot)
        self.treeWidget.itemChanged.connect(self.updateTablesToPlot)

        # We have to run showData() at least once so that self.model isn't None
        point = QPoint(10, 10)
        item = self.treeWidget.itemAt(point).child(0)
        self.showData(item, 0)

        self.reloadButton.setEnabled(True)
        # enable right part of the screen
        self.tabWidget.setEnabled(True)
        self.browseButton.setEnabled(False)

        # assuming all tables have the same columns
        self.updateColumns()

        # display constants
        self.updateConstants()
        
        # display operations
        #if self.operationCombo.currentText == "":
        for i, op in enumerate(self.operationsDictionary):
            self.operationCombo.addItem(op)
            if i == self.border-1:
                self.operationCombo.addItem("-----")
        
        #self.progressBar.setValue(self.progressBar.maximum())

    def checkIfConstantNeeded(self, index):
        item = self.operationCombo.itemText(index)
        if item in [key for key in self.operationsDictionary][self.border:]:
            self.constCombo.setEnabled(True)
        else:
            self.constCombo.setEnabled(False)

    def editColumn(self):
        # Prepare arguments
        inputColumn = self.inputColCombo.currentText()
        operation = self.operationCombo.currentText()
        constant = self.constCombo.currentText()
        outputColumn = self.outputColLineEdit.text()

        # Run operation
        if operation == "-----":
            return
        
        if operation in ["Convert unit"]:
            self.operationsDictionary[operation](self.paket, inputColumn, outputColumn, constant)
        else:
            self.operationsDictionary[operation](inputColumn, outputColumn, constant)

        self.updateColumns()

    def updateColumns(self):
        # populate comboboxes with columns
        self.xAxisCombo.clear()
        #self.yAxisCombo.clear()
        self.inputColCombo.clear()
        self.splittingColumnCombo.clear()
        #self.yColumnsScrollArea.clear()

        for val in self.model._dataframe.columns.values:
            self.xAxisCombo.addItem(val)
            #self.yAxisCombo.addItem(val)
            self.inputColCombo.addItem(val)
            self.splittingColumnCombo.addItem(val)

        # display columns that can be deleted
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        for val in self.model._dataframe.columns.values:
            tmpCheckBox = QCheckBox(val, self.columnsScrollArea)
            tmpCheckBox.setCheckState(Qt.Checked)
            layout.addWidget(tmpCheckBox)
        
        self.columnsScrollArea.setWidget(widget)
        self.scrollAreaLayout = layout

        # display columns that will be plotted
        widget = QWidget()
        layout = QVBoxLayout(widget)

        for val in self.model._dataframe.columns.values:
            tmpCheckBox = QCheckBox(val, self.yColumnsScrollArea)
            tmpCheckBox.setCheckState(Qt.Unchecked)
            layout.addWidget(tmpCheckBox)
        
        self.yColumnsScrollArea.setWidget(widget)
        self.yScrollAreaLayout = layout
    
    def updateConstants(self, currFile=None, currTable=None):
        if currFile == None or currTable == None:
            currFile, currTable = self.getCurrentFileTable()

        self.constCombo.clear()
        widget = QWidget()
        layout = QHBoxLayout(widget)
        tmp = QPushButton("+"); tmp.setMaximumSize(50,50); layout.addWidget(tmp); self.addConstantButton = tmp; self.addConstantButton.clicked.connect(self.openAddConstantDialog)
        for constName in self.paket.constants[currFile][currTable]:
            value = self.paket.constants[currFile][currTable][constName]
            tmpWidget = QMeasurement(constName, value)
            tmpWidget.line_edit.setEnabled(False)
            layout.addWidget(tmpWidget)
            tmpWidget.unitChanged.connect(self.paket.changeUnitOfConstant)
            self.constCombo.addItem(constName)
        self.constantScrollArea.setWidget(widget)

        file, table = self.getCurrentFileTable(True)
        self.treeWidget.setCurrentItem(table)

    def updateFilesToPlot(self, item, column):
        if item.parent() != None: return
        print("UPDATE FILES TO PLOT TRIGGERED")
        currentFile = item
        if currentFile == None: print("NONE ERROR"); return
        else: print("\n=====", currentFile)

        if currentFile.checkState(column) == Qt.Checked:
            if currentFile.text(column) not in self.filesToPlot:
                self.filesToPlot.add(currentFile.text(column))
                print("NOW ADDED HIM TO LIST")
        
        elif currentFile.checkState(column) == Qt.Unchecked:
            if currentFile.text(column) in self.filesToPlot:
                self.filesToPlot.remove(currentFile.text(column))
                print("NOW REMOVED HIM FROM LIST")
    
    def updateTablesToPlot(self, item, column):
        currentTable = item
        if currentTable == None: return
        currentFile = item.parent()
        if currentFile == None: return

        if currentTable.checkState(0) == Qt.Checked:
            if currentTable.text(0) not in self.tablesToPlot[currentFile.text(0)]:
                self.tablesToPlot[currentFile.text(0)].add(currentTable.text(0))
                print("NOW ADDED HIM TO LIST")

        elif currentTable.checkState(0) == Qt.Unchecked:
            if currentTable.text(0) in self.tablesToPlot[currentFile.text(0)]:
                self.tablesToPlot[currentFile.text(0)].remove(currentTable.text(0))
                print("NOW REMOVED HIM FROM LIST")

    def prepareForExport(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "")
        self.paket.exportToExcel(directory)

    def __init__(self, app):
        super(MyApplicationMainWindow,self).__init__()
        self.setupUI()
        self.app = app
        
        self.paket = brlopack.brlopack()
        
        self.exportButton.clicked.connect(self.prepareForExport)#needs to be here instead of setupUi because of some scope problem, doesnt see self.paket??
        self.plotExportButton.clicked.connect(self.exportFromPlot)

        self.filesToPlot = set()
        self.tablesToPlot = {}
        self.fileNames = None

        #from brlopack import brlopack.inverseColumn, brlopack.squareColumn, brlopack.sqrtColumn, brlopack.divideConstant, brlopack.multiplyConstant, brlopack.addConstant, brlopack.subtractConstant
        self.operationsDictionary = {
            "Convert unit": arrayConversion.adapter_ConvertPrefix, 
            "Inverse/reciprocal value (^-1)": self.paket.inverseColumn,
            "Square value (^2)": self.paket.squareColumn,
            "Square root value (^0.5)": self.paket.sqrtColumn,

            "Divide by constant": self.paket.divideConstant,
            "Multiply by constant": self.paket.multiplyConstant,
            "Add constant": self.paket.addConstant,
            "Subtract constant": self.paket.subtractConstant
        }

        self.border = 4
        self.coef = 2

    def reloadFiles(self):
        QLoadingMessageBox(self, "You have reloaded the files. Deleted columns are now back and any newly added ones are gone.")

        self.browseFiles(dontBrowse=True)

    def browseFiles(self, dontBrowse=False, dontLoad=False):
        #self.treeWidget.clear()
        if not dontBrowse:
            self.fileNames = QFileDialog.getOpenFileNames(self, "Open file", "data")[0]
        elif self.fileNames == None:
            raise Exception("Which files am I supposed to load?")
        else:
            self.treeWidget.clear()
            self.operationCombo.clear()

        self.setEnabled(False)
        #self.progressBarThread.start()
        #progress_value = ProgressValue()
        #progress_value.valueChanged.connect(self.progressBar.setValue)


        self.paket.tellFiles(list(self.fileNames))
        #self.killThread = False
        #operationThread = threading.Thread(target=QLoadingMessageBox, args=[self, "Please wait until the files load", True])
        #operationThread.start()
        #timer = QTimer()
        #timer.timeout.connect(self.update_progress)
        #timer.start(2)
        #QLoadingMessageBox(self, "Loading the files, please wait.", False)

        from time import time

        now = time()

        if not dontLoad:
             self.paket.loadFiles(self.update_progress)

        self.progressBar.setValue(self.progressBar.maximum())

        delta = round(time()-now, 4)
        print("Operation lasted {} seconds".format(delta))
        #self.killThread = True
        #operationThread = threading.Thread(target=self.paket.loadFiles)
        #operationThread.start()
        #for i in range(101):
            #progress_value.value = i
        #self.app.processEvents() # for updating the bar
        try:
            print()
        #self.progressBarThread.terminate()
        except Exception as e:
            QLoadingMessageBox(self, "An error 1 happened. Crashed during file load. Try again.")

            print(e)
            return

        if self.fileNames == []:
            QLoadingMessageBox(self, "An error 2 happened. 0 files loaded. Try again.")
            return

        # Populating the tree widget with files and tables
        for i, file in enumerate(self.paket.tellMeFiles()):
            tmp = QTreeWidgetItem(self.treeWidget, [file])
            tmp.setCheckState(0, Qt.Checked)
            
            for table in self.paket.tellMeTablesInFile(file):
                tmpChild = QTreeWidgetItem(tmp, [table])#(tmp)
                tmpChild.setCheckState(0, Qt.Checked)
            
        # TODO Put in setupui()??? seems to crash after loading
         

        # Put all to be plotted
        for file in self.paket.tellMeFiles():
            self.filesToPlot.add(file)
            self.tablesToPlot[file] = set()
            for table in self.paket.tellMeTablesInFile(file):
                self.tablesToPlot[file].add(table)
        
        self.setupUI2()

        """from improvedFunctions import forDataFrame
        firstFile = self.paket.tellMeFiles()[0]
        firstTable = self.paket.tellMeTablesInFile(firstFile)[0]
        dataFrame = self.paket.data[firstFile][firstTable]
        res = forDataFrame(dataFrame)"""
        #print(res)
        
    def showData(self, item, column):
        # TODO clear prevous??
        #currentItem = self.treeWidget.currentItem()
        if item.parent() == None: 
            return

        currFile, currTable = self.getCurrentFileTable()
        dataFrame = self.paket.data[currFile][currTable]

        self.model = PandasModel(dataFrame)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()

        self.updateConstants(currFile, currTable)


    def plotData(self):
        x_axis = self.xAxisCombo.currentText() 
        y_axes = [checkBox.text() for checkBox in self.yColumnsScrollArea.findChildren(QCheckBox) if checkBox.checkState() == Qt.Checked] 
        if x_axis == "" or y_axes == []:
            return

        if self.paket.tellMeFiles()[0].endswith(".csv"):
            conditionColName="AVG T  [°C]"; minimumValue=200    
        else:
            conditionColName=None; minimumValue=None    
        plotType = self.plotTypeCombo.currentText()
        #show = self.showCheckbox.isChecked()

        self.paket.plotData(x_axis, y_axes, self.filesToPlot, self.tablesToPlot, conditionColName, minimumValue, plotType)
        #TODO
    def deleteColumns(self, columnsArg = None):
        self.tableView.setModel(None)
        if not columnsArg:
            columnsToDelete = []  

            for checkBox in self.columnsScrollArea.findChildren(QCheckBox):
                if checkBox.checkState() == Qt.Unchecked:
                    if checkBox.isEnabled():
                        columnName = checkBox.text()
                        columnsToDelete.append(columnName)
                        checkBox.setEnabled(False)
        else:
            columnsToDelete =  columnsArg

        """for columnName in columnsToDelete:
            index = self.xAxisCombo.findText(columnName)
            self.xAxisCombo.removeItem(index)
            #self.yAxisCombo.removeItem(index)
            self.yColumnsScrollArea.removeItem(columnName)
            self.inputColCombo.removeItem(index)"""
        
        
        for file in self.paket.tellMeFiles():
            for table in self.paket.tellMeTablesInFile(file):

                for columnToDel in columnsToDelete:
                    del self.paket.data[file][table][columnToDel]

        QLoadingMessageBox(self, "You have just deleted the columns that were unselected. To get them back, reload the files. (That also means any new ones that were unsaved are going to be lost)")
        self.updateColumns()

    def parseCode(self):
        #with open("macroExample.txt", "r") as f:
        for line in self.codePlainEdit.toPlainText().split("\n"):
            try:
                if len(line) <= 1: continue
                if line[0] == "#" or line == "\n": continue

                start = line.find("(")
                end = line.rfind(")")

                args = line[start+1:end]
                args = args.split('", "')
                args[0] = args[0][1:]
                args[-1] = args[-1][:-1]
                

                if line.startswith("delete"):
                    self.deleteColumns(args)

                elif line.startswith("convert"):
                    input = args[0]
                    output = args[1]

                    if input.find("[") == -1: #constant convert:
                        constant = input
                        newPrefix = output[0]
                        self.paket.changeUnitOfConstant(constant, newPrefix)
                        self.updateConstants()
                    else: # column convert
                        arrayConversion.adapter_ConvertPrefix(self.paket, input, output)
                

                elif line.startswith("export"):
                    QLoadingMessageBox(self, "You are saving all of the changes to the data and exporting them to Excel.\nThis will take a while.")
                    
                    self.paket.exportToExcel()
                    
                    QLoadingMessageBox(self, "Exporting done!")
                
                elif self.operationsWithConstants(line):
                    input = args[0]
                    constant = args[1]
                    output = args[2]

                    firstFile = self.paket.tellMeFiles()[0]
                    firstTable = self.paket.tellMeTablesInFile(firstFile)[0]

                    if constant not in self.paket.constants[firstFile][firstTable]:
                        QLoadingMessageBox(self, "This constant ({}) doesn't exist, stopping macro.".format(constant))
                        return
                    if input not in self.paket.data[firstFile][firstTable].columns:
                        QLoadingMessageBox(self, "This column ({}) doesn't exist, stopping macro.".format(input))
                        return

                    self.operationsWithConstants(line)(input, output, constant)

                elif self.powerOperations(line):
                    input = args[0]
                    output = args[1]

                    if input not in self.paket.data[firstFile][firstTable].columns:
                        QLoadingMessageBox(self, "This column ({}) doesn't exist, stopping macro.".format(input))
                        return

                    self.powerOperations(line)(input, output)

                else:
                    print("bruh")
            except:
                continue
            
            self.updateColumns()
    
    def operationsWithConstants(self, line):
        operations ={
            "divide": self.paket.divideConstant,
            "multiply": self.paket.multiplyConstant,
            "add": self.paket.addConstant,
            "subtract": self.paket.subtractConstant,
        }
        for key in operations:
            if line.startswith(key):
                return operations[key]
        
        return False
    
    def powerOperations(self, line):
        operations ={
            "inverse": self.paket.inverseColumn,
            "square": self.paket.squareColumn,
            "sqrt": self.paket.sqrtColumn,
        }
        for key in operations:
            if line.startswith(key):
                return operations[key]
        
        return False
    
import os



def aplikacija():                
    app = QtWidgets.QApplication(sys.argv)

    apply_stylesheet(app, theme='dark_teal.xml')

    window = MyApplicationMainWindow(app)
    window.setWindowTitle("Brillo")
    window.codePlainEdit.setProperty('class', 'code_editor')

    stylesheet = app.styleSheet()
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "style.qss")
    with open(path) as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window.show()
    app.exec()
    input()

if __name__=="__main__":
    aplikacija()

