import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt

from PandasModelClass import PandasModel

class MyApplicationMainWindow(QMainWindow):
    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow.ui", self)

        # Slot-signal connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotData)  
        

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
    
        """def showTables(self, item, column):
        #self.tableListWidget.clear()

        currentItem = item
        if currentItem == None: return

        fileName = currentItem.text(column)
        for table in self.paket.tellMeTablesInFile(fileName):
            tmp = QListWidgetItem(table)
            if table in self.tablesToPlot[fileName]:
                tmp.setCheckState(Qt.Checked)
            else:
                tmp.setCheckState(Qt.Unchecked)
            self.tableListWidget.addItem(tmp)

        self.tableListWidget.itemClicked.connect(self.showData)
        self.tableListWidget.itemChanged.connect(self.updateTablesToPlot)"""
        
        self.plotButton.enabled = True

    def showData(self, item, column):
        # TODO clear prevous??
        #currentItem = self.treeWidget.currentItem()
        if item.parent() == None: return

        dataFrame = self.paket.data[item.parent().text(0)][item.text(0)]

        self.model = PandasModel(dataFrame)
        self.tableView.setModel(self.model)

        if self.xAxisCombo.count() == 0:
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

