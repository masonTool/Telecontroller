from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import (QTcpSocket)


class SocketClient(QObject):

    message = pyqtSignal([str])

    def __init__(self, ip, port):
        super().__init__()
        self.port = int(port)
        self.ip = ip
        self.isConnected = False

        self.messageBox = []
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.connected.connect(self.connected)
        self.tcpSocket.readyRead.connect(self.readyRead)
        self.tcpSocket.disconnected.connect(self.disconnected)
        pass

    def close(self):
        self.tcpSocket.abort()
        self.tcpSocket.close()
        # ????
        pass

    def connected(self):
        if len(self.messageBox) > 0:
            message = self.messageBox[0]
            if self.tcpSocket.writeData(message.encode()) > 0:
                print("send succssed:" + message)
                self.messageBox.remove(message)
                if len(self.messageBox) > 0:
                    self.sendNext()

        pass

    def disconnected(self):
        pass

    def sendNext(self):
        self.close()
        self.tcpSocket.connectToHost(self.ip, self.port)
        pass

    def send(self, message):
        self.messageBox.append(message)
        self.sendNext()
        pass

    def readyRead(self):
        result = str(self.tcpSocket.readLine(), encoding='utf-8')
        self.message.emit(result)
        pass
