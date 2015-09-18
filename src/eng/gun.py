import pymunk as pm
import pygame
from pygame.color import *
from pygame.mixer import *
import math
from bullet import Bullet
from pa_poly import PAPoly

class Gun(object):
    
    def __init__(self, stage, pos_x, pos_y, width, height, elasticity, friction, rotation_speed):
        #The cannon should be made so that it can only hold one ball at a time and can only shoot if it has a ball in it
        self.stage = stage
        
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.cannonShoot = pygame.mixer.Sound(self.stage.sound_path+"boop.ogg")
        self.cannonShoot.set_volume(self.stage.player.volume)

        self.body = pm.Body(pm.inf, pm.inf)
        self.body.position = (pos_x,pos_y)
        self.width = width
        self.height = height
        
#        self.cannon_shape = pm.Poly(self.body,  [(-width,-height), (-width,height),(width,height),(width,-height)] ,(0, 0), False)
        self.cannon_shape = PAPoly(self.body,  [(-width,-3*height), (-width,-height),(width,-height),(width,-3*height)] ,(0, 0), False, self)
        self.cannon_shape.elasticity = elasticity
        self.cannon_shape.friction = friction
        
        #make 3 the collision type for cannons
        #self.cannon_shape.collision_type = 3
        
        self.rot_speed = rotation_speed

        #self.stage.space.add(self.cannon_shape) #the body is not added to the space
        #self.stage.cannons.append(self)
        self.capacity_upgrade_level = 0
        self.capacity_upgrade_level_max = 3
        self.rate_upgrade_level = 0
        self.rate_upgrade_level_max = 3
        self.impulse_upgrade_level = 0
        self.impulse_upgrade_level_max = 3
#================================================================================
#    This is a test for bullet capacity
#    it should be a parameter in the future
#================================================================================
        self.max_bullets = 3 
        self.bullets_curr = self.max_bullets
        self.reload_rate = 1.1 #frequency of reloads
        self.last_reload_time = 0.0
        
        self.gun = pygame.image.load(self.stage.graphics_path + "cannon.png").convert_alpha()
        self.gun2 = pygame.image.load(self.stage.graphics_path + "cannon2.png").convert_alpha() 
        
    def shoot(self, impulse):
        if self.bullets_curr > 0:
            self.cannonShoot.play()
            pos_x = self.body.position.x + math.sin(self.body.angle)*(3*self.height+10)
            pos_y = self.body.position.y + math.cos(self.body.angle)*-(3*self.height+10)
            
            #create the ball and fire it using the magnitude of the force 
            new_ball = Bullet(self.stage, pos_x, pos_y ,2.0,10,0.7,self.stage.bullet_color) 
            new_ball.body.apply_impulse((math.sin(self.body.angle)*impulse,-math.cos(self.body.angle)*impulse + (75 * self.impulse_upgrade_level)),(0,0))
            self.bullets_curr -= 1
            
            
    def move_left(self):
        if self.body.angle + self.rot_speed <= 3*math.pi/2:
            self.body.angle = self.body.angle + self.rot_speed
            #print self.body.angle
    
    def move_right(self):
        if self.body.angle - self.rot_speed >= math.pi/2:
            self.body.angle = self.body.angle - self.rot_speed
            #print self.body.angle

    def draw_self(self,player_num):
            #need to rotate and place based on position of cannon_shape
            if player_num == 0:
                gun_turned = pygame.transform.rotate(self.gun, (self.body.angle*180)/math.pi)
            else:
                gun_turned = pygame.transform.rotate(self.gun2, (self.body.angle*180)/math.pi)
            gun_flipped = pygame.transform.flip(gun_turned, True, True)
            
            if self.body.angle > math.pi:
                xpos = -math.cos(self.body.angle) * (-self.width - 3) + -math.sin(self.body.angle) * (-3*self.height - 3) 
                ypos = -math.sin(self.body.angle) * (-self.width - 3) + -math.cos(self.body.angle) * (-3*self.height - 3) 
            else:
                xpos = -math.cos(self.body.angle) * (-self.width - 3) + -math.sin(self.body.angle) * (-self.height + 3) 
                ypos = -math.sin(self.body.angle) * (self.width + 3) + -math.cos(self.body.angle) * (-3*self.height - 3) 
            
            self.stage.screen.blit(gun_flipped, (self.cannon_shape.body.position.x+self.stage.x_offset + xpos, self.stage.display_height - self.cannon_shape.body.position.y + ypos))