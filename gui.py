import pygame
from pygame.locals import *
import random
import math

BALLSIZE = 25
CHARACTERX = 50
CHARACTERY = 50

class Player(pygame.sprite.Sprite):
    def __init__(self, image, sizeX, sizeY, posx, posy):
        super(Player, self).__init__()
        self.cont = 0
        self.xLimit = 0
        self.yLimit = 0
        self.x = 0
        self.y = 0
        self.w = sizeX
        self.h = sizeY
        self.posx = posx
        self.posy = posy
        #self.rect = [random.randint(sizeX,550 - sizeX), random.randint(sizeY,550 - sizeY)]
        self.rect = [posx, posy]
        self.surf = pygame.image.load(image)
        self.surf = pygame.transform.scale(self.surf, (sizeX,sizeY))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #self.rect = self.surf.get_rect()
        #self.rect.center = (posx, posy)
        #self.rect.width = sizeX
        #self.rect.height = sizeY
        #self.rect = self.surf.get_rect()

    def setXLimit(self, x):
        self.xLimit = x

    def setYLimit(self, y):
        self.yLimit = y

    def setRect(self, x, y):
        self.rect = [x, y]

    def moveSurf(self, x, y):
        self.rect = [self.rect[0] + x, self.rect[1] + y]
        self.posx = self.rect[0]
        self.posy = self.rect[1]

    def move(self, lenght, angle, speed, step):
        if (self.yLimit + self.xLimit == 0):
            self.y = lenght * math.sin(angle) * -1
            self.x = lenght * math.cos(angle)
            self.yLimit = abs(self.y)
            self.xLimit = abs(self.x)
        if (self.cont == speed):
            self.cont = 0
            self.moveSurf(self.x//step, self.y//step)
            self.yLimit -= abs(self.y/step)
            self.xLimit -= abs(self.x/step)
            #if ((self.posx > (550-self.w)) or 
            if (self.posx < 0):
                self.x = self.x * -1
            if (self.posx > (550 - self.w)):
                self.x = self.x * -1
            if (self.posy < 0):
                self.y = self.y * -1
            if (self.posy > (550 - self.h)):
                self.y = self.y * -1
            

        else:
            self.cont += 1
        #print(self.x, self.y, self.xLimit, self.yLimit)
        return (self.yLimit + self.xLimit > 0)


def collition(x1, y1, x2, y2):
    return (abs(y1 - (y2 - 25)) <= 25) and (abs(x1 - (x2-15)) <= 25) 

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 550
WIDTH = 550
ACC = 0.5
FRIC = -0.12
FPS = 60
bg = pygame.image.load("soccerField.jpg")
net = pygame.image.load("soccerNet.jpg")

player = Player("sprite.png", CHARACTERX, CHARACTERY, 50, 50)
ball = Player("soccerBall.png", BALLSIZE, BALLSIZE, 50, 200)


FramePerSec = pygame.time.Clock()
moving = False
movingBall = True

while True:
    #set widht and height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #set bg image
    screen.blit(bg,[0,0])
    
    pygame.display.set_caption("Game")
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    if (moving):
        moving = player.move(400, 1 * math.pi / 2, 5, 20)
        if(collition(player.posx, player.posy, ball.posx, ball.posy)):
            #print("si")
            ball.setRect(player.posx + 50, player.posy + 25)
            moving = False
            movingBall = True
    
    if (movingBall):
        movingBall = ball.move(600, 0 * math.pi / 2, 5, 20)
        if(collition(player.posx, player.posy, ball.posx, ball.posy)):
            #print("si")
            ball.setRect(player.posx + 50, player.posy + 25)
        if(collition(535, 225, ball.posx, ball.posy)):
            movingBall = False
            print("gool")


    screen.blit(net,[535,225])
    pygame.display.flip()

    #Check if window was close
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)