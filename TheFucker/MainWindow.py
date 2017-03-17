#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main interface
"""

from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QPoint, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QInputDialog, QLineEdit
from pymouse import PyMouseEvent

import AdbOperator
import EventUtils
import GlobalValue
import Utils
from DeviceDialog import DeviceDialog
from SocketClient import SocketClient
from SettingsDialog import SettingsDialog


class EventBound(QObject):
    event = pyqtSignal([str])


def debug(str):
    print(str)
    pass

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.sizeRecord = QSize(0, 0)
        self.positionRecord = QPoint(0, 0)
        self.proxyMode = False
        self.eventBound = EventBound()
        self.client = SocketClient('127.0.0.1', GlobalValue.pc_port)
        self.client.message[str].connect(self.showReceived)
        self.eventBound.event[str].connect(self.sendWrapper)

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
        configAction.triggered.connect(self.showSettingsDialog)

        infoAction = QAction(QIcon('img/info.png'), 'Info', self)
        infoAction.setShortcut('Ctrl+I')
        infoAction.setStatusTip('Info')
        infoAction.triggered.connect(self.startSend)

        toolbar = self.addToolBar('')
        toolbar.addAction(self.playAction)
        toolbar.addAction(deviceAction)
        toolbar.addAction(configAction)
        toolbar.addAction(infoAction)

        self.statusBar()
        self.resize(500, 500)
        GlobalValue.deviceSize = [500, 500]
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

    def showSettingsDialog(self):
        """
        设置界面
        """
        settingsDialog = SettingsDialog(self)
        settingsDialog.exec()
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

    def startCapture(self):
        self.proxyMode = True
        self.playAction.setIcon(QIcon('img/pause.png'))
        self.mouseEvent = MyMouseEvent(self.eventBound)
        self.mouseEvent.start()
        pass

    def stopCapture(self):
        self.proxyMode = False
        self.playAction.setIcon(QIcon('img/play.png'))
        self.mouseEvent.stop()
        pass


    def toggleProxy(self):
        if self.proxyMode:
            self.stopCapture()
        else:
            self.startCapture()

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
        if e.key() == 16777216 and self.proxyMode: #ESC
            self.stopCapture()

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

    def mouseMoveEvent(self, QMouseEvent): # MyMouseEvent不能处理按下鼠标移动的情况
        """
        按下鼠标按键的移动事件
        """
        if not self.proxyMode:
            return

        x = QMouseEvent.globalX()
        y = QMouseEvent.globalY()

        debug('mouse moved: %s %s' %(x, y))
        data = '%s,%s,%s,%s'%(EventUtils.MOUSE_TYPE, EventUtils.MOUSE_ACTION_MOVE, x, y)
        self.eventBound.event.emit(data)
        pass

    def resizeEvent(self, QResizeEvent):
        """
        接收窗口大小变化数据
        """
        self.sizeRecord = QResizeEvent.size()
        pass

    def moveEvent(self, QMoveEvent):
        """
        接收窗口移动数据
        """
        self.positionRecord = QMoveEvent.pos()
        pass

    def sendWrapper(self, message):
        """
        鼠标坐标转换处理
        """
        result = list(map(lambda it:int(float(it)), message.split(',')))
        if result[0] == EventUtils.MOUSE_TYPE:
            x = (result[2]-self.positionRecord.x())/self.sizeRecord.width() * GlobalValue.deviceSize[0]
            y = (result[3]-self.positionRecord.y())/self.sizeRecord.height() * GlobalValue.deviceSize[1]
            message = '%s,%s,%s,%s' %(result[0], result[1], int(x), int(y))
            pass

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