# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-21
descriptor: msgid 和 protocol 对照 
"""
from msgs import card_game_pb2
from hand_msgs import handle_ready_game, handle_start_game, handle_play_card, handle_start_round, handle_action_request

# 可以添加更多消息类型的描述符映射
MSGID_TO_MESSAGE = {
    # 消息ID: [消息解析proto， 消息处理方法]
    # e.g.
    # 1001: [card_game_pb2.ReadyGameRequest, handle_ready_game]
    card_game_pb2.DESCRIPTOR.message_types_by_name["ReadyGameRequest"].fields_by_name['msgId'].number:  [card_game_pb2.ReadyGameRequest,  handle_ready_game],
    card_game_pb2.DESCRIPTOR.message_types_by_name["StartGameRequest"].fields_by_name['msgId'].number:  [card_game_pb2.StartGameRequest,  handle_start_game],
    card_game_pb2.DESCRIPTOR.message_types_by_name["StartRoundRequest"].fields_by_name['msgId'].number: [card_game_pb2.StartRoundRequest, handle_start_round],
    card_game_pb2.DESCRIPTOR.message_types_by_name["PlayCardRequest"].fields_by_name['msgId'].number: [card_game_pb2.PlayCardRequest, handle_play_card],
    card_game_pb2.DESCRIPTOR.message_types_by_name["ActionRequest"].fields_by_name['msgId'].number:     [card_game_pb2.ActionRequest,     handle_action_request],
}


if __name__ == "__main__":
    # print(MSGID_TO_MESSAGE)
    parse_proto, message_handle = MSGID_TO_MESSAGE.get(1001)
