#!/usr/bin/env python3

from sys import exit
from qasync import QEventLoop
from PySide6 import QtWidgets, QtCore
from Widgets.ConfigLoader import ConfigLoader
from Widgets.OBSConnect import OBSConnect
import asyncio


class PierreDeckWindow(QtWidgets.QMainWindow):
    def __init__(self, loop=None):
        super().__init__()

        self.menuBar().addMenu("File")

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.configLoader = ConfigLoader(self.centralWidget)
        self.obsConnect = OBSConnect(self.centralWidget)

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
            QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignLeft,
        )

        self.resize(600, 400)

        self.loop = loop or asyncio.get_event_loop()


def main():
    app = QtWidgets.QApplication(["PierreDeck"])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    pierreDeck = PierreDeckWindow()
    pierreDeck.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
