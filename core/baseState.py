import pygame
from core.library import Library

file_library = Library()

class baseState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.s_rect  = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font    = pygame.font.Font(None, 18)
        self.texLib  = file_library

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt, f_time):
        pass

    def draw(self, surface):
        pass
