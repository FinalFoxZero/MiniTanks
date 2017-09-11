import pygame
from core.baseState import baseState
from random import randint
from core.gui import Button, stateDone, closeGame

class StartState(baseState):
    def __init__(self):
        super(StartState, self).__init__()
        self.persist = {'terrainLoaded':False}
        self.controls= self.texLib.grab('controls.png')
        self.cont_rec= self.controls.get_rect(topright=self.s_rect.topright)

        self.intro = 'Welcome to the game Mini Tanks'
        self.text  = self.font.render(self.intro, True, (255,255,255))
        self.tRect = self.text.get_rect(midtop=self.s_rect.midtop)

        self.b0 = Button(self, (320, 240), 'Play',  stateDone('GAME'))
        self.b1 = Button(self, (320, 275), 'Reset')
        self.b2 = Button(self, (320, 310), 'Exit',  closeGame())

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.next = 'GAME'
            self.done = True

    def update(self, dt, f_time):
        if self.b1.getReturn(): self.persist['terrainLoaded'] = False
        

    def draw(self, surface):
        surface.blit(self.text, self.tRect)
        surface.blit(self.controls, self.cont_rec)
