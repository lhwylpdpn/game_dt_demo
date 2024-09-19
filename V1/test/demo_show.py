import json
import time
import os
import pygame
import random
from PIL import Image, ImageDraw, ImageFont
from utils.config import demo_skill
from utils.config import bass_class
# 初始化 Pygame

# 棋子类
class Piece:
    def __init__(self, image_path, position,piece_type,piece_id,isboss):
        self.image = pygame.image.load(image_path)
        self.position = position
        print('棋子初始化',position)
        self.piece_type=piece_type
        self.piece_id=piece_id
        self.isboss=isboss
        self.avg_damage={}




    def move(self, new_position):
        self.position = new_position
    def set_hp(self,hp):
        self.hp=hp
        self.max_hp = hp

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def draw_boss(self,screen):
    # 创建一个新的 Surface 对象，大小和原图像一样，启用透明度
        circle_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)

        # 在新的 Surface 对象上绘制一个纯色的圆形
        pygame.draw.circle(circle_image, (255, 0, 0), (self.image.get_width() // 2, self.image.get_height() // 2), min(self.image.get_width(), self.image.get_height()) // 2)

        # 使用源图像和圆形 Surface 对象创建一个新的 Surface 对象，这个新的 Surface 对象只包含源图像中的圆形部分
        final_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        final_image.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        final_image.blit(circle_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        print(self.position)
    # 将最终的图像绘制到屏幕上
        screen.blit(final_image, self.position)



    def draw_hp_bar(self, screen,damage):
        # 计算 HP 条的宽度
        bar_width = 50
        bar_height = 5
        self.hp = self.hp-damage
        print('hp',self.hp)
        print('max_hp',self.max_hp)
        hp_ratio = self.hp / self.max_hp
        print(hp_ratio)

        # HP 条位置设置为角色位置上方
        hp_bar_x = self.position[0]
        hp_bar_y = self.position[1] - 10

        # 绘制背景和当前 HP
        pygame.draw.rect(screen, (255, 0, 0), (hp_bar_x, hp_bar_y, bar_width, bar_height))  # 背景
        pygame.draw.rect(screen, (0, 255, 0), (hp_bar_x, hp_bar_y, bar_width * hp_ratio, bar_height))
        font = pygame.font.Font(None, 24)
        damage_text = font.render(f"-{round(damage,2)}", True, (255, 0, 0))  # 红色字体
        screen.blit(damage_text, (hp_bar_x + bar_width + 5, hp_bar_y - 5))  # 在 HP 条旁边显示

    def draw_action(self, screen, action):
        font = pygame.font.Font("utils/fireflysung.ttf", 20)

        if int(action.replace('SKILL_','')) in demo_skill.values():
            action = list(demo_skill.keys())[list(demo_skill.values()).index(int(action.replace('SKILL_','')))]
        action_text = font.render(action, True, (255, 0, 0))
        #action_text居中显示

        screen.blit(action_text, (self.position[0], self.position[1]-35))
class game:
    def __init__(self,state):
        pygame.init()

        # 设置屏幕尺寸
        self.WIDTH, self.HEIGHT = 1000, 1000
        self.SCREEN_WIDTH=self.WIDTH+500
        pygame.display.set_caption("彬哥的棋盘游戏")
        self.WHITE = (255, 255, 255)
        self.state=state
    def add_color_effect(self, position):
        # 在指定位置绘制颜色，改变颜色和透明度
        color = (255, 0, 0, 128)  # 红色半透明
        pygame.draw.rect(self.overlay, color, (position[0], position[1], 50, 50))  # 根据地块大小调整
    def add_color_effect_rect_line(self, position):
        # 在指定位置绘制颜色，改变颜色和透明度
        color = (204, 0, 204, 255)  # 纯粹的黑色线
        pygame.draw.rect(self.overlay, color, (position[0], position[1], 50, 50),5)  # 根据地块大小调整

    def position_change_to_pygame(self,x, y):
        print('棋子初始化翻译前', x, y)
        x = x * self.WIDTH // self.BOARD_WIDTH
        y = (self.BOARD_HEIGHT-1-y) * self.HEIGHT // self.BOARD_HEIGHT
        print('棋子初始化翻译后',x,y)
        return (x, y)

    def update_display(self):
        #self.screen.blit(self.broad, (0, 0))  # 绘制原地图
        self.screen.blit(self.overlay, (0, 0))  # 绘制遮罩层
        pygame.display.flip()  # 更新显示
        pygame.time.delay(300)

    def game_init(self):
        self.generate_state()
        self.broad=pygame.image.load('broad.png')
        self.generate_piece()
        self.overlay = pygame.Surface(self.broad.get_size(), pygame.SRCALPHA)

    def over_state(self):
        print('游戏结束')
        for h in self.hero_piece:
            if len(h.avg_damage)>0:
                print('英雄平均伤害',h.piece_id,h.avg_damage)
            else:
                print('英雄平均伤害',h.piece_id,0,0)
        for m in self.monster_piece:
            if len(m.avg_damage)>0:
                print('怪兽平均伤害',m.piece_id,m.avg_damage)
            else:
                print('怪兽平均伤害',h.piece_id,0,0)


    def attack(self, position,selfposition):
        # 假设 position 是攻击的地块的坐标

        #self.add_color_effect_rect_line(selfposition)
        self.add_color_effect(position)
        print('攻击效果',position,selfposition)


    def run(self,json_data):


        print('开始游戏')
        all_data=json.loads(json_data)

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920, 10)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.HEIGHT),pygame.NOFRAME)
        self.screen.fill(self.WHITE)
        self.screen.blit(self.broad, (0, 0))
        font = pygame.font.Font(None, 15)

        for h in self.hero_piece:
            h.draw(self.screen)
        for m in self.monster_piece:
            m.draw(self.screen)
        pygame.display.flip()
        action_dict = {'LEFT':'向左移动', 'RIGHT':'向右移动', 'TOP':'向上移动', 'BOTTOM':'向下移动','WAIT':'待机'}
        skillid=[]
        for i in all_data['init_state']['hero']:
            for skill in all_data['init_state']['hero'][i]['skills']:
                if skill['SkillId'] not in skillid:
                    skillid.append(skill['SkillId'])
        for skill in skillid:
            action='SKILL_'+str(skill)
            action_dict[action]=list(demo_skill.keys())[list(demo_skill.values()).index(int(skill))]

        info_list=[]


        for i in all_data['update']:

            for action_num in range(len(i['action'])):
                action=i['action'][action_num]
                #todo 每个动作 做三件事：1、更新棋盘看效果 2、检查动作决策是否正确 3、检查动作带来状态变化合理性
                if action['action_type'] in action_dict.keys():
                    self.screen.fill(self.WHITE)
                    self.screen.blit(self.broad, (0, 0))
                    self.overlay.fill((0, 0, 0, 0))
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
                            if action['action_type'] == 'WAIT':
                                h.move((h.position[0], h.position[1]))
                            self.add_color_effect_rect_line(h.position)

                            #如果是SKILL_开头的动作
                            if action['action_type'].startswith('SKILL_'):
                                h.draw_action(self.screen, action['action_type'])

                                self.attack(self.position_change_to_pygame(action['atk_position'][0],action['atk_position'][2]),h.position)
                                print(str(action['id'])+"使用技能"+str(action['action_type'])+"攻击了"+str(action['atk_position'])+"位置")
                                print('完整的state变化',i['state'])
                                w=0
                                for _ in i['state']:
                                    print('逐步的变化',w,_)
                                    w+=1
                                for change in i['state'][action_num]:
                                    print('完整change',change)

                                    if change[1][2]=='position' and change[1][0]=='monster': # 特殊 带有击退怪兽效果的内容
                                        print('怪物位置变化',change)
                                        for m in self.monster_piece:
                                            if m.piece_id==change[1][1]:
                                                if str(change[1][3])=='0': #代表x变化，代表左右
                                                    p_change=change[2][1]-change[2][0]
                                                    while p_change>0:#向右移动
                                                        print('应该right',change[2])
                                                        m.move((m.position[0] + self.WIDTH // self.BOARD_WIDTH, m.position[1]))
                                                        p_change-=1
                                                    while p_change<0:#向左移动
                                                        print('应该left',change[2])
                                                        m.move((m.position[0] - self.WIDTH // self.BOARD_WIDTH, m.position[1]))
                                                        p_change+=1
                                                if str(change[1][3])=='2':#代表y变化，代表上下
                                                    p_change=change[2][1]-change[2][0]
                                                    while p_change>0:#向上移动
                                                        print('向上',change[2])
                                                        m.move((m.position[0], m.position[1] - self.HEIGHT // self.BOARD_HEIGHT))
                                                        p_change-=1
                                                    while p_change<0:#向下移动
                                                        print('向下',change[2])
                                                        m.move((m.position[0], m.position[1] + self.HEIGHT // self.BOARD_HEIGHT))
                                                        p_change+=1
                                    if change[1][2]=='Hp':
                                        print('英雄'+str(action['atk_position'])+'血量变化:',change)
                                        for m in self.monster_piece:
                                            if m.piece_id==change[1][1]:
                                                m.draw_hp_bar(self.screen,change[2][0]-change[2][1])
                                        h.avg_damage[action['action_type']]=h.avg_damage.get(action['action_type'],[])+[change[2][0]-change[2][1]]
                                        for h in self.hero_piece:#可能带有反击导致自己受伤
                                            if h.piece_id==change[1][1]:
                                                h.draw_hp_bar(self.screen,change[2][0]-change[2][1])
                            info_list.append('第'+str(i['tick'])+'tick:英雄'+str(h.piece_id)+'选择的行动:'+str(action_dict.get(action['action_type'],action['action_type'])))

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
                            if action['action_type'] == 'WAIT':
                                m.move((m.position[0], m.position[1]))
                            self.add_color_effect_rect_line(m.position)
                            #如果是SKILL_开头的动作
                            if action['action_type'].startswith('SKILL_'):
                                m.draw_action(self.screen, action['action_type'])

                                self.attack(self.position_change_to_pygame(action['atk_position'][0],action['atk_position'][2]),m.position)
                                print(str(action['id'])+"使用技能"+str(action['action_type'])+"攻击了"+str(action['atk_position'])+"位置")
                                for change in i['state'][action_num]:
                                    if change[1][2] == 'position' and change[1][0] == 'hero':
                                        print('英雄位置变化', change)
                                        for h in self.hero_piece:
                                            if h.piece_id == change[1][1]:
                                                if str(change[1][3]) == '0':
                                                    p_change = change[2][1] - change[2][0]
                                                    while p_change > 0:
                                                        h.move((h.position[0] + self.WIDTH // self.BOARD_WIDTH, h.position[1]))
                                                        p_change -= 1
                                                    while p_change < 0:
                                                        h.move((h.position[0] - self.WIDTH // self.BOARD_WIDTH, h.position[1]))
                                                        p_change += 1
                                                if str(change[1][3]) == '2':
                                                    p_change = change[2][1] - change[2][0]
                                                    while p_change > 0:
                                                        h.move((h.position[0], h.position[1] - self.HEIGHT // self.BOARD_HEIGHT))
                                                        p_change -= 1
                                                    while p_change < 0:
                                                        h.move((h.position[0], h.position[1] + self.HEIGHT // self.BOARD_HEIGHT))
                                                        p_change += 1
                                    if change[1][2]=='Hp':
                                        print('怪物'+str(action['atk_position'])+'血量变化:',change)
                                        for h in self.hero_piece:
                                            if h.piece_id==change[1][1]:
                                                h.draw_hp_bar(self.screen,change[2][0]-change[2][1])
                                        m.avg_damage[action['action_type']]=m.avg_damage.get(action['action_type'],[])+[change[2][0]-change[2][1]]
                                        for m in self.monster_piece:#可能带有反击导致自己受伤
                                            if m.piece_id==change[1][1]:
                                                m.draw_hp_bar(self.screen,change[2][0]-change[2][1])
                            info_list.append('第'+str(i['tick'])+'tick:怪物'+str(m.piece_id)+'选择的行动:'+str(action_dict.get(action['action_type'],action['action_type'])))
                    font = pygame.font.Font("utils/fireflysung.ttf", 20)
                    info_list=info_list[-15:]
                    for ii in range(len(info_list)):
                        if '英雄' in info_list[ii]:
                            text = font.render(info_list[ii], True, (0, 0, 255))
                        elif '怪物' in info_list[ii]:
                            text = font.render(info_list[ii], True, (0, 255, 0))
                        else:
                            text = font.render(info_list[ii], True, (0, 0, 0))
                        self.screen.blit(text, (self.WIDTH + 10, 40+30*ii))
                    for h in self.hero_piece:
                        if int(h.hp)>0:
                            h.draw(self.screen)
                    for m in self.monster_piece:
                        if int(m.hp)>0:
                            m.draw(self.screen)



                    self.update_display()
        font = pygame.font.Font(None, 300)
        text = font.render('game over', True, (255, 0, 0))
        self.screen.blit(text, ( 10, 200))
        self.update_display()
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


            img = Image.new('RGBA', (self.WIDTH // self.BOARD_WIDTH, self.HEIGHT // self.BOARD_HEIGHT),color=(0, 0,255, 200))
            d = ImageDraw.Draw(img)
            fnt = ImageFont.truetype('utils/fireflysung.ttf', 15)

            d.text((0, 0), "H"+str(h['HeroID']), font=fnt, fill=(255, 255, 255))

            d.text((0, 15), list(bass_class.keys())[list(bass_class.values()).index(h['BaseClassID'])], font=fnt, fill=(255, 255, 255))

            # 保存图片
            img.save('hero'+str(i)+'.png')
            self.hero_piece.append(Piece('hero'+str(i)+'.png', self.position_change_to_pygame(h['position'][0], h['position'][2]),'hero',h['HeroID'],1))#1代表不是boss
            self.hero_piece[-1].set_hp(h['Hp'])
            i += 1
        i=0
        for m in self.monster:
            if m['Quality']==2:
                img = Image.new('RGBA', (self.WIDTH // self.BOARD_WIDTH, self.HEIGHT // self.BOARD_HEIGHT),
                                color=(255, 255, 255, 0))
            else:
                img = Image.new('RGBA', (self.WIDTH // self.BOARD_WIDTH, self.HEIGHT // self.BOARD_HEIGHT),color=(0, 255, 0, 200))
            d = ImageDraw.Draw(img)
            fnt = ImageFont.truetype('utils/fireflysung.ttf', 15)
            if m['Quality']==2:
                d.ellipse([(0, 0), img.size], fill=(255, 0,0 ,200))

            d.text((0, 0), "M"+str(m['HeroID']), font=fnt, fill=(0, 0, 0))
            d.text((0, 15), list(bass_class.keys())[list(bass_class.values()).index(m['BaseClassID'])] , font=fnt, fill=(0, 0, 0))

            img.save('monster'+str(i)+'.png')
            self.monster_piece.append(Piece('monster'+str(i)+'.png', self.position_change_to_pygame(m['position'][0], m['position'][2]),'monster',m['HeroID'],m['Quality']))
            self.monster_piece[-1].set_hp(m['Hp'])
            i += 1
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

        color_map = {}
        for i in range(21):
            color_map[i] = ( 255 - i * 10, 255 - i * 10, 255 - i * 10)

        # 生成一张按照宽高格子生成的棋盘地图，类似国际象棋，不需要颜色直接是网格图就行
        broad_picture = pygame.Surface((self.WIDTH, self.HEIGHT))
        broad_picture.fill(self.WHITE)
        font = pygame.font.Font(None, 18)
        for i in range(self.BOARD_WIDTH):
            for j in range(self.BOARD_HEIGHT):
                # 我希望棋盘上有BOARD_WIDTH*BOARD_HEIGHT个格子，每个格子的宽度和高度都是WIDTH/BOARD_WIDTH和HEIGHT/BOARD_HEIGHT


                for p in self.map:

                    block=self.map[p]['Block']

                    if i==p[0] and j==p[2] and block==1:
                        color = color_map.get(p[1], (0, 0, 0))  # 如果 p[1] 的值不在 color_map 中，使用黑色
                        rect = pygame.Rect(i * self.WIDTH // self.BOARD_WIDTH, (self.BOARD_HEIGHT-1-j) * self.HEIGHT // self.BOARD_HEIGHT,
                                           self.WIDTH // self.BOARD_WIDTH,
                                           self.HEIGHT // self.BOARD_HEIGHT)

                        pygame.draw.rect(broad_picture, color, rect)
                        # text = font.render(f'{p[1]}', True, (0, 0, 0))
                        # text_rect = text.get_rect(center=rect.center)
                        text = font.render(f'({p[0]},{p[1]},{p[2]})', True, (0, 0, 0))
                        text_rect = text.get_rect(center=rect.center)
                        broad_picture.blit(text, text_rect)


        pygame.image.save(broad_picture, 'broad.png')



if __name__ == '__main__':
    #generate_state()
    #test_main()

    bass_class = {}
    bass_class['战士'] = 1
    bass_class['弓箭手'] = 2
    k=1
    #取到bass_class的k对应的key
    print(list(bass_class.keys())[list(bass_class.values()).index(k)])
    #测试下
