import pygame
from core.baseState import baseState

class GameState(baseState):
    def __init__(self):
        super(GameState, self).__init__()
        self.intro = 'Currently The Game is Under Construction, Sorry :('
        self.intro2= 'Press ESC to go back to the menu'
        self.text  = self.font.render(self.intro, True, (255,255,255))
        self.text2 = self.font.render(self.intro2,True, (255,255,255))
        self.tRect = self.text.get_rect(center=(self.s_rect.centerx,
                                                self.s_rect.centery-60))
        self.tRec2 = self.text2.get_rect(midtop=self.s_rect.midtop)

        self.wLable = self.texLib.grab('warning_strip.jpg')
        self.wRect  = self.wLable.get_rect(center=self.s_rect.center)

        self.timer  = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'START'
                self.done = True

    def update(self, dt, f_time):
        pass
        
    def draw(self, surface):
        surface.blit(self.wLable, self.wRect)
        surface.blit(self.text, self.tRect)
        surface.blit(self.text2, self.tRec2)
