import pygame as pg
import numpy as np

def imdisplay(imarray, screen=None):
    """Splashes the given image array on the given pygame screen """
    a = pg.surfarray.make_surface(imarray.swapaxes(0, 1))
    if screen is None:
        screen = pg.display.set_mode(imarray.shape[:2][::-1])
    screen.blit(a, (0, 0))
    pg.display.flip()

b = [123,145,123]

a = np.zeros([100,100])

a.fill([5,5])

print(a)