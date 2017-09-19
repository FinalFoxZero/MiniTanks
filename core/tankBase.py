import pygame

projectile_types = {'Small Shell':999,
                    'Large Shell':999,
                    'Shatter Shell':999}

class TankBase(object):
    terrain = None
    player_count = 1
    def __init__(self, x, y):
        self.s_rect  = pygame.display.get_surface().get_rect()
        self.x = x
        self.y = y
        self.health = 100
        self.power  = 0
        self.angle  = 0
        self.trajectory  = []
        self.ammo   = projectile_types
        self.active = 'Small Shell'
        self.player = TankBase.player_count
        TankBase.player_count += 1

    def collision(self, dt):
        if self.x < 5: self.x = 5
        elif self.x > self.s_rect.w-5:
            self.x = self.s_rect.w-5

        if self.y < 5: self.y = 5
        elif self.y > self.s_rect.h-5:
            self.y = self.s_rect.h-5
        
        px = TankBase.terrain.pixels[self.y][self.x].x
        py = TankBase.terrain.pixels[self.y][self.x].y
        pc = TankBase.terrain.pixels[self.y][self.x].col

        if self.x == px and self.y == py \
           and pc == True: self.y = py
        else: self.y += int(dt * 60)

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def drawGhost(self, surface):
        if len(self.trajectory) > 2:
            for p in range(len(self.trajectory)-1):
                point_1, point_2 = self.trajectory[p], self.trajectory[p+1]
                pygame.draw.line(surface, [150]*3, point_1, point_2)
