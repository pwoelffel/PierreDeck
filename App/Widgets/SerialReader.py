from PySide6 import QtWidgets
from serial import Serial
from serial.tools import list_ports, list_ports_linux


class SerialReader(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent.centralWidget)
        self.parent = parent

        portList = list_ports.comports()
        self.serial = Serial()

        self.combo = QtWidgets.QComboBox()

        self.combo.currentIndexChanged.connect(self.changePort)

        if len(portList) == 0:
            self.combo.insertItem(0, "Aucun appareil série détecté")

        for i in range(len(portList)):
            self.combo.insertItem(i + 1, portList[i].name, portList[i].device)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.combo, 0, 0)

    def changePort(self):
        self.serial.port = self.combo.currentData()
