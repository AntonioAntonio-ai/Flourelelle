import pygame
from pygame import *
from random import randint
from pureanim import Pgif

class Sprite(pygame.sprite.Sprite):
    def __init__(self,num,pos,info=0,lvl=None):
        super().__init__()

        self.num = num
        self.info = info # a general variable, quite useful for minor variations on sprites
        self.lvl = lvl

        self.vx = 0
        self.vy = 0
        self.block = [False,False,False,False] # top,bottom,left,right
        self.dead = False

        if num == 0: # gromble
            self.img = 'ff//0_L.bmp'
            
            self.jumps = 0 # number of times it jumps
            self.vx = -2
        elif num == 1: # worker bee
            self.img = 'ff//'
            possbn = 'mfn' # the possible worker bee name/img...
            self.img += '1_' + possbn[randint(0,2)] + '.bmp' # decided by random
            
            self.movy = 0
            self.movup = True
            self.vy = randint(-1,1)
        elif num == 2: # breadlift bucket
            self.img = 'ff//2.bmp'
            self.timer = 0
            if info == 0:
                self.carried = False
        elif num == 3: # shroom
            self.img = 'ff//3.bmp'
            self.vx = -2
        elif num == 4: # worker bee generator
            # For this one, info is a list with an interval time and a bucket
            # spawning percent chance (i.e. [60,100]). This requires lvl.
            self.img = 'nothing.bmp'
            self.timer = 0
            if self.info == 0:
                self.info = [60,0]

        self.image = pygame.image.load('images//sprites//'+self.img)
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 32
        self.rect.y = pos[1] * 32

        if num == 2:
            self.rect.y += 6
            if info == 1:
                # rope bucket pgif
                self.lvl.add_pgif('s21',[self.rect.x,self.rect.y],self)
            elif info == 0:
                # change this when the player picks up the bucket
                self.player = None
        elif num == 3:
            if info == 1:
                # schroom coming out of block
                self.image.set_alpha(0)
                self.timer = 0
                self.vx = 0

    def draw(self,display):
        display.blit(self.image,self.rect)
    def collisions_t(self, tiles):
        # this next one is for finding out if the sprite is blocked
        cull_rect = Rect(self.rect.x+self.vx,self.rect.y+self.vy,self.rect.width,self.rect.height)
        n_block = [False,False,False,False]
        
        for tile in tiles:
            if cull_rect.colliderect(tile.rect):
                if self.rect.right > tile.rect.left and self.rect.left < tile.rect.right:
                    if self.rect.top + self.vy < tile.rect.bottom and self.rect.top > tile.rect.top:
                        # bottom of tile collision
                        if tile.parms[0]: # solidity
                            n_block[0] = True
                            self.rect.top = tile.rect.bottom
                            self.vy = 0
                        tile.touched(self,'sb')
                    if self.rect.bottom + self.vy > tile.rect.top and self.rect.bottom < tile.rect.bottom:
                        # top of tile collision
                        if tile.parms[0]: # solidity
                            n_block[1] = True
                            self.rect.bottom = tile.rect.top
                            self.vy = 0
                        tile.touched(self,'st')

                if self.rect.bottom > tile.rect.top and self.rect.top < tile.rect.bottom:
                    if self.rect.left + self.vx < tile.rect.right and self.rect.left > tile.rect.left:
                        # right of tile collision
                        if tile.parms[0]: # solidity
                            n_block[2] = True
                            self.rect.left = tile.rect.right
                            self.vx = 0
                        tile.touched(self,'sr')
                    if self.rect.right + self.vx > tile.rect.left and self.rect.right < tile.rect.right:
                        # left of tile collision
                        if tile.parms[0]: # solidity
                            n_block[3] = True
                            self.rect.right = tile.rect.left
                            self.vx = 0
                        tile.touched(self,'sl')
                     
            if n_block == [True,True,True,True]:
                # reduces time taken
                break

        self.block = n_block

    def collisions_s(self, sprites):
        cull_rect = Rect(self.rect.x+self.vx,self.rect.y+self.vy,self.rect.width,self.rect.height)
        
        for spr in sprites:
            if (self is not spr) and cull_rect.colliderect(spr.rect):
                if self.rect.right > spr.rect.left and self.rect.left < spr.rect.right:
                    if self.rect.top + self.vy < spr.rect.bottom and self.rect.top > spr.rect.top:
                        spr.touched(self,'sb')
                    if self.rect.bottom + self.vy > spr.rect.top and self.rect.bottom < spr.rect.bottom:
                        spr.touched(self,'st')

                if self.rect.bottom > spr.rect.top and self.rect.top < spr.rect.bottom:
                    if self.rect.left + self.vx < spr.rect.right and self.rect.left > spr.rect.left:
                        spr.touched(self,'sr')
                    if self.rect.right + self.vx > spr.rect.left and self.rect.right < spr.rect.right:
                        spr.touched(self,'sl')

    def touched(self, toucher, how):
        if self.num == 0 or self.num == 1:
            # player or sprite collisions
            if how[-1] == 'l':
                if toucher.rect.centerx > self.rect.left:
                    toucher.vy = -11
                toucher.rect.right = self.rect.left
                toucher.vx = -6
                self.vx = 2
            if how[-1] == 'r':
                if toucher.rect.centerx < self.rect.right:
                    toucher.vy = -11
                toucher.rect.left = self.rect.right
                toucher.vx = 6
                self.vx = -2
            if how[-1] == 't':
                toucher.rect.bottom = self.rect.top
                toucher.vy = -7
                self.vy = 2
                if how[0] != 's': # player only
                    self.dead = True
            else:
                if how[0] != 's': # player only
                    # hurt
                    toucher.hurt(1)
            if how[-1] == 'b':
                self.block[1] = True
                toucher.block[1] = True
                self.rect.bottom = toucher.rect.top
                if not self.block[0]:
                    self.vy = -7

        elif self.num == 2:
            if self.info == 0:
                if how[0] != 's': # player collisions
                    if self.block[0]:
                        toucher.block[0]
                        toucher.rect.top = self.rect.bottom
                        toucher.vy = 0
                    if toucher.run:
                        # player pick up a free moving bucket if run
                        toucher.carrying = 0 # player must be carrying the bucket then.
                        toucher.carried = self
                        self.player = toucher
                        self.carried = True
                    else:
                        if how == 'b':
                            self.block[1] = True
                            self.rect.bottom = toucher.rect.top
                            self.vy = -5
                        elif how == 't':
                            toucher.block[1] = True
                            toucher.rect.bottom = self.rect.top
                            toucher.vy = 0
                            toucher.jumpt = 0
                        elif how == 'r':
                            toucher.block[2] = True
                            toucher.rect.left = self.rect.right
                            toucher.vx = 0
                        elif how == 'l':
                            toucher.block[3] = True
                            toucher.rect.right = self.rect.left
                            toucher.vx = 0
            elif self.info == 1:
                # any collisions
                if how[-1] == 'b':
                    self.block[1] = True
                    self.rect.bottom = toucher.rect.top
                    self.vy = -5
                    toucher.block[0] = True
                    toucher.vy = 0
                elif how[-1] == 't':
                    toucher.block[1] = True
                    toucher.rect.bottom = self.rect.top
                    toucher.vy = 0
                elif how[-1] == 'r':
                    toucher.block[2] = True
                    toucher.rect.left = self.rect.right
                    toucher.vx = 0
                elif how[-1] == 'l':
                    toucher.block[3] = True
                    toucher.rect.right = self.rect.left
                    toucher.vx = 0
        elif self.num == 3:
            if how[0] != 's': # player collision
                if self.image.get_alpha() != 0: # this is for info 1
                    toucher.health += 1
                    self.kill()
            else:
                # sprite collisions
                if how == 'sb':
                    toucher.block[0] = True
                    toucher.rect.top = self.rect.bottom
                    toucher.vy = 0
                    toucher.jumpt = 99
                elif how == 'st':
                    toucher.block[1] = True
                    toucher.rect.bottom = self.rect.top
                    toucher.vy = 0
                    toucher.jumpt = 0
                elif how == 'sr':
                    toucher.block[2] = True
                    toucher.rect.left = self.rect.right
                    toucher.vx = 0
                elif how == 'sl':
                    toucher.block[3] = True
                    toucher.rect.right = self.rect.left
                    toucher.vx = 0

    def update(self):
        # updating position for speed
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        exec('update_{}(self)'.format(self.num))

def update_0(self):
    # gromble update
    # gravity
    if not self.block[1]:
        if self.vy < 14:
            self.vy += 3

    # being blocked
    if self.block[2]:
        if self.jumps > 3:
            self.block[2] = False
            self.vx = 2
            self.jumps = 0
        elif self.vy == 0:
            self.vx = -2
            self.vy = -19
            self.jumps += 1
        else:
            self.vx = -2
    elif self.block[3]:
        if self.jumps > 3:
            self.block[3] = False
            self.vx = -2
            self.jumps = 0
        elif self.vy == 0:
            self.vx = 2
            self.vy = -19
            self.jumps += 1
        else:
            self.vx = 2

    # correcting speed
    if self.vx == 1 or self.vx > 2:
        self.vx = 2
    elif self.vx == -1 or self.vx < -2:
        self.vx = -2

    # be dead
    if self.dead:
        self.kill()
    
def update_1(self):
    # worker bee update
    # switching between moving up and down
    if self.movup == True:
        self.vy -= 1
    else:
        self.vy += 1

    self.movy += 1
    if self.movy >= 6:
        self.movy = -6
        self.movup = self.movup * -1 + 1 # flipping the bool state

    self.vx -= 0.1 # constant acceleration

    # if hit face on wall
    if self.block[2]:
        self.vx = 2
        self.vy = -2

    # die if go off screen or get stuck
    if self.rect.x < -100 or self.block == [1,1,1,0]:
        self.dead = True

    # be dead
    if self.dead:
        self.kill()

def update_2(self):
    # breadlift update
    if self.info == 0:
        # free bucket
        if not self.carried:
            # gravity
            if not self.block[1]:
                if self.vy < 14:
                    self.vy += 3
            # friction
            if self.vx > 0:
                self.vx -= 1
            elif self.vx < 0:
                self.vx += 1
        else:
            self.vx = self.player.vx
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y - 25

    elif self.info == 1:
        # up and down elevating
        if self.timer < 60:
            self.vy = -(7 - self.timer // 10)
        elif not self.block[1]:
            self.vy += 3
        else:
            self.timer = 0
        self.timer += 1
        if self.vy > 21:
            self.vy = 21
    elif self.info == 2:
        # bee bucket
        pass

def update_3(self):    
    # shrrom update
    # gravity
    if not self.block[1]:
        if self.vy < 14:
            self.vy += 3

    # being blocked
    if self.block[2]:
        self.vx = 2
    elif self.block[3]:
        self.vx = -2

    if self.info == 1:
        # schroom coming out of block
        if self.timer < 16:
            self.timer += 1
        else:
            self.image.set_alpha(255)
            self.vx = -2

def update_4(self):
    # worker bee generator update
    if self.timer == self.info[0]:
        self.lvl.add_sprite(1,[800/32,randint(4,18)])
        self.timer = 0
    else:
        self.timer += 1
