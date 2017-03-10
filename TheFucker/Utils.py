#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
this is just a toolkit
"""
import PyQt5


def center(widget):
    """
    居中显示
    """
    screen = PyQt5.QtWidgets.QDesktopWidget().screenGeometry()
    size = widget.geometry()
    widget.move((screen.width() - size.width()) / 2,
              (screen.height() - size.height()) / 2)
    pass
