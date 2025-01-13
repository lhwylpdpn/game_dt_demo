from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from msgs import card_game_pb2


class CardGameClientProtocol(LineReceiver):
    def connectionMade(self):
        # 当连接建立后，发送序列化后的请求
        self.sendRequest()

    def sendRequest(self):
        # 创建 ReadyGameRequest 对象
        __request = card_game_pb2.ReadyGameRequest()
        __request.client_id = "test5678"
        __request.game_id = "game_5678"
        __request_string = __request.SerializeToString()
        # 计算长度前缀
        length_prefix = len(__request_string).to_bytes(4, byteorder="big")
        # 发送长度前缀和序列化后的请求
        print(length_prefix + __request_string + b'\r\n')
        self.transport.write(length_prefix + __request_string + b'\r\n')  # 添加行结束符
        print("Request sent.")

    def lineReceived(self, data):
        # 接收服务器的响应

        try:
            if len(data) < 4:
                print("Incomplete data: waiting for length prefix")
                return
            # 提取长度前缀
            length_prefix = int.from_bytes(data[:4], byteorder="big")
            payload = data[4:4 + length_prefix]
            # 假设服务器发送的是 ReadyGameResponse
            response = card_game_pb2.ReadyGameResponse()
            response.ParseFromString(payload)
            print(f"Received Response: success={response.success}, message={response.message}")
            # 关闭连接
        except Exception as e:
            print(f"Error processing response: {e}")


class CardGameClientFactory(protocol.ClientFactory):
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
    reactor.connectTCP("localhost", 8000, CardGameClientFactory())
    reactor.run()