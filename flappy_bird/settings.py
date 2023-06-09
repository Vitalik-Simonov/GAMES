import pygame as pg
from taichi_glsl import vec2, vec3


# all_sprites = pg.sprite.Group()
resolution = width, height = vec2(1980, 1080)

texture = pg.image.load('img/wall_1.jpg')
player_texture = pg.image.load('img/playerpng.png')
pipe_top_texture = pg.image.load('img/top.png')
pipe_bottom_texture = pg.image.load('img/bottom.png')

RED = vec3(1.0, 0.0, 0.0)
GREEN = vec3(0.0, 1.0, 0.0)
BLUE = vec3(0.0, 0.0, 1.0)
BLACK = vec3(0.0, 0.0, 0.0)
WHITE = vec3(1.0, 1.0, 1.0)
YELLOW = vec3(1.0, 1.0, 0.0)

RED_COLOR = RED * 255
GREEN_COLOR = GREEN * 255
BLUE_COLOR = BLUE * 255
BLACK_COLOR = BLACK * 255
WHITE_COLOR = WHITE * 255
YELLOW_COLOR = YELLOW * 255

G = 1.03

pg.font.init()
FONT = pg.font.Font('fonts/f.ttf', 100)
FONT_POS = (width // 2, height // 8)

FPS_FONT = pg.font.Font('fonts/f.ttf', 40)
FPS_POS = (35, 15)
FPS = 60

PIPE_WIDHT = 250
PIPE_HEIGHT = height
DIST_BETWEEN_PIPES = 1400
# размер проёма
GAP_HEIGHT = int(player_texture.get_size()[1] * 1.75)
HALF_GAP_HEIGHT = GAP_HEIGHT // 2

SCROLL_SPEED = 10
GROUND_HEIGHT = 0

BIRD_POS = (width / 6, height / 18)