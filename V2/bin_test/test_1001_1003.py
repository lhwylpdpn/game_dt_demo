import asyncio
import struct

import websockets
from msgs import card_game_pb2

async def connect():
    uri = "ws://localhost:17090"  # 连接到本地 WebSocket 服务
    async with websockets.connect(uri) as websocket:
        # 构建 ReadyGameRequest 消息
        request = card_game_pb2.ReadyGameRequest()
        request.msgId = 1001
        request.mapId = 1
        hero = request.heroes.add()
        hero.position = 1
        hero.heroId = 1
        hero.cardId.append(1)
        msg_id = 1001
        player_id = 10000000
        serialized_request = request.SerializeToString()
        message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_request

        # 发送消息
        await websocket.send(message)
        print("ReadyGameRequest 消息已发送")

        # 接收并处理 ReadyGameResponse
        response = await websocket.recv()
        msgid_received = struct.unpack("<I", response[:4])[0]  # 读取 msgid

        pb_response = response[12:]  # 读取 Protobuf 数据部分

        if msgid_received == 1002:
            response_obj = card_game_pb2.ReadyGameResponse()
            response_obj.ParseFromString(pb_response)
            print(f"Parsed Response: roomId={response_obj.roomId}, result={response_obj.result}")
        else:
            print(f"Unknown msgid: {msgid_received}")


        # 接收并处理 StartGameResponse
        response = await websocket.recv()
        msgid_received = struct.unpack("<I", response[:4])[0]  # 读取 msgid

        if msgid_received == 1003:
            response_obj = card_game_pb2.StartGameRequest()
            pb_response = response[12:]
            response_obj.ParseFromString(pb_response)
            print(f"收到 StartGameResponse: {response_obj.roomId, response_obj.ownChange}")
        else:
            print(f"Unknown msgid: {msgid_received}")

        # start_game_response_data = await websocket.recv()
        # start_game_response = card_game_pb2.StartGameResponse()
        # start_game_response.ParseFromString(start_game_response_data)

# 运行客户端
asyncio.run(connect())
