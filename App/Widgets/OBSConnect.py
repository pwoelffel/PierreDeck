from PySide6 import QtWidgets, QtCore, QtGui
from simpleobsws import WebSocketClient, Request
from qasync import asyncSlot


class OBSConnect(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent.centralWidget)
        self.parent = parent

        self.layout = QtWidgets.QStackedLayout(self)

        self.icon = QtGui.QIcon("App/assets/icons/obs_logo_loading.png")
        self.button = QtWidgets.QPushButton(icon=self.icon, parent=self)
        self.button.clicked.connect(self.connect)
        self.button.setIconSize(QtCore.QSize(50, 50))

        self.layout.addWidget(self.button)

        self.connected = False
        self.obsWebSocket = WebSocketClient(password="")

        self.button.setMinimumSize(55, 55)

        self.connect()

    @asyncSlot()
    async def connect(self):
        self.button.setIcon(QtGui.QIcon("App/assets/icons/obs_logo_loading.png"))
        try:
            await self.obsWebSocket.connect()
        except OSError:
            self.connected = False
            self.button.setIcon(
                QtGui.QIcon("App/assets/icons/obs_logo_not_connected.png")
            )
            return
        await self.obsWebSocket.wait_until_identified()
        if self.obsWebSocket.identified:
            self.connected = True
            self.button.setIcon(QtGui.QIcon("App/assets/icons/obs_logo_connected.png"))
        else:
            self.connected = False
            self.button.setIcon(
                QtGui.QIcon("App/assets/icons/obs_logo_not_connected.png")
            )

    async def callObs(self, route, args):
        if not self.connected:
            return

        await self.obsWebSocket.call(Request(route, args))
