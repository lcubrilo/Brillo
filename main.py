import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QTreeWidgetItem, QTreeWidget, QWidget, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

from PandasModelClass import PandasModel

class MyApplicationMainWindow(QMainWindow):
    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow.ui", self)

        # Slot-signal connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotData)  
        self.deleteButton.clicked.connect(self.deleteColumns)
        
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

    def browseFiles(self):
        self.plotButton.enabled = False
        #self.treeWidget.clear()
        fileNames = QFileDialog.getOpenFileNames(self, "Open file", "data")[0]

        self.paket.tellFiles(list(fileNames))
        self.paket.loadFiles()

        items = []
        for i, file in enumerate(self.paket.tellMeFiles()):
            tmp = QTreeWidgetItem(self.treeWidget, [file])
            items.append(tmp)
            items[i].setCheckState(0, Qt.Checked)
        
        #self.treeWidget.insertTopLevelItems(0, items)
            
            for table in self.paket.tellMeTablesInFile(file):
                tmpChild = QTreeWidgetItem(tmp, [table])#(tmp)
                #tmpChild.setText(table)
                tmpChild.setCheckState(0, Qt.Checked)
                #tmp.addChild(tmpChild)
            

        self.treeWidget.itemClicked.connect(self.showData)
        self.treeWidget.itemChanged.connect(self.updateFilesToPlot)
        self.treeWidget.itemChanged.connect(self.updateTablesToPlot)
        

        # Put all to be plotted
        for file in self.paket.tellMeFiles():
            self.filesToPlot.add(file)
            self.tablesToPlot[file] = set()
            for table in self.paket.tellMeTablesInFile(file):
                self.tablesToPlot[file].add(table)
        
        self.plotButton.enabled = True
        self.exportButton.enabled = True
        
    def showData(self, item, column):
        # TODO clear prevous??
        #currentItem = self.treeWidget.currentItem()
        if item.parent() == None: return

        self.currentFileSelected = item.parent().text(0)
        self.currentTableSelected = item.text(0)
        dataFrame = self.paket.data[self.currentFileSelected][self.currentTableSelected]

        self.model = PandasModel(dataFrame)
        self.tableView.setModel(self.model)

        if self.xAxisCombo.count() == 0:
            for val in self.model._dataframe.columns.values:
                self.xAxisCombo.addItem(val)
                self.yAxisCombo.addItem(val)

        if len(self.scrollArea.findChildren(QWidget)) == 6:
            widget = QWidget()
            layout = QHBoxLayout(widget)
            for val in self.model._dataframe.columns.values:
                tmpCheckBox = QCheckBox(val, self.scrollArea)
                tmpCheckBox.setCheckState(Qt.Checked)
                layout.addWidget(tmpCheckBox)
            self.scrollArea.setWidget(widget)
            
    def plotData(self):
        x_axis = self.xAxisCombo.currentText()
        y_axis = self.yAxisCombo.currentText()
    
        
        if x_axis == "" or y_axis == "":
            return
            
        self.paket.plotData(x_axis, y_axis, self.filesToPlot, self.tablesToPlot)
    
    def deleteColumns(self):
        self.tableView.setModel(None)
        columnsToDelete = []

        for checkBox in self.scrollArea.findChildren(QCheckBox):
            if checkBox.checkState() == Qt.Unchecked:
                if checkBox.isEnabled():
                    columnName = checkBox.text()
                    columnsToDelete.append(columnName)

                    index = self.xAxisCombo.findText(columnName)
                    self.xAxisCombo.removeItem(index)
                    
                    index = self.yAxisCombo.findText(columnName)
                    self.yAxisCombo.removeItem(index)

                    checkBox.setEnabled(False)
        
        for file in self.paket.tellMeFiles():
            for table in self.paket.tellMeTablesInFile(file):

                for columnToDel in columnsToDelete:
                    del self.paket.data[file][table][columnToDel]

        msg = QMessageBox()

        msg.setWindowTitle("Notification")
        msg.setText("You have just deleted the columns that were unselected. To get them back, reload the files.")
        x = msg.exec_()  

app = QtWidgets.QApplication(sys.argv)
window = MyApplicationMainWindow()
window.show()
app.exec()

