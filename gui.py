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
            #rebote
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
    x=(abs(x1-x2))
    y=(abs(y1-y2))
    distance=math.sqrt((x*x+y*y))
    return (distance < 50) 

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 550
WIDTH = 550
ACC = 0.5
FRIC = -0.12
FPS = 60
bg = pygame.image.load("soccerField.jpg")
net = pygame.image.load("soccerNet.jpg")
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 

display_surface = pygame.display.set_mode((550, 550))

font = pygame.font.Font('freesansbold.ttf', 82)
text = font.render('Gol!', True, white)

font2= pygame.font.Font('freesansbold.ttf', 14)
text2 = font2.render('Presione Esc para salir', True, white)

player = Player("sprite.png", CHARACTERX, CHARACTERY, random.randint(50, 250), random.randint(150, 350))
ball = Player("soccerBall.png", BALLSIZE, BALLSIZE, random.randint(150, 400), random.randint(150, 350))


FramePerSec = pygame.time.Clock()

def valoresjug(ppx,ppy,pbx,pby,anglep):
    x=float(abs(ppx-pbx))
    y=float(abs(ppy-pby))
    distance=math.sqrt((x*x+y*y))
    angle = 0
    if(ppx>pbx):
        if(y!=0):
            angle1=math.degrees(math.atan(x/y))
        elif(y==0):
            angle=(-1*anglep)
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
            if(0<=anglep<=180):
                angle=angle1-anglep
            elif(180<anglep<=360):
                angle=360-(angle1+anglep)
        elif(ppy<pby):
            angle=-angle1-anglep
        else:
            angle=-anglep 
    elif(ppx==ppx):
        angle=-1*(anglep+90)  
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

def giromucho(x):
    l1=360/4
    l2=3*l1
    valor=0
    if(x<l1):
        valor=0
    elif(l1<=x<l2):
        valor=((x-l1)/(l2-l1))
    elif(l2<=1):
        valor=1
    return valor

def giropoco(x):
    l1=360/4
    l2=3*l1
    valor=0
    if(x<l1):
        valor=1
    elif(l1<=x<l2):
        valor=((x-l2)/(l1-l2))
    elif(l2<=1):
        valor=0
    return valor

def memuevomucho(x,Dmax):
    l1=Dmax/4
    l2=3*l1
    valor=0
    if(x<l1):
        valor=0
    elif(l1<=x<l2):
        valor=((x-l1)/(l2-l1))
    elif(l2<=1):
        valor=1
    return valor

def memuevopoco(x,Dmax):
    l1=Dmax/4
    l2=3*l1
    valor=0
    if(x<l1):
        valor=1
    elif(l1<=x<l2):
        valor=((x-l2)/(l1-l2))
    elif(l2<=1):
        valor=0
    return valor

def fuzzylogic(distance,angle,Dmax):
    cerca,medio,lejos=distancebelongsto(distance,Dmax)
    poco,maso,mucho=anglebelongsto(angle)
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    # 1. si estoy muy volteado con respecto a la pelota, giro mucho
    # 2. si estoy medio volteado y lejos, giro un poco y avanzo mucho
    min2=min(maso,lejos)
    # 3. si estoy poco volteado y lejos, avanzo mucho
    # 4. si estoy medio volteado y medio lejos, giro un poco y avanzo un poco
    min4=min(maso,medio)
    # 5. si estoy medio volteado y cerca, me volteo un poco
    min5=min(maso,cerca)
    #PARA GIRAR
    for i in range(0,360):
        if(-0.01<giromucho(i)-mucho<0.01):
            list1.append(i)
            list2.append(giromucho(i))
        if(-0.01<giropoco(i)-min2<0.01):
            list1.append(i)
            list2.append(giropoco(i))
        if(-0.01<giropoco(i)-min4<0.01):
            list1.append(i)
            list2.append(giropoco(i))
        if(-0.01<giropoco(i)-min5<0.01):
            list1.append(i)
            list2.append(giropoco(i))
    suma=0
    suma2=0
    for k in range(len(list1)):
        suma=suma+list1[k]*list2[k]
        suma2=suma2+list2[k]
    angulonuevo=suma/suma2
    #PARA MOVERME     
    for j in range(778):
        if(-0.01<memuevomucho(j,Dmax)-min2<0.01):
            list3.append(j)
            list4.append(memuevomucho(j,Dmax))
        min3=min(poco,lejos)
        if(-0.01<memuevomucho(j,Dmax)-min3<0.01):
            list3.append(j)
            list4.append(memuevomucho(j,Dmax))
        if(-0.01<memuevopoco(j,Dmax)-min4<0.01):
            list3.append(j)
            list4.append(memuevopoco(j,Dmax))
    suma3=0
    suma4=0
    for l in range(len(list3)):
        suma3=suma3+list3[l]*list4[l]
        suma4=suma4+list4[l]
    distancianueva=suma3/suma4
    return angulonuevo,distancianueva

def angulodetiro(ppx,ppy):
    x=abs(525-ppx)
    y=abs(225-ppy)
    if (x == 0):
        return 90 if (ppy<225) else -90
    angulodetiro=math.degrees(math.atan(y/x))
    if(ppy<225):
        angulodetiro=-1*angulodetiro 
        angulodetiro=angulodetiro%360
    elif(ppy>225):
        angulodetiro=angulodetiro%360
    elif(ppy==225):
        angulodetiro=0
    angulodetiro=angulodetiro+ ((2 * random.random() -1)*10)
    return angulodetiro

Dmax=math.sqrt(550*550*2)
moving = False
movingBall = False
anguloPelota = 0
notOver = True
angulonuevo, distancianueva = 0,0
while True:
    #set widht and height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #set bg image
    screen.blit(bg,[0,0])
    display_surface.blit(text2,[530,225])
    pygame.display.set_caption("Game")
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    if (moving):
        #player.posx=math.cos(angle)*distance+player.posx
        #player.posy=math.sin(angle)*distance+player.posy
        moving = player.move(distancianueva, math.radians(angle), 5, 20) #poner los parametros
        if(collition(player.posx, player.posy, ball.posx, ball.posy)):
            ball.setRect(player.posx + 50, player.posy + 25)
            moving = False
            anguloPelota = angulodetiro(ball.posx, ball.posy)
            movingBall = True
    else:
        if (not(movingBall) and notOver):
            distance,angle=valoresjug(player.posx,player.posy,ball.posx,ball.posy,math.degrees(player.angle))
            angulonuevo,distancianueva=fuzzylogic(distance,angle,Dmax)
            player.angle = math.radians(angulonuevo) + player.angle
            print("cambie", player.angle)

            moving = True
    
    if (movingBall):
        #print(anguloPelota)
        movingBall = ball.move(400, math.radians(anguloPelota), 5, 20) #poner los parametros
        if(collition(player.posx, player.posy, ball.posx, ball.posy)):
            ball.setRect(player.posx + 60, player.posy + 25)
        if(collition(525, 225, ball.posx, ball.posy)):
            print("gool")
            notOver = False
            movingBall = False
    else: 
        if (not(moving) and notOver):
            moving = True

    screen.blit(net,[525,225])
    if (not(notOver)):
        display_surface.blit(text,[200, 225])
    pygame.display.flip()

    #Check if window was close
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)