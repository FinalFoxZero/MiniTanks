import pygame


class Player(object):
    def __init__(self, x, y):
        self.s_rect = pygame.display.get_surface().get_rect()
        self.x = x
        self.y = y
        self.color = (255,0,0)
        self.power = 0
        self.angle = 0

        self.px = 0
        self.py = 0
        self.pc = False

    def getCoords(self):
        return((self.x, self.y), (self.px, self.py), self.pc)

    def controls(self, dt, key):
        if key[pygame.K_w]:      self.y -= int(dt * 120)
        elif key[pygame.K_s]:    self.y += int(dt * 60)
        
        if key[pygame.K_a]:      self.x -= int(dt * 60)
        elif key[pygame.K_d]:    self.x += int(dt * 60)

        if key[pygame.K_RIGHT]:  self.angle += dt * 30
        elif key[pygame.K_LEFT]: self.angle -= dt * 30

        if key[pygame.K_UP]:     self.power += dt * 30
        elif key[pygame.K_DOWN]: self.power -= dt * 30
        self.angle %= 360

    def collision(self, dt, tArray):
        if self.x < 5: self.x = 5
        elif self.x > self.s_rect.w-5: self.x = self.s_rect.w-5

        if self.y < 5: self.y = 5
        elif self.y > self.s_rect.h-5: self.y = self.s_rect.h-5

        self.px = tArray[self.y][self.x].x
        self.py = tArray[self.y][self.x].y
        self.pc = tArray[self.y][self.x].col
        if self.x == self.px and self.y == self.py and self.pc == True:
            self.y = self.py
        else: self.y += int(dt * 60)

    def update(self, dt, key, tArray):
        self.controls(dt, key)
        self.collision(dt, tArray)

    def draw(self, surface):
        rect = pygame.Rect((0,0), (24,10))
        rect.midbottom = (self.x, self.y)
        pygame.draw.rect(surface, self.color, rect)
        
