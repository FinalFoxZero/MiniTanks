import pygame
from core.baseState import baseState

class PauseState(baseState):
    def __init__(self):
        super(PauseState, self).__init__()
        self.text = self.font.render('PAUSED', True, (255,255,255))
        self.tRec = self.text.get_rect(center=self.s_rect.center)
        self.next = 'GAME'

    def startup(self, persistent):
        self.persist = persistent
        self.backdrop = self.persist['ScreenShot']
        fade = pygame.Surface(self.s_rect.size, pygame.SRCALPHA)
        fade.fill((0,0,0,180))
        self.backdrop.blit(fade, (0,0))

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAUSE or \
               event.key == pygame.K_p:
                self.done = True

    def draw(self, surface):
        surface.blit(self.backdrop, (0,0))
        surface.blit(self.text, self.tRec)
