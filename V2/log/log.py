# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/15 18:29
import json
import os
from datetime import datetime
import uuid
class LogManager:
    def __init__(self, file_name= ''.join(str(uuid.uuid4()).split('-')) + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + "logs.json"):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_directory, file_name)
        print(self.file_path)
        self.counter=0

    def add_log(self, log_data):
        self.counter+=1
        # 获取当前时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + "_{}".format(self.counter)
        # 构造要记录的数据
        log_entry = {timestamp: log_data}
        # 将日志记录到文件中
        # self._write_log(log_entry)
        return timestamp

    def _write_log(self, log_entry):

        try:
            # 读取现有日志数据
            with open(self.file_path, "r") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = {}

        # 更新日志数据
        logs.update(log_entry)

        # 写回文件
        with open(self.file_path, "w") as file:
            json.dump(logs, file, ensure_ascii=False,indent=4)

    def get_log(self, timestamp):
        try:
            # 读取日志文件
            with open(self.file_path, "r") as file:
                logs = json.load(file)
            # 根据时间戳获取对应的日志信息
            return logs.get(timestamp, "Log not found")
        except (FileNotFoundError, json.JSONDecodeError):
            return "Log file not found or is corrupted"


# 示例使用
log_manager = LogManager()
# #
# # # 添加日志，直接传入一个字典
# log_manager.add_log(str({"event": "start", "status": "success", "details": "Initial setup completed"}))
# log_manager.add_log({"event": "process", "status": "running", "details": "Process running smoothly"})
# #
# # 获取日志
# timestamp_to_query = list(json.load(open("logs.json")).keys())[0]  # 获取第一个时间戳
# log = log_manager.get_log(timestamp_to_query)
#
# print(f"Log at {timestamp_to_query}: {log}")