import pygame
from core.textureLib import textures

texture_center = textures()

class baseState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.s_rect  = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font    = pygame.font.Font(None, 18)
        self.texLib  = texture_center

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt, f_time):
        pass

    def draw(self, surface):
        pass
