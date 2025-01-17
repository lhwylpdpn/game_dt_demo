from twisted.internet import reactor, protocol
# from twisted.protocols.basic import LineReceiver
from msgs import card_game_pb2
from autobahn.twisted.websocket import connectWS, WebSocketClientProtocol, WebSocketClientFactory

class CardGameClientProtocol(WebSocketClientProtocol):
    
    def onConnect(self, response):
        print("Connected: {}".format(response.peer))

    def onOpen(self):
        print("Connection established")
        #self.sendMessage(b"Hello Server")
        self.sendRequest()

    def onMessage(self, msg, isBinary):
        print(f"Received msg: {msg}")
        response = card_game_pb2.ReadyGameResponse()
        response.ParseFromString(msg)
        print(f"Received Response: success={response.success}, message={response.message}")
        
    def onClose(self, wasClean, code,  reason):
        print("Connected colsed: {}".format(reason))
        reactor.stop()
        
    def sendRequest(self):
        # 创建 ReadyGameRequest 对象
        __request = card_game_pb2.ReadyGameRequest()
        __request.client_id = "test5678"
        __request.game_id = "game_5678"
        __request_string = __request.SerializeToString()
        print(f"read for send request:{__request_string}")
        self.sendMessage(__request_string)

class CardGameClientFactory(WebSocketClientFactory):
    def buildProtocol(self, addr):
        return CardGameClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason.getErrorMessage()}")
        reactor.stop()


if __name__ == "__main__":
    # 连接到本地服务器
    # reactor.connectTCP("localhost", 8000, CardGameClientFactory())
    # reactor.run()
    factory = WebSocketClientFactory("ws://127.0.0.1:17090")
    factory.protocol = CardGameClientProtocol
    
    # 连接到WebSocket服务器
    reactor.connectTCP("127.0.0.1", 17090, factory)
    
    # 启动reactor事件循环
    reactor.run()
