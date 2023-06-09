from shader import *
from bird import *
from obj import *


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(resolution, pg.SCALED)
        pg.display.set_caption('Король и шут')
        self.clock = pg.time.Clock()
        self.shader = PyShader(self)
        self.score = Score(self)
        self.delta = 0

    def draw(self, GRAV):
        self.delta += SCROLL_SPEED
        self.shader.run(self.delta)

        self.all_sprites.draw(self.screen)
        self.all_sprites.update(GRAV)
        self.pipe_handler.update()

        self.score.draw(self.pipe_handler.passed_pipes)

    def run(self):
        GRAV = 0
        self.all_sprites = pg.sprite.Group()
        self.pipe_group = pg.sprite.Group()
        self.pipe_handler = PipeHandler(self)
        self.bird = Bird(game=self)
        self.all_sprites.add(self.bird)

        self.bird.start()

        while True:

            for i in pg.event.get():
                if i.type == pg.QUIT or pg.key.get_pressed()[pg.K_q]:
                    exit()

            if pg.key.get_pressed()[pg.K_UP]:
                if GRAV > 1:
                    GRAV = -12
            else:
                GRAV += 0.5
                if GRAV > 0:
                    GRAV *= G

            self.draw(GRAV)

            pg.display.flip()

            self.clock.tick(FPS)


if __name__ == '__main__':
    app = App()
    app.run()
