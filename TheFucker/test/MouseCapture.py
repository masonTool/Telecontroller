#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mason created

used to test the mouse and key capture.
"""

import sys
import subprocess
from PyQt5 import QtWidgets, QtCore
from pymouse import PyMouseEvent
from pykeyboard import PyKeyboardEvent

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel("ddddddd", self)

        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        # hbox = QtWidgets.QHBo、xLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(self.label)
        # # self.setCentralWidget(self.label)
        #
        # vbox = QtWidgets.QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        #
        # self.setLayout(vbox)

        self.resize(500, 500)
        self.center()
        self.setWindowTitle('Mouse & Key')

    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    # def keyPressEvent(self, e):
    #     print('pressed: %s  %s  %s  ' %(e.text(), e.count(), e.key()))
    #     self.label.setText(e.text())
    #     self.statusBar().showMessage(e.text())
    #
    # def keyReleaseEvent(self, e):
    #     print('released: %s  %s  %s  ' % (e.text(), e.count(), e.key()))

    # def mouseMoveEvent(self, e):
    #     self.label.setText("("+str(e.x())+","+str(e.y())+")")
    #     self.statusBar().showMessage("("+str(e.x())+","+str(e.y())+")")
    #
    # def mousePressEvent(self, e):
    #     if e.button() == QtCore.Qt.LeftButton:
    #         self.label.setText(self.tr("Mouse Left Button Pressed:"))
    #         self.statusBar().showMessage(self.tr("Mouse Left Button Pressed:"))
    #     elif e.button() == QtCore.Qt.RightButton:
    #         self.label.setText(self.tr("Mouse Right Button Pressed:"))
    #         self.statusBar().showMessage(self.tr("Mouse Right Button Pressed:"))


class MyMouseEvent(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        print('clicked: %s  %s  %s  %s' %(x, y, button, press))

    def scroll(self, x, y, vertical, horizontal):
        print('scrolled: %s  %s  %s  %s' % (x, y, vertical, horizontal))
        pass

    # def move(self, x, y):
    #     print(str(x) + "--" + str(y))


class MyKeyboardEvent(PyKeyboardEvent):
    def tap(self, keycode, character, press):
        print('tabed: %s  %s  %s' % (keycode, character, press))
        pass

    # def escape(self, event):
    #     """
    #     A function that defines when to stop listening; subclass this with your
    #     escape behavior. If the program is meant to stop, this method should
    #     return True. Every key event will go through this method before going to
    #     tap(), allowing this method to check for exit conditions.
    #
    #     The default behavior is to stop when the 'Esc' key is pressed.
    #
    #     If one wishes to use key combinations, or key series, one might be
    #     interested in reading about Finite State Machines.
    #     http://en.wikipedia.org/wiki/Deterministic_finite_automaton
    #     """
    #     condition = None
    #     return event == condition


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    a = MyMouseEvent()
    k = MyKeyboardEvent()
    window = Window()
    window.show()
    a.start()
    k.start()

    print("sssss")
    sys.exit(app.exec_())
