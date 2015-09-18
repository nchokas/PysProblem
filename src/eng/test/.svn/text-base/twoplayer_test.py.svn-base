import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
import math
from lineswing import Lineswing
from polyswing import Polyswing
from bullet import Bullet

#test

def main():
    pygame.init()
    screen = pygame.display.set_mode((1300, 600),0 , 32)
    pygame.display.set_caption("Pymunk test")
    clock = pygame.time.Clock()
    running = True
    
    pm.init_pymunk()
    
    #player1 space
    space1 = pm.Space()
    space1.gravity = (0.0, -100.0)
    space1._space.contents.elasticIterations = 10
    
    #player2 space
    space2 = pm.Space()
    space2.gravity = (0.0, -100.0)
    space2._space.contents.elasticIterations = 10

    balls1=[]
    segments1=[]
    polys1=[]
    
    balls2=[]
    segments2=[]
    polys2=[]
    
    ground_lines1 = add_ground(space1)
    ground_lines2 = add_ground(space2)
    
    for line in ground_lines1:
        segments1.append(line)
        
    for line in ground_lines2:
        segments2.append(line)
    
    #this adds the first swing
    swing_main1 = Lineswing(space1, 300, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments1.append(swing_main1.s1)
    balls1.append(swing_main1.circle)
    
    #this adds the second swing
    swing_main2 = Lineswing(space1, 350, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments1.append(swing_main2.s1)
    balls1.append(swing_main2.circle)
    
    #this adds the third swing
    swing_main3 = Lineswing(space1, 400, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments1.append(swing_main3.s1)
    balls1.append(swing_main3.circle)
    
    #this adds the third swing
    swing_main4 = Lineswing(space1, 450, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments1.append(swing_main4.s1)
    balls1.append(swing_main4.circle)
    
    
#for play2   
    #this adds the first swing
    swing_main1 = Lineswing(space2, 300, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments2.append(swing_main1.s1)
    balls2.append(swing_main1.circle)
    
    #this adds the second swing
    swing_main2 = Lineswing(space2, 350, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments2.append(swing_main2.s1)
    balls2.append(swing_main2.circle)
    
    #this adds the third swing
    swing_main3 = Lineswing(space2, 400, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments2.append(swing_main3.s1)
    balls2.append(swing_main3.circle)
    
    #this adds the third swing
    swing_main4 = Lineswing(space2, 450, 300, 50, 20.0, 10.0, 20, 1.0, 0, 5000, 1.0)
    segments2.append(swing_main4.s1)
    balls2.append(swing_main4.circle)
    

#    1: the space the polyswing will belong to
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
    
    poly_swing1 = Polyswing(space1,100,550,1,10,10,500,1,1,20,1,6)
    poly_swing2 = Polyswing(space2,100,550,1,10,10,500,1,1,20,1,6)
#    polys.append(poly_swing1.section1)
#    polys.append(poly_swing1.section2)
#    polys.append(poly_swing1.section3)
#    polys.append(poly_swing1.section4)
#    polys.append(poly_swing1.section5)
    for poly in poly_swing1.sections:
        polys1.append(poly)
        
    balls1.append(poly_swing1.circle)
    
    for poly in poly_swing2.sections:
        polys2.append(poly)
        
    balls2.append(poly_swing2.circle) 
    
    ticks_to_next_ball = 10
    ticks_to_next_poly = 20
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            #player1 shoots    
            elif event.type == KEYDOWN and event.key == K_UP:
                new_ball = Bullet(space1,300,30,2.0,20.0,0.5,'green', balls1)
                new_ball.body.apply_impulse((0,1000),(0,0))
            elif event.type == KEYDOWN and event.key == K_LEFT:
                new_ball = Bullet(space1,300,30,2.0,20.0,0.5,'green', balls1)
                new_ball.body.apply_impulse((-500,1000),(0,0))
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                new_ball = Bullet(space1,300,30,2.0,20.0,0.5,'green', balls1)
                new_ball.body.apply_impulse((500,1000),(0,0))
        
            #player2 shoots
            elif event.type == KEYDOWN and event.key == K_w:
                new_ball = Bullet(space2,300,30,2.0,20.0,0.5,'green', balls2)
                new_ball.body.apply_impulse((0,1000),(0,0))
            elif event.type == KEYDOWN and event.key == K_a:
                new_ball = Bullet(space2,300,30,2.0,20.0,0.5,'green', balls2)
                new_ball.body.apply_impulse((-500,1000),(0,0))
            elif event.type == KEYDOWN and event.key == K_d:
                new_ball = Bullet(space2,300,30,2.0,20.0,0.5,'green', balls2)
                new_ball.body.apply_impulse((500,1000),(0,0))
        
        #use balls
        ticks_to_next_ball -= 1 #comment out to never add balls
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            
            ball_shape1 = add_ball(space1)
            ball_shape2 = add_ball(space2)
            balls1.append(ball_shape1)
            balls2.append(ball_shape2)
        
        screen.fill(THECOLORS["black"])
        
        balls_to_remove1 = []
        for ball in balls1:
            if ball.body.position.y < 0:
                balls_to_remove1.append(ball)
            draw_ball1(screen, ball)
        
        for ball in balls_to_remove1:
            space1.remove(ball, ball.body)
            balls1.remove(ball)


        
        balls_to_remove2 = []
        for ball in balls2:
            if ball.body.position.y < 0:
                balls_to_remove2.append(ball)
            draw_ball2(screen, ball)
        
        for ball in balls_to_remove2:
            space2.remove(ball, ball.body)
            balls2.remove(ball)
        #end use balls

        #use polys
        ticks_to_next_poly -= 1 #comment out to never add balls
        if ticks_to_next_poly <= 0:
            ticks_to_next_poly = 25
            
            poly_shape1 = add_poly(space1)
            poly_shape2 = add_poly(space2)
            polys1.append(poly_shape1)
            polys2.append(poly_shape2)
        
        #screen.fill(THECOLORS["black"])
        
        polys_to_remove1 = []
        polys_to_remove2 = []
        for poly in polys1:
            if poly.body.position.y < 0:
                polys_to_remove1.append(poly)
            draw_poly1(screen, poly)
        
        for poly in polys_to_remove1:
            space1.remove(poly, poly.body)
            polys1.remove(poly)
            
        for poly in polys2:
            if poly.body.position.y < 0:
                polys_to_remove2.append(poly)
            draw_poly2(screen, poly)
        
        for poly in polys_to_remove2:
            space2.remove(poly, poly.body)
            polys2.remove(poly)
        #end use polys   
        
        
        #draws all the lines
        for segment in segments1:
            draw_segment1(screen, segment)
            
        for segment in segments2:
            draw_segment2(screen, segment)
            
        for poly in polys1:
            draw_poly1(screen, poly)
            
        for poly in polys2:
            draw_poly2(screen, poly)
            
        space1.step(1/60.0)
        space2.step(1/60.0)
        
        pygame.display.flip()
        clock.tick(60)
        
def add_ground(space):
    body1 = pm.Body(pm.inf,pm.inf)
    body1.position = (0,150)
    line1 = pm.Segment(body1,(0.,0.),(200.,0.),5.)
    line1.elasticity = 1.
    
    body2 = pm.Body(pm.inf,pm.inf)
    body2.position = (200,150)
    line2 = pm.Segment(body2,(0.,0.),(50.,-50.),5.)
    line2.elasticity = 1.
    
    body3 = pm.Body(pm.inf,pm.inf)
    body3.position = (400,150)
    line3 = pm.Segment(body3,(0.,0.),(-50.,-50.),5.)
    line3.elasticity = 1.
    
    body4 = pm.Body(pm.inf,pm.inf)
    body4.position = (600,150)
    line4 = pm.Segment(body4,(0.,0.),(-200.,0.),5.)
    line4.elasticity = 1.
    
    #this is the lhs wall
    body5 = pm.Body(pm.inf,pm.inf)
    body5.position = (0,300)
    line5 = pm.Segment(body5,(0.,-300.),(0.,300.),5.)
    line5.elasticity = 1.
    
    #this is the rhs wall
    body6 = pm.Body(pm.inf,pm.inf)
    body6.position = (600,300)
    line6 = pm.Segment(body6,(0.,-300.),(0.,300.),5.)
    line6.elasticity = 1.
    
    #this is the top
    body7 = pm.Body(pm.inf,pm.inf)
    body7.position = (300,600)
    line7 = pm.Segment(body7,(-300.,0.),(300.,0.),5.)
    line7.elasticity = 1.
       
    space.add(line1,line2,line3,line4,line5,line6,line7)
    return line1,line2,line3,line4,line5,line6,line7

def draw_poly1(screen,line):
        body = line.body
#        pv1 = body.position# + line.a.rotated(math.degrees(body.angle))
#        pv2 = body.position# + line.b.rotated(math.degrees(body.angle))
#        p1 = to_pygame(pv1)
#        p2 = to_pygame(pv2)
        allpoints = line.get_points()
        correctedpoints = []
        for point in allpoints:
             correctedpoints.append((point.x, -point.y + 600))
            
        pygame.draw.lines(screen,THECOLORS["red"], True, correctedpoints) 

def draw_poly2(screen,line):
        body = line.body
#        pv1 = body.position# + line.a.rotated(math.degrees(body.angle))
#        pv2 = body.position# + line.b.rotated(math.degrees(body.angle))
#        p1 = to_pygame(pv1)
#        p2 = to_pygame(pv2)
        allpoints = line.get_points()
        correctedpoints = []
        for point in allpoints:
             correctedpoints.append((point.x + 700, -point.y + 600))
            
        pygame.draw.lines(screen,THECOLORS["red"], True, correctedpoints) 
            
def draw_segment1(screen,line):
        body = line.body
        pv1 = body.position + line.a.rotated(math.degrees(body.angle))
        pv2 = body.position + line.b.rotated(math.degrees(body.angle))
        p1 = (pv1.x, -pv1.y + 600)
        p2 = (pv2.x, -pv2.y + 600)
        pygame.draw.lines(screen,THECOLORS["lightgray"], False, [p1,p2]) 

def draw_segment2(screen,line):
        body = line.body
        pv1 = body.position + line.a.rotated(math.degrees(body.angle))
        pv2 = body.position + line.b.rotated(math.degrees(body.angle))
        p1 = (pv1.x + 700, -pv1.y + 600)
        p2 = (pv2.x + 700, -pv2.y + 600)
        pygame.draw.lines(screen,THECOLORS["lightgray"], False, [p1,p2]) 

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)
    
def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 10
    inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
    body = pm.Body(mass, inertia)
    x = random.randint(100,450)
    body.position = x, 550
    shape = pm.Circle(body, radius, (0,0))
    shape.elasticity = 1.
    #print "ball group: " , shape.group
    space.add(body, shape)
    return shape

def add_poly(space):
    """Add a poly to the given space at a random position"""
    mass = 1
    inertia = 10
    section_width = 5
    section_height = 5
    body = pm.Body(mass, inertia)
    x = random.randint(100,450)
    body.position = x, 550
    #shape = pm.Poly(body, [(-(section_width/2),section_height/2), (-(section_width/2),-(section_height/2)),(section_width/2,-(section_height/2)),(section_width/2,section_height/2)] ,(0, 0), False)
    #shape = pm.Poly(body, [(0,0), (-section_width,-section_height),(section_width,-section_height),(section_width , section_height)] ,(0, 0), False)
    shape = pm.Poly(body, [(-section_width,-section_height), (-section_width,section_height),(section_width,section_height),(section_width,-section_height)] ,(0, 0), False)
    #print shape.group
    shape.elasticity = 1.
    space.add(body, shape)
    return shape

def draw_ball1(screen, ball):
    """Draw a ball shape"""
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)
    
def draw_ball2(screen, ball):
    """Draw a ball shape"""
    p = int(ball.body.position.x + 700), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)

        
if __name__ == '__main__':
    sys.exit(main())