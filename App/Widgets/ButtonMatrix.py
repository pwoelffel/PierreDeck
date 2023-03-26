from PySide6 import QtWidgets, QtCore


class Button:
    def __init__(self, text, parent):
        self.parent = parent

        self.text = text
        self.button = QtWidgets.QPushButton(text)
        self.button.clicked.connect(self.trigger)
        self.button.setMinimumSize(50, 50)
        self.commands = []

    @QtCore.Slot()
    def trigger(self):
        page = self.parent.getPage() - 1

        if page >= len(self.commands):
            return

        for command in self.commands[page]:
            print(command)

            if command["action"] == "none":
                continue

            if command["action"] == "function":
                self.parent.execFunction(command["function"])

            if command["action"] == "obs":
                self.parent.execObs(command["call"], command["args"])

    def setCommands(self, commands):
        self.commands = commands


class ButtonMatrix(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent.centralWidget)
        self.parent = parent

        self.layout = QtWidgets.QGridLayout(self)

        self.buttons = [Button(str(i), self.parent) for i in range(16)]

        for i in range(4):
            for j in range(4):
                self.layout.addWidget(
                    self.buttons[i * 4 + j].button,
                    i,
                    j,
                    QtCore.Qt.AlignmentFlag.AlignCenter,
                )

    def getButtons(self):
        return self.buttons

    def setButtons(self, config):
        for i in range(16):
            self.buttons[i].setCommands(
                [config[page][i] for page in range(len(config))]
            )
