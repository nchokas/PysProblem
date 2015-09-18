import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
from pygame.mixer import *
import pymunk as pm
import math
from lineswing import Lineswing
from ball import Ball
from bullet import Bullet
from stage import Stage
from polyswing import Polyswing
from barrelcannon import Barrelcannon
from spinner import Spinner
from gun import Gun
from player import Player
import random
import time

def main():
    global stage_width,stage_height,sidebar_width,wall_gap,gap_size,padding,colors,screen,stage,stage2, barrel_cannon1, child_bonus, grandchild_bonus
    stage_width,stage_height = 550,720
    sidebar_width = 150 # sidebar displays statistics
    wall_gap = 20.0 # space between the walls and the edge of the window
    gap_size = 350.0 # how big the gap in the middle is
    padding = 5.0 # segment padding
    gravity = (0.0, -100.0)
    bound_color = "lightgray" # boundary walls color
    bg_color = "black" # window background color
    ball_spacing = 10 # used to space initially fixed balls
    ball_radius = 20
    bullet_color = "green"
    child_bonus = 1.5
    grandchild_bonus = 2.0
    
    # used in collisions to change ball color
    colors = ["red","orange","yellow","green","blue","purple"]
    
    pygame.init()
    screen = pygame.display.set_mode((stage_width+sidebar_width,stage_height))
    clock = pygame.time.Clock()
    running = True
    
    pm.init_pymunk()
    matt = Player("Matt", 1)
    
    stage = Stage(matt, screen, K_LEFT,K_RIGHT,K_UP,stage_width, stage_height, wall_gap, gap_size, padding, bound_color, gravity, 0, 100,bullet_color)
    
    stage.space.add_collisionpair_func(1, 3, barrelcannon_load)
    
    spinner1 = Spinner(stage, 150, 100, 25, 25, 1, 1, math.pi/120, 1, .2*stage_width, .5*stage_width)
    spinner2 = Spinner(stage, 275, 200, 25, 25, 1, 1, -math.pi/60, 2, .5*stage_width, .8*stage_width)
    poly_swing1 = Polyswing(stage,100,600,1,10,10,500,1,10,20,1,3, None, 3, 1, "orange")
    poly_swing2 = Polyswing(stage,275,650,1,10,10,500,1,10,20,1,3, None, 3, 1, "red")
    poly_swing3 = Polyswing(stage,450,600,1,10,10,500,1,10,20,1,3, None, 3, 1, "orange")
    stage.swing_limit = len(stage.swings) * 10
    
    
    barrel_cannon1 = Barrelcannon(stage, 275, 300, 20, 30, 1, 1, -math.pi/60, 1, .2*stage_width, .8*stage_width)
 
    ticks_to_next_reload = 0
    ticks_to_next_respawn = 120 
    
    swing_index = 0
    last_swing_spawn = 0 
    
    start_time = time.time()
    while running: # main game loop
        pg_time = pygame.time.get_ticks()/1000.
        
#===============================================================================
#        ball_spawn_interval should decrease with time
#===============================================================================
        if pg_time < 30:
            ball_spawn_interval = 3
        elif pg_time < 60:
            ball_spawn_interval = 2.75
        elif pg_time < 90:
            ball_spawn_interval = 2.5
        elif pg_time < 120:
            ball_spawn_interval = 2.25
        elif pg_time < 150:
            ball_spawn_interval = 2
        elif pg_time < 180:
            ball_spawn_interval = 1.75
        elif pg_time < 210:
            ball_spawn_interval = 1.5
        elif pg_time < 240:
            ball_spawn_interval = 1.25
        elif pg_time < 270:
            ball_spawn_interval = 1
        elif pg_time < 300:  
            ball_spawn_interval = .75
        elif pg_time < 330:  
            ball_spawn_interval = .5
              
        if pg_time-last_swing_spawn >= ball_spawn_interval:
            last_swing_spawn = pg_time
            stage.spawn_swing()
        
        for event in pygame.event.get():
            try:
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                elif event.type == KEYDOWN and event.key == K_UP and stage.running == True:    
                        stage.gun.shoot(1000)
                #upgrades
                
                elif event.type == KEYDOWN and event.key == K_e and stage.running == True:
                    selected_swing.destroy_joint(child_bonus,grandchild_bonus)
                elif event.type == KEYDOWN and event.key == K_s and stage.running == True:
                    #SECRET WEAPONNNNN!!!!
                    for swing in stage.swings:
                        swing.destroy_joint(child_bonus, grandchild_bonus)                        
                elif event.type == KEYDOWN and event.key == K_r and stage.running == True: 
                    #If there is no ball, respawn the ball
                    if selected_swing.ball == None:
                        selected_swing.respawn_ball(selected_swing.circle_mass,selected_swing.radius,1, "red") 
                    else:
                    #If there is a ball create a new child
                    
                    #the masses of the segments and balls are determined by which tier the swing is
                    #Tier1 swing is the original swing and can have 3 children. Has 3 segments
                    #Tier2 swings are children of tier1 swings and can have 2 children. Masses are 1/3 of the tier1. Has 2 segments
                    #Tier3 swings are children of tier2 swings and can't have children. Masses are 1/2 of tier2. Has 1 segment

                        new_tier = selected_swing.tier + 1
                        
                        if new_tier == 2:
                            new_swing = Polyswing(stage,200,550,1,10,.33 * selected_swing.section_mass,500,1,.33 * selected_swing.circle_mass,15,1,2, selected_swing, 2,new_tier,"red")
                        else: #its tier 3
                            new_swing = Polyswing(stage,200,550,1,10,.5 * selected_swing.section_mass,500,1,.5 * selected_swing.circle_mass,10,1,1, selected_swing, 0 ,new_tier, "red")
                elif event.type == KEYDOWN and event.key == K_t:  
                    #toggle through the swings
                    try:
                        selected_swing.selected = False
                    except UnboundLocalError:
                        print "no selected swing yet" 
                    try:
                        selected_swing = stage.swings[swing_index]
                    except IndexError:
                        print "the swing that was selected isn't there anymore"                                             
                    selected_swing.selected = True
                    if swing_index +1 > len(stage.swings)-1: 
                        swing_index = 0
                    else:
                        swing_index = swing_index + 1
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    barrel_cannon1.shoot(1200, bullet_color)
                    #new_ball = Bullet(stage, f275, 36 ,2.0,10,0.5,bullet_color)                       
            except UnboundLocalError:
                print "im too lazy to fix this problem right now" #cant release or make the ball for poly_swing2 unless it exists
 
        if stage.running == True:        
            barrel_cannon1.move()
            spinner1.move()
            spinner2.move()
        
        screen.fill(THECOLORS[bg_color])
        stage.process_input()
        
        stage.draw_stats()

        # create new threads for these calls?
        if stage.running == True: #two of these need to be done because step must be infront of draw
                stage.bullet_reload(pg_time)
                stage.space.step(1/60.0)
        else:
                stage.set_end_time()
                
        stage.draw_self()
        
        pygame.display.flip()
        clock.tick(60)
        pygame.display.set_caption("FPS: " + str(clock.get_fps()))
        

def barrelcannon_load(shapeA, shapeB, contacts, normal_coef, data=None):
    if shapeB.container.loaded == False:
        shapeA.body.position.y = -1000 #clears the bullet
        shapeB.container.collect() #loads the cannon
    return True

               
if __name__ == '__main__':
    sys.exit(main())