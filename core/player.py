import pygame
from core.projectile import Projectile
from core.tankBase import TankBase

class Player(TankBase):
    def __init__(self, x, y, tank_top, tank_bot):
        super(Player, self).__init__(x, y)
        self.imTop = tank_top
        self.imBot = tank_bot
        self.imTR  = self.imTop.get_rect()
        self.imBR  = self.imBot.get_rect()
        self.tx    = 0
        self.ty    = 0
        self.turn  = False
        self.timer = 0

    def controls(self, dt, key):
        speed_cont = 30 # dt * 30 = fps(in ms) * 30 = 1 tick per second
        if key[pygame.K_LSHIFT]:  speed_cont = 60
        elif key[pygame.K_LCTRL]: speed_cont = 10
        if key[pygame.K_RIGHT]:  self.angle -= dt * speed_cont
        elif key[pygame.K_LEFT]: self.angle += dt * speed_cont
        if key[pygame.K_UP]:     self.power += dt * speed_cont
        elif key[pygame.K_DOWN]: self.power -= dt * speed_cont

        self.angle = round(self.angle, 2)
        self.angle %= 360
        self.power = round(self.power, 2)

        if self.power > 100: self.power = 100
        elif self.power < 0: self.power = 0

        if key[pygame.K_SPACE] and self.ammo_count[self.active_ammo] > 0 \
           and self.timer > 30:
            Projectile(self, self.tx, self.ty, self.power, self.angle)
            self.ammo_count[self.active_ammo] -= 1
            self.timer = 0

    def update(self, dt, key):
        self.imBR.midbottom = (self.x, self.y)
        self.tx = self.imBR.centerx - 4
        self.ty = self.imBR.centery - 6

        if self.turn:
            self.controls(dt, key)
        self.timer += 1

        self.screen_collision()
        self.ground_collision(dt)

    def draw(self, surface):
        rotated = pygame.transform.rotozoom(self.imTop.copy(), self.angle, 1)
        surface.blit(rotated, rotated.get_rect(center=(self.tx, self.ty)))
        surface.blit(self.imBot, self.imBR)
        
