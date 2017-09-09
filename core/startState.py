import pygame
from core.baseState import baseState
from random import randint
#from core.UIElements import Button

class StartState(baseState):
    def __init__(self):
        super(StartState, self).__init__()
        self.persist = {'terrainLoaded':False}

        self.intro = 'Welcome to the game Mini Tanks'
        self.text  = self.font.render(self.intro, True, (255,255,255))
        self.tRect = self.text.get_rect(midtop=self.s_rect.midtop)

        self.pgText = self.font.render('Play', True, (255,255,255))
        self.pgRect = pygame.Rect((0,0), (80,30))
        self.rCent  = self.s_rect.center
        self.pgRect.center = self.rCent
        self.rTime  = 0
        self.bOver  = False
        self.bCols  = ((80,80,80), (25,25,25))

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.next = 'GAME'
            self.done = True

    def update(self, dt, f_time):
        self.bOver = False
        mpos = pygame.mouse.get_pos()
        mbut = pygame.mouse.get_pressed()

        #dx = (self.rCent[0] - self.pgRect.center[0]) / 35
        #dy = (self.rCent[1] - self.pgRect.center[1]) / 35
        #self.pgRect.centerx += dx
        #self.pgRect.centery += dy

        if self.pgRect.collidepoint(mpos):
            self.bOver = True
            if mbut[0]: self.next = 'GAME'; self.done = True
            if self.rTime >= 30:
                self.rCent = (randint(0, self.s_rect.w), randint(0, self.s_rect.h))
                self.rTime = 0
        self.rTime += 1
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.bCols[self.bOver], self.pgRect)
        pygame.draw.rect(surface, (50,50,50), self.pgRect, 3)
        surface.blit(self.pgText, self.pgText.get_rect(center=self.pgRect.center))
        surface.blit(self.text, self.tRect)
