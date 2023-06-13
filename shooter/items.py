from settings import *
import arm
from random import randrange as rnd, choice


class Item(pg.sprite.Sprite):
    def __init__(self, game, x, y, im):
        super(Item, self).__init__(game.items, game.all_sprites)
        self.game = game
        im.set_colorkey(BG_OUT)
        self.image = im.copy()
        self.orig_image = im.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pg.sprite.spritecollideany(self, self.game.player):
            self.kill()
            self.change_arm()

    def change_coords(self, dx, dy):
        # print(self.rect.x, self.rect.y, 'it')
        self.rect.x += dx
        self.rect.y += dy

    def change_arm(self):
        pass


class GunItem(Item):
    def __init__(self, game, x, y):
        super(GunItem, self).__init__(game, x, y, pg.image.load(r'imgs\pistol.png'))

    def change_arm(self):
        self.game.player.arm = arm.Gun(self.game.player)


class Star(Item):
    def __init__(self, game, x, y):
        super(Star, self).__init__(game, x, y, pg.image.load(r'imgs\star.png'))

    def change_arm(self):
        k = self.game.player.inventory.list[0].size / max(self.image.get_width(), self.image.get_height()) * 0.75
        im = pg.transform.scale(self.image, (self.image.get_width() * k, self.image.get_height() * k)).copy()
        self.game.player.inventory.put(Star, im)


class Decoration(pg.sprite.Sprite):
    def __init__(self, game, x=None, y=None, typed=None):
        super(Decoration, self).__init__(game.all_sprites)
        if typed is None:
            typed = choice(['rock', 'grass', 'bush', 'rock2'])
        self.game = game
        self.image = pg.image.load('imgs/' + typed + '.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        if x is None:
            for i in range(10):
                x = rnd(-FIELD_WIDHT // 2, FIELD_WIDHT // 2)
                if not pg.sprite.spritecollideany(self, game.all_sprites):
                    break
        if y is None:
            for i in range(10):
                y = rnd(-FIELD_HEIGHT // 2, FIELD_HEIGHT // 2)
                if not pg.sprite.spritecollideany(self, game.all_sprites):
                    break
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def change_coords(self, dx, dy):
        # print(self.rect.x, self.rect.y, 'it')
        self.rect.x += dx
        self.rect.y += dy