import pygame
from core.baseState import baseState
from core.terrainGenerator import Terrain
from core.player import Player

class GameState(baseState):
    def __init__(self):
        super(GameState, self).__init__()
        self.terrain = Terrain(*self.s_rect.size)

    def startup(self, persistent):
        self.persist = persistent
        if not self.persist['terrainLoaded']:
            self.terrain.generateTerrain()
            self.persist['terrainLoaded'] = True
            self.players = [Player(60,60)]

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'START'
                self.done = True

    def update(self, dt, f_time):
        key = pygame.key.get_pressed()
        for player in self.players:
            player.update(dt, key, self.terrain.pixels)
        
    def draw(self, surface):
        surface.blit(self.terrain.surface, (0,0))
        for player in self.players:
            player.draw(surface)

        coords = self.players[0].getCoords()
        coords = self.font.render(str(coords), True, (200,200,200))
        surface.blit(coords, coords.get_rect(topright=self.s_rect.topright))
