from settings import *
from arm import *
from ui import *


class Player(pg.sprite.Group):
    def __init__(self, game):
        super(Player, self).__init__()
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.virtx = START_POS_X
        self.virty = START_POS_Y
        self.game = game
        self.body = Body(self)
        self.arm = Arm(self)
        self.speedx = 0
        self.speedy = 0
        self.lives = LIVES
        self.inventory = Inventory(self.game)

    def update(self):
        if pg.key.get_pressed()[pg.K_RIGHT] or pg.key.get_pressed()[pg.K_d]:
            self.speedx += 0.1
            self.speedx = 4
        elif pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_a]:
            self.speedx -= 0.1
            self.speedx = -4
        else:
            self.speedx = 0
        if pg.key.get_pressed()[pg.K_UP] or pg.key.get_pressed()[pg.K_w]:
            self.speedy -= 0.1
            self.speedy = -4
        elif pg.key.get_pressed()[pg.K_DOWN] or pg.key.get_pressed()[pg.K_s]:
            self.speedy += 0.1
            self.speedy = 4
        else:
            self.speedy = 0

        # if self.speedx ** 2 + self.speedy ** 2 > SPEED ** 2:
        #     sp = (self.speedx ** 2 + self.speedy ** 2) / SPEED ** 2
        #     self.speedx /= sp
        #     self.speedy /= sp

        self.change_coords(self.speedx, self.speedy)

        self.body.update(self.x, self.y)
        self.arm.update(self.body.rect.centerx, self.body.rect.centery)

    def draw(self, surface):
        surface.blit(self.body.image, self.body.rect)
        surface.blit(self.arm.image, self.arm.rect)

    def change_coords(self, dx, dy):
        self.virtx += dx
        self.virty += dy

        if FIELD_WIDHT - self.virtx >= WIDTH // 2 and self.virtx >= WIDTH // 2:
            for i in self.game.all_sprites:
                if hasattr(i, 'change_coords'):
                    i.change_coords(-dx, 0)
            # for i in self.game.bullets:
            #     i.change_coords(-dx, 0)
            for i in self.game.mobs:
                i.change_coords(-dx, 0)
            # for i in self.game.items:
            #     i.change_coords(-dx, 0)

        else:
            self.x += dx
        if FIELD_HEIGHT - self.virty >= HEIGHT // 2 and self.virty >= HEIGHT // 2:
            for i in self.game.all_sprites:
                if hasattr(i, 'change_coords'):
                    i.change_coords(0, -dy)
            # for i in self.game.bullets:
            #     i.change_coords(0, -dy)
            for i in self.game.mobs:
                i.change_coords(0, -dy)
            # for i in self.game.items:
            #     i.change_coords(0, -dy)
        else:
            self.y += dy

    def damage(self, n):
        self.lives -= n
        PLAYER_DAMAGE_SOUND.play()
        if self.lives <= 0:
            self.kill()

    def kill(self):
        self.game.game_continue = False


class Body(pg.sprite.Sprite):
    def __init__(self, pers):
        super(Body, self).__init__(pers)
        self.image = pg.image.load(r'imgs\player\down.png')
        self.right = pg.image.load(r'imgs\player\right.png')
        self.left = pg.image.load(r'imgs\player\left.png')
        self.up = pg.image.load(r'imgs\player\up.png')
        self.down = pg.image.load(r'imgs\player\down.png')
        self.image.set_colorkey(BG_OUT)
        self.right.set_colorkey(BG_OUT)
        self.left.set_colorkey(BG_OUT)
        self.up.set_colorkey(BG_OUT)
        self.down.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        if pg.key.get_pressed()[pg.K_RIGHT] or pg.key.get_pressed()[pg.K_d]:
            self.image = self.right
        elif pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_a]:
            self.image = self.left
        elif pg.key.get_pressed()[pg.K_UP] or pg.key.get_pressed()[pg.K_w]:
            self.image = self.up
        elif pg.key.get_pressed()[pg.K_DOWN] or pg.key.get_pressed()[pg.K_s]:
            self.image = self.down
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
