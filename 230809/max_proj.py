# здесь подключаются модули
import pygame
from pygame import gfxdraw
from pygame.locals import *
import sys
from death import Labirinth
 
# здесь определяются константы,
# классы и функции
FPS = 60

MAP = [[[0] for j in range(60)] for i in range(40)]

class Camera:
    def __init__(self):
        self.last_pos = (300,200)
        self.pos = (300,200)
        self.angle = 0
        self.v_vel = 0
        self.h_vel = 0

    def test_print(self):
        print(self.pos, self.angle)

    def rotate(self, direction):
            if direction == 'L':
                self.angle += 1
                if self.angle == 360:
                    self.angle = 0
            elif direction == 'R':
                 self.angle -= 1
                 if self.angle == -1:
                      self.angle = 359

    def move_forward(self):
        global collision_massive
        if 0 <  self.angle < 90:
            v_multiplier = 10/9*self.angle*-1
            h_multiplier = 100 - (10/9*self.angle)

        elif 90 < self.angle < 180:
            v_multiplier = (100 - (10/9*(self.angle - 90)))*-1
            h_multiplier = -10/9*(self.angle - 90)

        elif 180 < self.angle < 270:
            v_multiplier = 10/9*(self.angle-180)
            h_multiplier = (100 - (10/9*(self.angle-180)))*-1

        elif 270 < self.angle <= 359:
            v_multiplier = 100 - (10/9*(self.angle - 270))
            h_multiplier = 10/9*(self.angle - 270)

        elif self.angle == 0:
             h_multiplier = 100
             v_multiplier = 0

        elif self.angle == 90:
             h_multiplier = 0
             v_multiplier = -100

        elif self.angle == 180:
             h_multiplier = -100
             v_multiplier = 0
            
        elif self.angle == 270:
             h_multiplier = 0
             v_multiplier = 100

        self.v_vel = 0.25 * v_multiplier / 100
        self.h_vel = 0.25 * h_multiplier / 100

        prev_pos = self.pos
        self.last_pos = self.pos
        self.pos = (prev_pos[0] + self.h_vel, prev_pos[1] + self.v_vel)
        if (round(self.pos[0]),round(self.pos[1])) in collision_massive:
             print('stooop')
             self.pos = self.last_pos

# здесь происходит инициация,
# создание объектов
pygame.init()
dis = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()



lab = Labirinth(60,40,50)
lab.initialization()
lab.generation()
MAP = lab.lab

cam = Camera()

collision_massive = []

for map_collision_x in range(60):
     for map_collision_y in range(40):
          if MAP[map_collision_y][map_collision_x] == 0:
               for collision_x in range(1320+map_collision_x*10, 1320+map_collision_x*10+10):
                    for collision_y in range(680+map_collision_y*10, 680+map_collision_y*10+10):
                         collision_massive.append((collision_x,collision_y))
          elif MAP[map_collision_y][map_collision_x] == 2:
               print('found start pos')
               cam.pos = (1320+map_collision_x*10+5, 680+map_collision_y*10+5)
          elif MAP[map_collision_y][map_collision_x] == 3:
               for collision_x in range(1320+map_collision_x*10, 1320+map_collision_x*10+10):
                    for collision_y in range(680+map_collision_y*10, 680+map_collision_y*10+10):
                         gfxdraw.pixel(dis, collision_x, collision_y, (0,100,0))
 


for draw_collision in collision_massive:
        gfxdraw.pixel(dis, draw_collision[0], draw_collision[1], (0,0,100))
 
# если надо до цикла отобразить
# какие-то объекты, обновляем экран
pygame.display.update()
 
# главный цикл
while True:
    # цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    if pygame.key.get_pressed()[K_LEFT]:
         cam.rotate('L')
    elif pygame.key.get_pressed()[K_RIGHT]:
         cam.rotate('R')
    elif pygame.key.get_pressed()[K_UP]:
         cam.move_forward()

    # --------
    # изменение объектов
    # --------
    
    cam.test_print()
    gfxdraw.pixel(dis, round(cam.last_pos[0]), round(cam.last_pos[1]), (0,0,0))
    gfxdraw.pixel(dis, round(cam.pos[0]), round(cam.pos[1]), (255,0,0))


    # обновление экрана
    pygame.display.update()

    clock.tick(FPS)