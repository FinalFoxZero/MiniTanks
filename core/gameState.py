import pygame
from core.baseState import baseState
from core.terrainGenerator import Terrain
from core.player import Player
from core.projectile import Projectile
from core.tankBase import TankBase

class GameState(baseState):
    def __init__(self):
        super(GameState, self).__init__()
        self.terrain = Terrain(*self.s_rect.size)
        self.tank_t  = self.texLib.grab('tenk_turret.png')
        self.tank_b  = self.texLib.grab('tenk_body.png')
        self.tanks   = []
        self.turn    = 0

    def spawnPlayer(self):
        x, y = self.terrain.pickLocation()
        p = Player(x, y, self.tank_t, self.tank_b)
        self.tanks.append(p)

    def spawnAI(self):
        x, y = self.terrain.pickLocation()
        p = None
        
    def startup(self, persistent):
        self.persist = persistent

        if not self.persist['terrainLoaded']:
            self.terrain.generateTerrain()
            self.persist['terrainLoaded'] = True

            self.spawnPlayer()

            Projectile.randomWind()
            TankBase.terrain = self.terrain

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'START'
                self.done = True
            if event.key == pygame.K_PAUSE or \
               event.key == pygame.K_p:
                self.persist['ScreenShot'] = pygame.display.get_surface().copy()
                self.next = 'PAUSE'
                self.done = True

    def update(self, dt, f_time):
        mpos = pygame.mouse.get_pos()
        mbut = pygame.mouse.get_pressed()
        key  = pygame.key.get_pressed()

        for i, tank in enumerate(self.tanks):
            if self.turn == i: tank.turn = True
            else: tank.turn = False
            tank.update(dt, key)
        Projectile.update(dt)

        if mbut[0]: self.terrain.cutSection(mpos, 12)
        
    def draw(self, surface):
        surface.blit(self.terrain.surface, (0,0))

        for tank in self.tanks:
            tank.draw(surface)
        Projectile.draw(surface)

        wind = Projectile.wind
        if wind[0] == 90:
            w = self.font.render(str(round(wind[1], 3)) + ' -->', True, [255]*3)
            surface.blit(w, w.get_rect(center=(320, 440)))
        else:
            w = self.font.render('<-- ' + str(round(wind[1], 3)), True, [255]*3)
            surface.blit(w, w.get_rect(center=(320, 440)))
