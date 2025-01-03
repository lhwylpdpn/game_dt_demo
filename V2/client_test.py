import subprocess
import json
import time


def send_request(action):
    timestamp = time.time()  # 生成时间戳
    url = "http://127.0.0.1:8000/room"
    data = json.dumps({"action": action, "timestamp": timestamp,'client_id':44})

    # 使用 subprocess 调用 curl
    result = subprocess.run(
        ["curl", "-X", "POST", url, "-H", "Content-Type: application/json", "-d", data],
        capture_output=True, text=True
    )

    # 打印输出和错误
    # print("Response:", result.stdout)
    # if result.stderr:
    #     print("Error:", result.stderr)

    # 处理服务器响应
    try:
        response_data = json.loads(result.stdout)
        # 根据具体的响应内容进行处理
        if response_data.get("message") == "Game started!":
            print("The game has started!")
        else:
            print("Received:", response_data)
    except json.JSONDecodeError:
        print("Failed to decode JSON response")


# 示例：先发送 enter 动作，然后在不同时间发送 ready 动作
send_request("enter")
time.sleep(2)  # 等待2秒
send_request("ready")  # 发送 ready 动作
time.sleep(5)
send_request("ready")  # 发送 ready 动作