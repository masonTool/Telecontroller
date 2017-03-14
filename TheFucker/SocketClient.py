from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import (QTcpSocket)


class SocketClient(QObject):

    message = pyqtSignal([str])
    connection = pyqtSignal([bool])

    def __init__(self, ip, port):
        super().__init__()
        self.port = port
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
        self.isConnected = True
        self.actionSend()
        self.connection.emit(True)
        pass

    def disconnected(self):
        self.isConnected = False
        self.connection.emit(False)
        pass

    def actionSend(self):
        if self.isConnected:
            tmp = self.messageBox
            for item in tmp:
                ss = ""
                ss.encode()
                length = self.tcpSocket.writeData(item.encode())
                self.tcpSocket.flush()

                self.messageBox.remove(item)
                if length >0:
                    print("send: " + str(self.tcpSocket.isWritable()) + "-" + str(length) + "--" +item)
        else:
            self.tcpSocket.connectToHost(self.ip, self.port)
        pass

    def send(self, message):
        self.messageBox.append(message)
        self.actionSend()
        pass

    def readyRead(self):
        result = str(self.tcpSocket.readLine(), encoding='utf-8')
        print('received: ' + result)
        self.message.emit(result)
        pass
