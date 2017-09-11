import pygame, random
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

    def startup(self, persistent):
        self.persist = persistent
        if not self.persist['terrainLoaded']:
            self.terrain.generateTerrain()
            self.persist['terrainLoaded'] = True
            self.players = [ Player(320, 10, self.tank_t, self.tank_b),
                             Player(320, 10, self.tank_t, self.tank_b) ]
            TankBase.terrain = self.terrain

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'START'
                self.done = True

    def update(self, dt, f_time):
        mpos = pygame.mouse.get_pos()
        mbut = pygame.mouse.get_pressed()
        key  = pygame.key.get_pressed()

        for player in self.players:
            player.update(dt, key)
        Projectile.update(dt)

        if mbut[0]: self.terrain.cutSection(mpos, 12)
        
    def draw(self, surface):
        surface.blit(self.terrain.surface, (0,0))
        for player in self.players:
            player.draw(surface)

            angle = self.font.render('Angle: {}'.format(player.angle), True, (200,200,200))
            power = self.font.render('Power: {}'.format(player.power), True, (200,200,200))

            surface.blit(angle, angle.get_rect(midtop=self.s_rect.midtop))
            surface.blit(power, power.get_rect(midtop=(self.s_rect.midtop[0],16)))
        Projectile.draw(surface)
