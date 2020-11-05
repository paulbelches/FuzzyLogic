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
        self.angle = 0
        self.posy = posy
        self.rect = [posx, posy]
        self.surf = pygame.image.load(image)
        self.surf = pygame.transform.scale(self.surf, (sizeX,sizeY))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

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
ball = Player("soccerBall.png", BALLSIZE, BALLSIZE, 50, 250)


FramePerSec = pygame.time.Clock()
moving = True
movingBall = False

def valoresjug(ppx,ppy,pbx,pby,anglep):
    x=abs(ppx-pbx)
    y=abs(ppy-pby)
    distance=math.sqrt((x*x+y*y))
    anglep=math.degrees(anglep)
    if(ppx>pbx):
        angle1=math.degrees(math.atan(x/y))
        if(ppy>pby):
            if(90<=anglep<=180):
                angle=angle1-anglep
            else:
                angle=angle1+anglep
        elif(ppy<pby):
            if(90<=anglep<=180):
                angle=180-angle1-anglep
            else:
                angle=180-angle1+anglep
        else:
            angle=90-anglep
    elif(ppx<pbx):
        angle1=math.degrees(math.atan(y/x))
        if(ppy>pby):
            angle=angle1-anglep
        elif(ppy<pby):
            angle=-angle1-anglep
        else:
            angle=-anglep
    angle=angle%360    
    return distance,angle

def distancebelongsto(distance,Dmax):
    l1=Dmax/4
    l2=2*l1
    l3=3*l1
    if (distance<l1):
        cerca=1
        medio=0
        lejos=0
    elif(l1<=distance<l2):
        cerca=((distance-l2)/(l1-l2))
        medio=((distance-l1)/(l2-l1))
        lejos=0
    elif(l2<=distance<l3):
        cerca=0
        medio=((distance-l3)/(l2-l3))
        lejos=((distance-l2)/(l3-l2))
    elif(l3<=distance):
        cerca=0
        medio=0
        lejos=1
    return cerca,medio,lejos
#siempre gira en el sentido de las manecillas del reloj
def anglebelongsto(angle):
    l1=360/4
    l2=2*l1
    l3=3*l1
    if (angle<l1):
        poco=1
        maso=0
        mucho=0
    elif(l1<=angle<l2):
        poco=((angle-l2)/(l1-l2))
        maso=((angle-l1)/(l2-l1))
        mucho=0
    elif(l2<=angle<l3):
        poco=0
        maso=((angle-l3)/(l2-l3))
        mucho=((angle-l2)/(l3-l2))
    elif(l3<=angle):
        poco=0
        maso=0
        mucho=1
    return poco,maso,mucho

# 1. si estoy muy volteado con respecto a la pelota, giro mucho
# 2. si estoy medio volteado y lejos, giro un poco y avanzo muhco
# 3. si estoy poco volteado y lejos, avanzo mucho
# 4. si estoy medio lejos y medio volteado, giro un poco y avanzo un poco
# 5. si estoy cerca y medio volteado, me volteo un poco


def fuzzylogic(distance,angle,Dmax):
    cerca,medio,lejos=distancebelongsto(distance,Dmax)
    poco,maso,mucho=anglebelongsto(angle)
    


        
#while distancia entre pelota y jugador es muy grande, mover al jugador
while True:
    #set widht and height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #set bg image
    screen.blit(bg,[0,0])
    
    pygame.display.set_caption("Game")
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    if (moving):
        moving = player.move(400, 1 * math.pi / 2, 5, 20) #poner los parametros
        if(collition(player.posx, player.posy, ball.posx, ball.posy)):
            ball.setRect(player.posx + 50, player.posy + 25)
            moving = False
            #mover parametros de la pelota
            movingBall = True
    #else:
        #if (not(movingBall)):WHIT
            #Recalculada 
            #Mover los parametros
            #moving = True
    
    if (movingBall):
        movingBall = ball.move(1000, 0 * math.pi / 2, 5, 20) #poner los parametros
        if(collition(player.posx, player.posy, ball.posx, ball.posy)):
            ball.setRect(player.posx + 50, player.posy + 25)
        if(collition(525, 225, ball.posx, ball.posy)):
            print("gool")
            movingBall = False
    #else: 
        #if (not(moving)):
            #Recalculada 
            #Mover los parametros
            #moving = True


    screen.blit(net,[525,225])
    pygame.display.flip()

    #Check if window was close
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)