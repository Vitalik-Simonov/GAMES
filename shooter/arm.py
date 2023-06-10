from settings import *
from math import acos, degrees, sqrt, cos, sin, radians
from time import time as now


class RotateObj(pg.sprite.Sprite):
    def __init__(self, pers, im, l=60):
        super(RotateObj, self).__init__(pers)
        im.set_colorkey(BG_OUT)
        self.image = im.copy()
        self.orig_image = im.copy()
        self.rect = self.image.get_rect()
        self.angle = 90
        self.l = l

    def turn_coords(self, target_x, target_y):
        x, y = self.rect.x, self.rect.y
        try:
            angle = degrees(
                acos((self.rect.y - target_y) / (sqrt((self.rect.y - target_y) ** 2 + (self.rect.x - target_x) ** 2))))
            if target_x < self.rect.x:
                angle = -angle
            self.image = pg.transform.rotate(self.orig_image, 90 - angle)
            self.angle = angle
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        except:
            pass

        self.rect.centerx += sin(radians(self.angle)) * self.l
        self.rect.centery -= cos(radians(self.angle)) * self.l

    def turn_mouse(self):
        x, y = self.rect.x, self.rect.y
        mouse_x, mouse_y = pg.mouse.get_pos()
        try:
            angle = degrees(acos((self.rect.y - mouse_y)/(sqrt((self.rect.y - mouse_y) ** 2 + (self.rect.x - mouse_x) ** 2))))
            if mouse_x < self.rect.x:
                angle = -angle
            self.image = pg.transform.rotate(self.orig_image, 90 - angle)
            self.angle = angle
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        except:
            pass

        self.rect.centerx += sin(radians(self.angle)) * self.l
        self.rect.centery -= cos(radians(self.angle)) * self.l

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.turn_mouse()

    def change_coords(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Arm(RotateObj):
    def __init__(self, pers):
        super(Arm, self).__init__(pers, pg.image.load(r'imgs\player\arm.png'), l=60)

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.turn_mouse()


class Bullet(pg.sprite.Sprite):
    def __init__(self, gun, pers, im):
        super(Bullet, self).__init__(pers.game.bullets, pers.game.all_sprites)
        self.image = im.copy()
        self.game = pers.game
        self.gun = gun
        self.damage = 1
        self.angle = self.gun.angle
        self.gun_rect = self.gun.rect
        self.image = pg.transform.rotate(self.image, 90 - self.gun.angle)
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.im = self.image.copy()
        self.image = pg.Surface((0, 0))

        self.i = 0
        self.bullet_speed = 15
        self.lenght = 300

    def check(self):
        for mob in self.game.mobs:
            if pg.sprite.spritecollideany(self, mob):
                self.kill()
                mob.damage(self.damage)
        if self.i >= self.lenght:
            self.kill()

    def update(self):
        if self.i >= self.bullet_speed:
            self.image = self.im.copy()
        self.rect.centerx = self.gun_rect.centerx + sin(radians(self.angle)) * (self.gun.self_len + self.i + self.gun.l)
        self.rect.centery = self.gun_rect.centery - cos(radians(self.angle)) * (self.gun.self_len + self.i + self.gun.l)
        self.check()
        self.i += self.bullet_speed

    def change_coords(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Gun(RotateObj):
    def __init__(self, pers, l=80, self_len=None, speed=None):
        super(Gun, self).__init__(pers, pg.image.load(r'imgs\pistol.png'), l=l)
        if speed is None:
            self.speed = 0.1
        else:
            self.speed = speed
        self.pers = pers
        self.timer = now()
        if self_len is None:
            self.self_len = pg.image.load(r'imgs\pistol.png').get_size()[0] // 2
        else:
            self.self_len = self_len

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.turn_mouse()
        self.gun()

    def gun(self):
        if pg.mouse.get_pressed(3)[0] and now() - self.timer >= self.speed:
            self.timer = now()
            Bullet(self, self.pers, pg.image.load(r'imgs\bullet.png'))

