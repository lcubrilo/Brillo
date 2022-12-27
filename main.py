import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QTreeWidgetItem, QTreeWidget, QWidget, QCheckBox, QHBoxLayout, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QPoint
from QMeasurement import QMeasurement

from PandasModelClass import PandasModel

class MyApplicationMainWindow(QMainWindow):
    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow_tabs.ui", self)

        # Slot-signal connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotData)  
        self.deleteButton.clicked.connect(self.deleteColumns)
        self.reloadButton.clicked.connect(self.reloadFiles)
        self.editButton.clicked.connect(self.editColumn)

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

        # populate comboboxes with columns
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
        from brlopack import brlopack
        import arrayConversion
        operations = {
            "Divide by constant": brlopack.divide,
            "Convert unit": arrayConversion.adapter_ConvertPrefix
        }

        inputColumn = self.inputColCombo.currentText()
        operation = self.operationCombo.currentText()
        constant = self.constCombo.currentText()
        outputColumn = self.outputColLineEdit.text()

        operations[operation](self.paket, inputColumn, outputColumn, constant)


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
        self.plotButton.enabled = False
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
        for constName in self.paket.constants[currFile][currTable]:
            value = self.paket.constants[currFile][currTable][constName]
            tmpWidget = QMeasurement(constName, value)
            tmpWidget.line_edit.setEnabled(False)
            layout.addWidget(tmpWidget)

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
    
    def deleteColumns(self):
        self.tableView.setModel(None)
        columnsToDelete = []

        for checkBox in self.columnsScrollArea.findChildren(QCheckBox):
            if checkBox.checkState() == Qt.Unchecked:
                if checkBox.isEnabled():
                    columnName = checkBox.text()
                    columnsToDelete.append(columnName)

                    index = self.xAxisCombo.findText(columnName)
                    self.xAxisCombo.removeItem(index)
                    self.yAxisCombo.removeItem(index)
                    self.inputColCombo.removeItem(index)

                    checkBox.setEnabled(False)
        
        for file in self.paket.tellMeFiles():
            for table in self.paket.tellMeTablesInFile(file):

                for columnToDel in columnsToDelete:
                    del self.paket.data[file][table][columnToDel]

        msg = QMessageBox()

        msg.setWindowTitle("Notification")
        msg.setText("You have just deleted the columns that were unselected. To get them back, reload the files. (That also means any new ones that were unsaved are going to be lost)")
        x = msg.exec_()  

app = QtWidgets.QApplication(sys.argv)
window = MyApplicationMainWindow()
window.show()
app.exec()

