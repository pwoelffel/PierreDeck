from os import getcwd
from PySide6 import QtWidgets, QtCore
import json


class ConfigLoader(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent.centralWidget)
        self.parent = parent

        self.button = QtWidgets.QPushButton("Load config")
        self.button.clicked.connect(self.loadFile)

        self.fileName = QtWidgets.QLabel(
            "No file loaded", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.fileName, 0, 0)
        self.layout.addWidget(self.button, 0, 1)

    @QtCore.Slot()
    def loadFile(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", getcwd(), "Config Files (*.json)"
        )
        self.fileName.setText("File Name : " + self.file[0].split("/")[-1])

        with open(self.file[0], "r") as file:
            fileContent = file.read()
            jsonContent = json.loads(fileContent)
            self.parent.setButtons(jsonContent)

    def getFile(self):
        return self.file
