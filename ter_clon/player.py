from settings import *
import pygame as pg


class Player(pg.sprite.Group):
    def __init__(self, game):
        super(Player, self).__init__()
        self.x = 0
        self.y = HEIGHT // 2
        self.game = game
        self.body = Body(self)
        self.eye = Eye(self)
        self.hair = Hair(self)
        self.mouth = Mouth(self)
        self.leg1 = Leg(self)
        self.leg2 = Leg(self)
        self.arm1 = Arm(self)
        self.arm2 = Arm(self)

    def update(self):
        self.x += 1
        self.body.update(self.x, self.y)
        self.eye.update(self.x, self.y)
        self.hair.update(self.x, self.y)
        self.mouth.update(self.x, self.y)
        self.leg1.update(self.x, self.y)
        self.leg2.update(self.x, self.y)
        self.arm1.update(self.x, self.y)
        self.arm2.update(self.x, self.y)

        # if pg.key.get_pressed()[pg.K_UP] and self.jump is False:
        #     self.jump_forse = self.max_forse
        #     self.jump = True
        # elif pg.key.get_pressed()[pg.K_DOWN]:
        #     self.jump = 0 # SPEED * 500

    def draw(self, surface):
        surface.blit(self.arm2.image, self.arm2.rect)
        surface.blit(self.leg2.image, self.leg2.rect)
        surface.blit(self.body.image, self.body.rect)
        surface.blit(self.eye.image, self.eye.rect)
        surface.blit(self.mouth.image, self.mouth.rect)
        surface.blit(self.hair.image, self.hair.rect)
        surface.blit(self.leg1.image, self.leg1.rect)
        surface.blit(self.arm1.image, self.arm1.rect)


class Body(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Body, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\base.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Eye(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Eye, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\eye.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Hair(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Hair, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\hair.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Mouth(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Mouth, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\mouth.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Arm(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Arm, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\arm.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Leg(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Leg, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\leg.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
