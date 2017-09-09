import pygame

if not pygame.font.get_init(): pygame.font.init()
font = pygame.font.Font(None, 12)



class Button(object):
    def __init__(self, position, *args, **kwargs):
        self.position = position
        for arg in kwargs: setattr(self, arg, kwargs[arg])
        self.render()
        
    def render(self):
        if hasattr(self, 'text'):
            self.text = font.render(self.text, True, (255,255,255))
            x,y = self.text.get_size()
            self.rect = pygame.Rect((0,0), (x+8, y+8))
            self.rect.center = self.position

        if hasattr(self, 'image'):
            self.image = pygame.image.load(self.image).convert()
            self.rect  = self.image.get_rect()
            self.rect.center = self.position

    def getEvent(self, mpos, mbut):
        if self.rect.collidepoint(mpos):
            if mbut[0]:
                if hasattr(self, 'action'):
                    self.action
                else:
                    print('Nothing here')
