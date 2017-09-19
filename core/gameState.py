import pygame
from core.baseState import baseState
from core.terrainGenerator import Terrain
from core.player import Player
from core.projectile import Projectile
from core.tankBase import TankBase

class GameState(baseState):
    def __init__(self):
        super(GameState, self).__init__()
        self.background = self.texLib.grab('background.png')
        self.tank_t  = self.texLib.grab('tenk_turret.png')
        self.tank_b  = self.texLib.grab('tenk_body.png')
        self.text    = None
        self.text_timer = 0
        self.terrain = Terrain(*self.s_rect.size)
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
            self.tanks = []; self.turn = 0
            self.terrain.resetTerrain()
            self.terrain.generateTerrain()
            self.persist['terrainLoaded'] = True

            self.spawnPlayer() # Player 1
            self.spawnPlayer() # Player 2

            TankBase.terrain   = self.terrain
            Projectile.terrain = self.terrain
            Projectile.tank_ls = self.tanks
            Projectile.randomWind()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'START'; self.done = True
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
            if self.turn == i:
                tank.takeTurn(dt, key)
                if tank.turnDone:
                    self.turn += 1
                    Projectile.randomWind()
            tank.update(dt)
        Projectile.update(dt)

        if self.turn > len(self.tanks)-1:
            self.turn = 0
        if self.text: self.text_timer += 1
        if self.text_timer > 30: self.text = None; self.text_time = 0
        
    def draw(self, surface):
        surface.blit(self.terrain.surface, (0,0))
        pygame.draw.rect(surface, (90,90,90), pygame.Rect(0,0,640,18))
        pygame.draw.rect(surface, (20,20,20), pygame.Rect(0,0,640,18), 1)

        if self.text: surface.blit(self.text, self.text.get_rect(center=(320,240)))

        for i, tank in enumerate(self.tanks):
            tank.draw(surface)

            if self.turn == i:
                hRect  = pygame.Rect(0, 0, 35, 4)
                hRectU = pygame.Rect(0, 0, (tank.health / 100) * 35, 4)

                cPlay  = self.font.render('Player: {}'.format(tank.player), True, [255]*3)
                power  = self.font.render('Power : {}'.format(tank.power ), True, [255]*3)
                angle  = self.font.render('Angle : {}'.format(tank.angle ), True, [255]*3)
                health = self.font.render('Health: {}'.format(tank.health), True, [255]*3)
                shell  = self.font.render('Ammo[{}] {}'.format(tank.ammo[tank.active], tank.active), True, [255]*3)

                surface.blit(cPlay,  cPlay.get_rect( topleft=( 50, 2)))
                surface.blit(power,  power.get_rect( topleft=(150, 2)))
                surface.blit(angle,  angle.get_rect( topleft=(250, 2)))
                surface.blit(health, health.get_rect(topleft=(350, 2)))
                surface.blit(shell,  shell.get_rect( topleft=(450, 2)))

                hRect.center = (tank.x, tank.y-35); hRectU.topleft = hRect.topleft

                pygame.draw.rect(surface, (80,80,80), hRect)
                pygame.draw.rect(surface, (255,0,0), hRectU)
                pygame.draw.rect(surface, (20,20,20), hRect, 1)

            if tank.health <= 0:
                self.tanks.remove(tank)
                self.text = self.font.render('Player {} destroyed'.format(i+1), True, [50]*3)

        #if len(self.tanks) == 1:
        #    self.text = self.font.render('Player
                
            
        Projectile.draw(surface)
