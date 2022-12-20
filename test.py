from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow
app = QApplication([])
# Create the main window
window = QMainWindow()

# Create a QTreeWidget and set it as the central widget of the main window
treeWidget = QTreeWidget()
window.setCentralWidget(treeWidget)

# Set the tree widget's header labels
treeWidget.setHeaderLabels(["Name", "Type", "Size"])

# Add items to the tree widget
root = QTreeWidgetItem(treeWidget, ["Root"])

child1 = QTreeWidgetItem(root, ["Child 1"])
child2 = QTreeWidgetItem(root, ["Child 2"])

grandchild1 = QTreeWidgetItem(child1, ["Grandchild 1"])
grandchild2 = QTreeWidgetItem(child1, ["Grandchild 2"])

# Show the main window
window.show()

# Run the Qt application

app.exec_()
