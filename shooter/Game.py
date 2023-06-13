import time
from settings import *
from player import Player
from random import randrange as rnd
from enemy import Spawner, Enemy
from items import *
from tasker import *
from map import *
from score import *
from ui import *


class App:
    def __init__(self):
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        # self.all_sprites = pg.sprite.Group()
        # self.bullets = pg.sprite.Group()
        # self.items = pg.sprite.Group()
        # self.mobs = []
        # self.player = Player(self)
        # self.tasker = Tasker(self)
        # self.map = Map(self)
        # self.game_continue = True

    def setup(self):
        pg.mixer.music.load('sounds/bg.mp3')
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.5)
        self.sound_on = True
        self.all_sprites = pg.sprite.Group()
        self.ui = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = []
        self.player = Player(self)
        self.tasker = Tasker(self)
        GunItem(self, WIDTH // 20, HEIGHT // 2)
        Spawner(self, WIDTH // 2 + 900, HEIGHT // 2)
        Spawner(self, WIDTH // 2 - 1000, HEIGHT // 2)
        Spawner(self, WIDTH // 2, HEIGHT // 2 + 900)
        Spawner(self, WIDTH // 2, HEIGHT // 2 - 900)

        Spawner(self, -FIELD_WIDHT // 4 + 200, -FIELD_HEIGHT // 20 + 200)
        Spawner(self, FIELD_WIDHT // 4 + 300, FIELD_HEIGHT // 2.2 - 100)
        Spawner(self, FIELD_WIDHT // 4 + 100, -FIELD_HEIGHT // 4 + 100)

        HP(self)
        Pause(self)
        Bag(self)
        SoundOnOff(self)
        self.map = Map(self)
        self.game_continue = True
        for i in range(90):
            Decoration(self)

    def draw(self):
        self.screen.fill((60, 150, 10))
        self.all_sprites.draw(self.screen)
        self.ui.draw(self.screen)
        # self.items.draw(self.screen)
        [mob.draw(self.screen) for mob in self.mobs]
        self.player.draw(self.screen)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def update(self):
        self.check_events()
        self.all_sprites.update()
        self.ui.update()
        # self.items.update()
        [mob.update() for mob in self.mobs]
        self.player.update()
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    def run(self):
        self.setup()
        StartMenu(self)
        while self.game_continue:
            self.update()
            self.draw()
        self.end()

    def end(self):
        self.screen.fill('black')
        self.update()
        time.sleep(5)
        self.run()

    def happy_end(self):
        self.screen.fill('red')
        pg.display.flip()
        time.sleep(5)
        self.run()


if __name__ == '__main__':
    app = App()
    app.run()
