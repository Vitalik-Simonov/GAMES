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
        self.items = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = []
        self.mobs += [Enemy(self)]
        self.player = Player(self)
        self.tasker = Tasker(self)
        GunItem(self, WIDTH // 20, HEIGHT // 2)
        Star(self, WIDTH // 2, HEIGHT // 20)
        Spawner(self, WIDTH // 2 + 900, HEIGHT // 2)
        HP(self)
        Pause(self)
        Bag(self)
        SoundOnOff(self)
        self.map = Map(self)
        self.game_continue = True

    def draw(self):
        self.screen.fill((60, 150, 10))
        self.all_sprites.draw(self.screen)
        # self.bullets.draw(self.screen)
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
        # self.bullets.update()
        # self.items.update()
        [mob.update() for mob in self.mobs]
        self.player.update()
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    def run(self):
        self.setup()
        while self.game_continue:
            self.update()
            self.draw()
        self.end()

    def end(self):
        self.screen.fill('black')
        self.update()
        time.sleep(5)
        self.setup()
        self.run()


if __name__ == '__main__':
    app = App()
    app.run()
