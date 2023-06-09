from settings import *
import pygame as pg
from math import acos, degrees, sqrt, cos, sin, radians
from arm import RotateObj
from random import randrange as rnd


class Enemy(pg.sprite.Group):
    def __init__(self, game):
        super(Enemy, self).__init__()
        self.x = rnd(WIDTH)
        self.y = rnd(HEIGHT)
        self.game = game
        self.body = Body(self)
        self.arm = Arm(self)
        self.speed = 3
        self.lives = 3
        self.dist = 80

    def update(self):
        target_x, target_y = self.game.player.x, self.game.player.y
        angle = degrees(
            acos((self.y - target_y) / (sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2))))
        if target_x < self.x:
            angle = -angle
        if sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2) >= self.dist:
            speed = self.speed
        else:
            speed = 0
        self.x += sin(radians(angle)) * speed
        self.y -= cos(radians(angle)) * speed

        self.body.update(self.x, self.y)
        self.arm.update(self.body.rect.centerx, self.body.rect.centery)

    def draw(self, surface):
        surface.blit(self.body.image, self.body.rect)
        surface.blit(self.arm.image, self.arm.rect)

    def damage(self, n):
        self.lives -= n
        ENEMY_DAMAGE_SOUND.play()
        if self.lives <= 0:
            self.kill()

    def kill(self):
        for i in range(len(self.game.mobs)):
            if self.game.mobs[i] == self:
                del self.game.mobs[i]
                return


class Body(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Body, self).__init__(pers)
        self.image = pg.image.load(r'imgs\enemy\enemy.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Arm(RotateObj):
    def __init__(self, pers):
        super(Arm, self).__init__(pers, pg.image.load(r'imgs\enemy\arm.png'), l=60)
        self.pers = pers

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.turn_coords(self.pers.game.player.x, self.pers.game.player.y)
