# -*- coding:utf-8 -*-

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("What's your name?".encode())

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]#断开连接后删除键值对

    def lineReceived(self, line):#收到消息数据后执行
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("Name taken, please choose another.".encode())
            return
        self.sendLine(f"Welcome, {name}!".encode())
        self.name = name
        self.users[name] = self    #将当前的Chat保存为值，name为键
        self.state = "CHAT"       #重置状态

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for protocol in self.users.values():#给其他用户发送消息
            if protocol != self:
                protocol.sendLine(message.encode())


class ChatFactory(Factory):

    def __init__(self):
        self.users = {} #创建了一个公用的字典来保存用户名和对应的Chat实例

    def buildProtocol(self, addr):
        return Chat(self.users)


reactor.listenTCP(8123, ChatFactory())
reactor.run()