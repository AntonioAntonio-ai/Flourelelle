import pygame
from pygame.locals import *

class Text(pygame.sprite.Sprite):
    def __init__(self,file,pos):
        self.image = pygame.Surface((64,64))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = pos
        
        self.image.blit(pygame.image.load('images//text//test.bmp'), self.rect)
    def draw(self, display):
        display.blit(self.image,self.rect)
