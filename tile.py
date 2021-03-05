import pygame
from pygame.locals import *

def tile_object(num,pos,size):
    tiles = []
    # add compositions
    for ix in range(0,size[0]):
        for iy in range(0,size[1]):
            curr_tile = Tile(num,[pos[0]+ix,pos[1]+iy])
            if num == 0:
                exec('tobj_{}_comp(curr_tile,size[0],size[1],ix,iy)'.format(num))
            tiles.append(curr_tile)
    return tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self,num,pos,info=0,lvl=None):
        super().__init__()
        
        self.num = str(num)
        self.pos = pos
        self.info = info
        self.lvl = lvl

        exec("tile_{}_init(self)".format(num))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 32
        self.rect.y = pos[1] * 32

        if self.num == 4:
            self.rect.x += 6
    def touched(self,player,how): # use this function with player.collisions
        exec('tile_' + str(self.num) + '_touched(self,player,how)')
    def draw(self,display):
        display.blit(self.image, self.rect)

# These next few could go in one of the classes above, but I really would like
# them down here so the classes don't get so cluttered.
def tile_0_init(self):
    # general solid block
    if self.info == 0:
        self.info = 'groundm'
    self.image = pygame.image.load('images//tiles//{}.bmp'.format(self.info))
    self.parms = [1, 0, 0] # solid, x-reflect, y-reflect
def tile_1_init(self):
    # 1 coin
    self.image = pygame.image.load('images//tiles//coin.bmp')
    self.image.set_colorkey((255,255,255))
    self.parms = [0, 0, 0]
def tile_2_init(self):
    # coin block
    # If info == 1 (schroomblock), then lvl is needed.
    self.image = pygame.image.load('images//tiles//coinblock.bmp')
    self.parms = [1, 0, 0]
def tile_3_init(self):
    # honey block
    self.image = pygame.image.load('images//tiles//honey.bmp')
    self.parms = [0, 0, 0]
    self.pl_touch = False
def tile_4_init(self):
    # breakable wall block
    self.image = pygame.image.load('images//tiles//break.bmp')
    self.image.set_colorkey((255,255,255))
    self.parms = [1, 0, 0]
#-----------------------------------------------------------------------------
def tile_0_touched(self,toucher,how):
    # nothing special
    pass
def tile_1_touched(self,toucher,how):
    if how[0] != 's': # this only pertains to the player
        toucher.coins += 1
        self.kill()
def tile_2_touched(self,toucher,how):
    if how == 'b': # this only pertains to the player
        self.num = 0 # maybe change this later
        self.image = pygame.image.load('images//tiles//usedblock.bmp')
        if self.info == '0': # coinblock
            toucher.coins += 1
        elif self.info == 1: # shroomblock
            self.lvl.add_pgif('t21',[self.rect.x,self.rect.y])
            self.lvl.add_sprite(3,[self.rect.x/32,self.rect.y/32-1],1)
def tile_3_touched(self,toucher,how):
    if how[0] == 's' and toucher.num != 1: # sprite touch, not for worker bees
        if toucher.vx > 1:
            toucher.vx -= 1
        elif toucher.vx < -1:
            toucher.vx += 1
        if toucher.vy > 1:
            toucher.vy -= 1
        elif toucher.vy < -1:
            toucher.vy += 1
def tile_4_touched(self,toucher,how):
    pass
#-----------------------------------------------------------------------------
# these next ones are for determining the composition for certain tile objects
def tobj_0_comp(tile, width, height, ix, iy):
    sub_tile = ''
    if iy == 0:
        sub_tile = 'grass'
    else:
        sub_tile = 'ground'
    if ix == 0:
        sub_tile += 'l'
    elif ix == width - 1:
        sub_tile += 'r'
    else:
        sub_tile += 'm'
    tile.image = pygame.image.load('images//tiles//{}.bmp'.format(sub_tile))
    tile.image.set_colorkey((255,255,255))
