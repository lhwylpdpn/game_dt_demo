import login_pb2
from google.protobuf import any_pb2

a = login_pb2.CSPlayerLogin()
# -----
a.msgid = 1001
a.deviceOSVersion = "test"
# a_string = a.SerializeToString()      # 序列化, 服务器和client直接传递的就是这个消息

# 使用Any来封装a消息
any_a = any_pb2.Any()
any_a.Pack(a)
string_a = any_a.SerializeToString()
# ------
  #  网络传递过来
  # 获取消息的全名

# print(f"Message type: {message_type}")
unpacked_a = any_pb2.Any().Unpack(string_a)
print(unpacked_a) 
# -------
# b = login_pb2.CSPlayerLogin()
# b.ParseFromString(a_string) # 反列化
# print(b) 


