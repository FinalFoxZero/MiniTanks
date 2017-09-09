import pygame


class Player(object):
    def __init__(self, x, y, tank_top, tank_bot):
        self.s_rect = pygame.display.get_surface().get_rect()
        self.imTop = tank_top
        self.imBot = tank_bot
        self.imTR  = self.imTop.get_rect()
        self.imBR  = self.imBot.get_rect()
        self.x = x
        self.y = y
        self.power = 0
        self.angle = 0
        self.turn  = True
        self.trajectory = []
        self.ammo = {'Small Shell': 999}

    def getCoords(self):
        return((self.x, self.y), (self.px, self.py), self.pc)

    def controls(self, dt, key):
        speed_cont = 30 # dt * 30 = fps(in ms) * 30 = 1 tick per second
        if key[pygame.K_LSHIFT]: speed_cont = 60
        if key[pygame.K_LCTRL]:  speed_cont = 15
        #if key[pygame.K_w]:      self.y -= int(dt * 120)
        #elif key[pygame.K_s]:    self.y += int(dt * 60)
        #if key[pygame.K_a]:      self.x -= int(dt * 60)
        #elif key[pygame.K_d]:    self.x += int(dt * 60)

        if key[pygame.K_RIGHT]:  self.angle -= dt * speed_cont
        elif key[pygame.K_LEFT]: self.angle += dt * speed_cont

        if key[pygame.K_UP]:     self.power += dt * speed_cont
        elif key[pygame.K_DOWN]: self.power -= dt * speed_cont

        self.angle = round(self.angle, 2)
        self.angle %= 360

        self.power = round(self.power, 2)
        if self.power > 100: self.power = 100
        elif self.power < 0: self.power = 0

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
        self.imBR.midbottom = (self.x, self.y)
        if self.turn:
            self.controls(dt, key)
            self.collision(dt, tArray)

    def draw(self, surface):
        #rect = pygame.Rect((0,0), (24,10))
        #rect.midbottom = (self.x, self.y)
        #pygame.draw.rect(surface, self.color, rect)
        rotated = pygame.transform.rotozoom(self.imTop.copy(), self.angle, 1)

        tOffset_x = self.imBR.centerx - 4
        tOffset_y = self.imBR.centery - 6

        surface.blit(rotated, rotated.get_rect(center=(tOffset_x, tOffset_y)))
        surface.blit(self.imBot, self.imBR)
        
