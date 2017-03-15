#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Settings Dialog
"""
from PyQt5.QtWidgets import (QDialog, QPushButton, QGroupBox,
                             QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout)

import GlobalValue
import Utils


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        pass

    def initUI(self):

        # Port
        portGroup = QGroupBox("Port Setting")
        pcPortLabel = QLabel('PC: ')
        self.pcPortEdit = QLineEdit(GlobalValue.pc_port)
        phonePortLabel = QLabel('Phone:')
        self.phonePortEdit = QLineEdit(GlobalValue.phone_port)

        portLayout = QGridLayout()
        portLayout.addWidget(pcPortLabel, 0, 0)
        portLayout.addWidget(self.pcPortEdit, 0, 1)
        portLayout.addWidget(phonePortLabel, 1, 0)
        portLayout.addWidget(self.phonePortEdit, 1, 1)
        portGroup.setLayout(portLayout)

        # OK button
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.okAction)
        okLayout = QHBoxLayout()
        okLayout.addStretch(1)
        okLayout.addWidget(okButton)

        # mainLayout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(portGroup)
        mainLayout.addLayout(okLayout)
        self.setLayout(mainLayout)

        self.setFixedSize(200, 150)
        self.setWindowTitle('Settings')
        Utils.center(self)
        pass


    def okAction(self):
        GlobalValue.pc_port = self.pcPortEdit.text()
        GlobalValue.phone_port = self.phonePortEdit.text()

        # TODO
        pass

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SettingsDialog()
    window.show()
    sys.exit(app.exec_())