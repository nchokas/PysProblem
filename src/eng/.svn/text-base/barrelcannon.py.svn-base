import pymunk as pm
import pygame
from pygame.color import *
import math
from bullet import Bullet
from pa_poly import PAPoly

class Barrelcannon(object):
    
    def __init__(self, stage, pos_x, pos_y, width, height, elasticity, friction, rotation_speed, movement_speed, x_min, x_max):
        #The cannon should be made so that it can only hold one ball at a time and can only shoot if it has a ball in it
        self.stage = stage
        
        self.body = pm.Body(pm.inf, pm.inf)
        self.body.position = (pos_x,pos_y)
        self.width = width
        self.height = height
        
#        self.cannon_shape = pm.Poly(self.body,  [(-width,-height), (-width,height),(width,height),(width,-height)] ,(0, 0), False)
        self.cannon_shape = PAPoly(self.body,  [(-width,-height), (-width,height),(width,height),(width,-height)] ,(0, 0), False, self)
        self.cannon_shape.elasticity = elasticity
        self.cannon_shape.friction = friction
        
        #make 3 the collision type for cannons
        self.cannon_shape.collision_type = 3
        
        self.rot_speed = rotation_speed
        self.mov_speed = movement_speed
        
        self.x_min = x_min
        self.x_max = x_max
        
        #boolean value to indicate whether there is a bullet in the cannon
        self.loaded = False
        
        self.stage.space.add(self.cannon_shape) #the body is not added to the space
        self.stage.cannons.append(self)
        
        self.upgrade = 0
        self.upgrade_max = 2
        
        self.BC_unloaded = pygame.image.load(self.stage.graphics_path + "bc.png").convert_alpha()
        self.BC_loaded = pygame.image.load(self.stage.graphics_path + "bcloaded.png").convert_alpha()
         
    def shoot(self, impulse):
        if self.loaded:
            #update 3/23/2009
#            upgrade 0 - 1 ball straight ahead
#            upgrade 1 - 3 balls fanning out
#            upgrade 2 - 5 balls fanning out           
            
            #this method will shoot the ball that is inside the cannon
            #print self.upgrade
            self.impulse = impulse + 150*self.upgrade 
            #calculate the location 
            # TODO: the 10 is the radius of the ball and should not be hard coded in the future
            # it would probably be a good idea to get the info from the ball that goes into the cannon
            
            for count in range (-self.upgrade, self.upgrade + 1):
                ten_degrees = 0.174532925
                pos_x = self.body.position.x + math.sin(self.body.angle + ten_degrees * count)*(self.height+10)
                pos_y = self.body.position.y + math.cos(self.body.angle + ten_degrees * count)*-(self.height+10)
                
                new_ball = Bullet(self.stage, pos_x, pos_y ,2.0,10,0.7,"green")
                new_ball.body.apply_impulse((math.sin(self.body.angle + ten_degrees * count)*self.impulse,-math.cos(self.body.angle + ten_degrees * count)*impulse),(0,0))
                
#            pos_x = self.body.position.x + math.sin(self.body.angle)*(self.height+10)
#            pos_y = self.body.position.y + math.cos(self.body.angle)*-(self.height+10)
#            
#            #create the ball and fire it using the magnitude of the force 
#            new_ball = Bullet(self.stage, pos_x, pos_y ,2.0,10,0.7,"green")
#            new_ball.body.apply_impulse((math.sin(self.body.angle)*force,-math.cos(self.body.angle)*force),(0,0))
            
            self.loaded = False
    
            
    def collect(self):    
        #this method will suck in the ball
        #print 'load'
        if self.loaded == False:
            self.loaded = True
        
    def move(self):
        #this method will move the cannon
        self.body.angle = self.body.angle + self.rot_speed
        
        if (self.body.position.x + self.mov_speed > self.x_max) or (self.body.position.x + self.mov_speed < self.x_min):
#            print "xmax: ", self.x_max
#            print "position: ", self.body.position.x
#            print "speed: ", self.mov_speed
#            print "changing directions"
            self.mov_speed = -self.mov_speed
            
        self.body.position.x = self.body.position.x + self.mov_speed
        
    def draw_self(self):
        if self.loaded:
            cannon_turned = pygame.transform.rotate(self.BC_loaded, (self.body.angle*180)/math.pi)
        else: 
            cannon_turned = pygame.transform.rotate(self.BC_unloaded, (self.body.angle*180)/math.pi)
        
        cannon_flipped = pygame.transform.flip(cannon_turned, True, True)
            #can account for the black outline too but it is negligible
            
        if self.body.angle <= 0 and self.body.angle > -math.pi/2:
            #print "down to left"
            xpos = math.cos(self.body.angle) * (-self.width) + -math.sin(self.body.angle) * (-self.height) 
            ypos = -math.sin(self.body.angle) * (-self.width) + -math.cos(self.body.angle) * (self.height) 
        elif self.body.angle <= -math.pi/2 and self.body.angle > -math.pi:
            #print "left to up"
            xpos = -math.cos(self.body.angle) * (-self.width) + -math.sin(self.body.angle) * (-self.height) 
            ypos = -math.sin(self.body.angle) * (-self.width) + -math.cos(self.body.angle) * (-self.height) 
        elif self.body.angle <= -math.pi and self.body.angle > -3*math.pi/2:
            #print "up to right"
            xpos = -math.cos(self.body.angle) * (-self.width) + math.sin(self.body.angle) * (-self.height) 
            ypos = math.sin(self.body.angle) * (-self.width) + -math.cos(self.body.angle) * (-self.height)
        else:
            #print "right to down"
            xpos = math.cos(self.body.angle) * (-self.width) + math.sin(self.body.angle) * (-self.height) 
            ypos = math.sin(self.body.angle) * (-self.width) + math.cos(self.body.angle) * (-self.height)
            
        self.stage.screen.blit(cannon_flipped, (self.body.position.x+self.stage.x_offset + xpos, self.stage.display_height - self.body.position.y + ypos))