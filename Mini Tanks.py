from core import *
from time import time

debug = ['FPS -------------| ',
         'Current State ---| ',
         'Current Frame ---| ',
         'State Draw ------| ',
         'State Logic -----| ',
         'Last State Swap -| ']

class Game(object):
    def __init__(self, screen, states, start_state):
        self.done       = False
        self.screen     = screen
        self.clock      = pygame.time.Clock()
        self.frame_time = 0
        self.states     = states
        self.state_name = start_state
        self.state      = self.states[self.state_name]
        self.gFont      = pygame.font.Font('DejaVuSans.ttf', 10)

        self.debug      = True
        self.sDrawTime  = 0.0
        self.sLogicTime = 0.0
        self.sSwapTime  = 0.0

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT: self.done = True
            if event.type == KEYDOWN:
                if event.key == K_i:self.debug = not self.debug
            self.state.get_event(event)

    def default_load(self):
        self.screen.fill((10,10,10))
        ld  = self.gFont.render('| Loading |', True, (255,255,255))
        ldr = ld.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(ld, ldr)
        pygame.display.flip()

    def flip_state(self):
        self.sSwapTime  = time()
        current_state   = self.state_name
        next_state      = self.state.next
        self.state.done = False
        self.state_name = next_state
        persistent      = self.state.persist
        self.state      = self.states[self.state_name]
        self.default_load()
        self.state.startup(persistent)
        self.sSwapTime  = time() - self.sSwapTime

    def update(self, dt, f_time):
        self.sLogicTime = time()

        if   self.state.quit: self.done = True
        elif self.state.done: self.flip_state()
        self.state.update(dt, f_time)
        GUI.update(self.state)

        self.sLogicTime = time() - self.sLogicTime

    def render(self):
        self.sDrawTime = time()

        if hasattr(self.state, 'background'):
            self.screen.blit(self.state.background, (0,0))
        else: self.screen.fill((0,0,0))

        self.state.draw(self.screen)
        GUI.render(self.state, self.screen)

        self.sDrawTime = time() - self.sDrawTime

        if self.debug:
            for i, text in enumerate(self.debug_overlay()):
                self.screen.blit(text, text.get_rect(topleft=(4, i*text.get_height()+20)))

    def debug_overlay(self):
        deb_ = self.gFont.render('Debug Information ([i] toggle)',                 True, (255, 255, 255))
        fps_ = self.gFont.render(debug[0] + str(round(self.clock.get_fps(), 2)),   True, (255, 255,   0))
        cst_ = self.gFont.render(debug[1] + self.state_name,                       True, ( 60, 180,  30))
        cft_ = self.gFont.render(debug[2] + str(self.frame_time),                  True, ( 30, 160, 250))
        sdt_ = self.gFont.render(debug[3] + str(round(self.sDrawTime,  4)) + 'ms', True, (255, 255, 255))
        slt_ = self.gFont.render(debug[4] + str(round(self.sLogicTime, 4)) + 'ms', True, (255, 255, 255))
        sst_ = self.gFont.render(debug[5] + str(round(self.sSwapTime,  4)) + 'ms', True, (255, 255, 255))
        return(deb_, fps_, cst_, cft_, sdt_, slt_, sst_)
        
    def run(self):
        while not self.done:
            dt = self.clock.tick(30) / 1000
            self.event_loop()
            self.update(dt, self.frame_time)
            self.render()
            pygame.display.update()
            self.frame_time += 1

if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)

    pygame.init()

    screen = pygame.display.set_mode((640, 480), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Mini Tanks v0.1')

    states = {'START' : StartState(),
              'GAME'  : GameState(),
              'PAUSE' : PauseState()}
    
    game = Game(screen, states, 'START')
    game.run()

    pygame.quit(); quit()
