import asyncio
import struct

import websockets
from msgs import card_game_pb2

async def connect1():
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
        print("connect1: ReadyGameRequest 消息已发送")

        # 接收并处理 ReadyGameResponse
        response = await websocket.recv()
        msgid_received = struct.unpack("<I", response[:4])[0]  # 读取 msgid

        pb_response = response[12:]  # 读取 Protobuf 数据部分

        if msgid_received == 1002:
            response_obj = card_game_pb2.ReadyGameResponse()
            response_obj.ParseFromString(pb_response)
            print(f"connect1: Parsed Response: roomId={response_obj.roomId}, result={response_obj.result}")
        else:
            print(f"connect1: Unknown msgid: {msgid_received}")


        # 接收并处理 StartGameResponse
        response = await websocket.recv()
        msgid_received = struct.unpack("<I", response[:4])[0]  # 读取 msgid

        if msgid_received == 1003:
            response_obj = card_game_pb2.StartGameRequest()
            pb_response = response[12:]
            response_obj.ParseFromString(pb_response)
            print(f"connect1: 收到 StartGameResponse: {response_obj.roomId, response_obj.change}")
        else:
            print(f"connect1: Unknown msgid: {msgid_received}")


async def connect2():
    uri = "ws://localhost:17090"  # 连接到本地 WebSocket 服务
    async with websockets.connect(uri) as websocket:
        # 构建 ReadyGameRequest 消息
        request = card_game_pb2.ReadyGameRequest()
        request.msgId = 1001
        request.mapId = 1
        hero = request.heroes.add()
        hero.position = 1
        hero.heroId = 2
        hero.cardId.append(2)
        msg_id = 1001
        player_id = 10000001
        serialized_request = request.SerializeToString()
        message = struct.pack("<I", msg_id) + struct.pack("<Q", player_id) + serialized_request

        # 发送消息
        await websocket.send(message)
        print("connect2: ReadyGameRequest 消息已发送")

        # 接收并处理 ReadyGameResponse
        response = await websocket.recv()
        msgid_received = struct.unpack("<I", response[:4])[0]  # 读取 msgid

        pb_response = response[12:]  # 读取 Protobuf 数据部分

        if msgid_received == 1002:
            response_obj = card_game_pb2.ReadyGameResponse()
            response_obj.ParseFromString(pb_response)
            print(f"connect2: Parsed Response: roomId={response_obj.roomId}, result={response_obj.result}")
        else:
            print(f"connect2: Unknown msgid: {msgid_received}")


        # 接收并处理 StartGameResponse
        response = await websocket.recv()
        msgid_received = struct.unpack("<I", response[:4])[0]  # 读取 msgid

        if msgid_received == 1003:
            response_obj = card_game_pb2.StartGameRequest()
            pb_response = response[12:]
            response_obj.ParseFromString(pb_response)
            print(f"connect2: 收到 StartGameResponse: {response_obj.roomId, response_obj.change}")
        else:
            print(f"connect2: Unknown msgid: {msgid_received}")

async def main():
    # 创建并运行两个客户端
    await asyncio.gather(connect1(), connect2())

# 运行主程序
asyncio.run(main())