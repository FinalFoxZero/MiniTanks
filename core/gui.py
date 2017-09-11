import pygame

if not pygame.font.get_init(): pygame.font.init()
font = pygame.font.Font(None, 18)

def stateDone(next_state):
    def _stateDone(state):
        state.next = next_state
        state.done = True
    return(_stateDone)

def closeGame():
    def _closeGame(state):
        state.quit = True
    return(_closeGame)

class GUI(object):
    gui_list = []
    @classmethod
    def update(cls, state):
        mbut = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        for obj in cls.gui_list:
            if obj.state == state:
                try: obj.update(mpos, mbut)
                except:pass
    @classmethod
    def render(cls, state, surface):
        for obj in cls.gui_list:
            if obj.state == state:
                obj.draw(surface)
        

class Button(object):
    base_colors = ((90,90,90), (60,60,60), (40,40,40), (200,200,200))
    def __init__(self, state, position, text, function=None):
        self.state    = state
        self.colors   = Button.base_colors
        self.position = position
        self.function = function
        self.generate(text)
        self.mOver  = False
        self.retVal = False
        GUI.gui_list.append(self)

    def generate(self, text):
        text = font.render(str(text), True, self.colors[3])
        sx, sy = text.get_size()
        self.rect = pygame.Rect((0,0), (80, 24))
        self.rect.center = self.position
        self.text = text
        self.tRect = self.text.get_rect(center=self.rect.center)

    def getReturn(self):
        return(self.retVal)

    def update(self, mpos, mbut):
        self.retVal = False
        if self.rect.collidepoint(mpos): self.mOver = True
        else: self.mOver = False
        if self.mOver and mbut[0]:
            self.retVal = True
            if self.function: self.function(self.state)
            else: print('No assigned functions')
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.colors[self.mOver], self.rect)
        pygame.draw.rect(surface, self.colors[2], self.rect, 2)
        surface.blit(self.text, self.tRect)
