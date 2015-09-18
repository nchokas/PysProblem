import pymunk as pm
import pygame
from pygame.color import *
import math

class Spinner(object):
    
    def __init__(self, stage, pos_x, pos_y, width, height, elasticity, friction, rotation_speed, movement_speed, x_min, x_max):
        self.stage = stage
        
        self.body = pm.Body(pm.inf, pm.inf)
        self.body.position = (pos_x,pos_y)
        self.width = width
        self.height = height
        
        self.seg1 = pm.Segment(self.body, (-width/2,0), (width/2,0), 10)
        self.seg2 = pm.Segment(self.body, (0,-height/2), (0,height/2), 10)

        
        self.seg1.elasticity = elasticity
        self.seg1.friction = friction
        
        self.seg2.elasticity = elasticity
        self.seg2.friction = friction
        
        
        self.rot_speed = rotation_speed
        self.mov_speed = movement_speed
        
        self.x_min = x_min
        self.x_max = x_max
        
        self.stage.space.add(self.seg1, self.seg2) #the body is not added to the space 

        self.spinner_graphic = pygame.image.load(self.stage.graphics_path + "spinner.png").convert_alpha()
        
    def move(self):
        self.body.angle = self.body.angle + self.rot_speed
        
        if (self.body.position.x + self.mov_speed > self.x_max) or (self.body.position.x + self.mov_speed < self.x_min):
            self.mov_speed = -self.mov_speed
            
        self.body.position.x = self.body.position.x + self.mov_speed
        
    def draw_self(self):
            spinner_scaled = pygame.transform.scale(self.spinner_graphic, (self.stage.spinner_size + 2, self.stage.spinner_size + 2))
            spinner_turned = pygame.transform.rotate(spinner_scaled, (self.body.angle*180)/math.pi)
            spinner_flipped = pygame.transform.flip(spinner_turned, True, True)
            #spinner_scaled = pygame.transform.scale(spinner_flipped, (int((.14645*math.cos(self.body.angle - math.pi/4) + .85355)*2*self.width), int((.14645*math.cos(self.body.angle - math.pi/4) + .85355)*2*self.height)))

            #spinner_scaled = pygame.transform.scale(spinner_flipped, (2*self.width, 2*self.height))
                     
            #this gets a number between root2/2 and 1 based on angle
            #print (.14645*math.cos(self.body.angle) + .85355)
            
            if self.body.angle <= 0 and self.body.angle > -math.pi/2:
                #print "down to left"
                xpos = math.cos(self.body.angle) * (-self.stage.spinner_size/2 - 2) + -math.sin(self.body.angle) * (-self.stage.spinner_size/2 - 2) 
                ypos = -math.sin(self.body.angle) * (-self.stage.spinner_size/2 - 2) + -math.cos(self.body.angle) * (self.stage.spinner_size/2 + 2) 
            elif self.body.angle <= -math.pi/2 and self.body.angle > -math.pi:
                #print "left to up"
                xpos = -math.cos(self.body.angle) * (-self.stage.spinner_size/2 - 2) + -math.sin(self.body.angle) * (-self.stage.spinner_size/2  - 2) 
                ypos = -math.sin(self.body.angle) * (-self.stage.spinner_size/2 - 2) + -math.cos(self.body.angle) * (-self.stage.spinner_size/2 - 2) 
            elif self.body.angle <= -math.pi and self.body.angle > -3*math.pi/2:
                #print "up to right"
                xpos = -math.cos(self.body.angle) * (-self.stage.spinner_size/2 - 2) + math.sin(self.body.angle) * (-self.stage.spinner_size/2 - 2) 
                ypos = math.sin(self.body.angle) * (-self.stage.spinner_size/2 - 2) + -math.cos(self.body.angle) * (-self.stage.spinner_size/2 - 2)
            else:
                #print "right to down"
                xpos = math.cos(self.body.angle) * (-self.stage.spinner_size/2 - 2) + math.sin(self.body.angle) * (-self.stage.spinner_size/2 -2) 
                ypos = math.sin(self.body.angle) * (-self.stage.spinner_size/2 - 2) + math.cos(self.body.angle) * (-self.stage.spinner_size/2 -2)
                
            self.stage.screen.blit(spinner_flipped, (self.body.position.x+self.stage.x_offset + xpos, self.stage.display_height - self.body.position.y + ypos))
    
                
            
#            body = self.seg1.body
#            pv1 = body.position + self.seg1.a.rotated(math.degrees(body.angle))
#            pv2 = body.position + self.seg1.b.rotated(math.degrees(body.angle))
#            p1 = self.stage.to_pygame(pv1)
#            p2 = self.stage.to_pygame(pv2)
#            pygame.draw.lines(self.stage.screen,THECOLORS["lightgray"], False, [p1,p2])
#            
#            body = self.seg2.body
#            pv1 = body.position + self.seg2.a.rotated(math.degrees(body.angle))
#            pv2 = body.position + self.seg2.b.rotated(math.degrees(body.angle))
#            p1 = self.stage.to_pygame(pv1)
#            p2 = self.stage.to_pygame(pv2)
#            pygame.draw.lines(self.stage.screen,THECOLORS["lightgray"], False, [p1,p2])