import pygame as pg
from random import randrange
from settings import *
from collections import deque


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super(Player, self).__init__(game.all_sprites)
        self.game = game
        self.delta = 150
        self.jump = False
        self.jump_forse = 0
        self.max_forse = 27
        self.start = pg.time.get_ticks()
        self.images = deque([pg.image.load('img/step1.png'), pg.image.load('img/step2.png')])
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 6
        self.rect.bottom = GROUND_HEIGHT

    def update(self):
        self.delta += self.game.handler.delta_speed
        self.max_forse -= self.game.handler.delta_speed
        self.max_forse = max(20, self.max_forse)
        if self.rect.bottom > GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.jump = False
            self.jump_forse = 0
        else:
            self.rect.y -= self.jump_forse
            self.jump_forse -= 1
        if pg.time.get_ticks() - self.start >= self.delta:
            self.start = pg.time.get_ticks()
            self.images.rotate()
            self.image = self.images[0]
            self.image.set_colorkey((10, 10, 10))

        if pg.key.get_pressed()[pg.K_UP] and self.jump is False:
            self.jump_forse = self.max_forse
            self.jump = True
        # elif pg.key.get_pressed()[pg.K_DOWN]:
        #     self.jump = 0 # SPEED * 500



class Atlas(pg.sprite.Sprite):
    def __init__(self, game):
        super(Atlas, self).__init__(game.all_sprites)
        self.type = randrange(3)
        if self.type == 0:
            self.image = pg.image.load('img/atlas5.png')
        if self.type == 1:
            self.image = pg.image.load('img/atlas8.png')
        if self.type == 2:
            self.image = pg.image.load('img/atlas9.png')

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.bottom = GROUND_HEIGHT

    def update(self):
        self.rect.x -= SPEED
        if self.rect.right <= 0:
            self.kill()


class SpriteHandler:
    def __init__(self, game):
        self.game = game
        self.delta = 500
        self.delta_dist = 10
        self.delta_speed = 0.001
        self.min_dist = 300
        self.max_speed = 10
        self.start = self.delta - 10

    def update(self):
        global SPEED
        SPEED += self.delta_speed
        SPEED = min(SPEED, self.max_speed)
        self.start += SPEED
        if self.start >= self.delta:
            self.delta -= self.delta_dist
            self.delta = max(self.delta, self.min_dist)
            at = Atlas(self.game)
            self.start = -at.image.get_size()[0]
            self.game.all_sprites.add(at)


class App:
    def __init__(self):
        self.handler = SpriteHandler(self)
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.all_sprites.draw(self.screen)

    def check_events(self):
        self.FPS = 90
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def update(self):
        self.check_events()

        self.handler.update()
        self.all_sprites.update()
        
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    def run(self):
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(Player(self))
        while True:
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
