#!/usr/bin/env python3

from sys import exit
from qasync import QEventLoop
from PySide6 import QtWidgets, QtCore
from Widgets.ConfigLoader import ConfigLoader
from Widgets.OBSConnect import OBSConnect
from Widgets.ButtonMatrix import ButtonMatrix
from Widgets.PageChanger import PageChanger
from Widgets.SerialReader import SerialReader
import asyncio


class PierreDeckWindow(QtWidgets.QMainWindow):
    def __init__(self, loop=None):
        super().__init__()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.obsConnect = OBSConnect(self)
        self.configLoader = ConfigLoader(self)
        self.serialReader = SerialReader(self)
        self.buttonMatrix = ButtonMatrix(self)
        self.pageChanger = PageChanger(self)

        self.centralWidget.layout = QtWidgets.QGridLayout(self.centralWidget)
        self.centralWidget.layout.addWidget(
            self.obsConnect,
            0,
            0,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.centralWidget.layout.addWidget(
            self.configLoader,
            0,
            1,
            QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft,
        )

        self.centralWidget.layout.addWidget(
            self.serialReader,
            0,
            2,
            1,
            2,
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        self.centralWidget.layout.addWidget(self.pageChanger, 1, 0, 1, 4)
        self.centralWidget.layout.addWidget(self.buttonMatrix, 2, 0, 4, 4)

        self.resize(500, 400)

        self.loop = loop or asyncio.get_event_loop()

    def getPage(self):
        return self.pageChanger.getPage()

    def setButtons(self, config):
        self.buttonMatrix.setButtons(config)

    """def execFunction(self, function):
        exec(function)"""

    def execObs(self, route, args):
        self.loop.create_task(self.obsConnect.callObs(route, args))


def main():
    app = QtWidgets.QApplication(["App"])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    pierreDeck = PierreDeckWindow()
    pierreDeck.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
