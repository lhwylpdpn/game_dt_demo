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

            elif msgId == 1005:
                start_round_req = card_game_pb2.StartRoundRequest()
                start_round_req.ParseFromString(data[12:])
                self.handle_start_round(player_id, start_round_req)

            elif msgId == 1007:
                play_card_req = card_game_pb2.PlayCardRequest()
                play_card_req.ParseFromString(data[12:])
                self.handle_play_card(player_id, play_card_req)

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
        msg_id = 1002
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response

        self.sendMessage(response_message, isBinary=True)
        self.handle_start_game(player_id)


    def handle_start_game(self, player_id):
        print(f"Sending StartGameRequest, playerId={player_id}")

        # 构造 StartGameRequest 消息
        start_game_request = card_game_pb2.StartGameRequest()
        start_game_request.roomId = 888
        hero_changes = [
            (1, "hero1_position"),
        ]
        # 填充己方和敌方的 heroChange
        for hero_unique_id, position in hero_changes:
            hero_change = start_game_request.ownChange.add()
            hero_change.heroUniqueId = hero_unique_id
            hero_change.heroId = hero_unique_id
            hero_change.position.x = 1
            hero_change.position.y = 1
            hero_change.position.z = 6
            hero_change.positionType = 0
        enemy_changes = [
            (2, "hero1_position"),
        ]
        for hero_unique_id, position in enemy_changes:
            hero_change = start_game_request.enemyChange.add()
            hero_change.heroUniqueId = hero_unique_id
            hero_change.heroId = hero_unique_id
            hero_change.position.x = 8
            hero_change.position.y = 1
            hero_change.position.z = 3
            hero_change.positionType = 0


        # 发送消息
        msg_id = 1003
        serialized_request = start_game_request.SerializeToString()
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_request
        self.sendMessage(response_message, isBinary=True)

    def handle_play_card(self, player_id, data):
        print(f"PlayCardRequest: roomId={data.roomId}, round={data.round}")

        response = card_game_pb2.PlayCardResponse()
        response.roomId = data.roomId
        response.result = True

        serialized_response = response.SerializeToString()
        msg_id = 1008
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)
        self.handle_action_request(player_id)


    def handle_start_round(self, player_id, data):
        print(f"StartRoundRequest: roomId={data.roomId}, round={data.round}")
        response = card_game_pb2.StartRoundResponse()
        response.result = True
        response.round = data.round
        response.roomId = data.roomId
        serialized_response = response.SerializeToString()

        msg_id = 1006
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)

    def handle_action_request(self, player_id):
        print(f"Received ActionRequest: playerId={player_id}")

        fake_move_action = card_game_pb2.MoveAction()
        fake_move_action.movePath.append(card_game_pb2.PbVector3(x=1, y=2, z=3))
        fake_move_action.targetHeroList.add(heroUniqueId=101)

        fake_skill_action = card_game_pb2.SkillAction()
        fake_skill_action.skillId = 123
        fake_skill_action.targetHeroList.add(heroUniqueId=102)

        battle_action_base = card_game_pb2.BattleActionBase()
        battle_action_base.heroUniqueId = 101
        battle_action_base.moveAction.CopyFrom(fake_move_action)

        action_response = card_game_pb2.ActionResponse()
        action_response.roomId = 888
        action_response.round = 2
        action_response.actionId = 89
        action_response.result = True

        serialized_response = action_response.SerializeToString()

        msg_id = 1010
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self.sendMessage(response_message, isBinary=True)


if __name__ == "__main__":
    fac = WebSocketServerFactory("ws://localhost:17090")
    fac.protocol = CardGameProtocol
    reactor.listenTCP(17090, fac)
    print("Server is running on port 17090.")
    reactor.run()