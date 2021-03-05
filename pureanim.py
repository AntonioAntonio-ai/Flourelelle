import pygame
from pygame.locals import *

# this is for purely pure animations being portrayed

class Pgif(pygame.sprite.Sprite):
    def __init__(self,in_id,coords,parent=None):
        super().__init__()
        
        self.coords = coords # change this instead of self.rect.x/y
        self.id = in_id
        self.parent = parent
        
        self.vx = 0
        self.vy = 0
        self.timer = 0
        
        exec('init_{}(self)'.format(in_id))

        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
    def draw(self,display):
        if self.id == 's21':
            # specific draw for only specific pgifs
            exec('draw_{}(self,display)'.format(self.id))
        else:
            # more general draw
            display.blit(self.image,self.rect)
    def update(self):
        if True:
            # specific update for only specific pgifs
            exec('update_{}(self)'.format(self.id))

        self.coords[0] += self.vx
        self.coords[1] += self.vy
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
#----------------------------------------------------------------
def init_pl_d(self): # player death animation
    self.image = pygame.image.load('images//player//r_s_1_0.bmp')
    self.image.set_colorkey((255,255,255))
def init_t21(self): # tile 2 info 1 (schroomblock) shrooming animation
    self.image = pygame.image.load('images//sprites//ff//3.bmp')
    self.image.set_colorkey((255,255,255))
    self.vy = -2
def init_s21(self): # sprite 2 info 1 (up-down bucket) rope animation
    # requires parent of the sprite
    self.image = pygame.image.load('images//sprites//ff//2_1.bmp')
    self.image.set_colorkey((255,255,255))
    self.riy = self.coords[1]
#----------------------------------------------------------------
def update_pl_d(self):
    self.vy = self.timer - 14
    self.timer += 1
    if self.rect.top > 800:
        self.kill()
def update_t21(self):
    if self.timer == 16:
        self.kill()
    else:
        self.timer += 1
def update_s21(self):
    self.coords[0] = self.parent.rect.x + 11
    self.coords[1] = self.parent.rect.y
#----------------------------------------------------------------
def draw_s21(self,display):
    # drawing the rope for the bucket
    self.riy = self.coords[1]
    while self.riy > 0:
        rope_rect = pygame.Rect(self.coords[0],self.riy-32,32,32)
        display.blit(self.image,rope_rect)
        self.riy -= 32
