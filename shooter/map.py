from settings import *


class Map(pg.sprite.Sprite):
    def __init__(self, game):
        super(Map, self).__init__(game.all_sprites, game.ui)
        self.image = pg.surface.Surface((FIELD_WIDHT // MAP_SIZE, FIELD_HEIGHT // MAP_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - FIELD_WIDHT // MAP_SIZE
        self.rect.y = 0
        self.game = game
        self.r = 3  # радиус отображения меток

    def update(self):
        self.image.fill('green')
        for mob in self.game.mobs:
            dx, dy = self.game.player.virtx + mob.x - self.game.player.x, \
                     self.game.player.virty + mob.y - self.game.player.y
            pg.draw.circle(self.image, 'red', (dx // MAP_SIZE, dy // MAP_SIZE), self.r)
        for item in self.game.items:
            dx, dy = self.game.player.virtx + item.rect.x - self.game.player.x, \
                     self.game.player.virty + item.rect.y - self.game.player.y
            pg.draw.circle(self.image, 'yellow', (dx // MAP_SIZE, dy // MAP_SIZE), self.r)
        pg.draw.circle(self.image, 'darkgreen',
                       (self.game.player.virtx // MAP_SIZE, self.game.player.virty // MAP_SIZE), self.r)

        dx, dy = self.game.player.virtx + self.game.tasker.rect.x - self.game.player.x, self.game.player.virty + \
                 self.game.tasker.rect.y - self.game.player.y
        pg.draw.circle(self.image, 'blue', (dx // MAP_SIZE,
                                            dy // MAP_SIZE), self.r)
