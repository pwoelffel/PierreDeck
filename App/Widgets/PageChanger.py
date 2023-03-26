from PySide6 import QtWidgets, QtCore


class PageChanger(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent.centralWidget)
        self.parent = parent

        self.page = 1
        self.layout = QtWidgets.QHBoxLayout(self)

        self.left = QtWidgets.QPushButton("<")
        self.left.clicked.connect(self.decreasePage)
        self.left.setMinimumSize(50, 50)
        self.left.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.number = QtWidgets.QLabel(str(self.page))
        self.number.setAlignment(QtCore.Qt.AlignCenter)

        self.right = QtWidgets.QPushButton(">")
        self.right.clicked.connect(self.increasePage)
        self.right.setMinimumSize(50, 50)
        self.right.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.layout.addWidget(self.left)
        self.layout.addWidget(self.number)
        self.layout.addWidget(self.right)

    @QtCore.Slot()
    def decreasePage(self):
        self.page -= 1
        if self.page < 1:
            self.page = 3
        self.number.setText(str(self.page))

    @QtCore.Slot()
    def increasePage(self):
        self.page = (self.page) % 3 + 1
        self.number.setText(str(self.page))
        print(self.page)

    def getPage(self):
        return self.page
