# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-21
descriptor: msgid 和 protocol 对照 
"""
import card_game_pb2

# 可以添加更多消息类型的描述符映射
msgid_to_message = {
    # e.g.
    # login_pb2.DESCRIPTOR.message_types_by_name['CSPlayerLogin'].fields_by_name['msgid'].number:  login_pb2.CSPlayerLogin,
    # login_pb2.DESCRIPTOR.message_types_by_name['SCLoginSuccess'].fields_by_name['msgid'].number: login_pb2.SCLoginSuccess,
    card_game_pb2.DESCRIPTOR.message_types_by_name["ReadyGameRequest"].fields_by_name['msgId'].number: [card_game_pb2.ReadyGameRequest],
    card_game_pb2.DESCRIPTOR.message_types_by_name["ReadyGameResponse"].fields_by_name['msgId'].number: card_game_pb2.ReadyGameResponse,
}


if __name__ == "__main__":
    print(msgid_to_message)