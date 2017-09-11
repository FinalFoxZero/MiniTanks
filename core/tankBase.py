import pygame

class TankBase(object):
    terrain = None
    def __init__(self, x, y):
        self.s_rect  = pygame.display.get_surface().get_rect()
        self.x = x
        self.y = y
        self.power = 0
        self.angle = 0
        self.trajectory  = []
        self.ammo_count  = {'Small_Shell':99}
        self.active_ammo = 'Small_Shell'

    def screen_collision(self):
        if self.x < 5: self.x = 5
        elif self.x > self.s_rect.w-5:
            self.x = self.s_rect.w-5

        if self.y < 5: self.y = 5
        elif self.y > self.s_rect.h-5:
            self.y = self.s_rect.h-5

    def ground_collision(self, dt):
        px = TankBase.terrain.pixels[self.y][self.x].x
        py = TankBase.terrain.pixels[self.y][self.x].y
        pc = TankBase.terrain.pixels[self.y][self.x].col

        if self.x == px and self.y == py \
           and pc == True: self.y = py
        else: self.y += int(dt * 60)

    def update(self, dt):
        self.screen_collision()
        self.ground_collision(dt)

    def draw(self, surface):
        pass

    def getTerrain(self):
        return(TankBase.terrain)

    @classmethod
    def setTerrain(cls, terrain_array):
        cls.terrain = terrain_array
