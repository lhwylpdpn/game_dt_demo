# -*- coding:utf-8 -*-
import struct
import traceback
from pprint import pprint

from protobuf_to_dict import protobuf_to_dict

from twisted.internet.protocol import Factory
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory, ConnectionDeny
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver


from msgs import card_game_pb2
from models.player import Player
from msgid_to_message import MSGID_TO_MESSAGE

# from servics.playermanager import PlayerManagerService  # TODO

MAX_PLAYER = 2 # 房间最大人数


class CardGameProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super(CardGameProtocol, self).__init__(*args, **kwargs)
        self.player = None

    def onConnect(self, request):
        print(f"Client connecting: {request.peer}")
        if len(self.factory.clients) >= MAX_PLAYER:
            raise ConnectionDeny(403, f"Server is Full.")
        self.factory.register(self)
        self.player = Player()           ## 创建当前玩家的实体

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket connection closed: {reason}")
        self.factory.unregister(self)

    def onMessage(self, data, isBinary):
        print(f"Server received")
        try:
            msgId, player_id = self.extract_msgId(data)
            self.player.set_playerId(player_id)
             
            # 统一处理msg
            parse_proto, message_handle = MSGID_TO_MESSAGE.get(msgId)
            _req_data = parse_proto().ParseFromString(data[12:])
            message_handle(self, player_id, _req_data)

            # if msgId == 1001:
            #     ready_req = card_game_pb2.ReadyGameRequest()
            #     ready_req.ParseFromString(data[12:])
            #     self.handle_ready_game(player_id, ready_req)

            # elif msgId == 1005:
            #     start_round_req = card_game_pb2.StartRoundRequest()
            #     start_round_req.ParseFromString(data[12:])
            #     self.handle_start_round(player_id, start_round_req)

            # elif msgId == 1007:
            #     play_card_req = card_game_pb2.PlayCardRequest()
            #     play_card_req.ParseFromString(data[12:])
            #     self.handle_play_card(player_id, play_card_req)

            # else:
            #     print(f"Unknown msgId: {msgId}")

        except Exception as e:
            print(f"Error processing request: {e}")
            traceback.print_exc()

    def extract_msgId(self, data):
        msgId, player_id = struct.unpack("<I", data[:4])[0], struct.unpack("<Q", data[4:12])[0]
        print(f"msgid: {msgId}, player_id: {player_id}")
        return msgId, player_id

    def send_msg_to_another(self, data):  # 给其他玩家发送消息
        for player in self.factory.clients:
            if player != self:
                player.sendMessage(data)


class CardGameFactory(WebSocketServerFactory):
    def __init__(self, url):
        super(CardGameFactory, self).__init__(url)
        # 用于存储所有连接的客户端
        self.clients = []

    # 注册新的客户端连接
    def register(self, client):
        if client not in self.clients:
            print("Registered client {}".format(client.peer))
            self.clients.append(client)

    # 注销已关闭的客户端连接
    def unregister(self, client):
        if client in self.clients:
            print("Unregistered client {}".format(client.peer))
            self.clients.remove(client)

    # 广播消息给所有连接的客户端
    def broadcast(self, msg, isBinary):
        for c in self.clients:
            c.sendMessage(msg, isBinary)

    # 获取当前的游戏房间
    def game_rooms(self): 
        rooms = []
        for _ in self.clients:
            _room = _.player.room
            if _room and _room not in  rooms:
                rooms.append(_room)
        return rooms


if __name__ == "__main__":
    fac = CardGameFactory("ws://localhost:17090")
    fac.protocol = CardGameProtocol
    reactor.listenTCP(17090, fac)
    print("Server is running on port 17090.")
    reactor.run()