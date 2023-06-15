try:
    import pygame as pg
except Exception as e:
    with open('www.txt', 'w') as f:
        f.write(str(e))
input()