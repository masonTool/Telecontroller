#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main interface
"""

import GlobalValue
import Utils
import AdbOperator
from SocketClient import SocketClient
from DeviceDialog import DeviceDialog
from PyQt5.QtWidgets import QMainWindow, QAction, QDesktopWidget, QLabel, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.client = SocketClient('127.0.0.1', GlobalValue.pc_port)
        self.client.message[str].connect(self.showReceived)

        self.initUI()
        pass

    def initUI(self):
        """
        显示UI
        """
        phoneImg = QLabel()
        # phoneImg.setPixmap(QPixmap("img/phone.png"))
        self.setCentralWidget(phoneImg)

        self.playAction = QAction(QIcon('img/play.png'), 'Play', self)
        self.playAction.setShortcut('Ctrl+P')
        self.playAction.setStatusTip('Play')
        self.playAction.triggered.connect(self.startProxy)

        deviceAction = QAction(QIcon('img/device.png'), 'Device', self)
        deviceAction.setShortcut('Ctrl+D')
        deviceAction.setStatusTip('Device')
        deviceAction.triggered.connect(self.showDevice)

        configAction = QAction(QIcon('img/config.png'), 'Config', self)
        configAction.setShortcut('Ctrl+C')
        configAction.setStatusTip('Config')
        configAction.triggered.connect(self.startProxy)

        infoAction = QAction(QIcon('img/info.png'), 'Info', self)
        infoAction.setShortcut('Ctrl+I')
        infoAction.setStatusTip('Info')
        infoAction.triggered.connect(self.startProxy)

        toolbar = self.addToolBar('')
        toolbar.addAction(self.playAction)
        toolbar.addAction(deviceAction)
        toolbar.addAction(configAction)
        toolbar.addAction(infoAction)

        self.statusBar()
        self.resize(500, 500)
        self.setWindowTitle('Telecontroller')
        Utils.center(self)
        pass

    def center(self):
        """
        居中显示
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        pass

    def showDevice(self):
        """
        显示设备选择界面
        """
        deviceDialog = DeviceDialog(self)
        deviceDialog.exec()
        pass

    def showEvent(self, QShowEvent):
        """
        界面的显示事件
        """
        print('show')
        if not GlobalValue.connectedDevice:
            self.statusBar().showMessage('选择连接设备');
            self.timer = QTimer();
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.showDevice)
            self.timer.start(200)
        pass

    def startProxy(self):
        """
        开始用电脑代理鼠标和键盘
        """
        AdbOperator.buildBridge(GlobalValue.pc_port, GlobalValue.phone_port)

        text, ok = QInputDialog.getText(self, "QInputDialog.getText()",
                "User name:", QLineEdit.Normal, '')
        if ok and text != '':
            self.client.send(text)
        pass

    def showReceived(self, message):
        self.statusBar().showMessage(message)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())