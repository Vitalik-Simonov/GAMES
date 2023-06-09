from settings import *
from player import Player
from blocks import *
from random import randrange as rnd


class App:
    def __init__(self):
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player(self)
        self.setup()

    def setup(self):
        self.blocks = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)

        [self.get_block(rnd(3))(self, i * 64, j * 64) for j in range(HEIGHT // CELL) for i in range(WIDTH // CELL)]

    def get_block(self, n):
        return (Air, Ground, Grass)[n]

    def draw(self):
        self.screen.fill((180, 190, 255))
        self.all_sprites.draw(self.screen)
        self.blocks.draw(self.screen)
        self.player.draw(self.screen)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def update(self):
        self.check_events()
        self.all_sprites.update()
        self.player.update()
        self.blocks.update()
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    def run(self):
        self.setup()
        while True:
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
