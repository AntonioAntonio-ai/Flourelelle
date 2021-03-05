import pygame
from pygame.locals import *
from pureanim import Pgif
from sprite import Sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, lvl=None):
        super().__init__()

        # general variables
        self.lvl = lvl
        self.run = False

        # health variables
        self.health = 3
        self.dead = False
        self.inv = 0 # invincibility frames, death timer frames when man dies

        # sounds
        self.jmp = pygame.mixer.Sound('sfx//jump.mp3')
        
        # misc variables
        self.coins = 0
        self.block = [False,False,False,False] # bools as top, bottom, left, right if blocked in those directions
        self.jumpt = 0 # helps in timing the player's jumps to be more natural
        self.touching = [] # tells if the player is touching something that needs this variable, like water
        self.carrying = None # what is player holding. 0 = bucket
        self.carried = None
        
        # speed variables
        self.runspeed = 14
        self.vx = 0
        self.vy = 0
        self.fallmod = 0 # gravity modifier

        # managing player image
        self.image = pygame.image.load('images//player//r_s_1_0.bmp')
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 32
        self.rect.y = pos[1] * 32

    def hurt(self, damage):
        if self.inv == 0:
            if self.health > 0:
                self.health -= damage
                self.inv = 115
        
    def collisions_t(self, tiles):
        # this next one is for finding out if the player is blocked
        cull_rect = Rect(self.rect.x+self.vx,self.rect.y+self.vy,self.rect.width,self.rect.height)
        n_block = [False,False,False,False]
        self.touching = []
        
        for tile in tiles:
            if cull_rect.colliderect(tile.rect):
                self.touching.append(tile.num)
                if self.rect.right > tile.rect.left and self.rect.left < tile.rect.right:
                    if self.rect.top + self.vy < tile.rect.bottom and self.rect.top > tile.rect.top:
                        # bottom of tile collision
                        if tile.parms[0]: # solidity
                            n_block[0] = True
                            self.rect.top = tile.rect.bottom - 1 # the -1 so it can hit multiple things with head
                            self.vy = 0
                            self.jumpt = 99 # stop jumping if hit ceiling :(
                        tile.touched(self,'b')
                    if self.rect.bottom + self.vy > tile.rect.top and self.rect.bottom < tile.rect.bottom:
                        # top of tile collision
                        if tile.parms[0]: # solidity
                            n_block[1] = True
                            self.rect.bottom = tile.rect.top
                            self.vy = 0
                            self.jumpt = 0 # be able to jump if hit floor :)
                        tile.touched(self,'t')

                if self.rect.bottom > tile.rect.top and self.rect.top + 1 < tile.rect.bottom:
                    if self.rect.left + self.vx < tile.rect.right and self.rect.left > tile.rect.left:
                        # right of tile collision
                        if tile.parms[0]: # solidity
                            n_block[2] = True
                            self.rect.left = tile.rect.right
                            self.vx = 0
                        tile.touched(self,'r')
                    if self.rect.right + self.vx > tile.rect.left and self.rect.right < tile.rect.right:
                        # left of tile collision
                        if tile.parms[0]: # solidity
                            n_block[3] = True
                            self.rect.right = tile.rect.left
                            self.vx = 0
                        tile.touched(self,'l')
                     
            if n_block == [True,True,True,True]:
                # reduce time taken
                break

        self.block = n_block

    def collisions_s(self, sprites):
        cull_rect = Rect(self.rect.x+self.vx,self.rect.y+self.vy,self.rect.width,self.rect.height)
        
        for spr in sprites:
            if cull_rect.colliderect(spr.rect):
                if self.rect.right > spr.rect.left and self.rect.left < spr.rect.right:
                    if self.rect.top + self.vy < spr.rect.bottom and self.rect.top > spr.rect.top:
                        spr.touched(self,'b')
                    if self.rect.bottom + self.vy > spr.rect.top and self.rect.bottom < spr.rect.bottom:
                        spr.touched(self,'t')

                if self.rect.bottom > spr.rect.top and self.rect.top < spr.rect.bottom:
                    if self.rect.left + self.vx < spr.rect.right and self.rect.left > spr.rect.left:
                        spr.touched(self,'r')
                    if self.rect.right + self.vx > spr.rect.left and self.rect.right < spr.rect.right:
                        spr.touched(self,'l')
                    
    def controls(self, pushed):
        if pushed[K_RIGHT]:
            if not self.block[3]:
                if self.vx < self.runspeed:
                    self.vx += 2
        elif pushed[K_LEFT]:
            if not self.block[2]:
                if self.vx > -self.runspeed:
                    self.vx -= 2
        if pushed[K_DOWN]:
            # super fall
            self.fallmod += 3
            self.vy += 1
        elif self.fallmod > 0:
            self.fallmod // 2
                    
        if pushed[K_z]:
            if self.jumpt < 8:
                if self.jumpt == 0:
                    # sfx
                    #self.jmp.play()
                    pass
                self.vy = -15
                self.jumpt += 1
        else:
            self.jumpt = 99
            if '3' in self.touching:
                # honey being able to jump within it but not smoothly
                self.jumpt = 0
        if pushed[K_x]:
            self.runspeed = 21
            self.jmp = pygame.mixer.Sound('sfx//jump_r.mp3')
            self.run = True
        else:
            self.runspeed = 14
            self.jmp = pygame.mixer.Sound('sfx//jump.mp3')
            self.run = False
            
    def update(self):
        if self.health > 0:
            # self.touching things
            if '3' in self.touching:
                # honey slowdown
                if self.vx > 1:
                    self.vx = 1
                elif self.vx < -1:
                    self.vx = -1
                if self.vy > 1:
                    self.vy = 1
                elif self.vy < -4:
                    self.vy = -4
            
            # updating position for speed
            if self.vx != 0:
                self.rect.x += self.vx
            if self.vy != 0:
                self.rect.y += self.vy

            # gravity
            if not self.block[1]:
                if self.vy < 14 + self.fallmod:
                    self.vy += 3

            # decelerating
            if self.vx > 0:
                self.vx -= 1
            elif self.vx < 0:
                self.vx += 1
            if self.vy > 0:
                self.vy -= 1
            elif self.vy < 0:
                self.vy += 1

            # decrease invincibility frames
            if self.inv > 0:
                self.inv -= 1
                # this next part is invincibility frame image blinking
                if self.inv % (self.inv/30+7) // (self.inv/60+7):
                    self.image.set_alpha(0)
                else:
                    self.image.set_alpha(255)
            elif self.image.get_alpha() == 100:
                self.image.set_alpha(255)

            # if hit head, no jump
            if self.block[0]:
                self.jumpt = 99

            # throwing stuff that the player is carrying
            if self.carrying != None and not self.run:
                # stop carrying the thing
                self.carrying = None
                self.carried.carried = False
                self.carried.vx = self.vx * 2
        else:
            # dead
            if not self.dead:
                # initialize the death animation and desist player motion
                self.dead = True
                self.image.set_alpha(0)
                self.vx = 0
                self.vy = 0
                # death animation below
                self.lvl.pgifs.add(Pgif('pl_d',[self.rect.x,self.rect.y]))
                self.rect.y = -200

    def img_ch(self, name): # change image
        self.image = pygame.image.load('images//player//{}.bmp'.format(name))
        self.image.set_colorkey((255,255,255))
        
    def draw(self, display):
        display.blit(self.image,self.rect)
