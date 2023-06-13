from settings import *
from ui import *
from math import sqrt
from items import *


class Tasker(pg.sprite.Sprite):
    def __init__(self, game):
        super(Tasker, self).__init__(game.all_sprites)
        self.image = pg.image.load(r'imgs\tasker.png')
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.collide_rect = pg.surface.Surface((320, 320)).get_rect()
        self.rect.x = WIDTH // 2 + 300
        self.rect.y = HEIGHT // 2
        self.game = game
        self.dist = 160
        self.dialog_continue = False
        self.can_dialog_continue = True
        self.get_gear = False
        self.get_engine = False
        self.get_fuel = False
        self.take_gear = False
        self.take_engine = False
        self.take_fuel = False
        self.wait = False

    def update(self):
        self.collide_rect.x = self.rect.x
        self.collide_rect.y = self.rect.y
        self.collide_rect, self.rect = self.rect.copy(), self.collide_rect.copy()
        if pg.sprite.spritecollideany(self, self.game.items):
            if type(pg.sprite.spritecollideany(self, self.game.items)) == Gear:
                pg.sprite.spritecollideany(self, self.game.items).kill()
                self.get_gear = True
            elif type(pg.sprite.spritecollideany(self, self.game.items)) == Engine:
                pg.sprite.spritecollideany(self, self.game.items).kill()
                self.get_engine = True
            elif type(pg.sprite.spritecollideany(self, self.game.items)) == Fuel:
                pg.sprite.spritecollideany(self, self.game.items).kill()
                self.get_fuel = True
        self.collide_rect, self.rect = self.rect.copy(), self.collide_rect.copy()
        target_x, target_y = self.game.player.x, self.game.player.y
        if sqrt((self.rect.y - target_y) ** 2 + (self.rect.x - target_x) ** 2) < self.dist and not self.dialog_continue and self.can_dialog_continue:
            self.dialog()
        if self.can_dialog_continue is False and sqrt((self.rect.y - target_y) ** 2 + (self.rect.x - target_x) ** 2) >= self.dist:
            self.can_dialog_continue = True

        if (not self.dialog_continue) and self.get_fuel and self.wait:
            self.game.happy_end()

    def change_coords(self, dx, dy):
        # print(self.rect.x, self.rect.y, 'tas')
        self.rect.x += dx
        self.rect.y += dy

    def dialog(self):
        self.dialog_continue = True
        self.can_dialog_continue = False
        if self.get_gear is False:
            Dialog(self, self.game, DIALOGS['start'])
            if not self.take_gear:
                self.take_gear = True
                Gear(self.game, -FIELD_WIDHT // 4, -FIELD_HEIGHT // 20)
        else:
            if self.get_engine is False:
                Dialog(self, self.game, DIALOGS['gear'])
                if not self.take_engine:
                    self.take_engine = True
                    Engine(self.game, FIELD_WIDHT // 4, FIELD_HEIGHT // 2.2)
            else:
                if self.get_fuel is False:
                    Dialog(self, self.game, DIALOGS['engine'])
                    if not self.take_fuel:
                        self.take_fuel = True
                        Fuel(self.game, FIELD_WIDHT // 4, -FIELD_HEIGHT // 3)
                else:
                    Dialog(self, self.game, DIALOGS['fuel'])
                    self.wait = True
