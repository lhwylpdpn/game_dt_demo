import time

import pygame
import random
from PIL import Image, ImageDraw, ImageFont
# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
WIDTH, HEIGHT = 600, 600
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("彬哥的棋盘游戏")

# 颜色定义
WHITE = (255, 255, 255)
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

# 棋子类
class Piece:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def draw(self, screen):
        screen.blit(self.image, self.position)


def test_main():
    broad=pygame.image.load('broad.png')
    hero = Piece('libin.png', (0, 0))  # 替换为实际的图像路径
    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 清屏


        screen.fill(WHITE)

        screen.blit(broad, (0, 0))
        # 随机移动棋子
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
        dx, dy = random.choice(directions)
        #每次移动一个格子
        new_x, new_y = hero.position[0] + dx * WIDTH // BOARD_WIDTH, hero.position[1] + dy * HEIGHT // BOARD_HEIGHT



        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            hero.move((new_x, new_y))

        # 绘制棋子
        hero.draw(screen)

        # 更新显示
        pygame.display.flip()
        pygame.time.delay(500)

    # 退出 Pygame
    pygame.quit()

def generate_state(state):
    map=state['map'].dict()
    hero=[i.dict() for i in state['hero']]
    monster=[i.dict() for i in state['monster']]

    # 创建一个新的白色图片,创建个透明底色的图片
    img = Image.new('RGBA', (WIDTH // BOARD_WIDTH, HEIGHT // BOARD_HEIGHT), color=(0, 0, 0, 0))
    # 创建一个可以在图片上绘制的对象
    d = ImageDraw.Draw(img)
    # 创建一个字体对象
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 22)
    # 在图片上绘制文本
    d.text((10, 15), "libin", font=fnt, fill=(0, 0, 0))
    # 保存图片
    img.save('libin.png')



    for position in map:
        p=position['position']
        print(p)
    print('--------')
    for k in map_bin:
        print(k)



    # 生成一张按照宽高格子生成的棋盘地图，类似国际象棋，不需要颜色直接是网格图就行
    broad_picture = pygame.Surface((WIDTH, HEIGHT))
    broad_picture.fill(WHITE)
    font = pygame.font.Font(None, 12)
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            # 我希望棋盘上有BOARD_WIDTH*BOARD_HEIGHT个格子，每个格子的宽度和高度都是WIDTH/BOARD_WIDTH和HEIGHT/BOARD_HEIGHT
            color = (0, 0, 0)
            rect = pygame.Rect(i * WIDTH // BOARD_WIDTH, j * HEIGHT // BOARD_HEIGHT, WIDTH // BOARD_WIDTH,
                               HEIGHT // BOARD_HEIGHT)

            pygame.draw.rect(broad_picture, color, rect, 1)

            text = font.render(f'{i},{j}', True, (0,0,0))
            text_rect = text.get_rect(center=rect.center)
            broad_picture.blit(text,text_rect)

    pygame.image.save(broad_picture, 'broad.png')



if __name__ == '__main__':
    generate_state()
    #test_main()