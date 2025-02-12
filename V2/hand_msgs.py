# -*- coding:utf-8 -*-
import struct
import traceback
from twisted.internet import defer
from twisted.internet.threads import deferToThread
from msgs import card_game_pb2
from protobuf_to_dict import protobuf_to_dict


def handle_ready_game(self_client, player_id, data):
    print(f"ReadyGameRequest: mapId={data.mapId}, playerId={player_id}")

    data = protobuf_to_dict(data)
    self_client.player.match_player(
        current_avaliable_rooms=self_client.factory.game_rooms())  # 匹配对手，创建房间 zhaohu 20250125
    self_client.player.set_ready_game_data(data)

    # 构造 ReadyGameResponse
    response = card_game_pb2.ReadyGameResponse()
    response.roomId = self_client.player.room.room_id
    response.result = True
    serialized_response = response.SerializeToString()
    msg_id = 1002
    response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
    self_client.sendMessage(response_message, isBinary=True)

    if self_client.player.room.left_player and self_client.player.room.right_player:
        print(f"Room is full, start game")
        def start_game_in_background():
            handle_start_game(self_client, player_id)
        deferToThread(start_game_in_background)

        # def on_game_started(result):
        #     print(f"Game started successfully, result: {result}")
        # def on_error(failure):
        #     print(f"error: {failure}")
        # d.addCallback(on_game_started)
        # d.addErrback(on_error)

def handle_start_game(self_client, player_id):
    print(f"Sending StartGameRequest, playerId={player_id}")
    data = self_client.player.room.dict()

    # 构造 StartGameRequest 消息
    start_game_request = card_game_pb2.StartGameRequest()
    start_game_request.roomId = self_client.player.room.room_id

    self_client.player.room.init_game()

    if data["left_player"]:
        p_id = data["left_player"].get("playerId")
        if data["left_heros"]:
            for hero in data["left_heros"]:
                hero_change = start_game_request.change.add()
                hero_change.playerId = p_id
                hero_change.heroUniqueId = hero["unique_id"]
                hero_change.heroId = hero["HeroID"]
                hero_change.position.x, hero_change.position.y, hero_change.position.z = hero["position"][0], hero["position"][1], hero["position"][2]
                hero_change.positionType = hero["positionType"]
    if data["right_player"]:
        p_id = data["right_player"].get("playerId")
        if data["right_heros"]:
            for hero in data["right_heros"]:
                hero_change = start_game_request.change.add()
                hero_change.playerId = p_id
                hero_change.heroUniqueId = hero["unique_id"]
                hero_change.heroId = hero["HeroID"]
                hero_change.position.x, hero_change.position.y, hero_change.position.z = hero["position"][0], hero["position"][1], hero["position"][2]
                hero_change.positionType = hero["positionType"]

    # 发送消息
    msg_id = 1003
    serialized_request = start_game_request.SerializeToString()
    response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_request
    # self_client.factory.broadcast(response_message, isBinary=True) # 2025-2-12 hu del
    # self_client.sendMessage(response_message, isBinary=True)
    self_client.player.room.topic_manager.publish(self_client.player.room.room_id, response_message, isBinary=True) # HU add

def handle_start_round(self_client, player_id, data):
    print(f"11111StartRoundRequest ")
    response = card_game_pb2.StartRoundResponse()
    response.result = True
    response.round = self_client.player.room.round
    response.roomId = self_client.player.room.room_id
    serialized_response = response.SerializeToString()
    self_client.player.set_is_start_round()


    if self_client.player.room.left_player.is_start_round and self_client.player.room.right_player.is_start_round:
        msg_id = 1006
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self_client.player.room.topic_manager.publish(self_client.player.room.room_id, response_message, isBinary=True)  # HU add


def handle_play_card(self_client, player_id, data):
    print(f"PlayCardRequest: roomId={data.roomId}, round={data.round}")

    response = card_game_pb2.PlayCardResponse()
    response.roomId = data.roomId
    response.result = True

    data = protobuf_to_dict(data)
    self_client.player.set_show_cards(data)
    self_client.player.set_is_show_cards(True)

    serialized_response = response.SerializeToString()
    msg_id = 1008
    response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
    self_client.sendMessage(response_message, isBinary=True)
    # self_client.handle_action_request(player_id)

    room_data = self_client.player.room.dict()
    if room_data.get("left_player", {}).get("is_show_cards") and room_data.get("right_player", {}).get("is_show_cards"):
        print(f"双方玩家都已经出牌，开始计算Action")
        self_client.handle_start_round(self_client, player_id, room_data)

        card_actions = []
        self_client.player.room.game.single_run(handle_action_request, self_client, card_actions)


def handle_action_request(self_client, player_id):
    print(f"Received ActionRequest: playerId={player_id}")

    fake_move_action = card_game_pb2.MoveAction()
    fake_move_action.movePath.append(card_game_pb2.PbVector3(x=1, y=1, z=7))
    fake_move_action.targetHeroList.add(heroUniqueId=1)

    fake_skill_action = card_game_pb2.SkillAction()
    fake_skill_action.skillId = 1
    fake_skill_action.targetHeroList.add(heroUniqueId=2)

    battle_action_base = card_game_pb2.BattleActionBase()
    battle_action_base.heroUniqueId = 1
    battle_action_base.moveAction.CopyFrom(fake_move_action)

    action_response = card_game_pb2.ActionResponse()
    action_response.roomId = 888
    action_response.round = 2
    action_response.actionId = 89
    action_response.result = True

    serialized_response = action_response.SerializeToString()

    msg_id = 1010
    response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
    self_client.sendMessage(response_message, isBinary=True)