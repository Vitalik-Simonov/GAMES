from settings import *


class Button(pg.sprite.Sprite):
    def __init__(self, game, im, x, y, *groups):
        super(Button, self).__init__(groups)
        self.game = game
        self.image = im
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pressed(self):
        mouse = pg.mouse.get_pos()
        if mouse[0] >= self.rect.topleft[0]:
            if mouse[1] >= self.rect.topleft[1]:
                if mouse[0] <= self.rect.bottomright[0]:
                    if mouse[1] <= self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


class Pause(Button):
    def __init__(self, game):
        super(Pause, self).__init__(game, pg.image.load('imgs/pause.png'), 15, 10, game.all_sprites)
        self.game = game

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            d = PauseMenu(self.game)
            del d


class Play(Button):
    def __init__(self, game):
        super(Play, self).__init__(game, pg.image.load('imgs/play.png'), 300, 450)
        self.game = game

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            return True


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.play = Play(self.game)
        self.run()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def run(self):
        while True:
            self.game.screen.fill((60, 10, 150))
            self.check_events()
            self.game.screen.blit(self.play.image, self.play.rect)
            if self.play.update():
                del self.play
                break
            pg.display.flip()
            self.game.clock.tick(self.game.FPS)
