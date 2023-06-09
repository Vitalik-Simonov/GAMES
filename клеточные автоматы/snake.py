import pygame as pg
from random import randrange


class App:
    def __init__(self, WIDTH=1600, HEIGHT=900, CELL_SIZE=80, FPS=10):
        self.IS_GRID = False
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()

        self.CELL_SIZE = CELL_SIZE

        self.H, self.W = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.field = [[0 for i in range(self.W)] for j in range(self.H)]
        self.x = self.W // 2
        self.y = self.H // 2
        self.field[self.y][self.x] = 1
        self.duration = (0, -1)

        self.ma = 1

    def draw_tile(self, x, y):
        if self.field[y][x] != 'a':
            pg.draw.rect(self.screen, (0, self.field[y][x] * 255 / self.ma, 0),
                         (x * self.CELL_SIZE + 2, y * self.CELL_SIZE + 2, self.CELL_SIZE - 2, self.CELL_SIZE - 2))
        else:
            pg.draw.rect(self.screen, 'red',
                         (x * self.CELL_SIZE + 2, y * self.CELL_SIZE + 2, self.CELL_SIZE - 2, self.CELL_SIZE - 2))

    def draw(self):
        for i in self.field:
            if 'a' in i:
                break
        else:
            x = randrange(self.W)
            y = randrange(self.H)
            self.field[y][x] = 'a'
        for i in range(self.H):
            for j in range(self.W):
                self.draw_tile(j, i)


    def change(self):
        for i in range(self.H):
            for j in range(self.W):
                if self.field[i][j] != 0 and self.field[i][j] != 'a':
                    self.field[i][j] -= 1


    def run(self):
        while True:
            self.screen.fill(pg.Color('black'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if pg.key.get_pressed()[pg.K_UP]:
                        self.duration = (0, -1)
                    elif pg.key.get_pressed()[pg.K_DOWN]:
                        self.duration = (0, 1)
                    elif pg.key.get_pressed()[pg.K_RIGHT]:
                        self.duration = (1, 0)
                    elif pg.key.get_pressed()[pg.K_LEFT]:
                        self.duration = (-1, 0)
            if self.IS_GRID:
                [pg.draw.line(self.screen, pg.Color('darkslategray'), (x, 0), (x, self.HEIGHT)) for x in
                 range(0, self.WIDTH, self.CELL_SIZE)]
                [pg.draw.line(self.screen, pg.Color('darkslategray'), (0, y), (self.WIDTH, y)) for y in
                 range(0, self.HEIGHT, self.CELL_SIZE)]
            self.x += self.duration[0]
            self.y += self.duration[1]
            self.x %= self.W
            self.y %= self.H
            if self.field[self.y][self.x] == 'a':
                self.ma += 1
            elif self.field[self.y][self.x] != 0:
                break
            self.field[self.y][self.x] = self.ma + 1

            self.change()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = App(CELL_SIZE=32, FPS=10)
    app.run()