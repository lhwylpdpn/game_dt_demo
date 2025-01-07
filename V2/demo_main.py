# -*- coding:utf-8 -*-

from twisted.internet.protocol import Factory
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
# from bin_test import card_game_pb2

MAX_PLAYER = 2 # 房价最大人数

#class CardGameProtocol(protocol.Protocol):
class CardGameProtocol(LineReceiver):
    
    def __init__(self, factory):
        self.factory = factory
        self.state = "WAITING"
        
    def connectionMade(self):
        if len(self.factory.players) >= MAX_PLAYER:
            msg = "服务器已满".encode()
            length_prefix = len(msg).to_bytes(4, byteorder="big")
            self.transport.write(length_prefix + msg)
            self.transport.loseConnection()
        else:
            self.factory.players.add(self)
            if len(self.factory.players) == 1:    # 第一个进入
                self.state = "SHOWCARD"           # 设置为出牌状态
            msg = f"state: {self.state}".encode()
            length_prefix = len(msg).to_bytes(4, byteorder="big")
            self.transport.write(length_prefix + msg)
        
    def connectionLost(self, reason):
        self.factory.players.remove(self)

    # def dataReceived(self, data):
    #     self.hand_Data(data)
    #     for c in self.factory.players:
    #         if c != self:
    #             c.transport.write(data)
    
    def lineReceived(self, data):            # 收到消息数据后执行
        self.hand_Data(data)                 # TODO 丰富
        self.send_msg_to_another(data)       # TODO 丰富
        
                     
    def send_msg_to_another(self, data): # 给其他的player 发消息
        for player in self.factory.players:
            if player != self:
                player.sendLine(data) 
    
    def hand_Data(self, data):
        self.sendLine(f"Server Reciveced msg {data}".encode())
        # try:
        #     if len(data) < 4:
        #         print("Incomplete data: waiting for length prefix")
        #         return

        #     length_prefix = int.from_bytes(data[:4], byteorder="big")
        #     payload = data[4:4 + length_prefix]

        #     request = card_game_pb2.ReadyGameRequest()
        #     request.ParseFromString(payload)
        #     print(f"Received Request: client_id={request.client_id}, game_id={request.game_id}")

        #     response = card_game_pb2.ReadyGameResponse()
        #     response.success = True
        #     response.message = f"Player {request.client_id} is ready for game {request.game_id}"

        #     serialized_response = response.SerializeToString()
        #     length_prefix = len(serialized_response).to_bytes(4, byteorder="big")
        #     self.transport.write(length_prefix + serialized_response)
        # except Exception as e:
        #     print(f"Error processing request: {e}")

    
class CardGameFactory(protocol.Factory):
    
    def __init__(self):
        self.players = set()          # 创建了一个player的集合
    
    def buildProtocol(self, addr):
        return CardGameProtocol(self)


if __name__ == "__main__":
    reactor.listenTCP(8000, CardGameFactory())
    print("Server is running on port 8000.")
    reactor.run()