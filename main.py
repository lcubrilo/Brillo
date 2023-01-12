import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QTreeWidgetItem, QTreeWidget, QWidget, QCheckBox, QHBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QPoint, QFile
from PyQt5.QtGui import QFont
from QMeasurement import QMeasurement

# Custom packages
from PandasModelClass import PandasModel
from brlopack import brlopack
import arrayConversion
from addConstantDialog import addConstantDialog

# TODO: Constants can become zero after too many conversions due to huge precision loss
# Solution: do not ever change units in brlopack. only in the gui. then add a getter in the brlopack that says unit in the function name! so it only converts for the output
class MyApplicationMainWindow(QMainWindow):
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
    
    def saveCode(self):
        fileName = self.filenameLineEdit.text()
        try:
            with open("macros/"+fileName, "w") as f:
                for line in self.codePlainEdit.toPlainText():
                    f.write(line)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("You need to specify a file name")
            x = msg.exec_()

    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow_tabs.ui", self)
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

        self.operationCombo.currentIndexChanged.connect(self.checkIfConstantNeeded)

    def setupUI2(self):
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
        self.operationsDictionary[operation](self.paket, inputColumn, outputColumn, constant)

        self.updateColumns()

    def updateColumns(self):
        # populate comboboxes with columns
        self.xAxisCombo.clear()
        self.yAxisCombo.clear()
        self.inputColCombo.clear()
        
        for val in self.model._dataframe.columns.values:
            self.xAxisCombo.addItem(val)
            self.yAxisCombo.addItem(val)
            self.inputColCombo.addItem(val)

        # display columns that can be deleted
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        for val in self.model._dataframe.columns.values:
            tmpCheckBox = QCheckBox(val, self.columnsScrollArea)
            tmpCheckBox.setCheckState(Qt.Checked)
            layout.addWidget(tmpCheckBox)
        
        self.columnsScrollArea.setWidget(widget)
        self.scrollAreaLayout = layout
    
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

    def __init__(self):
        super(MyApplicationMainWindow,self).__init__()
        self.setupUI()

        try:
            from brlopack import brlopack
            print("Successfully loaded `brlopack` from `brlopack`")
        except:
            print("!!!!!!!!!!!!!")
            print("ERROR: Importing the package was NOT successful.")
        
        self.paket = brlopack()
        self.exportButton.clicked.connect(self.paket.exportToExcel)
        
        self.filesToPlot = set()
        self.tablesToPlot = {}
        self.fileNames = None

        self.operationsDictionary = {
            "Convert unit": arrayConversion.adapter_ConvertPrefix, 
            "Inverse/reciprocal value (^-1)": brlopack.inverseColumn,
            "Square value (^2)": brlopack.squareColumn,
            "Square root value (^0.5)": brlopack.sqrtColumn,

            "Divide by constant": brlopack.divideConstant,
            "Multiply by constant": brlopack.multiplyConstant,
            "Add constant": brlopack.addConstant,
            "Subtract constant": brlopack.subtractConstant
        }

        self.border = 4

    def reloadFiles(self):
        msg = QMessageBox()

        msg.setWindowTitle("Notification")
        msg.setText("You have reloaded the files. Deleted columns are now back and any newly added ones are gone.")
        x = msg.exec_()
        self.browseFiles(dontBrowse=True)

    def browseFiles(self, dontBrowse=False):
        #self.treeWidget.clear()
        if not dontBrowse:
            self.fileNames = QFileDialog.getOpenFileNames(self, "Open file", "data")[0]
        elif self.fileNames == None:
            raise Exception("Which files am I supposed to load?")
        else:
            self.treeWidget.clear()
            self.operationCombo.clear()

        try:
            self.paket.tellFiles(list(self.fileNames))
            self.paket.loadFiles()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("An error 1 happened. Crashed during file load. Try again.")
            x = msg.exec_()  
            return

        if self.fileNames == []:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("An error 2 happened. 0 files loaded. Try again.")
            x = msg.exec_()  
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
        y_axis = self.yAxisCombo.currentText()

        if x_axis == "" or y_axis == "":
            return

        if self.paket.tellMeFiles()[0].endswith(".csv"):
            conditionColName="AVG T  [°C]"; minimumValue=200    
        else:
            conditionColName=None; minimumValue=None    
        plotType = self.plotTypeCombo.currentText()
        self.paket.plotData(x_axis, y_axis, self.filesToPlot, self.tablesToPlot,conditionColName, minimumValue, plotType)
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

        for columnName in columnsToDelete:
            index = self.xAxisCombo.findText(columnName)
            self.xAxisCombo.removeItem(index)
            self.yAxisCombo.removeItem(index)
            self.inputColCombo.removeItem(index)
        
        for file in self.paket.tellMeFiles():
            for table in self.paket.tellMeTablesInFile(file):

                for columnToDel in columnsToDelete:
                    del self.paket.data[file][table][columnToDel]

        msg = QMessageBox()

        msg.setWindowTitle("Notification")
        msg.setText("You have just deleted the columns that were unselected. To get them back, reload the files. (That also means any new ones that were unsaved are going to be lost)")
        x = msg.exec_()  

    def parseCode(self):
        #with open("macroExample.txt", "r") as f:
        for line in self.codePlainEdit.toPlainText().split("\n"):
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
                msg = QMessageBox()
                msg.setWindowTitle("Notification")
                msg.setText("You are saving all of the changes to the data and exporting them to Excel.\nThis will take a while.")
                x = msg.exec_()
                
                self.paket.exportToExcel()
                
                msg = QMessageBox()
                msg.setWindowTitle("Notification")
                msg.setText("Exporting done!")
                x = msg.exec_()
            
            elif self.operationsWithConstants(line):
                input = args[0]
                constant = args[1]
                output = args[2]

                self.operationsWithConstants(line)(input, output, constant)

            elif self.powerOperations(line):
                input = args[0]
                constant = args[1]

                self.powerOperations(line)(input, output)

            else:
                print("bruh")
        
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

def aplikacija():                
    app = QtWidgets.QApplication(sys.argv)
    window = MyApplicationMainWindow()
    window.show()
    app.exec()

aplikacija()