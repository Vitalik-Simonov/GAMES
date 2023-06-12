from settings import *


class Button(pg.sprite.Sprite):
    def __init__(self, game, im, x, y, *groups):
        super(Button, self).__init__(*groups)
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
            # pg.mixer.music.pause()
            d = PauseMenu(self.game)
            del d
            # pg.mixer.music.unpause()


class Play(Button):
    def __init__(self, game):
        super(Play, self).__init__(game, pg.image.load('imgs/play.png'), 500, 450)
        self.game = game

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            return True


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.play = Play(self.game)
        self.slider = Slider(self.game, 'black', 'red', 1000, 700, 450, 100, pg.mixer.music.get_volume())
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
            self.slider.update()
            self.game.screen.blit(self.slider.image, self.slider.rect)
            if self.play.update():
                del self.play
                break
            pg.mixer.music.set_volume(self.slider.value)
            pg.display.flip()
            self.game.clock.tick(self.game.FPS)


class Slider(pg.sprite.Sprite):
    def __init__(self, game, color1, color2, x, y, l, w, value, *groups):
        super(Slider, self).__init__(*groups)
        self.game = game
        self.image = pg.surface.Surface((w, l))
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.color1 = color1
        self.color2 = color2
        self.l = l
        self.w = w
        self.value = value

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

    def update(self):
        if self.pressed():
            y = pg.mouse.get_pos()[1]
            self.value = abs(y - self.rect.bottom) / self.l
        self.image.fill(self.color2)
        pg.draw.rect(self.image, self.color1, (0, 0, self.w, self.l - self.value * self.l))
        self.image.set_colorkey(BG_OUT)


class Bag(Button):
    def __init__(self, game):
        super(Bag, self).__init__(game, pg.image.load('imgs/bag.png'), 400, 10, game.all_sprites)
        self.game = game
        self.is_pressed = True

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed() and self.is_pressed:
            self.is_pressed = False
            self.game.player.inventory.is_active = not self.game.player.inventory.is_active
        if not pg.mouse.get_pressed(3)[0]:
            self.is_pressed = True


class Cell(Button):
    def __init__(self, game, i):
        self.im = pg.image.load('imgs/cell.png')
        super(Cell, self).__init__(game, pg.surface.Surface((0, 0)), 500 + 70 * i, 10, game.all_sprites)
        self.is_active = False
        self.game = game
        self.i = i
        self.item = None
        self.item_image = pg.surface.Surface((0, 0))
        self.size = min(self.im.get_size()[0], self.im.get_size()[1])

    def update(self):
        if self.is_active:
            self.image = self.im.copy()
            rect = self.item_image.get_rect()
            if self.i == 0:
                print(self.item_image.get_size())
            rect.centerx = self.image.get_width() // 2
            rect.centery = self.image.get_height() // 2
            self.image.blit(self.item_image, rect)
        else:
            self.image = pg.surface.Surface((0, 0))
        self.image.set_colorkey(BG_OUT)
        self.rect = self.image.get_rect()
        self.rect.x = 500 + 70 * self.i
        self.rect.y = 10
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            self.game.player.inventory.full = False
            if self.item is not None:
                self.item(self.game, self.game.player.x - 150, self.game.player.y - 150)
                self.item = None
                self.item_image = pg.surface.Surface((0, 0))


class Inventory(pg.sprite.Sprite):
    def __init__(self, game):
        super(Inventory, self).__init__(game.all_sprites)
        self.game = game
        self.image = pg.surface.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.is_active = False
        self.full = False
        self.list = [Cell(game, i) for i in range(INVENTORY_LEN)]

    def update(self):
        for cell in self.list:
            cell.is_active = self.is_active
        if self.list[-1].item is not None:
            self.full = True
        else:
            self.full = False

    def put(self, item, im):
        for cell in self.list:
            if cell.item is None:
                cell.item = item
                cell.item_image = im.copy()
                break
