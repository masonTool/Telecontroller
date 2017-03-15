#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Utils
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar().showMessage('选择连接设备')
        self.resize(500, 500)
        self.setWindowTitle('Telecontroller')
        Utils.center(self)

        self.rate = 2.3
        pass



    def resizeEvent(self, QResizeEvent): # real signature unknown; restored from __doc__
        """ resizeEvent(self, QResizeEvent) """
        print('resizeEvnet: %s' %QResizeEvent.size())

        new_width = QResizeEvent.size().width()
        new_height = QResizeEvent.size().height()
        old_width = QResizeEvent.oldSize().width()
        old_height = QResizeEvent.oldSize().height()

        if int(new_width * 2.3) == new_height:
            return


        if new_height != old_height and new_width == old_width:
            self.resize(new_height/2.3, new_height)
        elif new_width != old_width and new_height == old_height:
            self.resize(new_width, new_width * 2.3)
        pass

    def changeEvent(self, QEvent): # real signature unknown; restored from __doc__
        """ changeEvent(self, QEvent) """
        # print('changeEvent: %s' % QEvent)
        pass

    def moveEvent(self, QMoveEvent): # real signature unknown; restored from __doc__
        """ moveEvent(self, QMoveEvent) """
        print('moveEvent: %s' % QMoveEvent.pos())
        pass


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())