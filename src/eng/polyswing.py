import pymunk as pm
import pygame
from pygame.color import *
from swingball import SwingBall
import math
from pygame.mixer import *

class Polyswing(object):
#    1: the stage the polyswing will belong to
#    2: the x position of the top 
#    3: the y position of the top
#    4: the half width of each section
#    5: the half height of each section
#    6: the mass of each section
#    7: the inertia of each section
#    8: the elasticity each section
#    9: the mass of the circle 
#    10: the radius of the circle
#    11: the elasticity of the circle 
#    12: number of segments
#    13: parent swing
#    14: maximum number of children this swing can have
#    15: tier
#    16: color/hitpoint of ball

#need to have a maximum amount of childswings
#if a childswing does not have a ball on it for x-seconds the whole thing gets dropped

    def __init__(self, stage, pos_x, pos_y, section_width, section_height, section_mass, section_intertia, section_elasticity, circle_mass, radius, circle_elasticity, num_segs, parent_swing, max_children, tier, color):
        
        #self.child_swing = None #max it out to 3
        self.stage = stage
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.vines = pygame.mixer.Sound(self.stage.sound_path+"vines.ogg")
        self.vines.set_volume(stage.player.volume)
        self.child_swings = []
        self.max_children = max_children
  
        self.section_mass = section_mass
        self.circle_mass = circle_mass
        self.tier = tier
        self.radius = radius
        
        self.removable = True
        self.num_segs = num_segs 
        self.section_width = section_width
        self.section_height = section_height
        
        #list of segments and their bodies
        self.sections = [] 
        self.bodies = []
        #list of joints
        self.rotation_center_joints = []
        self.parent_swing = parent_swing
        
        self.vine_top = pygame.image.load(self.stage.graphics_path + "vinetop.png").convert_alpha()
        self.vine_mid = pygame.image.load(self.stage.graphics_path + "vinemid.png").convert_alpha()
        self.vine_bot = pygame.image.load(self.stage.graphics_path + "vinebot.png").convert_alpha()
        
        self.vine_short = pygame.image.load(self.stage.graphics_path + "vineshort.png").convert_alpha()
        
        if parent_swing == None:
            self.rotation_center_body = pm.Body(pm.inf, pm.inf)
            self.rotation_center_body.position = (pos_x,pos_y)
            
            #adds to the stage
            self.stage.swings.append(self)
            #starts off connected
            self.stage.connected_swings.append(self)
      
            #loops to create all the sections and bodies for polygons
            for i in range(1,num_segs+1): 
                self.bodies.append(pm.Body(section_mass, section_intertia))
                self.bodies[i-1].position = (pos_x , pos_y - (2*section_height*(i-1)))
                
                self.sections.append(pm.Poly(self.bodies[i-1],  [(-section_width,-section_height), (-section_width,section_height),(section_width,section_height),(section_width,-section_height)] ,(0, 0), False))
                self.sections[i-1].elasticity = section_elasticity
            
                 
            self.ball = SwingBall(self.stage,self,pos_x,pos_y - ((2*section_height*num_segs) + (radius - section_height)),circle_mass,radius,circle_elasticity, color)
                
                   
            self.rotation_center_joints.append(pm.PinJoint(self.bodies[0], self.rotation_center_body, (0,0), (0,0)))
            
            #loops to create the joints
            for i in range(1,num_segs):       
#                self.rotation_center_joints.append(pm.PinJoint(self.bodies[i-1], self.bodies[i], (0,-(section_height)), (0,section_height)))
                self.rotation_center_joints.append(pm.SlideJoint(self.bodies[i-1], self.bodies[i], (0,0), (0,0), 0 , 9))
            
            #attaches the ball to the last joint
            self.rotation_center_joints.append(pm.PinJoint(self.bodies[num_segs-1], self.ball.body, (0,-section_height), (0,0)))  
            
            #adds the sections of the polygons to the space
            for section in self.sections:
                self.stage.space.add(section)
            
            #adds the bodies of the polygons to the space
            for body in self.bodies:
                self.stage.space.add(body)
                
            #adds the joints to the space
            for joint in self.rotation_center_joints:
                self.stage.space.add(joint)
        else: #if there is a parent swing argument, ignore the stage, x and y positions. only work if there is a ball
            
            #it should have a ball
#            if parent_swing.ball != None:
                #don't add the swing because we have reached the maximum number of children
                if (len(parent_swing.child_swings) < parent_swing.max_children):
#                    print "too many children, maximum is: " , parent_swing.max_children
                #if it is tier2, only attach if it's parent swing is attached, if tier3 only attach if grandparent swing is attached
#                elif (self.tier == 2 and self.parent_swing == None) or (self.tier == 3 and self.parent_swing == None and self.parent_swing.parent_swing == None):
#                    if (self.tier == 2 and self.parent_swing != None) or (self.tier == 3 and (self.parent_swing.parent_swing != None and self.parent_swing != None) ):

#may just need the if that checks the max child swing
                    parent_swing.child_swings.append(self)
                    
                    self.rotation_center_body = parent_swing.ball.body 
                    
                    pos_x = self.rotation_center_body.position.x 
                    pos_y = self.rotation_center_body.position.y - (parent_swing.ball.radius + section_height) 
                    #adds to the stage
                    self.stage.swings.append(self)
                    #starts off connected
                    self.stage.connected_swings.append(self)
                    
                    #loops 5 times to create all the sections and bodies for polygons
                    for i in range(1,num_segs+1): 
                        self.bodies.append(pm.Body(section_mass, section_intertia))
                        self.bodies[i-1].position = (pos_x , pos_y - (2*section_height*(i-1)))
                        
                        self.sections.append(pm.Poly(self.bodies[i-1],  [(-section_width,-section_height), (-section_width,section_height),(section_width,section_height),(section_width,-section_height)] ,(0, 0), False))
                        self.sections[i-1].elasticity = section_elasticity
                    
      
                    self.ball = SwingBall(self.stage,self,pos_x,pos_y - ((2*section_height*num_segs) + (radius - section_height)),circle_mass,radius,circle_elasticity,color) 
                         
           
                    self.rotation_center_joints.append(pm.PinJoint(self.bodies[0], self.rotation_center_body, (0,section_height), (0,0)))
                            
                    #loops to create the joints
                    for i in range(1,num_segs):       
#                        self.rotation_center_joints.append(pm.PinJoint(self.bodies[i-1], self.bodies[i], (0,-(section_height)), (0,section_height)))
                        self.rotation_center_joints.append(pm.SlideJoint(self.bodies[i-1], self.bodies[i], (0,0), (0,0), 0 , 9))
                        
                    #attaches the ball to the last joint
                    self.rotation_center_joints.append(pm.PinJoint(self.bodies[num_segs-1], self.ball.body, (0,-section_height), (0,0)))   
                    
                    #adds the sections of the polygons to the space
                    for section in self.sections:
                        self.stage.space.add(section)
                    
                    #adds the bodies of the polygons to the space
                    for body in self.bodies:
                        self.stage.space.add(body)
                        
                    #adds the joints to the space
                    for joint in self.rotation_center_joints:
                        self.stage.space.add(joint)
                                
                
                
    def destroy_joint(self, child_bonus, grandchild_bonus):
        try:
        #removes the last joint
            if self.removable == True:
                #remove from set of swings and add to fallen swings
#                self.stage.swings.remove(self)
#                self.stage.fallen_swings.append(self) 
                self.stage.space.remove(self.rotation_center_joints.pop(-1))
                #if the ball becomes detached them reset the multiplier to 1
                self.ball.point_multiplier = 1 
                self.ball = None
                self.removable = False
        #unties the relationship between a swing and its children
        #applies proper bonuses to children and grandchildren
        #when a swing disconnects its ball, that means the children and grandchildren become disconnected
                for child in self.child_swings:
                    #a tier 3 child could try to be removed as a child but it could already have been removed as a grandchild
                    try:
                        self.stage.connected_swings.remove(child)
                    except ValueError:
                        #print "already removed"
                        pass
                    if child.ball != None:
                        child.ball.point_multiplier = child_bonus
                    child.parent_swing = None
                    for grandchild in child.child_swings:
                        self.stage.connected_swings.remove(grandchild)
                        if grandchild.ball != None:
                            grandchild.ball.point_multiplier = grandchild_bonus
                        
                #self.child_swing.parent_swing = None
                
                self.child_swings = []
                self.vines.play()
#                print self.child_swings
        except IndexError:
#            print 'no more joints'
            pass    
        except AttributeError:
#            print 'no child already'
            pass
        except KeyError:
            #joint was already removed from space
            pass
            
    def respawn_ball(self, circle_mass,radius,circle_elasticity, color):
        
        #can only respawn ball if there's is already no ball
        #and if the swing is directly or indrectly connected to the tier1 unless it is the tier1
#        if self.ball == None and (self.tier == 1 or (self.tier == 2 and self.parent_swing != None) or (self.tier == 3 and self.parent_swing != None and self.parent_swing.parent_swing != None)):
        #may not need this if statement, the stage might already check
        pos_x = self.bodies[-1].position.x + math.sin(self.bodies[-1].angle)*(self.section_height+radius)
        pos_y = self.bodies[-1].position.y + math.cos(self.bodies[-1].angle)*-(self.section_height+radius) 
        

        self.ball = SwingBall(self.stage, self, pos_x, pos_y, circle_mass, radius,circle_elasticity, color)
        
              
        self.rotation_center_joints.append(pm.PinJoint(self.bodies[self.num_segs-1], self.ball.body, (0 ,-self.section_height), (0 ,0)))
            
        self.stage.space.add(self.rotation_center_joints[-1])
        self.removable = True
        return True
#        else:
#            return False

    def distance(self, p1, p2):
            x1 = p1.x
            x2 = p2.x
            
            y1 = p1.y
            y2 = p2.y
            return math.sqrt( ( x1-x2 )**2 + ( y1-y2 )**2 )
        
    def angle(self, p1, p2):
            x1 = p1.x
            x2 = p2.x
            
            y1 = p1.y
            y2 = p2.y
            return math.atan2(y2-y1, x2-x1)
        
    def draw_self(self):

        #draw all the segments
        #if the segment is below 0 then remove it from the space
        for section in self.sections:
            if section.body.position.y < -100:
                self.sections.remove(section) #remove from self
                self.stage.space.remove(section.body, section)
            else:
                
                #gets the 2 points and calculates the length if its not the last section
                if section != self.sections[-1]:
                    length = self.distance(section.body.position, self.sections[self.sections.index(section)+1].body.position)
                    angle = self.angle(section.body.position, self.sections[self.sections.index(section)+1].body.position)
#                    print angle
                    
                    if len(self.sections) == 2:
                        vine_scaled = pygame.transform.scale(self.vine_short, (6, int(length + 2)))
                    else: #its longer than 2
                        if section == self.sections[0]: #first section
                            vine_scaled = pygame.transform.scale(self.vine_top, (6, int(length + 2)))
                        elif section == self.sections[-2]: # second to last section
                            vine_scaled = pygame.transform.scale(self.vine_bot, (6, int(length + 2)))
                        else: #everything else
                            vine_scaled = pygame.transform.scale(self.vine_mid, (6, int(length + 2)))
                    
                    
                    vine_turned = pygame.transform.rotate(vine_scaled, 90 + (angle*180)/math.pi)
                    #vine_flipped = pygame.transform.flip(vine_turned, True, True)
                    
                    #at 0 degrees it points to the right and it rotates CCW
                    
                    if angle <= 0 and angle > -math.pi/2:

                        xpos = -math.sin(angle) * -3
                        ypos = math.cos(angle) * -3
                        
                    elif angle  <= -math.pi/2 and angle > -math.pi:
                        
                        xpos = -math.sin(angle) * (-3) + math.cos(angle) * (length + 2)
                        ypos = -math.cos(angle) * (-3)

                    elif angle  <= math.pi and angle > math.pi/2:
                        
                        xpos = math.cos(angle) * (length + 2) + math.sin(angle) * -3
                        ypos = -math.sin(angle) * (length + 2)
                    else:
                        xpos = math.sin(angle) * (-3)
                        ypos = math.cos(angle) * -3 + -math.sin(angle) * (length + 2)

                    self.stage.screen.blit(vine_turned, (section.body.position.x+self.stage.x_offset + xpos, self.stage.display_height - section.body.position.y + ypos))
   
#                allpoints = section.get_points()
#                correctedpoints = []
#                for point in allpoints:
#                    new_pos_y = self.stage.display_height - int(point.y)
#                    p = int(point.x+self.stage.x_offset), new_pos_y
#                    correctedpoints.append(p)

#                new_pos_y = self.stage.display_height-int(section.body.position.y)
#                p = int(section.body.position.x+self.stage.x_offset), new_pos_y
#                pygame.draw.circle(self.stage.screen, THECOLORS["red"], p, 2, 2)

                #pygame.draw.lines(self.stage.screen,THECOLORS["red"], True, correctedpoints)

        
        #final check
        if self.sections.__len__() == 0:
#            self.stage.fallen_swings.remove(self) 
            for joint in self.rotation_center_joints:
                self.stage.space.remove(joint)
                
            self.stage.swings.remove(self) 
        

            
            
        
        