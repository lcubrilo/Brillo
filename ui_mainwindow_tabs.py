# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Admin\Documents\git clones\Brillo\mainwindow_tabs.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(790, 700)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.fileSelectionGroup = QtWidgets.QGroupBox(self.splitter_2)
        self.fileSelectionGroup.setObjectName("fileSelectionGroup")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.fileSelectionGroup)
        self.horizontalLayout_10.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.progressBar = QtWidgets.QProgressBar(self.fileSelectionGroup)
        self.progressBar.setMaximumSize(QtCore.QSize(8, 16777215))
        self.progressBar.setMaximum(1000)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_10.addWidget(self.progressBar)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.browseButton = QtWidgets.QPushButton(self.fileSelectionGroup)
        self.browseButton.setObjectName("browseButton")
        self.verticalLayout_10.addWidget(self.browseButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_10.addItem(spacerItem)
        self.treeWidget = QtWidgets.QTreeWidget(self.fileSelectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_10.addWidget(self.treeWidget)
        self.reloadButton = QtWidgets.QPushButton(self.fileSelectionGroup)
        self.reloadButton.setEnabled(False)
        self.reloadButton.setObjectName("reloadButton")
        self.verticalLayout_10.addWidget(self.reloadButton)
        self.horizontalLayout_10.addLayout(self.verticalLayout_10)
        self.tabWidget = QtWidgets.QTabWidget(self.splitter_2)
        self.tabWidget.setEnabled(False)
        self.tabWidget.setMinimumSize(QtCore.QSize(550, 0))
        self.tabWidget.setObjectName("tabWidget")
        self.showDataTab = QtWidgets.QWidget()
        self.showDataTab.setObjectName("showDataTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.showDataTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.showDataTab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.constantScrollArea = QtWidgets.QScrollArea(self.showDataTab)
        self.constantScrollArea.setMaximumSize(QtCore.QSize(16777215, 75))
        self.constantScrollArea.setWidgetResizable(True)
        self.constantScrollArea.setObjectName("constantScrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 520, 73))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.addConstantButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.addConstantButton.setMaximumSize(QtCore.QSize(55, 55))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.addConstantButton.setFont(font)
        self.addConstantButton.setObjectName("addConstantButton")
        self.horizontalLayout_6.addWidget(self.addConstantButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.constantScrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.constantScrollArea)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tableView = QtWidgets.QTableView(self.showDataTab)
        self.tableView.setMinimumSize(QtCore.QSize(0, 200))
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.exportButton = QtWidgets.QPushButton(self.showDataTab)
        self.exportButton.setEnabled(False)
        self.exportButton.setObjectName("exportButton")
        self.verticalLayout_2.addWidget(self.exportButton)
        self.tabWidget.addTab(self.showDataTab, "")
        self.editDataTab = QtWidgets.QWidget()
        self.editDataTab.setObjectName("editDataTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.editDataTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.deleteColumnsGroup = QtWidgets.QGroupBox(self.editDataTab)
        self.deleteColumnsGroup.setObjectName("deleteColumnsGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.deleteColumnsGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.columnsScrollArea = QtWidgets.QScrollArea(self.deleteColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.columnsScrollArea.sizePolicy().hasHeightForWidth())
        self.columnsScrollArea.setSizePolicy(sizePolicy)
        self.columnsScrollArea.setMaximumSize(QtCore.QSize(16777215, 65))
        self.columnsScrollArea.setWidgetResizable(True)
        self.columnsScrollArea.setObjectName("columnsScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 439, 63))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.columnsScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.columnsScrollArea)
        self.deleteButton = QtWidgets.QPushButton(self.deleteColumnsGroup)
        self.deleteButton.setMinimumSize(QtCore.QSize(0, 65))
        self.deleteButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.verticalLayout_3.addWidget(self.deleteColumnsGroup)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.editColumnsGroup = QtWidgets.QGroupBox(self.editDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editColumnsGroup.sizePolicy().hasHeightForWidth())
        self.editColumnsGroup.setSizePolicy(sizePolicy)
        self.editColumnsGroup.setObjectName("editColumnsGroup")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.editColumnsGroup)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.inputLabel = QtWidgets.QLabel(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputLabel.sizePolicy().hasHeightForWidth())
        self.inputLabel.setSizePolicy(sizePolicy)
        self.inputLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.inputLabel.setObjectName("inputLabel")
        self.verticalLayout_7.addWidget(self.inputLabel)
        self.constLabel = QtWidgets.QLabel(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.constLabel.sizePolicy().hasHeightForWidth())
        self.constLabel.setSizePolicy(sizePolicy)
        self.constLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.constLabel.setObjectName("constLabel")
        self.verticalLayout_7.addWidget(self.constLabel)
        self.operationLabel = QtWidgets.QLabel(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operationLabel.sizePolicy().hasHeightForWidth())
        self.operationLabel.setSizePolicy(sizePolicy)
        self.operationLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.operationLabel.setObjectName("operationLabel")
        self.verticalLayout_7.addWidget(self.operationLabel)
        self.outputLabel = QtWidgets.QLabel(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputLabel.sizePolicy().hasHeightForWidth())
        self.outputLabel.setSizePolicy(sizePolicy)
        self.outputLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.outputLabel.setObjectName("outputLabel")
        self.verticalLayout_7.addWidget(self.outputLabel)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.inputColCombo = QtWidgets.QComboBox(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputColCombo.sizePolicy().hasHeightForWidth())
        self.inputColCombo.setSizePolicy(sizePolicy)
        self.inputColCombo.setWhatsThis("")
        self.inputColCombo.setCurrentText("")
        self.inputColCombo.setObjectName("inputColCombo")
        self.horizontalLayout_9.addWidget(self.inputColCombo)
        self.inputColCombo2 = QtWidgets.QComboBox(self.editColumnsGroup)
        self.inputColCombo2.setObjectName("inputColCombo2")
        self.horizontalLayout_9.addWidget(self.inputColCombo2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.constCombo = QtWidgets.QComboBox(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.constCombo.sizePolicy().hasHeightForWidth())
        self.constCombo.setSizePolicy(sizePolicy)
        self.constCombo.setObjectName("constCombo")
        self.verticalLayout_5.addWidget(self.constCombo)
        self.operationCombo = QtWidgets.QComboBox(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operationCombo.sizePolicy().hasHeightForWidth())
        self.operationCombo.setSizePolicy(sizePolicy)
        self.operationCombo.setObjectName("operationCombo")
        self.verticalLayout_5.addWidget(self.operationCombo)
        self.outputColLineEdit = QtWidgets.QLineEdit(self.editColumnsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputColLineEdit.sizePolicy().hasHeightForWidth())
        self.outputColLineEdit.setSizePolicy(sizePolicy)
        self.outputColLineEdit.setText("")
        self.outputColLineEdit.setObjectName("outputColLineEdit")
        self.verticalLayout_5.addWidget(self.outputColLineEdit)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.editButton = QtWidgets.QPushButton(self.editColumnsGroup)
        self.editButton.setObjectName("editButton")
        self.verticalLayout_8.addWidget(self.editButton)
        self.verticalLayout_3.addWidget(self.editColumnsGroup)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem5)
        self.splittingGroupbox = QtWidgets.QGroupBox(self.editDataTab)
        self.splittingGroupbox.setObjectName("splittingGroupbox")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.splittingGroupbox)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.splittingColumnCombo = QtWidgets.QComboBox(self.splittingGroupbox)
        self.splittingColumnCombo.setObjectName("splittingColumnCombo")
        self.horizontalLayout_11.addWidget(self.splittingColumnCombo)
        self.splitDataButton = QtWidgets.QPushButton(self.splittingGroupbox)
        self.splitDataButton.setObjectName("splitDataButton")
        self.horizontalLayout_11.addWidget(self.splitDataButton)
        self.verticalLayout_3.addWidget(self.splittingGroupbox)
        self.tabWidget.addTab(self.editDataTab, "")
        self.plotDataTab = QtWidgets.QWidget()
        self.plotDataTab.setObjectName("plotDataTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.plotDataTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.plotTypeLabel = QtWidgets.QLabel(self.plotDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotTypeLabel.sizePolicy().hasHeightForWidth())
        self.plotTypeLabel.setSizePolicy(sizePolicy)
        self.plotTypeLabel.setObjectName("plotTypeLabel")
        self.horizontalLayout_7.addWidget(self.plotTypeLabel)
        self.plotTypeCombo = QtWidgets.QComboBox(self.plotDataTab)
        self.plotTypeCombo.setObjectName("plotTypeCombo")
        self.plotTypeCombo.addItem("")
        self.plotTypeCombo.addItem("")
        self.plotTypeCombo.addItem("")
        self.horizontalLayout_7.addWidget(self.plotTypeCombo)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.plotDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.xAxisCombo = QtWidgets.QComboBox(self.plotDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xAxisCombo.sizePolicy().hasHeightForWidth())
        self.xAxisCombo.setSizePolicy(sizePolicy)
        self.xAxisCombo.setObjectName("xAxisCombo")
        self.horizontalLayout_4.addWidget(self.xAxisCombo)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.yAxesLabel = QtWidgets.QLabel(self.plotDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yAxesLabel.sizePolicy().hasHeightForWidth())
        self.yAxesLabel.setSizePolicy(sizePolicy)
        self.yAxesLabel.setObjectName("yAxesLabel")
        self.verticalLayout_4.addWidget(self.yAxesLabel)
        self.yColumnsScrollArea = QtWidgets.QScrollArea(self.plotDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yColumnsScrollArea.sizePolicy().hasHeightForWidth())
        self.yColumnsScrollArea.setSizePolicy(sizePolicy)
        self.yColumnsScrollArea.setWidgetResizable(True)
        self.yColumnsScrollArea.setObjectName("yColumnsScrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 520, 322))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.yColumnsScrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_4.addWidget(self.yColumnsScrollArea)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.legendCheckBox = QtWidgets.QCheckBox(self.plotDataTab)
        self.legendCheckBox.setCheckable(True)
        self.legendCheckBox.setChecked(True)
        self.legendCheckBox.setObjectName("legendCheckBox")
        self.horizontalLayout_8.addWidget(self.legendCheckBox)
        self.gridCheckBox = QtWidgets.QCheckBox(self.plotDataTab)
        self.gridCheckBox.setObjectName("gridCheckBox")
        self.horizontalLayout_8.addWidget(self.gridCheckBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.plotButton = QtWidgets.QPushButton(self.plotDataTab)
        self.plotButton.setEnabled(False)
        self.plotButton.setObjectName("plotButton")
        self.verticalLayout_4.addWidget(self.plotButton)
        self.plotExportButton = QtWidgets.QPushButton(self.plotDataTab)
        self.plotExportButton.setObjectName("plotExportButton")
        self.verticalLayout_4.addWidget(self.plotExportButton)
        self.tabWidget.addTab(self.plotDataTab, "")
        self.codeTab = QtWidgets.QWidget()
        self.codeTab.setObjectName("codeTab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.codeTab)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.loadCodeButton = QtWidgets.QPushButton(self.codeTab)
        self.loadCodeButton.setObjectName("loadCodeButton")
        self.horizontalLayout_5.addWidget(self.loadCodeButton)
        self.saveCodeButton = QtWidgets.QPushButton(self.codeTab)
        self.saveCodeButton.setObjectName("saveCodeButton")
        self.horizontalLayout_5.addWidget(self.saveCodeButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.filenameLineEdit = QtWidgets.QLineEdit(self.codeTab)
        self.filenameLineEdit.setObjectName("filenameLineEdit")
        self.verticalLayout_9.addWidget(self.filenameLineEdit)
        self.codePlainEdit = QtWidgets.QPlainTextEdit(self.codeTab)
        self.codePlainEdit.setPlainText("")
        self.codePlainEdit.setObjectName("codePlainEdit")
        self.verticalLayout_9.addWidget(self.codePlainEdit)
        self.runCodeButton = QtWidgets.QPushButton(self.codeTab)
        self.runCodeButton.setObjectName("runCodeButton")
        self.verticalLayout_9.addWidget(self.runCodeButton)
        self.tabWidget.addTab(self.codeTab, "")
        self.verticalLayout_6.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fileSelectionGroup.setTitle(_translate("MainWindow", "File selection"))
        self.browseButton.setText(_translate("MainWindow", "Browse directories"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "File-table tree"))
        self.reloadButton.setText(_translate("MainWindow", "Reload files"))
        self.label_3.setText(_translate("MainWindow", "Pre-table constants"))
        self.addConstantButton.setText(_translate("MainWindow", "+"))
        self.exportButton.setText(_translate("MainWindow", "Export all to Excel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.showDataTab), _translate("MainWindow", "Show table data"))
        self.deleteColumnsGroup.setTitle(_translate("MainWindow", "Delete columns"))
        self.deleteButton.setText(_translate("MainWindow", "🗑"))
        self.editColumnsGroup.setTitle(_translate("MainWindow", "Create new columns"))
        self.inputLabel.setText(_translate("MainWindow", "Input column"))
        self.constLabel.setText(_translate("MainWindow", "Constant"))
        self.operationLabel.setText(_translate("MainWindow", "Operation"))
        self.outputLabel.setText(_translate("MainWindow", "Output name"))
        self.outputColLineEdit.setPlaceholderText(_translate("MainWindow", "Write desired name here [unit]"))
        self.editButton.setText(_translate("MainWindow", "Execute edit"))
        self.splittingGroupbox.setTitle(_translate("MainWindow", "Split data into rising, flat, dropping"))
        self.splittingColumnCombo.setProperty("placeholderText", _translate("MainWindow", "Reference column"))
        self.splitDataButton.setText(_translate("MainWindow", "Split data according to it"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editDataTab), _translate("MainWindow", "Edit table data"))
        self.plotTypeLabel.setText(_translate("MainWindow", "Plot type"))
        self.plotTypeCombo.setItemText(0, _translate("MainWindow", "Line"))
        self.plotTypeCombo.setItemText(1, _translate("MainWindow", "Dotted"))
        self.plotTypeCombo.setItemText(2, _translate("MainWindow", "Both"))
        self.label.setText(_translate("MainWindow", "X axis"))
        self.yAxesLabel.setText(_translate("MainWindow", "Y axes"))
        self.legendCheckBox.setText(_translate("MainWindow", "Show the legend on the plot"))
        self.gridCheckBox.setText(_translate("MainWindow", "Show gridlines on the plot"))
        self.plotButton.setText(_translate("MainWindow", "Show plot"))
        self.plotExportButton.setText(_translate("MainWindow", "Export from plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotDataTab), _translate("MainWindow", "Plotting data"))
        self.loadCodeButton.setText(_translate("MainWindow", "Load from file"))
        self.saveCodeButton.setText(_translate("MainWindow", "Save to file"))
        self.filenameLineEdit.setPlaceholderText(_translate("MainWindow", "File name"))
        self.runCodeButton.setText(_translate("MainWindow", "Run macros"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.codeTab), _translate("MainWindow", "Macros"))