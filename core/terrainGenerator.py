import pygame
from random import uniform, randint, random
from math import cos, sin


class Pix(object):
    def __init__(self, x, y, collision=True, destructable=True):
        self.x = x
        self.y = y
        self.col = collision
        self.des = destructable

class Terrain(object):
    def __init__(self, s_width, s_height):
        self.sWidth  = s_width
        self.sHeight = s_height
        self.pixels  = []
        self.surface = pygame.Surface((s_width, s_height),
                                      pygame.SRCALPHA | pygame.HWSURFACE)

    def resetTerrain(self):
        self.pixels = []
        self.surface = pygame.Surface((self.sWidth, self.sHeight),
                                      pygame.SRCALPHA | pygame.HWSURFACE )

    def pickLocation(self):
        x = randint(10, self.sWidth-10)
        y = sorted(self.pixels[i][x].y for i in range(len(self.pixels)))[0]
        return(x,y)

    def generateHeight(self):
        x_array = []
        rP_0, rP_1, rP_2, rP_3 = [randint(-5000, 5000) for i in range(4)] #random phase x4
        rA_l = randint(1, 5)  # low   amp
        rA_m = randint(3, 20) # mid   amp
        rA_h = randint(5, 50) # high  amp
        rA_u = randint(8, 80) # ultra amp
        rF_l = uniform(8, 20)   # low   freq
        rF_m = uniform(12, 32)  # mid   freq
        rF_h = uniform(30, 75)  # high  freq
        rF_u = uniform(50, 100) # ultra freq
        for x in range(self.sWidth):
            s0 = cos( (x + rP_0) / rF_l ) * rA_l + (self.sHeight - 200) # low cos
            s1 = sin( (x + rP_1) / rF_m ) * rA_m + (self.sHeight - 150) # mid sin
            s2 = sin( (x + rP_2) / rF_h ) * rA_h + (self.sHeight - 300) # high sin
            s3 = cos( (x + rP_3) / rF_u ) * rA_u + (self.sHeight - 500) # ultra cos
            c0 = (s0 + s1) / 2 # combine low and mid
            c1 = (s2 + s3) / 2 # combine high and ultra
            c2 = (s0 + s3) / 2 # combine low and ultra
            comb = (c0 + c1) / 2 + (c2 + s3)
            if comb > self.sHeight:
                delta = comb - self.sHeight
                comb += delta
            x_array.append( int(comb) )
        return( x_array )

    def generateTerrain(self):
        generated_world = self.generateHeight()
        for y in range(self.sHeight):
            y_temp = []
            for x, a in enumerate(generated_world):
                if y >= a:
                    rShade = abs(int(((self.sHeight - (y - (a-200))) / self.sHeight) * 255))
                    if rShade > 255: rShade = 255
                    elif rShade < 0: rShade = 0
                    rCol = pygame.Color(rShade,rShade,rShade)
                    self.surface.fill(rCol, (x,y,1,1))
                    y_temp.append( Pix(x,y) )
                else:
                    y_temp.append( Pix(2048, 2048, False) )
            self.pixels.append(y_temp)
            y_temp = []

    def pointsInCircle(self, position, radius):
        circle = []; x, y = position; r = radius
        for i in range(x-r, x+r):
            for j in range(y-r, y+r):
                if ((i-x)*(i-x) + (j-y)*(j-y)) <= r*r:
                    if (0<i<self.sWidth) and (0<j<self.sHeight):
                        circle.append((i,j))
        return( circle )

    def cutSection(self, position, radius):
        circlePoints = self.pointsInCircle(position, radius)
        for x,y in circlePoints:
            point = self.pixels[y][x]
            if (x,y) == (point.x, point.y):
                point.x = 2048; point.y = 2048
                point.col = False
                self.surface.fill((0,0,0,0), (x,y,1,1))
