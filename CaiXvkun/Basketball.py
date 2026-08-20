# coding : utf-8
import random
import pygame
import sys

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((950, 650))
pygame.display.set_caption("蔡徐坤打篮球")
music = ['jntm1.mp3', 'jntm2.mp3', 'jntm3.mp3', 'jntm4.mp3', 'jntm5.mp3']
clock = pygame.time.Clock()
font = pygame.font.SysFont("SimHei", 50)


class CXK:
    image = pygame.image.load("cxk.png").convert_alpha()

    def __init__(self):
        self.x = 0
        self.y = 550
        self.speed = 5
        self.lmove = False
        self.rmove = False
        self.score = 0
        self.life = 3

    def move(self):
        if self.lmove:
            self.x -= self.speed
            if self.x < 0:
                self.x = 1
        if self.rmove:
            self.x += self.speed
            if self.x > 900:
                self.x = 899


class Ball:
    image = pygame.image.load("ball.png").convert_alpha()

    def __init__(self):
        self.mspeed = 1
        self.lspeed = 3
        self.restart()

    def restart(self):
        self.x = random.randint(1, 915)
        self.y = -100
        self.speed = random.randint(self.mspeed, self.lspeed)

    def move(self):
        self.y += self.speed
        if self.y > 650:
            self.restart()
            cxk.life -= 1


def checkCrash(c, w):
    return (w.x + 0.7 * w.image.get_width() > c.x and
            w.x + 0.3 * w.image.get_width() < c.x + c.image.get_width() and
            w.y + 0.7 * w.image.get_height() > c.y and
            w.y + 0.3 * w.image.get_height() < c.y + c.image.get_height())


cxk = CXK()

blist = []
for i in range(8):
    blist.append(Ball())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                cxk.lmove = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                cxk.rmove = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                cxk.lmove = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                cxk.rmove = False

    if cxk.life <= 0:
        pygame.quit()
        sys.exit()

    clock.tick(50)
    screen.fill((230, 230, 230))

    cxk.move()
    screen.blit(cxk.image, (cxk.x, cxk.y))
    for balls in blist:
        balls.move()
        screen.blit(balls.image, (balls.x, balls.y))
        if checkCrash(cxk, balls):
            pygame.mixer.music.load(random.choice(music))
            pygame.mixer.music.play()
            balls.restart()
            cxk.score += 1
            if (cxk.score % 10) == 0:
                cxk.score = 0
                cxk.life += 1
                blist.append(Ball())
    fonts = font.render(f"生命:{cxk.life}", 1, (255, 0, 0))
    screen.blit(fonts, (0, 0))
    pygame.display.update()