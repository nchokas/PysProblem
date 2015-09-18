import pymunk as pm, pygame
from ball import Ball
from pygame.color import *

class Bullet(Ball):
    def __init__(self, stage, pos_x, pos_y, circle_mass, radius, circle_elasticity, color):
        Ball.__init__(self, stage, pos_x, pos_y, circle_mass, radius, circle_elasticity, color)
        self.circle.collision_type = 1
        self.point_value = 0

        self.gun_bullet = pygame.image.load(self.stage.graphics_path + "gunbullet.png").convert_alpha()
        self.cannon_bullet = pygame.image.load(self.stage.graphics_path + "cannonbullet.png").convert_alpha()        
        
    def draw_self(self):
        new_pos_y = self.stage.display_height-int(self.body.position.y)-self.radius -2 
        p = int(self.body.position.x+self.stage.x_offset-self.radius - 2), new_pos_y
        
        if self.color == "yellow": #this is a gun bullet
            self.stage.screen.blit(self.gun_bullet, p)
        if self.color == "green": #this is a gun bullet
            self.stage.screen.blit(self.cannon_bullet, p)
            
        

            