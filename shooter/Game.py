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
        pg.mixer.music.load('sounds/bg.wav')
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

    def start_animation(self):
        self.screen.blit(pg.image.load('imgs/first.png'), (0, 0))
        pg.display.flip()
        time.sleep(5)
        for slide in SLIDES:
            self.screen.blit(pg.image.load(slide), (0, 0))
            pg.display.flip()
            while not pg.mouse.get_pressed(3)[0] and not pg.key.get_pressed()[pg.K_SPACE]:
                self.check_events()
            while pg.mouse.get_pressed(3)[0] or pg.key.get_pressed()[pg.K_SPACE]:
                self.check_events()

        self.screen.blit(pg.image.load('imgs/anim_bg.png'), (0, 0))
        pg.display.flip()
        rocket = AnimatioRocket(self)
        for i in range(150):
            self.screen.blit(pg.image.load('imgs/anim_bg.png'), (0, 0))
            rocket.update1()
            self.screen.blit(rocket.image, rocket.rect)
            pg.display.flip()
            self.clock.tick(self.FPS)
        rocket.image.set_colorkey(BG_OUT)
        h, w = pg.image.load('imgs/rocket.png').get_size()
        w //= 2
        h //= 2
        orig_im = pg.transform.rotate(pg.image.load('imgs/rocket.png'), -90)
        for i in range(50):
            self.screen.blit(pg.image.load('imgs/anim_bg.png'), (0, 0))
            rocket.update2()
            self.screen.blit(rocket.image, rocket.rect)
            pg.display.flip()
            self.clock.tick(self.FPS)
            rocket.image = pg.transform.rotate(pg.transform.scale(orig_im, (w, h)), -45 + i)
            rocket.image.set_colorkey(BG_OUT)
            x, y = rocket.rect.right, rocket.rect.bottom
            rocket.rect = rocket.image.get_rect()
            rocket.rect.right, rocket.rect.bottom = x, y
            w *= 0.95
            h *= 0.95
        time.sleep(1)

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
        orig_im = pg.image.load('imgs/anim_bg2.png')
        w, h = orig_im.get_size()
        for i in range(800, 100, -15):
            self.screen.blit(pg.transform.scale(orig_im, (w * i / 199, h * i / 199)), (400 - i * 4, 200 - i * 2))
            pg.display.flip()
        self.run()

    def happy_end(self):
        self.screen.blit(pg.image.load('imgs/anim_bg.png'), (0, 0))
        pg.display.flip()
        rocket = AnimatioRocket(self)
        orig_im = pg.image.load('imgs/rocket_fire.png')
        rocket.rect.right = 900
        rocket.rect.bottom = 577
        w, h = orig_im.get_size()
        h *= 0.054
        w *= 0.054
        for i in range(45):
            self.screen.blit(pg.image.load('imgs/anim_bg.png'), (0, 0))
            rocket.rect.x -= 1.6
            rocket.rect.y -= 1.6
            self.screen.blit(rocket.image, rocket.rect)
            pg.display.flip()
            self.clock.tick(self.FPS)
            rocket.image = pg.transform.rotate(pg.transform.scale(orig_im, (w, h)), 45 + i)
            rocket.image.set_colorkey(BG_OUT)
            x, y = rocket.rect.right, rocket.rect.bottom
            rocket.rect = rocket.image.get_rect()
            rocket.rect.right, rocket.rect.bottom = x, y
            w *= 1.05
            h *= 1.05
        for i in range(200):
            self.screen.blit(pg.image.load('imgs/anim_bg.png'), (0, 0))
            rocket.rect.x -= 5
            self.screen.blit(rocket.image, rocket.rect)
            pg.display.flip()
            self.clock.tick(self.FPS)
        rocket.image.set_colorkey(BG_OUT)
        self.run()


class AnimatioRocket(pg.sprite.Sprite):
    def __init__(self, game):
        super(AnimatioRocket, self).__init__()
        self.game = game
        self.image = pg.transform.scale(pg.transform.rotate(pg.image.load('imgs/rocket_fire.png'), -90),
                                        (pg.image.load('imgs/rocket_fire.png').get_height() // 2,
                                         pg.image.load('imgs/rocket_fire.png').get_width() // 2))
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = -self.image.get_width()
        self.rect.y = HEIGHT // 4

    def update1(self):
        self.rect.x += 5

    def update2(self):
        self.rect.x += 3.6
        self.rect.y += 3.6


if __name__ == '__main__':
    app = App()
    app.start_animation()
    app.run()