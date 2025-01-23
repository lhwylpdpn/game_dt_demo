# -*- coding:utf-8 -*-
import struct

from twisted.internet.protocol import Factory
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver

from msgs import card_game_pb2

MAX_PLAYER = 2 # 房间最大人数


class CardGameProtocol(WebSocketServerProtocol):
    clients = []

    def onConnect(self, request):
        print(f"Client connecting: {request.peer}")
        if len(CardGameProtocol.clients) >= MAX_PLAYER:
            self.dropConnection()  # 服务器已满，拒绝连接
        CardGameProtocol.clients.append(self)

    def onOpen(self):
        print('Connection opened')

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket connection closed: {reason}")
        if self in CardGameProtocol.clients:
            CardGameProtocol.clients.remove(self)

    def onMessage(self, data, isBinary):
        print(f"Server received")
        try:
            msgId, player_id = self.extract_msgId(data)

            # ready_req = msgid_to_message(msgId)[0]
            # ready_req.ParseFromString(data[12:])

            if msgId == 1001:
                ready_req = card_game_pb2.ReadyGameRequest()
                ready_req.ParseFromString(data[12:])
                self.handle_ready_game(player_id, ready_req)

            elif msgId == 2001:
                start_req = card_game_pb2.StartGameRequest()
                start_req.ParseFromString(data[12:])
                self.handle_start_game(player_id, start_req)


            elif msgId == 3001:
                play_card_req = card_game_pb2.PlayCardRequest()
                play_card_req.ParseFromString(data[12:])
                self.handle_play_card(player_id, play_card_req)


            elif msgId == 4001:
                start_round_req = card_game_pb2.StartRoundRequest()
                start_round_req.ParseFromString(data[12:])
                self.handle_start_round(player_id, start_round_req)

            elif msgId == 5001:
                action_req = card_game_pb2.ActionRequest()
                action_req.ParseFromString(data[12:])
                self.handle_action_request(player_id, action_req)

            else:
                print(f"Unknown msgId: {msgId}")

        except Exception as e:
            print(f"Error processing request: {e}")

    def extract_msgId(self, data):
        msgId, player_id = struct.unpack("<I", data[:4])[0], struct.unpack("<Q", data[4:12])[0]
        print(f"msgid: {msgId}, player_id: {player_id}")
        return msgId, player_id

    def send_msg_to_another(self, data):  # 给其他玩家发送消息
        for player in CardGameProtocol.clients:
            if player != self:
                player.sendMessage(data)

    def handle_ready_game(self, player_id, data):
        print(f"ReadyGameRequest: mapId={data.mapId}, playerId={player_id}")

        # 构造 ReadyGameResponse
        response = card_game_pb2.ReadyGameResponse()
        response.roomId = 888
        response.result = True
        serialized_response = response.SerializeToString()
        msg_id = 1001
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response

        self.sendMessage(response_message, isBinary=True)

    def handle_start_game(self, player_id, data):
        print(f"StartGameRequest: roomId={data.roomId}")

        for change in data.ownChange:
            print(f"Hero {change.heroUniqueId} change to {change.position}, player_id: {player_id}")

        response = card_game_pb2.StartGameResponse()
        response.roomId = data.roomId
        response.result = True

        serialized_response = response.SerializeToString()

        msg_id = 2001
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)

    def handle_play_card(self, player_id, data):
        print(f"PlayCardRequest: roomId={data.roomId}, round={data.round}")

        response = card_game_pb2.PlayCardResponse()
        response.roomId = data.roomId
        response.result = True

        serialized_response = response.SerializeToString()
        msg_id = 3001
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)

    def handle_start_round(self, player_id, data):
        print(f"StartRoundRequest: roomId={data.roomId}, round={data.round}")
        response = card_game_pb2.StartRoundResponse()
        response.result = True
        response.round = data.round
        response.roomId = data.roomId
        serialized_response = response.SerializeToString()

        msg_id = 4001
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)

    def handle_action_request(self, player_id, data):
        print(f"ActionRequest: roomId={data.roomId}, playerId={player_id}, actionId={data.actionId}")

        if data.battleAction.HasField('moveAction'):
            print(f"MoveAction: {data.battleAction.moveAction.movePath}")
            for target_hero in data.battleAction.moveAction.targetHeroList:
                print(f"Target Hero ID: {target_hero.heroUniqueId}")

        elif data.battleAction.HasField('skillAction'):
            print(f"SkillAction: skillId={data.battleAction.skillAction.skillId}")
            for target_hero in data.battleAction.skillAction.targetHeroList:
                print(f"Target Hero ID: {target_hero.heroUniqueId}")

        response = card_game_pb2.ActionResponse()
        response.roomId = data.roomId
        response.round = data.round
        response.result = True

        serialized_response = response.SerializeToString()

        msg_id = 5001
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)


if __name__ == "__main__":
    fac = WebSocketServerFactory("ws://localhost:17090")
    fac.protocol = CardGameProtocol
    reactor.listenTCP(17090, fac)
    print("Server is running on port 17090.")
    reactor.run()