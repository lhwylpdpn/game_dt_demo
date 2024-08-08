import pygame

# 初始化 Pygame
pygame.init()

# 设置参数
WIDTH, HEIGHT = 600, 600
BOARD_WIDTH, BOARD_HEIGHT = 8, 8

# 创建表面
broad_picture = pygame.Surface((WIDTH, HEIGHT))
broad_picture.fill((255, 255, 255))  # 填充背景

# 设置字体
font = pygame.font.Font(None, 36)

# 绘制棋盘
for i in range(BOARD_WIDTH):
    for j in range(BOARD_HEIGHT):
        color = (0, 0, 0)
        rect = pygame.Rect(i * WIDTH // BOARD_WIDTH, j * HEIGHT // BOARD_HEIGHT,
                           WIDTH // BOARD_WIDTH, HEIGHT // BOARD_HEIGHT)

        pygame.draw.rect(broad_picture, color, rect, 1)

        # 绘制坐标
        text = font.render(f'{i},{j}', True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)

        # 调整文本位置，稍微向下或者向右偏移
        text_rect.y += 3  # 调整Y坐标

        broad_picture.blit(text, text_rect)

# 保存图像
pygame.image.save(broad_picture, 'broad.png')

# 清理
pygame.quit()