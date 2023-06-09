from settings import *
import pygame as pg


class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Block, self).__init__(game.blocks)
        self.image = AIR_IMG
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Air(Block):
    def __init__(self, game, x, y):
        super(Air, self).__init__(game, x, y)
        self.image = AIR_IMG
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Grass(Block):
    def __init__(self, game, x, y):
        super(Grass, self).__init__(game, x, y)
        self.image = GRASS_IMG
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ground(Block):
    def __init__(self, game, x, y):
        super(Ground, self).__init__(game, x, y)
        self.image = GROUND_IMG
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
