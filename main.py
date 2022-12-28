import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QTreeWidgetItem, QTreeWidget, QWidget, QCheckBox, QHBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QPoint, QFile
from QMeasurement import QMeasurement

# Custom packages
from PandasModelClass import PandasModel
from brlopack import brlopack
import arrayConversion
from addConstantDialog import addConstantDialog

class MyApplicationMainWindow(QMainWindow):
    def openAddConstantDialog(self):
        items = self.treeWidget.selectedItems()
        if not items: return
        file = items[0].parent().text(0)
        dialog = addConstantDialog(file)
        dialog.constantLoaded.connect(self.addingTheConstant)
        dialog.exec_()
    
    def addingTheConstant(self, constName, value, unit):
        items = self.treeWidget.selectedItems()
        if not items: return
        file = items[0].parent().text(0)
        for table in self.paket.tellMeTablesInFile(file):
            self.paket.constants[file][table][constName] = (value, unit)
    
    def loadCode(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", "macros")[0]
        file = QFile(fileName)
        file.open(QFile.ReadOnly | QFile.Text)
        text = file.readAll()
        text = bytearray(text.data()).decode("utf-8")
        file.close()
        self.codePlainEdit.setPlainText(str(text))
    
    def saveCode(self):
        fileName = self.filenameLineEdit.text()
        with open(fileName, "w") as f:
            for line in self.codePlainEdit.toPlainText():
                f.write(line)
        
    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow_tabs.ui", self)
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

        # assuming all tables have the same columns

        self.updateColumns()

        # display constants
        firstFile = self.paket.tellMeFiles()[0]
        firstTable = self.paket.tellMeTablesInFile(firstFile)[0]
        for constName in self.paket.constants[firstFile][firstTable]:
            self.constCombo.addItem(constName)
        
        # display operations
        operations = ["Divide by constant", "Convert unit"]
        for op in operations:
            self.operationCombo.addItem(op)
    
    def checkIfConstantNeeded(self, index):
        item = self.operationCombo.itemText(index)
        if item in ["Divide by constant"]:
            self.constCombo.setEnabled(True)
        else:
            self.constCombo.setEnabled(False)

    def editColumn(self):
        operations = {
            "Divide by constant": brlopack.divide,
            "Convert unit": arrayConversion.adapter_ConvertPrefix
        }

        # Prepare arguments
        inputColumn = self.inputColCombo.currentText()
        operation = self.operationCombo.currentText()
        constant = self.constCombo.currentText()
        outputColumn = self.outputColLineEdit.text()

        # Run operation
        operations[operation](self.paket, inputColumn, outputColumn, constant)

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

        self.paket.tellFiles(list(self.fileNames))
        self.paket.loadFiles()

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
        
    def showData(self, item, column):
        # TODO clear prevous??
        #currentItem = self.treeWidget.currentItem()
        if item.parent() == None: return

        currFile = item.parent().text(0)
        currTable = item.text(0)
        dataFrame = self.paket.data[currFile][currTable]

        self.model = PandasModel(dataFrame)
        self.tableView.setModel(self.model)

        # Load Constants
        widget = QWidget()
        layout = QHBoxLayout(widget)
        tmp = QPushButton("+"); tmp.setMaximumSize(50,50); layout.addWidget(tmp); self.addConstantButton = tmp; self.addConstantButton.clicked.connect(self.openAddConstantDialog)
        for constName in self.paket.constants[currFile][currTable]:
            value = self.paket.constants[currFile][currTable][constName]
            tmpWidget = QMeasurement(constName, value)
            tmpWidget.line_edit.setEnabled(False)
            layout.addWidget(tmpWidget)
            tmpWidget.unitChanged.connect(self.paket.changeUnitOfConstant)
            """layout.addWidget(QLabel(constName))
            
            tmp = QLineEdit()
            tmp.setText(str(value))
            tmp.setEnabled(False)
            layout.addWidget(tmp)"""

        self.constantScrollArea.setWidget(widget)
            
    def plotData(self):
        x_axis = self.xAxisCombo.currentText()
        y_axis = self.yAxisCombo.currentText()
    
        if x_axis == "" or y_axis == "":
            return
            
        self.paket.plotData(x_axis, y_axis, self.filesToPlot, self.tablesToPlot)
    
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
                    #print("Constant convert", constant, newPrefix)
                else: # column convert
                    arrayConversion.adapter_ConvertPrefix(self.paket, input, output)
            
            elif line.startswith("divide"):
                input = args[0]
                constant = args[1]
                output = args[2]
                self.paket.divide(input, output, constant)
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
            else:
                print("bruh")
        
        self.updateColumns()

def aplikacija():                
    app = QtWidgets.QApplication(sys.argv)
    window = MyApplicationMainWindow()
    window.show()
    app.exec()

def readCSV(fileName):
    
    f = open(fileName, "r") # open the file
    matrix = [] # get an empty table ready
    for line in f: # go line by line in file - that is gonna become our rows in table
        if line == "\n": continue # skip empty rows; "\n" means "newline"
        tmpArr = line.split(";") # separate values by the ";" character and store in a temporary array
        if len(tmpArr) > 1: tmpArr=tmpArr[1:] # they always had the first one empty, delete it
        if len(tmpArr) == 1: continue # if it has just one element it is pre-table bullshit
        if not tmpArr[0].isdigit(): # this only happens in the header row (where names of columns are)
            n = len("X data for ")
            for i in range(1, len(tmpArr)):
                tmpArr[i] = tmpArr[i][n:] # this removes "X data for " from beginning of column name

        # this keeps only even (not odd) column to avoid repeating data
        tmpArr = [tmpArr[i] for i in range(len(tmpArr)) if i%2==0 or i==1]
        matrix.append(tmpArr) # after processing this row, add it to table
    f.close()
    from pandas import DataFrame
    df = DataFrame(matrix[1:], columns=matrix[0])
    return {fileName:{"table1":df}}

"""data = readCSV("data/BCTZ_cicle16-2022-10-09-For easy export.csv")
paket = brlopack(data)
for file in paket.tellMeFiles():
    for table in paket.tellMeTablesInFile(file):
        print(paket.data[file][table].info())"""
"""
paket = brlopack()
paket.tellFiles(["data/BCTZ_cicle16-2022-10-09-For easy export.csv"])
paket.loadFiles()

for file in paket.tellMeFiles():
    for table in paket.tellMeTablesInFile(file):
        print("\n\n{}, {}".format(file, table))
        print(paket.data[file][table].info())"""
aplikacija()