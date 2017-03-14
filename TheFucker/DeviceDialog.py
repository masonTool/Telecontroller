#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main interface
"""
from PyQt5.QtWidgets import (QDialog, QPushButton, QGroupBox,
    QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QTimer
import GlobalValue
import AdbOperator
import Utils

class DeviceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        pass

    def initUI(self):

        self.deviceListWidget = QListWidget()
        self.deviceList = []
        self.updateDevices()

        confirmButton = QPushButton("OK")
        confirmButton.clicked.connect(self.okAction)
        okLayout = QHBoxLayout()
        okLayout.addStretch(1)
        okLayout.addWidget(confirmButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.deviceListWidget)
        mainLayout.addLayout(okLayout)

        self.resize(300, 300)
        Utils.center(self)
        self.setLayout(mainLayout)
        self.setWindowTitle("Device Selector")
        pass

    def showEvent(self, QShowEvent):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDevices)
        self.timer.start(500)
        pass

    def closeEvent(self, QCloseEvent):
        self.timer.stop()
        pass

    def okAction(self):
        item = self.deviceListWidget.selectedItems()
        if len(item) == 0:
            GlobalValue.connectedDevice = ''
        else:
            GlobalValue.connectedDevice = item[0].text()
            parent = self.parentWidget()
            parent.statusBar().showMessage(GlobalValue.connectedDevice + ' 连接成功')
            size = AdbOperator.getPhoneSize()
            parent.resize(int(size[0] / 4), int(size[1] / 4))
            parent.statusBar().showMessage('窗口调整为：' + str(size[0]) + 'x' + str(size[1]))

        self.close()
        pass

    def updateDevices(self):
        """
        更新设备列表, 及选中状态
        """
        # 将选中的QListWidgetItem列表转化为string列表
        selectedItems = list(map(lambda it:it.text(), self.deviceListWidget.selectedItems()))
        if len(selectedItems) == 0:
            selectedItems += [GlobalValue.connectedDevice]

        newDeviceList = AdbOperator.getDevices()
        if self.deviceList != newDeviceList:
            self.deviceListWidget.clear()
            self.deviceList = newDeviceList

            firstItem = 0
            for device in self.deviceList:
                item = QListWidgetItem(device)
                self.deviceListWidget.addItem(item)

                if firstItem == 0:
                    firstItem = item
                    firstItem.setSelected(True)
                elif device in selectedItems:
                    firstItem.setSelected(False)
                    item.setSelected(True)
        pass

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = DeviceDialog()
    window.show()
    sys.exit(app.exec_())
