#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main interface
"""

import sys
import GlobalValue
import DeviceSelectorDialog
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('trophy.png'), 'Play', self)
        exitAction.setShortcut('Ctrl+P')
        exitAction.setStatusTip('Play')
        exitAction.triggered.connect(self.startProxy)

        self.statusBar()

        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def closeEvent(self, QCloseEvent):
        print("closed")

    def showEvent(self, QShowEvent):
        if (not GlobalValue.connectedDevice):
            dialog = DeviceSelectorDialog.deviceSelectorDialog()
            print("no device selected")


    def startProxy(self):
        print("start Proxy")
        """start catch the pc event and send to phone"""
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())