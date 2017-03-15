#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main interface
"""

from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QInputDialog, QLineEdit
from pymouse import PyMouseEvent

import AdbOperator
import EventUtils
import GlobalValue
import Utils
from DeviceDialog import DeviceDialog
from SocketClient import SocketClient


class EventBound(QObject):
    event = pyqtSignal([str])


def debug(str):
    # print(str)
    pass

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.proxyMode = False
        self.eventBound = EventBound()
        self.client = SocketClient('127.0.0.1', GlobalValue.pc_port)
        self.client.message[str].connect(self.showReceived)
        self.eventBound.event[str].connect(self.eventReceiver)

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
        self.playAction.triggered.connect(self.toggleProxy)

        deviceAction = QAction(QIcon('img/device.png'), 'Device', self)
        deviceAction.setShortcut('Ctrl+D')
        deviceAction.setStatusTip('Device')
        deviceAction.triggered.connect(self.showDeviceDialog)

        configAction = QAction(QIcon('img/config.png'), 'Config', self)
        configAction.setShortcut('Ctrl+C')
        configAction.setStatusTip('Config')
        configAction.triggered.connect(self.startSend)

        infoAction = QAction(QIcon('img/info.png'), 'Info', self)
        infoAction.setShortcut('Ctrl+I')
        infoAction.setStatusTip('Info')
        # infoAction.triggered.connect(self.startProxy)

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

    def showDeviceDialog(self):
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
        debug('show')
        if not GlobalValue.connectedDevice:
            self.statusBar().showMessage('选择连接设备');
            self.timer = QTimer();
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.showDeviceDialog)
            self.timer.start(200)
        pass

    def toggleProxy(self):
        if self.proxyMode:
            self.proxyMode = False
            self.playAction.setIcon(QIcon('img/play.png'))
            self.mouseEvent.stop()
        else:
            self.proxyMode = True
            self.playAction.setIcon(QIcon('img/pause.png'))
            self.mouseEvent = MyMouseEvent(self.eventBound)
            self.mouseEvent.start()
        pass

    def startSend(self):
        """
        测试通信
        """
        text, ok = QInputDialog.getText(self, "QInputDialog.getText()",
                "User name:", QLineEdit.Normal, '')
        if ok and text != '':
            self.client.send(text)
        pass

    def showReceived(self, message):
        """
        槽函数显示手机端返回数据
        """
        debug('received: ' + message)
        pass

    def keyPressEvent(self, e):
        """
        接收键盘按下事件
        """
        if not self.proxyMode:
            return

        debug('keyboard pressed: %s %s' %(e.key(), e.text()))

        if len(e.text()) == 0:
            ascii = 0
        else:
            ascii = ord(e.text())

        data = '%s,%s,%s,%s' %(EventUtils.KEYBOARD_TYPE, EventUtils.KEYBOARD_ACTION_DOWN, e.key(), ascii)
        self.eventBound.event.emit(data)
        pass

    def keyReleaseEvent(self, e):
        """
        接收键盘释放事件
        """
        if not self.proxyMode:
            return

        debug('keyboard released: %s %s' % (e.key(), e.text()))

        if len(e.text()) == 0:
            ascii = 0
        else:
            ascii = ord(e.text())

        data = '%s,%s,%s,%s' %(EventUtils.KEYBOARD_TYPE, EventUtils.KEYBOARD_ACTION_UP, e.key(), ascii)
        self.eventBound.event.emit(data)
        pass

    def eventReceiver(self, message):
        result = list(map(lambda it:int(it), message.split(',')))
        if result[0] == EventUtils.MOUSE_TYPE:
            pass

        print('size :%s' %(self.geometry()))
        self.client.send(message)
        pass



class MyMouseEvent(PyMouseEvent):

    def __init__(self, eventBound):
        super().__init__()
        self.event = eventBound.event
        self.enabled = True
        pass

    def click(self, x, y, button, press):
        if not self.enabled:
            return

        debug('mouse clicked: %s  %s  %s  %s' %(x, y, button, press))

        if button == 1 and press:
            action = EventUtils.MOUSE_ACTION_LEFT_DOWN
        elif button == 1 and not press:
            action = EventUtils.MOUSE_ACTION_LEFT_UP
        elif button == 2 and press:
            action = EventUtils.MOUSE_ACTION_RIGHT_DOWN
        elif button == 2 and not press:
            action = EventUtils.MOUSE_ACTION_RIGHT_UP
        else:
            # TODO
            pass

        data = '%s,%s,%s,%s'%(EventUtils.MOUSE_TYPE, action, x, y)
        self.event.emit(data)
        pass

    def scroll(self, x, y, vertical, horizontal):
        if not self.enabled:
            return
        """
        TODO
        :param x:
        :param y:
        :param vertical:
        :param horizontal:
        :return:
        """
        debug('mouse scrolled: %s  %s  %s  %s' % (x, y, vertical, horizontal))
        pass

    def move(self, x, y):
        if not self.enabled:
            return
        debug('mouse moved: %s %s' %(x, y))
        data = '%s,%s,%s,%s'%(EventUtils.MOUSE_TYPE, EventUtils.MOUSE_ACTION_MOVE, x, y)
        self.event.emit(data)
        pass

    def stop(self):
        self.enabled = False
        try:
            super().stop()
        except:
            pass


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())