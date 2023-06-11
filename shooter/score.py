from settings import *


class HP(pg.sprite.Sprite):
    def __init__(self, game):
        super(HP, self).__init__(game.all_sprites)
        self.game = game
        self.im1 = pg.image.load('imgs/heart.png')
        self.im2 = pg.image.load('imgs/unheart.png')
        self.im1.set_colorkey(BG_OUT)
        self.im2.set_colorkey(BG_OUT)
        self.image = pg.surface.Surface(((15 + self.im1.get_size()[0]) * LIVES, self.im1.get_size()[1]))
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 10
        self.heart_rect = self.im1.get_rect()

    def update(self):
        self.image.fill(BG_OUT)
        for i in range(self.game.player.lives):
            self.heart_rect.x = (15 + self.im1.get_size()[0]) * i
            self.image.blit(self.im1, self.heart_rect)
        for i in range(self.game.player.lives, LIVES):
            self.heart_rect.x = (15 + self.im2.get_size()[0]) * i
            self.image.blit(self.im2, self.heart_rect)
        self.image.set_colorkey(BG_OUT)
