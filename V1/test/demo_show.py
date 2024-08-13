import json
import time

import pygame
import random
from PIL import Image, ImageDraw, ImageFont
# 初始化 Pygame

import textwrap



# 棋子类
class Piece:
    def __init__(self, image_path, position,piece_type,piece_id):
        self.image = pygame.image.load(image_path)
        self.position = position
        print('棋子初始化',position)
        self.piece_type=piece_type
        self.piece_id=piece_id

    def move(self, new_position):
        self.position = new_position

    def draw(self, screen):
        screen.blit(self.image, self.position)

class game:
    def __init__(self,state):
        pygame.init()

        # 设置屏幕尺寸
        self.WIDTH, self.HEIGHT = 1000, 1000
        self.SCREEN_WIDTH=self.WIDTH+500
        pygame.display.set_caption("彬哥的棋盘游戏")
        self.WHITE = (255, 255, 255)
        self.state=state

    def position_change_to_pygame(self,x, y):
        print('棋子初始化翻译前', x, y)
        x = x * self.WIDTH // self.BOARD_WIDTH
        y = y * self.HEIGHT // self.BOARD_HEIGHT
        print('棋子初始化翻译后',x,y)
        return (x, y)
    def game_init(self):
        self.generate_state()
        self.broad=pygame.image.load('broad.png')
        self.generate_piece()
    def run(self,json_data):


        print('开始游戏')
        all_data=json.loads(json_data)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.HEIGHT))
        self.screen.fill(self.WHITE)
        self.screen.blit(self.broad, (0, 0))
        font = pygame.font.Font(None, 15)

        for h in self.hero_piece:
            h.draw(self.screen)
        for m in self.monster_piece:
            m.draw(self.screen)
        pygame.display.flip()
        action_dict = {'LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'SKILL'}
        skillid=[]
        for i in all_data['init_state']['hero']:
            for skill in all_data['init_state']['hero'][i]['skills']:
                if skill['SkillId'] not in skillid:
                    skillid.append(skill['SkillId'])
        for skill in skillid:
            action_dict.add('SKILL_'+str(skill))

        for i in all_data['update']:
            for action in i['action']:
                #print('action',action['action_type'],action['class'],action['id'],i['state'])

                #todo 每个动作 做三件事：1、更新棋盘看效果 2、检查动作决策是否正确 3、检查动作带来状态变化合理性
                if action['action_type'] in action_dict:
                    self.screen.fill(self.WHITE)
                    self.screen.blit(self.broad, (0, 0))

                    for h in self.hero_piece:
                        if h.piece_id==action['id']:

                            if action['action_type'] == 'LEFT':
                                h.move((h.position[0] - self.WIDTH // self.BOARD_WIDTH, h.position[1]))
                            if action['action_type'] == 'RIGHT':
                                h.move((h.position[0] + self.WIDTH // self.BOARD_WIDTH, h.position[1]))
                            if action['action_type'] == 'TOP':
                                h.move((h.position[0], h.position[1] - self.HEIGHT // self.BOARD_HEIGHT))
                            if action['action_type'] == 'BOTTOM':
                                h.move((h.position[0], h.position[1] + self.HEIGHT // self.BOARD_HEIGHT))
                            text = font.render('state info :', True, (0, 0, 0))
                            self.screen.blit(text, (self.WIDTH + 10, 10))
                            text=font.render('hero'+str(h.piece_id)+'action:'+str(action), True, (0, 0, 0))
                            self.screen.blit(text, (self.WIDTH + 10, 40))
                    for m in self.monster_piece:
                        if m.piece_id==action['id']:
                            if action['action_type'] == 'LEFT':
                                m.move((m.position[0] - self.WIDTH // self.BOARD_WIDTH, m.position[1]))
                            if action['action_type'] == 'RIGHT':
                                m.move((m.position[0] + self.WIDTH // self.BOARD_WIDTH, m.position[1]))
                            if action['action_type'] == 'TOP':
                                m.move((m.position[0], m.position[1] - self.HEIGHT // self.BOARD_HEIGHT))
                            if action['action_type'] == 'BOTTOM':
                                m.move((m.position[0], m.position[1] + self.HEIGHT // self.BOARD_HEIGHT))
                            text = font.render('state info :', True, (0, 0, 0))
                            self.screen.blit(text, (self.WIDTH + 10, 10))
                            text=font.render('monster'+str(m.piece_id)+'action:'+str(action), True, (0, 0, 0))
                            self.screen.blit(text, (self.WIDTH + 10, 40))

                    for h in self.hero_piece:
                        h.draw(self.screen)
                    for m in self.monster_piece:
                        m.draw(self.screen)



                    pygame.display.flip()
                    pygame.time.delay(1500)

                # #2 不好处理  3 todo 先打印状态到棋盘旁边看看
                # for state in i['state']:
                #     for change in state:
                #             print('change',change[1],change[2])








        # running = True
        # while running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #
        #     self.screen.fill(self.WHITE)
        #     self.screen.blit(self.broad, (0, 0))
        #     for h in self.hero_piece:
        #         h.draw(self.screen)
        #     for m in self.monster_piece:
        #         m.draw(self.screen)
        #
        #     pygame.display.flip()
        #     # 随机移动棋子
        #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
        #     dx, dy = random.choice(directions)
        #     #每次移动一个格子
        #     new_x, new_y = self.hero0.position[0] + dx * self.WIDTH // self.BOARD_WIDTH, self.hero0.position[1] + dy * self.HEIGHT // self.BOARD_HEIGHT
        #
        #
        #
        #     if 0 <= new_x < self.WIDTH and 0 <= new_y < self.HEIGHT:
        #         self.hero0.move((new_x, new_y))
        #
        #     # 绘制棋子
        #     self.hero0.draw(self.screen)
        #
        #     # 更新显示
        #     pygame.display.flip()
        #     pygame.time.delay(500)
        #
        # # 退出 Pygame
        # pygame.quit()

    def generate_piece(self):
        self.hero = [i.dict(for_view=True) for i in self.state['hero']]
        self.monster = [i.dict(for_view=True) for i in self.state['monster']]
        i=0
        self.hero_piece=[]
        self.monster_piece=[]
        for h in self.hero:
            img = Image.new('RGBA', (self.WIDTH // self.BOARD_WIDTH, self.HEIGHT // self.BOARD_HEIGHT),color=(0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 17)
            d.text((0, 0), "H"+str(h['HeroID']), font=fnt, fill=(0, 0, 0))
            # 保存图片
            img.save('hero'+str(i)+'.png')
            self.hero_piece.append(Piece('hero'+str(i)+'.png', self.position_change_to_pygame(h['position'][0], h['position'][2]),'hero',h['HeroID']))
            i += 1
        i=0
        for m in self.monster:
            img = Image.new('RGBA', (self.WIDTH // self.BOARD_WIDTH, self.HEIGHT // self.BOARD_HEIGHT),color=(0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 17)
            d.text((0, 0), "M"+str(m['HeroID']), font=fnt, fill=(0, 0, 0))
            # 保存图片
            img.save('monster'+str(i)+'.png')
            self.monster_piece.append(Piece('monster'+str(i)+'.png', self.position_change_to_pygame(m['position'][0], m['position'][2]),'monster',m['HeroID']))
    def generate_state(self):
        self.map=self.state['map'].view_from_y_dict()

        x, y, z = 0, 0, 0

        for p in self.map:

            if p[0] > x:
                x = p[0]
            if p[2] > y:
                y = p[2]
            if p[1] > z:
                z = p[1]
        self.BOARD_WIDTH = x+1
        self.BOARD_HEIGHT = y+1

        print(self.BOARD_WIDTH,self.BOARD_HEIGHT)
        # 创建一个新的白色图片,创建个透明底色的图片


        # 生成一张按照宽高格子生成的棋盘地图，类似国际象棋，不需要颜色直接是网格图就行
        broad_picture = pygame.Surface((self.WIDTH, self.HEIGHT))
        broad_picture.fill(self.WHITE)
        font = pygame.font.Font(None, 18)
        for i in range(self.BOARD_WIDTH):
            for j in range(self.BOARD_HEIGHT):
                # 我希望棋盘上有BOARD_WIDTH*BOARD_HEIGHT个格子，每个格子的宽度和高度都是WIDTH/BOARD_WIDTH和HEIGHT/BOARD_HEIGHT
                color = (0, 0, 0)
                rect = pygame.Rect(i * self.WIDTH // self.BOARD_WIDTH, j * self.HEIGHT // self.BOARD_HEIGHT, self.WIDTH // self.BOARD_WIDTH,
                                   self.HEIGHT // self.BOARD_HEIGHT)

                pygame.draw.rect(broad_picture, color, rect, 1)

                for p in self.map:

                    block=self.map[p]['Block']

                    if i==p[0] and j==p[2] and block==1:

                        # text = font.render(f'{p[1]}', True, (0, 0, 0))
                        # text_rect = text.get_rect(center=rect.center)
                        text = font.render(f'({p[0]},{p[1]},{p[2]})', True, (0, 0, 0))
                        text_rect = text.get_rect(center=rect.center)
                        broad_picture.blit(text, text_rect)


        pygame.image.save(broad_picture, 'broad.png')



if __name__ == '__main__':
    #generate_state()
    #test_main()

    t={'0':{'t':3}}
    print(t[str(0)])