#initalize everything
import pygame, sys, os
from pygame.locals import *
from random import randint

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("Snak")

#game data
width = 35
height = 35
sx = 15
length = 1
sy = 14
dire = 0
dirs = [[1,0],[0,-1],[-1,0],[0,1]]
snake = [[sx,sy],[sx,sy]]
currentapple = 0
sd = [[sx,sy]]

#grid
grid = []
img = []
img.append(pygame.image.load("empty.png").convert())
img.append(pygame.image.load("apple.png").convert())
img.append(pygame.image.load("snake.png").convert())
for x in range(width*height):
    grid.append(0)

#functions
def newapple():
    global currentapple
    appleindex = randint(0,len(grid))
    while grid[appleindex] != 0:
        appleindex = randint(0,len(grid))
    grid[appleindex] = 1
    currentapple = appleindex
def index(x,y):
    return (x + (y*width))
def top(array):
    return array[len(array) - 1]
def die():
    pygame.quit()
    os.system("python3 " + __file__)
    sys.exit()
def setdir(setd):
    global dire
    if setd != ([2,3,0,1][dire]):
        dire = setd
#leftover setup
grid[index(sx,sy)] = 2
newapple()
clock = pygame.time.Clock()
move = 0

#sound
applsound = pygame.mixer.Sound("apple.wav")

#gameloop
while True:
    move += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                setdir(0)
            if event.key == K_UP:
                setdir(1)
            if event.key == K_LEFT:
                setdir(2)
            if event.key == K_DOWN:
                setdir(3)
    screen.fill((255,255,255))
    
    x = width
    y = 0
    for tile in grid:
        x += 1
        if x > width:
            x = 1
            y += 1
        screen.blit(img[tile],((x*20)-21,(y*20)-20))
    
    #change
    if move > 5:
        move = 0
        playerindex = index(snake[0][0],snake[0][1])
        nextplayer = playerindex + index(dirs[dire][0],dirs[dire][1])
        grid[playerindex + index(dirs[dire][0],dirs[dire][1])] = 2
        sd.insert(0,[dirs[dire][0] + snake[0][0],dirs[dire][1] + snake[0][1]])
        #snake data
        snake[1][0] = top(sd)[0]
        snake[1][1] = top(sd)[1]
        if len(sd) > length:
            sd.pop()
        rmindex = index(snake[1][0],snake[1][1])
        grid[rmindex] = 0
        snake[0][0] += dirs[dire][0]
        snake[0][1] += dirs[dire][1]
        if nextplayer > len(grid)-1 or nextplayer < 0 or snake[0][0] < 0 or snake[0][0] > width:
            die()
    
    if index(snake[0][0],snake[0][1]) == currentapple:
        newapple()
        applsound.play()
        length += 1
    
    num = 0
    for x in sd:
        num += 1
        if num > 1:
            if (x[0] == snake[0][0] and x[1] == snake[0][1]):
                die()
    
    pygame.display.update()
    clock.tick(60)