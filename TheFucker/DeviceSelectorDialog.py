#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main interface
"""
from PyQt5.QtWidgets import QDialog, QPushButton

class deviceSelectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(200, 200)
        test = QPushButton("test", self)
        self.setGeometry(300, 300, 250, 150)
        self.exec_()


