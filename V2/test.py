# import sys
# import os

# sys.path.append("E:\code\game_dt_demo\V2")


from models.player import Player

if __name__ == "__main__":
    player = Player()
    player.set_playerId(123123)
    rooms = []
    player.match_player(current_avaliable_rooms=rooms)
    data = {"heroes":[
        {"position": 1,
        "cardId":[1,2], 
        "heroId":1},
        {"position": 2,
        "cardId":[2,3], 
        "heroId":2},
    ]}
    player.set_ready_game_data(data)
    print(player.room.dict())