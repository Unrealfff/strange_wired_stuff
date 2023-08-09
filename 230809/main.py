import pygame
import time
import random


def draw(size: int, color: tuple, start_pos: tuple):
    pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], 50+20*size, 20))

color_by_id = {}
used_color = []
for color in range(1,6):
    cur_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    if cur_color not in used_color:
        color_by_id[color] = cur_color
        used_color.append(cur_color)

start_time = time.time()
move_counter = 0

WIDTH = 525
HEIGHT = 400
FPS = 10

player_pos = 0

class Pyramids:
    def __init__(self):
        self.pyramids = [[5,4,3,2,1],[],[]]
        self.status = False
        self.picked_item = 0

    def pick_up(self, pos:int):
        if not self.status and self.pyramids[pos]:
            self.picked_item = self.pyramids[pos].pop(-1)
            self.status = True
            pickup_sound.play()

    def lay_down(self, pos:int):
        if self.pyramids[pos]:
            if self.pyramids[pos][-1] > self.picked_item:
                self.pyramids[pos].append(self.picked_item)
                self.picked_item = 0
                self.status = False
                laydown_sound.play()
        else:
            self.pyramids[pos].append(self.picked_item)
            self.picked_item = 0
            self.status = False

pygame.init()
pygame.font.init()
pygame.mixer.init()

pickup_sound = pygame.mixer.Sound("pick_up.ogg")
laydown_sound = pygame.mixer.Sound("lay_down.ogg")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пирамидки")
clock = pygame.time.Clock()

board = Pyramids()

running = True
while running:
    screen.fill((255,255,255))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player_pos -= 1
                if player_pos == -1:
                    player_pos = 2
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player_pos += 1
                if player_pos == 3:
                    player_pos = 0
            elif event.key == pygame.K_SPACE:
                if board.status:
                    board.lay_down(player_pos)
                    move_counter += 1
                else:
                    board.pick_up(player_pos)
                    move_counter += 1

    main_font = pygame.font.Font(None, 24)
    text1 = main_font.render(f'Время: {round(time.time() - start_time)}   Ходы: {move_counter}', True, (180, 180, 180))


    pygame.draw.rect(screen, (20,20,20), (100,50,10,300))
    pygame.draw.rect(screen, (20, 20, 20), (425, 50, 10, 300))
    pygame.draw.rect(screen, (20, 20, 20), (257, 50, 10, 300))
    pygame.draw.rect(screen, (20,20,20), (0,300,525,200))

    if player_pos == 0:
        pygame.draw.circle(screen, (200, 0, 0), (105, 10), 5)
    elif player_pos == 1:
        pygame.draw.circle(screen, (200, 0, 0), (262, 10), 5)
    elif player_pos == 2:
        pygame.draw.circle(screen, (200, 0, 0), (430, 10), 5)

    pyramids = board.pyramids
    for pyramid in range(3):
        for printer in range(len(pyramids[pyramid])):
            id = pyramids[pyramid][printer]
            if pyramid == 0:
                draw(id, color_by_id[id], (130-50-10*id, 280-20*printer))
            elif pyramid == 1:
                draw(id, color_by_id[id], (287 - 50 - 10 * id, 280 - 20 * printer))
            elif pyramid == 2:
                draw(id, color_by_id[id], (455 - 50 - 10 * id, 280 - 20 * printer))

    if board.status:
        id = board.picked_item
        if player_pos == 0:
            draw(id, color_by_id[id], (130-50-10*id, 20))
        elif player_pos == 1:
            draw(id, color_by_id[id], (287 - 50 - 10 * id, 20))
        elif player_pos == 2:
            draw(id, color_by_id[id], (455 - 50 - 10 * id, 20))

    screen.blit(text1, (10, 380))

    pygame.display.flip()

    if board.pyramids == [[],[],[5,4,3,2,1]]:
        running = False
        print('ПОБЕДА')
        print(f'Время:{round(time.time() - start_time)}, кол.во ходов:{move_counter}')

pygame.quit()
