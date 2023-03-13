from PySide6 import QtWidgets, QtCore


class Button:
    def __init__(self, text):
        self.text = text
        self.button = QtWidgets.QPushButton(text)
        self.button.clicked.connect(self.log)
        self.button.setMinimumSize(50, 50)

    @QtCore.Slot()
    def log(self):
        print(f"button n°{self.text}")


class ButtonMatrix(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QtWidgets.QGridLayout(self)

        self.buttons = [Button(str(i)) for i in range(16)]

        for i in range(4):
            for j in range(4):
                self.layout.addWidget(
                    self.buttons[i * 4 + j].button, i, j, QtCore.Qt.AlignCenter
                )
