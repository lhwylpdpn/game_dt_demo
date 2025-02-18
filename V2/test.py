import sys
import os

sys.path.append("E:\code\game_dt_demo\V2")


from models.player import Player
from hand_msgs import card_actions


def test_player1():
    player = Player(None)
    player.set_playerId(1000001)
    rooms = []
    player.match_player(current_avaliable_rooms=rooms)
    data = {
      'mapId': 1,
      'heroes': [
        {
          'position': 1,
          'cardId': [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1],
          'heroId': 1
        },
        {
          'position': 2,
          'cardId': [
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2],
          'heroId': 2
        },
        {
          'position': 3,
          'cardId': [
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3],
          'heroId': 3
        }]
    }    
    player.set_ready_game_data(data)
    return player

def test_plarer2(test_room):
    player = Player(None)
    player.set_playerId(1000002)
    player.match_player(current_avaliable_rooms=[test_room])
    data = {
      'mapId': 1,
      'heroes': [
        {
          'position': 1,
          'cardId': [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1],
          'heroId': 1
        },
        {
          'position': 2,
          'cardId': [
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2],
          'heroId': 2
        },
        {
          'position': 3,
          'cardId': [
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3],
          'heroId': 3
        }]
    }
    player.set_ready_game_data(data)
    return player


if __name__ == "__main__":
    
    player_1 = test_player1()
    player_2 = test_plarer2(player_1.room)
    player_1.room.init_game()
    
    p_1_h = player_1.get_my_heros()[0]
    p_1_card = player_1.get_my_cards()[0]
    player_1.set_show_cards(
        {"change":[ {
        'cardUniqueId': p_1_card.unique_id,
        'releasePosition': {
          'x': 8.0,
          'y': 1.0,
          'z': 5.0
        },
        'targetType': 'hero',
        'heroUniqueId': p_1_h.unique_id,
        'cardId': 1
      }]
    })
    
    p_2_h = player_2.get_my_heros()[0]
    p_2_card = player_2.get_my_cards()[0]
    player_2.set_show_cards(
        {"change":[ {
        'cardUniqueId': p_2_card.unique_id,
        'releasePosition': {
          'x': 1.0,
          'y': 1.0,
          'z': 3.0
        },
        'targetType': 'hero',
        'heroUniqueId': p_2_h.unique_id,
        'cardId': 2
      }]
    })
    
    actions = card_actions(player_1.room)
    class clinet():
        pass
    
    def test_hand(*args):
        print(args)
        pass
    cli = clinet()
    cli.player = player_1
    player_1.room.game.single_run(test_hand, cli, actions)

    # print(player.room.game)
    # print(player.room.dict())
    # player.room.topic_manager.publish(player.room.room_id, "welcome")


# from twisted.internet import reactor
# from collections import defaultdict

# # 主题管理器类
# class TopicManager:
#     def __init__(self):
#         # 存储每个主题的订阅者列表
#         self.subscribers = defaultdict(list)
        
#     def subscribe(self, topic, subscriber):
#         # 将订阅者添加到指定主题的订阅者列表中
#         self.subscribers[topic].append(subscriber)
        
#     def unsubscribe(self, topic, subscriber):
#         # 从指定主题的订阅者列表中移除订阅者
#         if subscriber in self.subscribers[topic]:
#             self.subscribers[topic].remove(subscriber)
            
#     def publish(self, topic, message):
#         # 将消息发布到指定主题的所有订阅者
#         for subscriber in self.subscribers[topic]:
#             subscriber.receive_message(topic, message)

# # 订阅者类
# class Subscriber:
    
#     def __init__(self, name):
#         self.name = name
        
#     def receive_message(self, topic, message):
#         print(f"{self.name} 收到来自主题 {topic} 的消息: {message}")

# # 发布者类
# class Publisher:
#     def __init__(self, topic_manager):
#         self.topic_manager = topic_manager
#     def publish_message(self, topic, message):
#         # 调用主题管理器的发布方法
#         self.topic_manager.publish(topic, message)

# def main():
#     # 创建主题管理器
#     topic_manager = TopicManager()
#     # 创建订阅者
#     subscriber1 = Subscriber("订阅者1")
#     subscriber2 = Subscriber("订阅者2")
#     # 订阅主题
#     topic_manager.subscribe("主题1", subscriber1)
#     topic_manager.subscribe("主题1", subscriber2)
#     topic_manager.subscribe("主题2", subscriber2)
#     # 创建发布者
#     publisher = Publisher(topic_manager)
#     # 发布消息
#     publisher.publish_message("主题1", "这是主题1的消息")
#     publisher.publish_message("主题2", "这是主题2的消息")
#     # 停止事件循环
#     reactor.stop()

# if __name__ == "__main__":
#     # 启动事件循环
#     reactor.callWhenRunning(main)
#     reactor.run()