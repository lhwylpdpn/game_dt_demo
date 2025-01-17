# -*- coding:utf-8 -*-

from twisted.internet.protocol import Factory
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver

from msgs import card_game_pb2


MAX_PLAYER = 2 # 房价最大人数


class CardGameProtocol(WebSocketServerProtocol):
    
    clients = []
    
    def onConnect(self, request):
        print("Clinet conneting:{}".format(request.peer))
        if len(CardGameProtocol.clients) >= MAX_PLAYER:
            self.dropConnection() # reason="服务器已满"
        CardGameProtocol.clients.append(self)
    
    def onOpen(self):
        print('make an connection')
    
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
        if self in CardGameProtocol.clients:
            CardGameProtocol.clients.remove(self)
   
    def onMessage(self, data, isBinary):
        print("Server received: " + data.decode('utf-8'))
        self.hand_Data(data)                 # TODO 丰富
        self.send_msg_to_another(data)       # TODO 丰富
        
    def send_msg_to_another(self, data): # 给其他的player 发消息
        for player in CardGameProtocol.clients:
            if player != self:
                player.sendMessage(data)
                
   
    def hand_Data(self, data):
        print(f"Server Reciveced msg {data}".encode())
        try:
            request = card_game_pb2.ReadyGameRequest()
            request.ParseFromString(data)
            print(f"Received Request: client_id={request.client_id}, game_id={request.game_id}")

            response = card_game_pb2.ReadyGameResponse()
            response.success = True
            response.message = f"Player {request.client_id} is ready for game {request.game_id}"

            serialized_response = response.SerializeToString()
            self.sendMessage(serialized_response)
        except Exception as e:
            print(f"Error processing request: {e}")

    

if __name__ == "__main__":
    fac = WebSocketServerFactory("ws://localhost:17090")
    fac.protocol = CardGameProtocol
    reactor.listenTCP(17090, fac)
    print("Server is running on port 17090.")
    reactor.run()