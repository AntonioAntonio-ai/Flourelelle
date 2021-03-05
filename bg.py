import pygame
from pygame import *
import var

class Bg(pygame.sprite.Sprite):
    def __init__(self,file,offset_x=0,parallax=2):
        super().__init__()

        self.image = pygame.image.load("images//bg//test.bmp")
        self.offset_x = offset_x
        self.parallax = parallax # multiplicitive, higher is slower scroll

        self.rect = self.image.get_rect()

    def ch_offset(self, offset_x):
        self.offset_x += offset_x // self.parallax
        
    def draw(self, display):
        # var._width // self.rect.width + 2
        # is so all places on screen can be drawn with bg, even with scroll.
        # how offset_x works is by simultaneously offsetting ix and the temporary rect in the blit
        for ix in range((self.offset_x // self.rect.width), var._width // self.rect.width + 2 + (self.offset_x // self.rect.width)):
            for iy in range(0, var._height // self.rect.width + 2):
                display.blit(self.image, Rect(ix * self.rect.width-self.offset_x, iy * self.rect.height, self.rect.width, self.rect.height))

# test case
#bg = Bg('blah')
#bg.draw('bleh')
