import pygame
from pygame import gfxdraw
from pygame.locals import *
import sys
from death import Labirinth

class Settings:
    def __init__(self):
        self.window_width = 1920
        self.widown_height = 1080
        self.fps = 60
        self.lab_height = 40
        self.lab_width = 60
        self.start_pos = (0, 0)
        self.lab = (60, 40, 50)
        self.start_angle = 0
        self.draw_range = 15


class Game:
    def __init__(self):
        self.settings = Settings()
        self.lab = self._gen_lab()
        self.player = Player(self.settings.start_pos, self.settings.start_angle)
        self.collision_mas = list()
        self.draw = Draw()

    def _gen_lab(self) -> list:
        lab = Labirinth(self.settings.lab[0], self.settings.lab[1], self.settings.lab[2])
        lab.initialization()
        lab.generation()
        MAP = lab.lab
        return MAP
    
    def start(self):
        pygame.init()
        dis = pygame.display.set_mode((1920, 1080))
        clock = pygame.time.Clock()
        self._random_stuff_init(dis)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
               
                if pygame.key.get_pressed()[K_LEFT]:
                    self.player.rotate_left()
                elif pygame.key.get_pressed()[K_RIGHT]:
                    self.player.rotate_right()
                elif pygame.key.get_pressed()[K_UP]:
                    self.player.move_forward(self.collision_mas)

            self.draw.walls(self.player, dis, self.collision_mas)
            pygame.display.update()
            clock.tick(self.settings.fps)

    def _random_stuff_init(self, dis):
        for map_collision_x in range(60):
          for map_collision_y in range(40):
               if self.lab[map_collision_y][map_collision_x] == 0:
                    for collision_x in range(1320+map_collision_x*10, 1320+map_collision_x*10+10):
                         for collision_y in range(680+map_collision_y*10, 680+map_collision_y*10+10):
                              self.collision_mas.append((collision_x,collision_y))
               elif self.lab[map_collision_y][map_collision_x] == 2:
                    print('found start pos')
                    self.player.pos = (1320+map_collision_x*10+5, 680+map_collision_y*10+5)
               elif self.lab[map_collision_y][map_collision_x] == 3:
                    for collision_x in range(1320+map_collision_x*10, 1320+map_collision_x*10+10):
                         for collision_y in range(680+map_collision_y*10, 680+map_collision_y*10+10):
                              gfxdraw.pixel(dis, collision_x, collision_y, (0,100,0))

    

class Player:
    def __init__(self, pos:tuple, angle:int):
        self.pos = pos
        self.last_pos = self.pos
        self.angle = angle
        self.v_vel = 0
        self.h_vel = 0

    def rotate_left(self):
        self.angle -= 10
        if self.angle < 0:
            self.angle += 360
    
    def rotate_right(self):
        self.angle += 10
        if self.angle > 359:
            self.angle -= 360

    def move_forward(self, collision_massive):
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

        self.v_vel = 1 * v_multiplier / 100
        self.h_vel = 1 * h_multiplier / 100

        prev_pos = self.pos
        self.last_pos = self.pos
        self.pos = (prev_pos[0] + self.h_vel, prev_pos[1] + self.v_vel)
        if (round(self.pos[0]),round(self.pos[1])) in collision_massive:
             self.pos = self.last_pos
             return True
        

class Draw:
    def __init__(self):
        self.settings = Settings()
        self.collision_mas = list()
        self.range = self.settings.draw_range
    
    def _calculate_collision(self, cam:Player):
          collision_spots = []
          collision_visible_spots = []
          for collision_line in range(-44, 45, 8):
               angle = cam.angle + collision_line
               if angle > 359:
                    angle -= 360
               elif angle < 0:
                    angle += 360
               line = Player(cam.pos,angle)
               written_flag = False
               for _ in range(self.range):
                    if line.move_forward(self.collision_mas) == True:
                         collision_spots.append((round(line.pos[0]),round(line.pos[1])))
                         collision_visible_spots.append((round(abs(line.pos[0] - cam.pos[0])),round(abs(line.pos[1] - cam.pos[1]))))
                         written_flag = True
                         break
               if not written_flag:
                    collision_visible_spots.append((self.range, self.range))
          return collision_spots, collision_visible_spots
    
    def walls(self, player:Player, dis, collision_mas):
        self.collision_mas = collision_mas
        wall_points, wall_visible_points = self._calculate_collision(player)
        wall_number = 0
        for drawer in range(0,1920,160):
            pygame.draw.rect(dis, (255-round(255 * ((wall_visible_points[wall_number][0]+wall_visible_points[wall_number][1])/2)/self.range), 0,0), (drawer,0, drawer+160, 1080))
            wall_number += 1

    def get_col_mas(self):
        return self.collision_mas


if __name__ == "__main__":
    game = Game()
    game.start()