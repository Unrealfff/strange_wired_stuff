from random import randint

movement = [(1, 0), (0, -1), (-1, 0), (0, 1)]
class Labirinth:
    def __init__(self, width:int, height:int, tunnels_in_lab:int):
        self.width = width
        self.height = height
        self.tunnels_in_lab = tunnels_in_lab
        self.lab = []
        self.start_pos = None

    def initialization(self):
        for i in range(self.height):
            self.lab.append([])
            for j in range(self.width):
                self.lab[i].append(0)

    def generation(self):
        #0 - стена, 1 - путь, 2 - старт, 3 - финиш
        newtons = [(randint(1, self.height - 2), randint(1, self.width - 2))]
        self.lab[newtons[0][0]][newtons[0][1]] = 1

        tons = newtons.copy()

        s = self.width * self.height  # всего ячеек
        while len(tons) / s < self.tunnels_in_lab / 100:  # пока не закрасим нужный процент точек
            while newtons:
                newnewtons = []
                for i in range(len(newtons)):

                    # считаем сколько нулей вокруг текущей ячейки
                    m = []
                    for k in range(len(movement)):
                        if self.lab[newtons[i][0] + movement[k][0]][newtons[i][1] + movement[k][1]] == 0:
                            # запоминаем в какую сторону был ноль
                            m.append(k)

                    h = 0
                    while m:
                        # берем случайную сторону с нулем
                        a = randint(0, len(m) - 1)
                        # если мы еще в этом цикле не добавили единицы к массиву
                        # и ноль был только в одну сторону
                        # или с вероятностью 1/100 заходим в условие
                        if (h == 0 and len(m) == 1) or randint(0, 100) == 1:
                            # запомнили координаты точки с нулем
                            b = newtons[i][0] + movement[m[a]][0]
                            c = newtons[i][1] + movement[m[a]][1]

                            # если она попадает в массив (без крайних точек)
                            if 0 < b < self.height - 1 and 0 < c < self.width - 1:
                                # то запоминаем кто из ее соседей закрашена единицей
                                f = []
                                for k in range(len(movement)):
                                    if self.lab[b + movement[k][0]][c + movement[k][1]] == 1:
                                        f.append(k)

                                # если такой сосед всего один
                                if len(f) == 1:
                                    # то наша нулевая точка продолжение пути
                                    self.lab[b][c] = 1
                                    # запоминаем ее
                                    newnewtons.append((b, c))
                                    h += 1
                                # если таких соседа два
                                elif len(f) == 2:
                                    # и соседи на противоположных сторонах
                                    d = abs(f[0] - f[1])
                                    if d == 2:
                                        # соединяем их окрашивая в единицу
                                        self.lab[b][c] = 1
                                        newnewtons.append((b, c))
                                        h += 1
                                    # если соседи 90 градусов друг другу
                                    else:
                                        # и еще не соединены
                                        if self.lab[b + movement[f[0]][0] + movement[f[1]][0]][
                                            c + movement[f[0]][1] + movement[f[1]][1]] == 0:
                                            # соединяем их
                                            self.lab[b][c] = 1
                                            newnewtons.append((b, c))
                                            h += 1
                        # обработали сторону с нулем забываем про нее
                        m.pop(a)

                for i in range(len(newtons)):
                    if not newtons[i] in tons:
                        tons.append(newtons[i])
                newtons = newnewtons

            # если мы не нашли ячейку для окраски
            # то стартуем с рандомной точки в нашем пути
            newtons = [tons[randint(0, len(tons) - 1)]]

        # первую встретившуюся единицу заменяем двойкой
        # и запоминаем ее позицию
        a = False
        for i in range(self.height):
            for j in range(self.width):
                if self.lab[i][j] == 1:
                    self.lab[i][j] = 2
                    a = True
                    self.start_pos = [i, j]
                    break
            if a:
                break

        # последняя встретившаяся единица заменяется тройкой
        a = False
        for i in range(self.height - 1, 0, -1):
            for j in range(self.width - 1, 0, -1):
                if self.lab[i][j] == 1:
                    self.lab[i][j] = 3
                    a = True
                    break
            if a:
                break


class Player:
    def __init__(self, start_pos):
        self.now_pos = start_pos
        self.direction = 'up' #up, right, down, left

    def move_forward(self):
        if self.direction == 'up':
            self.now_pos[1] += movement[3][1]
        elif self.direction == 'right':
            self.now_pos[0] += movement[0][0]
        elif self.direction == 'down':
            self.now_pos[1] += movement[1][1]
        elif self.direction == 'left':
            self.now_pos[0] += movement[2][0]

    def rotate_right(self):
        if self.direction == 'up':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'left'
        elif self.direction == 'left':
            self.direction = 'up'

    def rotate_left(self):
        if self.direction == 'up':
            self.direction = 'left'
        elif self.direction == 'right':
            self.direction = 'up'
        elif self.direction == 'down':
            self.direction = 'right'
        elif self.direction == 'left':
            self.direction = 'down'


class Output:
    def right_is_wall(self):
        print('Ты повернулся вправо, впереди стена')
    def right_no_wall(self): print("Ты повернулся вправо, впереди нет стены")
    def left_is_wall(self): print("Ты повернулся влево, впереди стена")
    def left_no_wall(self): print("Ты повернулся влево, впереди нет стены")
    def intro(self): print("""Ты - крот, который немножко заблудился. Твоя задача - 
на ощупь найти выход из подземных тунелей. 
Ты можешь: двигаться вперед командой - 'w' и поворачивать вправо и 
влево на 90 градусов командами 'r' и 'l' соответственно.
Удачи в поисках выхода.""")
    def ending(self): print("Ты ПАБЕДИЛ!!!")
    def move_wall(self): print("Впереди стена")
    def move_path(self): print("Ты продвинулся")


class Game:
    def __init__(self):
        self.labirinth = Labirinth(6, 6, 20)
        self.player = None
        self.output = Output()

    def intro(self):
        self.output.intro()

    def ending(self):
        self.output.ending()

    def is_on_finish(self):
        if self.labirinth.lab[self.player.now_pos[0]][self.player.now_pos[1]] == 3:
            return True
        else:
            return False

    def next_cell(self):
        if self.player.direction == 'up':
            if self.labirinth.lab[self.player.now_pos[0] + movement[3][0]][self.player.now_pos[1] + movement[3][1]] == 0:
                return 'wall'
            else:
                return 'path'
        elif self.player.direction == 'right':
            if self.labirinth.lab[self.player.now_pos[0] + movement[0][0]][self.player.now_pos[1] + movement[0][1]] == 0:
                return 'wall'
            else:
                return 'path'
        elif self.player.direction == 'down':
            if self.labirinth.lab[self.player.now_pos[0] + movement[1][0]][self.player.now_pos[1] + movement[1][1]] == 0:
                return 'wall'
            else:
                return 'path'
        elif self.player.direction == 'left':
            if self.labirinth.lab[self.player.now_pos[0] + movement[2][0]][self.player.now_pos[1] + movement[2][1]] == 0:
                return 'wall'
            else:
                return 'path'

    def input_from_console(self):
        a = input()
        return a

    def start(self):
        self.labirinth.initialization()
        self.labirinth.generation()
        self.player = Player(self.labirinth.start_pos)
        self.intro()
        while self.is_on_finish() != True:
            action = self.input_from_console()
            if action == 'w':
                if self.next_cell() == 'path':
                    self.player.move_forward()
                    self.output.move_path()
                else:
                    self.output.move_wall()
            elif action == 'r':
                self.player.rotate_right()
                if self.next_cell() == 'wall':
                    self.output.right_is_wall()
                else:
                    self.output.right_no_wall()
            elif action == 'l':
                self.player.rotate_left()
                if self.next_cell() == 'wall':
                    self.output.left_is_wall()
                else:
                    self.output.left_no_wall()
        self.ending()


if __name__ == "__main__":
    game = Game()
    game.start()