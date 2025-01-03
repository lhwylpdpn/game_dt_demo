from twisted.internet import reactor, endpoints
from twisted.web import server, resource
from twisted.python import log
import random
import json
import sys
log.startLogging(sys.stdout)


class RoomResource(resource.Resource):
    isLeaf = True  # 标记为叶子资源，直接处理请求

    def __init__(self):
        self.clients = []
        self.client_states = {}  # 存储客户端状态，用于判断是否准备好

    def render_POST(self, request):
        print("Received POST request")
        sys.stdout.flush()  # 立即刷新输出缓冲区
        try:
            data = json.loads(request.content.read())
            action = data.get("action")
            timestamp = data.get("timestamp", None)  # 获取请求的时间戳，如果没有则为 None
            client_addr = data.get("client_id", None)

            if client_addr not in self.client_states:
                self.client_states[client_addr] = {"ready": False, "timestamp": None}  # 初始化客户端状态

            if action == "enter":
                self.clients.append(request)
                print(f"Client {client_addr} entered room at timestamp {timestamp}")
                return json.dumps({"status": "ok"}).encode()
            elif action == "ready":
                self.client_states[client_addr]["ready"] = True
                self.client_states[client_addr]["timestamp"] = timestamp
                print(f"Client {client_addr} is ready at timestamp {timestamp}")
                if all(client["ready"] for client in self.client_states.values()) and len(self.client_states) == 2:
                    self.start_game()
                return json.dumps({"status": "ok"}).encode()
        except Exception as e:
            print(f"Error: {e}")
            return json.dumps({"status": "error"}).encode()

    def start_game(self):
        print("Game starting!")
        sorted_clients = sorted(self.client_states.items(), key=lambda x: x[1]["timestamp"])  # 按时间戳排序客户端
        for client_addr, _ in sorted_clients:
            for client in self.clients:
                if client.getClientAddress().host == client_addr:
                    client.write(json.dumps({"message": "Game started!"}).encode())
                    client.finish()  # 关闭连接
        self.clients = []
        self.client_states = {}


root = resource.Resource()
root.putChild(b"room", RoomResource())  # 路径为 /room
site = server.Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
endpoint.listen(site)
print("Server started on port 8000")
reactor.run()