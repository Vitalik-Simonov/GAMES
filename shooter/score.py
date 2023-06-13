from settings import *
from math import ceil


class HP(pg.sprite.Sprite):
    def __init__(self, game):
        super(HP, self).__init__(game.all_sprites, game.ui)
        self.game = game
        self.im1 = pg.image.load('imgs/heart.png')
        self.im2 = pg.image.load('imgs/unheart.png')
        self.im1.set_colorkey(BG_OUT)
        self.im2.set_colorkey(BG_OUT)
        self.image = pg.surface.Surface(((15 + self.im1.get_size()[0]) * min(5, LIVES), (15 + self.im1.get_size()[1]) * ceil(LIVES / 5)))
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 10
        self.heart_rect = self.im1.get_rect()

    def update(self):
        self.image.fill(BG_OUT)
        if LIVES <= 5:
            for i in range(self.game.player.lives):
                self.heart_rect.x = (15 + self.im1.get_size()[0]) * i
                self.image.blit(self.im1, self.heart_rect)
            for i in range(self.game.player.lives, LIVES):
                self.heart_rect.x = (15 + self.im2.get_size()[0]) * i
                self.image.blit(self.im2, self.heart_rect)
        else:
            for i in range(self.game.player.lives):
                self.heart_rect.x = (15 + self.im1.get_size()[0]) * i
                self.heart_rect.y = (15 + self.im1.get_size()[1]) * (i // 5)
                self.image.blit(self.im1, self.heart_rect)
            for i in range(self.game.player.lives, LIVES):
                self.heart_rect.x = (15 + self.im2.get_size()[0]) * i
                self.heart_rect.y = (15 + self.im2.get_size()[1]) * (i // 5)
                self.image.blit(self.im2, self.heart_rect)
        self.image.set_colorkey(BG_OUT)
