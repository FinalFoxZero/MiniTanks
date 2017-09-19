import pygame
from math import *
from random import choice, random

def addVectors(ang1, len1, ang2, len2):
    x = sin(ang1) * len1 + sin(ang2) * len2
    y = cos(ang1) * len1 + cos(ang2) * len2
    length, angle = hypot(x,y), (0.5 * pi - atan2(y,x))
    return( angle, length )

class Projectile:
    terrain = None
    tank_ls = []

    pList = []
    drag  = 0.995
    grav  = (pi, 0.981)
    wind  = (radians(90), 1.0)

    def __init__(self, user):
        self.user = user
        self.x   = user.fire_vec[0]
        self.y   = user.fire_vec[1]
        self.vel = (user.power / 100) * 50
        self.ang = radians(-(user.angle-90))
        self.scl = 2
        self.rad = 24
        self.damage = 50
        Projectile.pList.append(self)

    def _calculateDamage(self):
        for tank in Projectile.tank_ls:
            dis = sqrt((self.x - tank.x)**2 + (self.y - tank.y)**2)
            if dis < self.rad:
                damage = (1 - dis / self.rad) * self.damage
                tank.health -= int(damage)
  
    def _collision(self):
        terrain_array = Projectile.terrain.pixels
        sw, sh = Projectile.terrain.sWidth, Projectile.terrain.sHeight

        if (0 > self.x > sw) or (self.y > sh): return(True)

        elif (0 < self.x < sw) and (0 < self.y < sh):
            cut = False

            for tank in Projectile.tank_ls:
                if tank.imBR.collidepoint((self.x,self.y)):
                    tank.health -= self.damage
                    return(True)
                
            if terrain_array[int(self.y)][int(self.x)].col:
                cut = True

            if cut:
                Projectile.terrain.cutSection((int(self.x),int(self.y)), self.rad)
                self._calculateDamage()
                return(True)

    def _update(self, dt):
        self.ang, self.vel = addVectors(self.ang, self.vel, *Projectile.grav)
        self.ang, self.vel = addVectors(self.ang, self.vel, *Projectile.wind)
        self.vel *= Projectile.drag
        self.x += sin(self.ang) * (dt * (self.vel * 10))
        self.y -= cos(self.ang) * (dt * (self.vel * 10))
        self.user.trajectory.append((self.x, self.y))

    def _draw(self, surface):
        pygame.draw.circle(surface, (160,160,160),
                           (int(self.x), int(self.y)), self.scl)

    @classmethod
    def randomWind(cls):
        cls.wind = (choice([90,180]), random())

    @classmethod
    def update(cls, dt):
        for proj in cls.pList:
            proj._update(dt)
            if proj._collision():
                cls.pList.remove(proj)
                proj.user.turnDone = True
                proj.user.fired    = False
                

    @classmethod
    def draw(cls, surface):
        for proj in cls.pList: proj._draw(surface)
