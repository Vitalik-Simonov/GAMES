import pygame as pg
from random import randrange
from copy import deepcopy
from random import randint


class App:
    def __init__(self, WIDTH=1600, HEIGHT=900, CELL_SIZE=8):
        self.IS_GRID = False
        self.FPS = 30
        self.color = pg.Color('forestgreen')
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()

        self.CELL_SIZE = CELL_SIZE

        self.H, self.W = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.next_field = [[0 for i in range(self.W)] for j in range(self.H)]
        self.current_field = [[0 for i in range(self.W)] for j in range(self.H)]
        # self.current_field = [[randint(0, 1) for i in range(self.W)] for j in range(self.H)]
        self.current_field = [[0 for i in range(self.W)] for j in range(self.H)]
        self.current_field[self.H // 2][self.W // 2 - 1] = 1
        self.current_field[self.H // 2][self.W // 2] = 1
        self.current_field[self.H // 2][self.W // 2 + 1] = 1

    @staticmethod
    def check_cell(current_field, x, y):
        count = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if current_field[j][i]:
                    count += 1

        if current_field[y][x]:
            count -= 1
            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0

    def check(self):
        for x in range(1, self.W - 1):
            for y in range(1, self.H - 1):
                if self.current_field[y][x]:
                    pg.draw.rect(self.screen, self.color,
                                     (x * self.CELL_SIZE + 2, y * self.CELL_SIZE + 2, self.CELL_SIZE - 2, self.CELL_SIZE - 2))
                    # pg.draw.rect(self.screen, self.get_color(),
                    #                  (x * self.CELL_SIZE + 2, y * self.CELL_SIZE + 2, self.CELL_SIZE - 2, self.CELL_SIZE - 2))
                self.next_field[y][x] = self.check_cell(self.current_field, x, y)

        self.current_field = deepcopy(self.next_field)

    @staticmethod
    def get_color():
        channel = lambda: randrange(30, 220)
        return channel(), channel(), channel()

    def run(self):
        q = 0
        while True:
            q += 1
            self.screen.fill(pg.Color('black'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    dx, dy = event.pos
                    dx //= self.CELL_SIZE
                    dy //= self.CELL_SIZE
                    rect = dx * self.CELL_SIZE, dy * self.CELL_SIZE, self.CELL_SIZE - 1, self.CELL_SIZE - 1
                    if event.button == 3:
                        self.current_field[dy][dx] = 0
                        pg.draw.rect(self.screen, pg.Color('black'), rect)
                    elif event.button == 1:
                        self.current_field[dy][dx] = 1
                        pg.draw.rect(self.screen, self.color, rect)
            if self.IS_GRID:
                [pg.draw.line(self.screen, pg.Color('darkslategray'), (x, 0), (x, self.HEIGHT)) for x in
                 range(0, self.WIDTH, self.CELL_SIZE)]
                [pg.draw.line(self.screen, pg.Color('darkslategray'), (0, y), (self.WIDTH, y)) for y in
                 range(0, self.HEIGHT, self.CELL_SIZE)]
            self.check()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            # if q % 20 == 0:
                # self.current_field[4][4] = 1
                # self.current_field[4][5] = 1
                # self.current_field[4][6] = 1
                # self.current_field[3][6] = 1
                # self.current_field[2][5] = 1
                #
                # self.current_field[-4][4] = 1
                # self.current_field[-4][5] = 1
                # self.current_field[-4][6] = 1
                # self.current_field[-3][6] = 1
                # self.current_field[-2][5] = 1

                # self.current_field[-4][-4] = 1
                # self.current_field[-4][-5] = 1
                # self.current_field[-4][-6] = 1
                # self.current_field[-3][-6] = 1
                # self.current_field[-2][-5] = 1

                # for i in range(17):
                #     self.current_field[-4][-4 - 12 * i] = 1
                #     self.current_field[-4][-5 - 12 * i] = 1
                #     self.current_field[-4][-6 - 12 * i] = 1
                #     self.current_field[-3][-6 - 12 * i] = 1
                #     self.current_field[-2][-5 - 12 * i] = 1


if __name__ == '__main__':
    app = App(CELL_SIZE=10)
    app.run()