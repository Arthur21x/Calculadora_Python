from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
                            QLabel, QLineEdit, QTextEdit, QGridLayout, QMessageBox
from display import Display
from info import Info
from styles import setupTheme
from buttons import Button, ButtonsGrid
from PySide6.QtGui import QIcon
from variables import *
import sys


class Calculadora(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)

        self.setCentralWidget(self.cw)
        self.setWindowTitle('Calculadora')

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, display):
        self.vLayout.addWidget(display)

    def makeMsgBox(self):
        return QMessageBox(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme()
    Window = Calculadora()
    icon = QIcon(str(WINDOW_ICON_PATH))
    Window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info('')
    Window.addWidgetToVLayout(info)

    display = Display()
    Window.addWidgetToVLayout(display)

    buttonsGrid = ButtonsGrid(display=display, info=info, window=Window)
    Window.vLayout.addLayout(buttonsGrid)


#    Window.adjustFixedSize()
    Window.show()
    app.exec()
