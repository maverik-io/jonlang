import pygame as pg
from sys import exit

pg.init()
screen = pg.display.set_mode((400, 400))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill('white')

    pg.display.flip()

