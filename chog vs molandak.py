import pygame
import sys
import os
from pygame.locals import *
from random import randint

# 初始化 Pygame
pygame.init()

# 设置图片资源路径
image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image')  # 获取image文件夹的路径

# 加载背景图片
bg = pygame.image.load(os.path.join(image_dir, 'place.png'))
bg_position = bg.get_rect()

# 设置窗口大小
size = width, height = 1000, 570
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Gmolandak！')

# 设置字体
font = pygame.font.Font(None, 36)

def main():
    class Chog(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            position = 100, 100
            self.image = pygame.image.load(os.path.join(image_dir, 'chog.png'))
            self.rect = self.image.get_rect()
            self.rect.center = position

        def move_left(self):
            self.speed = [-5, 0]
            if self.rect.left <= 0:
                self.rect.left = 0
            else:
                self.rect = self.rect.move(self.speed)

        def move_right(self):
            self.speed = [5, 0]
            if self.rect.right >= 1000:
                self.rect.right = 1000
            else:
                self.rect = self.rect.move(self.speed)

        def move_up(self):
            self.speed = [0, -5]
            if self.rect.top <= 0:
                self.rect.top = 0
            else:
                self.rect = self.rect.move(self.speed)

        def move_down(self):
            self.speed = [0, 5]
            if self.rect.bottom >= 570:
                self.rect.bottom = 570
            else:
                self.rect = self.rect.move(self.speed)

    class Mola(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            y = randint(0, 570)
            position = [1000, y]

            self.image = pygame.image.load(os.path.join(image_dir, 'molandak.png'))
            self.rect = self.image.get_rect()
            self.rect.center = position

            self.speed = [-4, 0]

        def move(self):
            self.rect = self.rect.move(self.speed)

    chog = Chog()

    i = 0
    group = pygame.sprite.Group()

    state = True
    score = 0

    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            chog.move_left()
        if key[K_RIGHT]:
            chog.move_right()
        if key[K_UP]:
           chog.move_up()
        if key[K_DOWN]:
            chog.move_down()

        screen.blit(bg, bg_position)
        screen.blit(chog.image, chog.rect)

        i = i + 1
        if i % 10 == 0:
            mola = Mola()
            group.add(mola)

        for p in group.sprites():
            p.move()
            screen.blit(p.image, p.rect)
            if pygame.sprite.collide_mask(chog, p):
                state = False
                pause(score)

        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        text_rect = score_text.get_rect(topright=(width - 10, 10))
        screen.blit(score_text, text_rect)

        score += 1

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def pause(score):
    bg_go = pygame.image.load(os.path.join(image_dir, 'start.png'))
    bg_go_pos = bg_go.get_rect()
    size = width, height = 1000, 570
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('GameOver!')

    score_text = font.render(f'Final Score: {score}', True, (255, 0, 0))
    score_rect = score_text.get_rect(center=(width // 2, height // 2 - 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        img_src = pygame.image.load(os.path.join(image_dir, 'restart.png'))
        img_src_pos = img_src.get_rect(center=(width // 2, height // 2 + 50))  # Center the button

        # Detect mouse click
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if img_src_pos.collidepoint(mouse_pos):
            img_src = pygame.image.load(os.path.join(image_dir, 'restart2.png'))
            if mouse_press[0]:
                main()

        screen.blit(bg_go, bg_go_pos)
        screen.blit(img_src, img_src_pos)
        screen.blit(score_text, score_rect)
        pygame.display.flip()

main()
