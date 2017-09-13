import pygame
from math import *
from random import choice, random

def addVectors(ang1, len1, ang2, len2):
    x = sin(ang1) * len1 + sin(ang2) * len2
    y = cos(ang1) * len1 + cos(ang2) * len2
    length, angle = hypot(x,y), (0.5 * pi - atan2(y,x))
    return( angle, length )

#       0
#       ^
# 180 < o > 90
#       v
#      360

class Projectile:
    pList = []
    drag  = 0.995
    grav  = (pi, 0.981)
    wind  = (radians(90), 1.0)

    def __init__(self, user, x, y, velocity, angle):
        self.user = user
        self.x   = x
        self.y   = y
        self.vel = velocity
        self.ang = radians(-(angle-90))
        self.scl = 3
        self.rad = 24
        Projectile.pList.append(self)

    def calculate_tank_collision(self, tankList):
        for tank in tankList:
            pass
        

    def _collision(self, tanks=None):
        terrain = self.user.getTerrain()
        terrain_array = terrain.pixels

        if (0 > self.x > self.user.s_rect.w) or \
            (self.y > self.user.s_rect.h):
            return(True)

        elif (0 < self.x < self.user.s_rect.w) and \
            (0 < self.y < self.user.s_rect.h):
            if terrain_array[int(self.y)][int(self.x)].col:
                terrain.cutSection((int(self.x),int(self.y)), self.rad)
                return(True)

    def _update(self, dt):
        self.ang, self.vel = addVectors(self.ang, self.vel, *Projectile.grav)
        self.ang, self.vel = addVectors(self.ang, self.vel, *Projectile.wind)
        self.vel *= Projectile.drag
        self.x += sin(self.ang) * (dt * (self.vel * 10))
        self.y -= cos(self.ang) * (dt * (self.vel * 10))

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

    @classmethod
    def draw(cls, surface):
        for proj in cls.pList: proj._draw(surface)
