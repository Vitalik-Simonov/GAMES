from settings import *

player_texture_size = player_texture.get_size()


class Bird(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = player_texture
        self.rect = self.image.get_rect()
        self.rect.center = BIRD_POS

    def update(self, GRAV):
        self.rect.y += GRAV
        self.check()

    def start(self):
        self.rect.y = height / 3

    def check(self):
        hit = pg.sprite.spritecollide(self, self.game.pipe_group, dokill=False, collided=pg.sprite.collide_mask)
        if hit or self.rect.bottom > height - GROUND_HEIGHT or self.rect.top < -self.image.get_height():
            # self.game.sound.hit_sound.play()
            # pg.time.wait(1000)
            self.kill()
            self.game.run()
