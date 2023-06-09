from settings import *
from arm import *


class Player(pg.sprite.Group):
    def __init__(self, game):
        super(Player, self).__init__()
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.virtx = FIELD_WIDHT // 2
        self.virty = FIELD_HEIGHT // 2
        self.game = game
        self.body = Body(self)
        self.eyes = Eyes(self)
        self.mouth = Mouth(self)
        self.arm = Arm(self)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        if pg.key.get_pressed()[pg.K_RIGHT] or pg.key.get_pressed()[pg.K_d]:
            self.speedx += 1
        elif pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_a]:
            self.speedx -= 1
        else:
            self.speedx = 0
        if pg.key.get_pressed()[pg.K_UP] or pg.key.get_pressed()[pg.K_w]:
            self.speedy -= 1
        elif pg.key.get_pressed()[pg.K_DOWN] or pg.key.get_pressed()[pg.K_s]:
            self.speedy += 1
        else:
            self.speedy = 0

        if self.speedx ** 2 + self.speedy ** 2 > SPEED ** 2:
            sp = (self.speedx ** 2 + self.speedy ** 2) / SPEED ** 2
            self.speedx /= sp
            self.speedy /= sp

        self.change_coords(self.speedx, self.speedy)

        self.body.update(self.x, self.y)
        self.eyes.update(self.x, self.y)
        self.mouth.update(self.x, self.y)
        self.arm.update(self.body.rect.centerx, self.body.rect.centery)

    def draw(self, surface):
        surface.blit(self.body.image, self.body.rect)
        surface.blit(self.eyes.image, self.eyes.rect)
        surface.blit(self.mouth.image, self.mouth.rect)
        surface.blit(self.arm.image, self.arm.rect)

    def change_coords(self, dx, dy):
        if FIELD_WIDHT - self.virtx >= WIDTH // 2 and self.virtx >= WIDTH // 2:
            self.virtx += dx
            for i in self.game.all_sprites:
                i.change_coords(-dx, 0)
            # for i in self.game.bullets:
            #     i.change_coords(-dx, 0)
            for i in self.game.mobs:
                i.change_coords(-dx, 0)
            # for i in self.game.items:
            #     i.change_coords(-dx, 0)

        else:
            self.x += dx
            self.virtx += dx
        if FIELD_HEIGHT - self.virty >= HEIGHT // 2 and self.virty >= HEIGHT // 2:
            self.virty += dy
            for i in self.game.all_sprites:
                i.change_coords(0, -dy)
            # for i in self.game.bullets:
            #     i.change_coords(0, -dy)
            for i in self.game.mobs:
                i.change_coords(0, -dy)
            # for i in self.game.items:
            #     i.change_coords(0, -dy)
        else:
            self.y += dy
            self.virty += dy


class Body(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Body, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\base.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Eyes(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Eyes, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\eyes.png')
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
