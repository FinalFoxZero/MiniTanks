from core import *
from time import time

debug = ['FPS: ', 'Current State: ', 'State Draw: ',
         'State Logic: ', 'Last State Swap: ',
         'Current Frame: ']

class Game(object):
    def __init__(self, screen, states, start_state):
        self.done       = False
        self.screen     = screen
        self.clock      = pygame.time.Clock()
        self.frame_time = 0
        self.fps        = 30
        self.states     = states
        self.state_name = start_state
        self.state      = self.states[self.state_name]
        self.gFont      = pygame.font.Font(None, 16)

        self.debug      = True
        self.sDrawTime  = 0.0
        self.sLogicTime = 0.0
        self.sSwapTime  = 0.0

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT: self.done = True
            #if event.type == KEYDOWN:
            #    if event.key == K_ESCAPE: self.done = True
            self.state.get_event(event)

    def flip_state(self):
        self.sSwapTime  = time()
        current_state   = self.state_name
        next_state      = self.state.next
        self.state.done = False
        self.state_name = next_state
        persistent      = self.state.persist
        self.state      = self.states[self.state_name]
        self.state.startup(persistent)
        self.sSwapTime  = time() - self.sSwapTime

    def update(self, dt, f_time):
        if self.state.quit:   self.done = True
        elif self.state.done: self.flip_state()

        self.sLogicTime = time()
        self.state.update(dt, f_time)
        self.sLogicTime = time() - self.sLogicTime

    def draw(self):
        self.screen.fill((0,0,0))

        self.sDrawTime = time()
        self.state.draw(self.screen)
        self.sDrawTime = time() - self.sDrawTime

        if self.debug:
            for i, text in enumerate(self.debug_overlay()):
                self.screen.blit(text, text.get_rect(topleft=(4, i*text.get_height()+5))) 

    def debug_overlay(self):
        deb_ = self.gFont.render('Debug Information', True, (255,255,255))
        fps_ = self.gFont.render(debug[0] + str(round(self.clock.get_fps(), 2)), True, (255,255,0))
        cst_ = self.gFont.render(debug[1] + self.state_name, True, (60,240,30))
        cft_ = self.gFont.render(debug[5] + str(self.frame_time), True, (30,160,250))
        sdt_ = self.gFont.render(debug[2] + str(round(self.sDrawTime,  4)) + 'ms', True, (255,255,255))
        slt_ = self.gFont.render(debug[3] + str(round(self.sLogicTime, 4)) + 'ms', True, (255,255,255))
        sst_ = self.gFont.render(debug[4] + str(round(self.sSwapTime,  4)) + 'ms', True, (255,255,255))
        return(deb_, fps_, cst_, cft_, sdt_, slt_, sst_)
        
    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps) / 1000
            self.event_loop()
            self.update(dt, self.frame_time)
            self.draw()
            pygame.display.update()
            self.frame_time += 1

if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)

    pygame.init()

    screen = pygame.display.set_mode((640, 480), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('A Python Game')
    
    states = {'START' : StartState(),
              'GAME'  : GameState()}

    game = Game(screen, states, 'START')
    game.run()

    pygame.quit(); quit()
