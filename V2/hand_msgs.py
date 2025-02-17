# -*- coding:utf-8 -*-
import struct
import traceback
from twisted.internet import defer
from twisted.internet.threads import deferToThread
from msgs import card_game_pb2
from protobuf_to_dict import protobuf_to_dict

from schedule.utils.strategy_utils.basic_utils import range_mht_hollow_circle


def handle_ready_game(self_client, player_id, data):
    print(f"ReadyGameRequest: mapId={data.mapId}, playerId={player_id}")

    data = protobuf_to_dict(data)
    print(f"ReadyGameRequest: data={data}")
    self_client.player.match_player(
        current_avaliable_rooms=self_client.factory.game_rooms(), map_id=data.get("mapId"))  # 匹配对手，创建房间 zhaohu 20250125
    self_client.player.set_ready_game_data(data)
    print(f"{player_id}: set_ready_game_data ok")

    # 构造 ReadyGameResponse
    response = card_game_pb2.ReadyGameResponse()
    response.roomId = self_client.player.room.room_id
    response.result = True
    serialized_response = response.SerializeToString()
    msg_id = 1002
    response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
    self_client.sendMessage(response_message, isBinary=True)
    print(f"left_player={self_client.player.room.left_player}, right_player={self_client.player.room.right_player}")
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
    # 构造 StartGameRequest 消息
    start_game_request = card_game_pb2.StartGameRequest()
    start_game_request.roomId = self_client.player.room.room_id

    self_client.player.room.init_game()
    data = self_client.player.room.dict()

    print("handle_start_game: data---->", data)
    if data["left_player"]:
        p_id = data["left_player"].get("playerId")
        if data["left_heros"]:
            for hero in data["left_heros"]:
                hero_change = start_game_request.change.add()
                hero_change.playerId = p_id
                hero_change.heroUniqueId = hero["unique_id"]
                hero_change.heroId = hero["HeroID"]
                hero_change.position.x, hero_change.position.y, hero_change.position.z = hero["position"][0], \
                hero["position"][1], hero["position"][2]
                hero_change.positionType = hero["positionType"]
                for card in hero["AvaliableCards"]:
                    card_message = hero_change.cards.add()
                    card_message.cardId = card["CardID"]
                    card_message.cardUniqueId = card.get("unique_id", 0)
    if data["right_player"]:
        p_id = data["right_player"].get("playerId")
        if data["right_heros"]:
            for hero in data["right_heros"]:
                hero_change = start_game_request.change.add()
                hero_change.playerId = p_id
                hero_change.heroUniqueId = hero["unique_id"]
                hero_change.heroId = hero["HeroID"]
                hero_change.position.x, hero_change.position.y, hero_change.position.z = hero["position"][0], \
                hero["position"][1], hero["position"][2]
                hero_change.positionType = hero["positionType"]
                for card in hero["AvaliableCards"]:
                    card_message = hero_change.cards.add()
                    card_message.cardId = card["CardID"]
                    card_message.cardUniqueId = card.get("unique_id", 0)

    # 发送消息
    msg_id = 1003
    serialized_request = start_game_request.SerializeToString()
    response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_request
    self_client.player.room.topic_manager.publish(self_client.player.room.room_id, response_message,
                                                  isBinary=True)  # HU add


def handle_start_round(self_client, player_id, data):
    print(f"StartRoundRequest ")
    response = card_game_pb2.StartRoundResponse()
    response.result = True
    response.round = self_client.player.room.round
    response.roomId = self_client.player.room.room_id
    serialized_response = response.SerializeToString()
    self_client.player.set_is_start_round()

    if self_client.player.room.left_player.is_start_round and self_client.player.room.right_player.is_start_round:
        msg_id = 1006
        response_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_response
        self_client.player.room.topic_manager.publish(self_client.player.room.room_id, response_message,
                                                      isBinary=True)  # HU add
        self_client.player.room.left_player.set_is_start_round()
        self_client.player.room.right_player.set_is_start_round()


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
        handle_start_round(self_client, player_id, room_data)
        print("room---->", self_client.player.room.dict())
        # [{hero:attr, card: [], speed : []}]

        actions = card_actions(self_client.player.room.dict())
        self_client.player.room.game.single_run(handle_action_request, self_client, actions)


def handle_action_request(self_client, player_id, data):
    print(f"ActionRequest: playerId={player_id} data:{data}")
    
    battle_action_base = card_game_pb2.BattleActionBase()
    battle_action_base.heroUniqueId = data["action"]["unique_id"]

    if data["action"]["action_type"] in ["LEFT", "RIGHT", "TOP", "BOTTOM"]:
        x, y, z = data["action"]["move_position"]
        fake_move_action = card_game_pb2.MoveAction()
        fake_move_action.movePath.append(card_game_pb2.PbVector3(x=x, y=y, z=z))
        fake_move_action.targetHeroList.add(heroUniqueId=data["action"]["unique_id"])
        battle_action_base.moveAction.CopyFrom(fake_move_action)

    if data["action"].get("type") in (1, 2):
        fake_type_action = card_game_pb2.TypeAction()
        fake_type_action.type = data["action"]["type"]
        fake_type_action.Id = data["action"]["id"]

        fake_skill_action = card_game_pb2.SkillAction()
        for t in data["action"]["target"]:
            fake_skill_action.targetHeroList.add(heroUniqueId=t)
            change_state = card_game_pb2.ChangeState()
            change_state.type = card_game_pb2.ChangeStateType.Damage
        fake_skill_action.position.x, fake_skill_action.position.y, fake_skill_action.position.z =  data["action"]["skill_pos"]
        battle_action_base.skillAction.CopyFrom(fake_skill_action)


    action_request = card_game_pb2.ActionRequest()
    action_request.roomId = self_client.player.room.room_id
    action_request.round = self_client.player.room.round
    action_request.actionId = data['tick']
    action_request.gameOver = data['gameover'] 
    action_request.roundStatus = data['roundover']

    action_request.battleAction.CopyFrom(battle_action_base)  
    action_request.playerId = player_id            

    serialized_request = action_request.SerializeToString()

    msg_id = 1009
    request_message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_request
    self_client.player.room.topic_manager.publish(self_client.player.room.room_id, request_message,
                                                  isBinary=True)  # HU add


def card_actions(game_data):
    actions = []
    maps = game_data["maps"]
    heroes = game_data["left_heros"] + game_data["right_heros"]
    sorted_heroes = sorted(heroes, key=lambda x: x["Speed"], reverse=True)
    for hero in sorted_heroes:
        if len(hero["AvaliableCards"]) > 0:
            for card in hero["AvaliableCards"]:
                release_position = card["releasePosition"]
                if release_position is None: # HU add temp (没出牌没有出牌位置)
                    continue
                release_points = range_mht_hollow_circle(release_position, card["AtkDistance"][1],
                                                         card["AtkDistance"][0], 0, 0, maps)
                targets = [t["HeroID"] for t in heroes if t["playerId"] != hero["playerId"] and tuple(t["position"]) in release_points]
                each = {
                    "action": {
                        "skill_pos": tuple(release_position),
                        "skill_range": release_points,
                        "release_range": [],
                        "type": "1",
                        "targets": targets,
                        "section": "2",
                        "id": card["CardID"],
                        "unique_id": hero["unique_id"],
                        "action_type": "ATK"
                    }
                }

                actions.append(each)
    return actions


if __name__ == '__main__':

    print(card_actions())
