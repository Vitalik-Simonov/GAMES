import pygame as pg
from random import randrange
'''
1 - pain U
2 - pain UR
3 - pain R
4 - pain DR
5 - pain D
6 - pain DL
7 - pain L
8 - pain UL
9 - MAX_ENERGY
10 - MAX_AGE
11 - class
12 - gen
# 12..self.n - gens
'''
'''
0 - none
1 - our
2 - plant
3 - meat
4 - their
5 - wall
'''
'''
0 - move
1 - turn L
2 - turn R
3 - pause
4 - eat
'''

class Unit:
    def __init__(self, number, parent, what_do, x, y, en):
        self.mutation = 33
        self.color = classes[parent]
        self.number = number
        self.what_do = self.gens(what_do)
        self.duration = 0
        self.x, self.y = x, y
        self.age = 0
        self.energy = en

    @staticmethod
    def get_rand_color():
        # случайный цвет
        channel = lambda: randrange(30, 220)
        return channel(), channel(), channel()

    def gens_mutation(self, lst):
        # мутация списка взаимодействия из-за того, что перед клеткой - "условия"
        lst2 = []
        for i, item in enumerate(lst):
            # если мутация
            if randrange(100) < self.mutation:
                # если пустая
                if i == 0:
                    # подходят только движения и повороты
                    lst2.append(randrange(3))
                # если стена
                elif i == 5:
                    # то подходят только повороты и пауза
                    lst2.append(randrange(1, 4))
                # в иначе попадают другие клетки, мясо и растения
                else:
                    # на них нельзя только ходить
                    lst2.append(randrange(1, 5))
            # если мутации нет
            else:
                # то просто добавляем содержимое
                lst2.append(item)
        # в конце возвращаем новое "условие"
        return lst2


    def gens(self, what_do):
        # цикл для прохода списка условий, ну в смысле что делать при боли или генам
        what = []
        for i, item in enumerate(what_do):
            # если мутация
            if randrange(100) < self.mutation:
                # если мутация "условия"
                if i < 8 or i > 10:
                    # то применяем команду мутации
                    what.append(self.gens_mutation(item))
                # если класс
                elif i == 10:
                    # длина списка это порядковый номер последнего + 1 => как раз новый класс
                    what.append(len(classes))
                    # содержимое класса - цвет => добаляем случайный
                    classes.append(self.get_rand_color())
                # иначе инфа => делаем случайное от 2/3 до 1,5 содержимого
                else:
                    what.append(randrange(item - item // 3, item + item // 2))
            # если мутации нет
            else:
                # то просто добавляем содержимое
                what.append(item)
        # в конце возвращаем гены
        return what

    def get_tile(self):
        # возвращает содержимое тайла перед клеткой(в смысле на который смотрит)
        match self.duration:
            case 0:
                return app.field[self.y - 1][self.x]
            case 45:
                return app.field[self.y - 1][self.x + 1]
            case 90:
                return app.field[self.y][self.x + 1]
            case 135:
                return app.field[self.y + 1][self.x + 1]
            case 180:
                return app.field[self.y + 1][self.x]
            case 225:
                return app.field[self.y + 1][self.x - 1]
            case 270:
                return app.field[self.y][self.x - 1]
            case 315:
                return app.field[self.y - 1][self.x - 1]


    # чтоб не путаться step - вызывается снаружи для совершения хода клетки
    def step(self):
        self.age += 1
        for i in who_bite:
            if i[0] == self.number:
                self.do(i[1])

    # а do - выполняет "условие"
    def do(self, what):
        match self.what_do[what - 1]:
            case 0:
                pass


class App:
    def __init__(self, WIDTH=1600, HEIGHT=900, TILE=8):
        self.PLANTS_SPEED = 10
        self.IS_GRID = False
        self.FPS = 30
        self.WIDTH = WIDTH - WIDTH % TILE
        self.HEIGHT = HEIGHT - HEIGHT % TILE
        pg.init()
        self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])
        self.clock = pg.time.Clock()
        self.TILE = TILE
        self.H, self.W = HEIGHT // self.TILE, WIDTH // self.TILE
        self.field = [[0 for i in range(self.W)] for j in range(self.H)]
        for i in range(self.W):
            self.field[0][i] = 3
            self.field[-1][i] = 3
        for i in range(self.H):
            self.field[i][0] = 3
            self.field[i][-1] = 3
        print(self.field)

    def draw(self, x, y):
        if self.field[y][x] == 0:
            pg.draw.rect(
                self.screen, pg.Color('black'),
                ((x + 1) * self.TILE + 2, (y + 1) * self.TILE + 2, self.TILE - 2, self.TILE - 2)
            )
        elif self.field[y][x] == 1:
            center = ((x + 1) * self.TILE - self.TILE // 2, (y + 1) * self.TILE - self.TILE // 2)
            pg.draw.circle(self.screen, pg.Color('forestgreen'), center, self.TILE // 2 - self.TILE // 8)
        elif self.field[y][x] == 2:
            center = ((x + 1) * self.TILE - self.TILE // 2, (y + 1) * self.TILE - self.TILE // 2)
            pg.draw.circle(self.screen, pg.Color('red'), center, self.TILE // 2 - self.TILE // 8)
        elif self.field[y][x] == 3:
            pg.draw.rect(
                self.screen, (100, 23, 24),
                (x * self.TILE, y * self.TILE, self.TILE, self.TILE)
            )
        elif self.field[y][x] > 3:
            pg.draw.rect(
                self.screen, self.get_color(self.field[y][x]), ((x + 1) * self.TILE + 2, (y + 1) * self.TILE + 2, self.TILE - 2, self.TILE - 2)
            )

    def check(self):
        for x in range(self.W):
            for y in range(self.H):
                self.draw(x, y)


    def plant(self):
        n = randrange(self.PLANTS_SPEED + 1)
        s = 0
        while s < n:
            x = randrange(1, self.W)
            y = randrange(1, self.H)
            if not self.field[y][x]:
                self.field[y][x] = 1
            s += 1

    @staticmethod
    def get_color(n):
        return classes[n]

    @staticmethod
    def get_rand_color():
        channel = lambda: randrange(30, 220)
        return channel(), channel(), channel()

    def run(self):
        while True:
            self.screen.fill(pg.Color('black'))

            # pg.draw.rect(
            #     self.screen, (100, 23, 24),
            #     (0, 0, self.WIDTH, self.TILE)
            # )
            # pg.draw.rect(
            #     self.screen, (100, 23, 24),
            #     (self.WIDTH - self.TILE, 0, self.TILE, self.HEIGHT)
            # )
            # pg.draw.rect(
            #     self.screen, (100, 23, 24),
            #     (0, self.HEIGHT - self.TILE, self.WIDTH, self.TILE)
            # )
            # pg.draw.rect(
            #     self.screen, (100, 23, 24),
            #     (0, 0, self.TILE, self.WIDTH)
            # )

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    dx, dy = event.pos
                    dx //= self.TILE
                    dy //= self.TILE
                    # rect = dx * self.TILE, dy * self.TILE, self.TILE - 1, self.TILE - 1
                    # if event.button == 3:
                    #     self.current_field[dy][dx] = 0
                    #     pg.draw.rect(self.screen, pg.Color('black'), rect)
                    # elif event.button == 1:
                    #     self.current_field[dy][dx] = 1
                    #     pg.draw.rect(self.screen, self.color, rect)
            if self.IS_GRID:
                [pg.draw.line(self.screen, pg.Color('darkslategray'), (x, 0), (x, self.HEIGHT)) for x in
                 range(0, self.WIDTH, self.TILE)]
                [pg.draw.line(self.screen, pg.Color('darkslategray'), (0, y), (self.WIDTH, y)) for y in
                 range(0, self.HEIGHT, self.TILE)]
            self.plant()
            self.check()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    MEAT_ENERGY = 30
    PLANT_ENERGY = 30
    classes = [(10, 100, 50)]
    who_bite = []
    app = App(TILE=15)
    app.run()