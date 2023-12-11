from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot, isValidNumber
from typing import TYPE_CHECKING
from math import pow

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main import Calculadora


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', window: 'Calculadora', info: 'Info', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '='],
        ]
        self.display = display
        self.window = window
        self._equation = ''
        self.info = info
        self._left = None
        self._right = None
        self._op = None
        self._makeGrid()

    @property
    def grid_mask(self) -> list[list[str]]:
        return self._grid_mask

    @grid_mask.setter
    def grid_mask(self, lista: list) -> None:
        self._grid_mask = lista

    @property
    def equation(self) -> str:
        return self._equation

    @equation.setter
    def equation(self, equation) -> None:
        self._equation = equation
        self.info.setText(self.equation)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self.insertToDisplay)
        self.display.OperatorPressed.connect(self._configLeftOp)
        
        for index, grid in enumerate(self.grid_mask, start=0):
            for row, mask in enumerate(grid, start=0):
                button = Button(mask)

                if mask not in '0123456789.':
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                if mask == '0':
                    self.addWidget(button, index, row, 1, 2)
                elif mask in ".=":
                    self.addWidget(button, index, row + 1)
                else:
                    self.addWidget(button, index, row)
                buttonSlot = self._makeSlot(self.insertToDisplay, mask)
                self._connectButtonClicked(button, buttonSlot)

    @staticmethod
    def _connectButtonClicked(button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)
        if text in '+-*/^':
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, text))
        if text == '=':
            self._connectButtonClicked(button, self._eq)
        if text == '◀':
            self._connectButtonClicked(button, self.display.backspace)

    @Slot()
    def _clear(self):
        self._left = None
        self._left = None
        self._right = None
        self._op = None
        self.equation = ''
        self.display.clear()

    @staticmethod
    def _makeSlot(func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    @Slot()
    def insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'

        if self._op == '^':
            try:
                result = pow(self._left, self._right)
            except OverflowError:
                self._showError("The program doesn't support too big numbers")
            except ValueError:
                self._showError('Imaginary Number')
        else:
            try:
                result = eval(self.equation)
            except ZeroDivisionError:
                self._showError("You can't divide by zero")

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setWindowTitle('ERROR!!!')
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.setStandardButtons(
            msgBox.StandardButton.Close
        )
        msgBox.exec()
