from settings import *
from math import sqrt


class Tasker(pg.sprite.Sprite):
    def __init__(self, game):
        super(Tasker, self).__init__(game.all_sprites)
        self.image = pg.image.load(r'imgs\tasker.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 + 300
        self.rect.y = HEIGHT // 2
        self.game = game
        self.dist = 160

    def update(self):
        target_x, target_y = self.game.player.x, self.game.player.y
        if sqrt((self.rect.y - target_y) ** 2 + (self.rect.x - target_x) ** 2) < self.dist:
            # print('I am ready')
            pass

    def change_coords(self, dx, dy):
        # print(self.rect.x, self.rect.y, 'tas')
        self.rect.x += dx
        self.rect.y += dy
