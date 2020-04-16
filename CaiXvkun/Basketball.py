# coding : utf-8
import random
import pygame
import sys
import time
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((950,650))
pygame.display.set_caption("蔡徐坤打篮球")
music = ['jntm1.mp3','jntm2.mp3','jntm3.mp3','jntm4.mp3','jntm5.mp3']
clock = pygame.time.Clock()
font = pygame.font.SysFont("SimHei",50)

class CXK:
    def __init__(self):
        self.x = 0
        self.y = 550
        self.image = pygame.image.load("cxk.png").convert_alpha()
        self.speed = 5
        self.lmove = False
        self.rmove = False
        self.score = 0
        self.life = 2000000000000000

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
    def restart(self):
        self.active = False
        self.x = random.randint(1,915)
        self.y = -100
        self.speed = random.randint(self.mspeed,self.lspeed)


    def __init__(self):
        self.x = random.randint(1,915)
        self.y = -100
        self.mspeed = 1
        self.lspeed = 3
        self.speed = random.randint(self.mspeed,self.lspeed)
        self.image = pygame.image.load("ball.png").convert_alpha()
        self.active = False

    def move(self):
        if self.active:
            self.y += self.speed
            if self.y > 650:
                self.restart()
                cxk.life -= 1



def checkCrash(c, w):
    if (w.x + 0.7 * w.image.get_width() > c.x) and (
            w.x + 0.3 * w.image.get_width() < c.x + c.image.get_width()) and (
            w.y + 0.7 * w.image.get_height() > c.y) and (
            w.y + 0.3 * w.image.get_height() < c.y + c.image.get_height()):
        return True
    return False


cxk = CXK()

blist = []
for i in range(3000):
    blist.append(Ball())


while True:
    if cxk.life > 0:
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
                cxk.rmove = False
                cxk.lmove = False
        clock.tick(50)
        screen.fill((230,230,230))

        cxk.move()
        screen.blit(cxk.image,(cxk.x,cxk.y))
        for balls in blist:
            balls.active = True
            if balls.active:
                balls.move()
                screen.blit(balls.image, (balls.x, balls.y))
                if checkCrash(cxk,balls):
                    pygame.mixer.music.load(random.choice(music))
                    pygame.mixer.music.play()
                    balls.restart()
                    balls.active = True
                    cxk.score += 1
                    if (cxk.score % 10) == 0:
                        cxk.score = 0
                        cxk.life += 1
                        blist.append(Ball())
        fonts = font.render(f"生命:{cxk.life}", 1, (255, 0, 0))
        screen.blit(fonts, (0, 0))
        if cxk.life <= 0:
            pygame.quit()
            sys.exit()
        pygame.display.update()

