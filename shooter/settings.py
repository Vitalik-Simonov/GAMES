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
DIALOGS = {
    'start': ['''Привет! Я бортовой компьютер Олег. Я могу помочь отремонтировать ракету,
но ты мне должен принести запчасти.''', 'Для начала - неси шестерню.', 'Тебе могут помешать, поэтому возьми пистолет.'],
    'gear': ['''Отлично, это как раз то что нужно. Идеально подходит по размеру.
Она поможет починить стартовый механизм.''', 'Но у нас нет двигателя.\nТебе нужно его найти'],
    'engine': ['''Надеюсь, его мощности хватит. Но у нас пустой бак,
а значит тебя ждут новые приключения'''],
    'fuel': ['Отлично, теперь у нас полный бак. Готовься к полёту!']
}
