import pygame
from pygame.locals import *
from tile import tile_object
from tile import Tile
from player import Player
from sprite import Sprite
from level import Level
pygame.init()
pygame.mixer.init()

from var import _display
_running = True
_internal_clock = pygame.time.Clock()
_fps = 30

keys_pressed = None
key_released = None

level0 = Level()

# test cases
p = Player([3,6],lvl=level0)

t0 = tile_object(0, [8,11], [24,5])
t1 = tile_object(1, [10,9], [4,1])
t2 = tile_object(0, [8,10], [1,1])
t3 = tile_object(0, [1,7], [7,9])
t4 = Tile(2, [14,7])
t5 = Tile(2, [15,7], info='1', lvl=level0)
t6 = tile_object(3, [24,7], [7,4])

s0 = Sprite(0, [23,10])
s1 = Sprite(0, [14,-2])
s2 = Sprite(4, [0,0], lvl=level0)
s3 = Sprite(2, [20, 10], info=1, lvl=level0)
s4 = Sprite(2, [3, 2])

level0.players = pygame.sprite.Group(p)
level0.tiles = pygame.sprite.Group(t0+t1+t2+t3+[t4,t5]+t6)
level0.sprites = pygame.sprite.Group([s0,s1,s2,s3,s4])

#for tile in tiles:
#   print(tile.num,tile.pos,tile.parms)

while _running:
    #events
    for event in pygame.event.get():
        if event.type == QUIT:
            _running = False
            break
        elif event.type == KEYUP:
            key_released = event.key
    #logic
    keys_pressed = pygame.key.get_pressed()
            
    level0.update_all(keys_pressed)

    #draw
    _display.fill((255,255,255))

    level0.draw_all(_display)

    pygame.display.flip()
    #misc
    _internal_clock.tick(_fps)
pygame.quit()
