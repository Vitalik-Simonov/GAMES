from settings import *
import random


class Score:
    def __init__(self, game):
        self.game = game

    def draw(self, score):
        self.text = FONT.render(str(score), True, 'white')
        self.fps = FPS_FONT.render(str(int(self.game.clock.get_fps())), True, 'red')
        self.game.screen.blit(self.text, FONT_POS)
        self.game.screen.blit(self.fps, FPS_POS)


class TopPipe(pg.sprite.Sprite):
    def __init__(self, app, gap_y_pos):
        super().__init__(app.pipe_group, app.all_sprites)
        self.image = pipe_top_texture
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = width, gap_y_pos - HALF_GAP_HEIGHT - GROUND_HEIGHT
        self.app = app
        self.flag = True

    def update(self, grav):
        self.rect.left -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()
        # if self.flag and self.rect.right < width / 5:
        #     self.flag = False
        #     self.app.scores += 1

class BottomPipe(TopPipe):
    def __init__(self, app, gap_y_pos):
        super().__init__(app, gap_y_pos)
        self.image = pipe_bottom_texture
        self.rect.topleft = width, gap_y_pos + HALF_GAP_HEIGHT - GROUND_HEIGHT


class PipeHandler:
    def __init__(self, game):
        self.game = game
        self.pipe_dist = DIST_BETWEEN_PIPES
        self.pipes = []
        self.passed_pipes = 0

    def update(self):
        self.generate_pipes()
        self.count_passed_pipes()

    def generate_pipes(self):
        self.pipe_dist += SCROLL_SPEED
        if self.pipe_dist > DIST_BETWEEN_PIPES:
            self.pipe_dist = 0
            gap_y = self.get_gap_y_position()

            TopPipe(self.game, gap_y)
            pipep = BottomPipe(self.game, gap_y)
            self.pipes.append(pipep)

    def count_passed_pipes(self):
        for pipe in self.pipes:
            if BIRD_POS[0] > pipe.rect.right:
                # self.game.sound.point_sound.play()
                self.passed_pipes += 1
                self.pipes.remove(pipe)

    @staticmethod
    def get_gap_y_position():
        return random.randint(GAP_HEIGHT, height - GAP_HEIGHT)