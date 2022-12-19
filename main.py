import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem

from PandasModelClass import TableViewWindow

class MyApplicationMainWindow(QMainWindow):
    def __init__(self):
        super(MyApplicationMainWindow,self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.browseButton.clicked.connect(self.browseFiles)
        self.tvw = TableViewWindow()

        try:
            from brlopack import brlopack
            print("Successfully loaded `brlopack` from `brlopack`")
        except:
            print("!!!!!!!!!!!!!")
            print("ERROR: Importing the package was NOT successful.")
        
        self.paket = brlopack()

    def browseFiles(self):
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

        self.tvw.changeModel(dataFrame)
        
        



app = QtWidgets.QApplication(sys.argv)
window = MyApplicationMainWindow()
window.show()
app.exec()

