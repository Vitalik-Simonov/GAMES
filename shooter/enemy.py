from settings import *
from math import acos, degrees, sqrt, cos, sin, radians
from arm import RotateObj
from random import randrange as rnd
from time import time as now


class Enemy(pg.sprite.Group):
    def __init__(self, game, x=None, y=None):
        super(Enemy, self).__init__()
        self.x = x
        self.y = y
        if x is None:
            self.x = rnd(WIDTH)
        if y is None:
            self.y = rnd(HEIGHT)
        self.game = game
        self.body = Body(self)
        self.arm = Arm(self)
        self.speed = 3
        self.lives = 3
        self.dist = 90
        self.shoot_speed = 1
        self.timer = now()

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
            if now() - self.timer >= self.shoot_speed:
                self.timer = now()
                self.game.player.damage(1)

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

    def change_coords(self, dx, dy):
        self.x += dx
        self.y += dy


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


class Spawner(pg.sprite.Sprite):
    def __init__(self, game, x, y, n=6):
        super(Spawner, self).__init__(game.all_sprites)
        self.image = pg.surface.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.dist = 300
        self.n = n
        self.angle = 360 / self.n
        self.r = 150  # расстояние окружности появления врагов

    def update(self):
        target_x, target_y = self.game.player.x, self.game.player.y
        if sqrt((self.rect.y - target_y) ** 2 + (self.rect.x - target_x) ** 2) < self.dist:
            for i in range(self.n // 2):
                self.game.mobs += [Enemy(self.game, self.rect.x + sin(radians(self.angle * i)) * self.r, self.rect.y +
                                         cos(radians(self.angle * i)) * self.r)]
            for i in range(self.n // 2, self.n):
                self.game.mobs += [EnemyStrike(self.game, self.rect.x + sin(radians(self.angle * i)) * self.r, self.rect.y +
                                         cos(radians(self.angle * i)) * self.r)]
                self.kill()
            self.kill()

    def change_coords(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class EnemyStrike(pg.sprite.Group):
    def __init__(self, game, x=None, y=None):
        super(EnemyStrike, self).__init__()
        self.x = x
        self.y = y
        if x is None:
            self.x = rnd(WIDTH)
        if y is None:
            self.y = rnd(HEIGHT)
        self.game = game
        self.body = Body(self)
        self.arm = Arm(self)
        self.speed = 3
        self.lives = 3
        self.dist = 600
        self.shoot_speed = 1
        self.timer = now() + self.shoot_speed * 1.5
        self.angle = 0

    def update(self):
        target_x, target_y = self.game.player.x, self.game.player.y
        self.angle = degrees(
            acos((self.y - target_y) / (sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2))))
        if target_x < self.x:
            self.angle = -self.angle
        if sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2) >= self.dist:
            speed = self.speed
        else:
            speed = 0
            if now() - self.timer >= self.shoot_speed:
                self.timer = now()
                EnemyBullet(self, pg.image.load(r'imgs\bullet.png'))

        self.x += sin(radians(self.angle)) * speed
        self.y -= cos(radians(self.angle)) * speed

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

    def change_coords(self, dx, dy):
        self.x += dx
        self.y += dy


class EnemyBullet(pg.sprite.Sprite):
    def __init__(self, pers, im):
        super(EnemyBullet, self).__init__(pers.game.bullets, pers.game.all_sprites)
        self.image = im.copy()
        self.game = pers.game
        self.pers = pers
        self.damage = 1
        self.angle = self.pers.angle
        self.image = pg.transform.rotate(self.image, 90 - self.pers.angle)
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.im = self.image.copy()
        self.image = pg.Surface((0, 0))

        self.i = 0
        self.bullet_speed = 7
        self.lenght = 600

    def check(self):
        if pg.sprite.spritecollideany(self, self.game.player):
            self.kill()
            self.game.player.damage(self.damage)
        if self.i >= self.lenght:
            self.kill()

    def update(self):
        if self.i >= self.bullet_speed:
            self.image = self.im.copy()
        self.rect.centerx = self.pers.body.rect.centerx + sin(radians(self.angle)) * self.i
        self.rect.centery = self.pers.body.rect.centery - cos(radians(self.angle)) * self.i
        self.check()
        self.i += self.bullet_speed

    def change_coords(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
