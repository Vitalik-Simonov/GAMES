import pygame as pg


pg.mixer.init()
WIDTH = 1600
HEIGHT = 896
CELL = 64
FPS = 90
SPEED = 5
BG_OUT = (200, 191, 231)  # "лишний" цвет
ENEMY_DAMAGE_SOUND = pg.mixer.Sound('sounds/enemy_damage.ogg')
