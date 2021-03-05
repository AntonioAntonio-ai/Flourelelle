import pygame
from pygame.locals import *
from player import Player
from sprite import Sprite
from tile import Tile
from pureanim import Pgif
from text import Text
from bg import Bg

class Level():
    def __init__(self, players=None, tiles=None, sprites=None):
        self.players = players
        self.tiles = tiles # tiles and sprites should be passed as sprite.Group
        self.sprites = sprites
        self.bg = Bg('Does not matter :)',0,3)

        self.pgifs = pygame.sprite.Group() # this is added to when some sprite or tile requests a pgif
        
        self.scroll_ptx = 350 # the point on the screen where it scrolls
        self.cam_x = 0
        # self.cam_y = 0
        
    def update_all(self,pressed):
        for player in self.players:
            player.update()
            player.controls(pressed)
            player.collisions_t(self.tiles)
            player.collisions_s(self.sprites)

            # scrolling
            if player.rect.x > self.scroll_ptx - self.cam_x:
                self.scroll_x(player.rect.x - self.scroll_ptx)
            else:
                self.scroll_x(0)

        # put tile update here

        for spr in self.sprites:
            spr.update()
            spr.collisions_t(self.tiles)
            spr.collisions_s(self.sprites)

        for pgif in self.pgifs:
            pgif.update()
            
    def draw_all(self,display):
        self.bg.draw(display)
        
        for tile in self.tiles:
            tile.draw(display)

        for spr in self.sprites:
            spr.draw(display)

        for player in self.players:
            player.draw(display)

        for pgif in self.pgifs:
            pgif.draw(display)

    def scroll_x(self,sx):
        self.cam_x += sx
        for player in self.players:
            player.rect.x -= sx
        for tile in self.tiles:
            tile.rect.x -= sx
        for spr in self.sprites:
            spr.rect.x -= sx
        for pgif in self.pgifs:
            pgif.coords[0] -= sx
        self.bg.ch_offset(sx)
    def scroll_y(self,sy):
        pass

    def add_tile(self,num,pos,info=0,lvl=None):
        self.tiles.add(Tile(num,pos,info,lvl))
    def add_sprite(self,num,pos,info=0,lvl=None):
        self.sprites.add(Sprite(num,pos,info,lvl))
    def add_pgif(self,in_id,coords,parent=None):
        self.pgifs.add(Pgif(in_id,coords,parent))
