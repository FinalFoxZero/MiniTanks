import pygame
from core.projectile import Projectile
from core.tankBase   import TankBase
from math import cos, sin, radians

def drawCross(pos, size=10, color=(255,255,255)):
    surf = pygame.display.get_surface()
    pygame.draw.line(surf, color, (pos[0]-size//2, pos[1]), (pos[0]+size//2, pos[1]))
    pygame.draw.line(surf, color, (pos[0], pos[1]-size//2), (pos[0], pos[1]+size//2))

class Player(TankBase):
    def __init__(self, x, y, tank_top, tank_bot):
        super(Player, self).__init__(x, y)
        self.img_top = tank_top
        self.img_bot = tank_bot
        self.imTR  = self.img_top.get_rect()
        self.imBR  = self.img_bot.get_rect()
        self.turr_pos = [0,0]
        self.fire_vec = [0,0]

        self.turnDone = False
        self.fired    = False

    def controls(self, dt, key):
        speed_cont = 30
        if   key[pygame.K_LSHIFT]: speed_cont = 60
        elif key[pygame.K_LCTRL]:  speed_cont = 10

        if   key[pygame.K_RIGHT]:  self.angle -= dt * speed_cont
        elif key[pygame.K_LEFT]:   self.angle += dt * speed_cont

        if   key[pygame.K_UP]:     self.power += dt * speed_cont
        elif key[pygame.K_DOWN]:   self.power -= dt * speed_cont

        self.angle = round(self.angle, 2)
        self.power = round(self.power, 2)

        if   self.angle <   0: self.angle = 0
        elif self.angle > 180: self.angle = 180

        rx,ry,ang = 20, 0, radians(self.angle)
        self.fire_vec[0] = (rx * cos(-ang)) - (ry * sin(-ang)) + self.turr_pos[0]
        self.fire_vec[1] = (ry * cos(-ang)) + (rx * sin(-ang)) + self.turr_pos[1]

        if self.power > 100: self.power = 100
        elif self.power < 0: self.power = 0

        if key[pygame.K_SPACE] and self.ammo[self.active] > 0 and not self.fired:
            self.trajectory = []
            Projectile(self)
            self.ammo[self.active] -= 1
            self.fired = True

    def takeTurn(self, dt, key):
        self.controls(dt, key)

    def update(self, dt):
        self.turnDone = False
        self.imBR.midbottom = (self.x, self.y)
        self.turr_pos = (self.x, self.y - 14)

        self.collision(dt)

    def draw(self, surface):
        self.drawGhost(surface)
        rotated = pygame.transform.rotate(self.img_top.copy(), self.angle)

        surface.blit(rotated, rotated.get_rect(center=self.turr_pos))
        surface.blit(self.img_bot, self.imBR)
        #drawCross(self.fire_vec)
        
