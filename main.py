import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt

from PandasModelClass import PandasModel

class MyApplicationMainWindow(QMainWindow):
    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow.ui", self)

        # Slot-signal connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotData)  

    def updateFilesToPlot(self):
        print("UPDATE FILES TO PLOT TRIGGERED")
        currentFile = self.fileListWidget.currentItem()
        if currentFile == None: print("NONE ERROR"); return
        else: print("\n=====", currentFile)

        if currentFile.checkState() == Qt.Checked:
            if currentFile.text() not in self.filesToPlot:
                self.filesToPlot.add(currentFile.text())
                print("NOW ADDED HIM TO LIST")
        
        elif currentFile.checkState() == Qt.Unchecked:
            if currentFile.text() in self.filesToPlot:
                self.filesToPlot.remove(currentFile.text())
                print("NOW REMOVED HIM FROM LIST")
    
    def updateTablesToPlot(self):
        currentFile = self.fileListWidget.currentItem()
        if currentFile == None: return
        currentTable = self.tableListWidget.currentItem()
        if currentTable == None: return

        if currentTable.checkState() == Qt.Checked:
            if currentTable.text() not in self.tablesToPlot[currentFile.text()]:
                self.tablesToPlot[currentFile.text()].add(currentTable.text())
                print("NOW ADDED HIM TO LIST")

        elif currentTable.checkState() == Qt.Unchecked:
            if currentTable.text() in self.tablesToPlot[currentFile.text()]:
                self.tablesToPlot[currentFile.text()].remove(currentTable.text())
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
        
        self.filesToPlot = set()
        self.tablesToPlot = {}

    def browseFiles(self):
        self.plotButton.enabled = False
        self.fileListWidget.clear()
        fileNames = QFileDialog.getOpenFileNames(self, "Open file", "data")[0]
        for i, file in enumerate(fileNames):
            #fileNames[i] = fileNames[i].split("/")[-1]
            #file = fileNames[i]
            tmp = QListWidgetItem(file)
            tmp.setCheckState(Qt.Checked)
            self.fileListWidget.addItem(tmp)

        self.fileListWidget.itemClicked.connect(self.showTables)
        self.fileListWidget.itemChanged.connect(self.updateFilesToPlot)
        

        self.paket.tellFiles(list(fileNames))
        self.paket.loadFiles()

        # Put all to be plotted
        for file in self.paket.tellMeFiles():
            self.filesToPlot.add(file)
            self.tablesToPlot[file] = set()
            for table in self.paket.tellMeTablesInFile(file):
                self.tablesToPlot[file].add(table)
    

    def showTables(self):
        self.tableListWidget.clear()

        currentItem = self.fileListWidget.currentItem()
        if currentItem == None: return

        fileName = currentItem.text()
        for table in self.paket.tellMeTablesInFile(fileName):
            tmp = QListWidgetItem(table)
            if table in self.tablesToPlot[fileName]:
                tmp.setCheckState(Qt.Checked)
            else:
                tmp.setCheckState(Qt.Unchecked)
            self.tableListWidget.addItem(tmp)

        self.tableListWidget.itemClicked.connect(self.showData)
        self.tableListWidget.itemChanged.connect(self.updateTablesToPlot)
        self.plotButton.enabled = True
    
    def showData(self):
        # TODO clear prevous??
        currentItem = self.fileListWidget.currentItem()
        if currentItem == None: return
        fileName = currentItem.text()

        currentItem = self.tableListWidget.currentItem()
        if currentItem == None: return
        tableName = currentItem.text()
        
        dataFrame = self.paket.data[fileName][tableName]
        
        
        #print("\n\n====\n",type(self.tableView))

        self.tableView
        self.model = PandasModel(dataFrame)
        self.tableView.setModel(self.model)

        for val in self.model._dataframe.columns.values:
            self.xAxisCombo.addItem(val)
            self.yAxisCombo.addItem(val)
            
    
    def plotData(self):
        x_axis = self.xAxisCombo.currentText()
        y_axis = self.yAxisCombo.currentText()
    
        
        if x_axis == "" or y_axis == "":
            return
            
        self.paket.plotData(x_axis, y_axis, self.filesToPlot, self.tablesToPlot)
        



app = QtWidgets.QApplication(sys.argv)
window = MyApplicationMainWindow()
window.show()
app.exec()

