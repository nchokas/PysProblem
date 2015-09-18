import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
import math

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 100
    radius = 14
    inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
    body = pm.Body(mass, inertia)
    x = random.randint(120,380)
    body.position = x, 550
    shape = pm.Circle(body, radius, (0,0))
    space.add(body, shape)
    return shape

def draw_ball(screen, ball):
    """Draw a ball shape"""
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)

def add_L(space):
    """Add a inverted L shape with two joints"""
    rotation_center_body = pm.Body(pm.inf, pm.inf)
    rotation_center_body.position = (300,300)
    
    rotation_limit_body = pm.Body(pm.inf, pm.inf) # 1
    rotation_limit_body.position = (200,300)
    
    body = pm.Body(10000000, 10000)
    body.position = (300,300)    
    l1 = pm.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pm.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)
    
    rotation_center_joint = pm.PinJoint(body, rotation_center_body, (0,0), (0,0)) 
    joint_limit = 25
    rotation_limit_joint = pm.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit) # 3
    #rotation_limit_joint = pm.PinJoint(body, rotation_limit_body, (-100,0), (0,0)) # 3

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1,l2

def draw_lines(screen, lines):
    """Draw the lines"""
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(math.degrees(body.angle))
        pv2 = body.position + line.b.rotated(math.degrees(body.angle))
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()
    running = True
    
    pm.init_pymunk()
    space = pm.Space()
    space.gravity = (0.0, -900.0)
    
    lines = add_L(space)
    balls = []
    
    ticks_to_next_ball = 10
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill(THECOLORS["white"])
        
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 150:
                balls_to_remove.append(ball)
            draw_ball(screen, ball)
        
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)
        
        draw_lines(screen, lines)
        
        pygame.draw.circle(screen, THECOLORS["red"], (300,300), 5)
        pygame.draw.circle(screen, THECOLORS["green"], (200,300), 25, 2)

        space.step(1/50.0)
        
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())