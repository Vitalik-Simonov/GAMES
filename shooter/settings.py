import pygame as pg


pg.mixer.init()
WIDTH = 1600
HEIGHT = 896

CELL = 64
FPS = 90
SPEED = 4
BG_OUT = (200, 191, 231)  # "лишний" цвет
ENEMY_DAMAGE_SOUND = pg.mixer.Sound('sounds/enemy_damage.ogg')
PLAYER_DAMAGE_SOUND = pg.mixer.Sound('sounds/enemy_damage.ogg')
FIELD_WIDHT = WIDTH * 3
FIELD_HEIGHT = HEIGHT * 3
MAP_SIZE = 20
START_POS_X = FIELD_WIDHT // 2
START_POS_Y = FIELD_HEIGHT // 2
LIVES = 5
INVENTORY_LEN = 6
