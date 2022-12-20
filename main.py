import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem

from PandasModelClass import PandasModel

class MyApplicationMainWindow(QMainWindow):
    def setupUI(self):
        # Load UI from .ui file
        uic.loadUi("mainwindow.ui", self)

        # Slot-signal connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotData)  

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

    def browseFiles(self):
        self.plotButton.enabled = False
        self.fileListWidget.clear()
        fileNames = QFileDialog.getOpenFileNames(self, "Open file", r"C:\Users\Uporabnik\Documents\Git projekti\ajzakt\data")[0]
        for file in fileNames:
            self.fileListWidget.addItem(QListWidgetItem(file))
        self.fileListWidget.currentItemChanged.connect(self.showTables)

        self.paket.tellFiles(list(fileNames))
        self.paket.loadFiles()
    

    def showTables(self):
        self.tableListWidget.clear()

        currentItem = self.fileListWidget.currentItem()
        if currentItem == None: return

        fileName = currentItem.text()
        for table in self.paket.tellMeTablesInFile(fileName):
            self.tableListWidget.addItem(QListWidgetItem(table))
        self.tableListWidget.currentItemChanged.connect(self.showData)
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
        
        
        print("\n\n====\n",type(self.tableView))

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
            
        self.paket.plotData(x_axis, y_axis)
        



app = QtWidgets.QApplication(sys.argv)
window = MyApplicationMainWindow()
window.show()
app.exec()

