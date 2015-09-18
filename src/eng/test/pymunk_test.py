import sys, random, time, pygame, pymunk as pm, math
from pygame.locals import *
from pygame.color import *
from pygame.mixer import *
from lineswing import Lineswing
from ball import Ball
from bullet import Bullet
from stage import Stage
from polyswing import Polyswing
from player import Player

def main():
    global stage_width,stage_height,sidebar_width,wall_gap,gap_size,padding,colors,screen,stage,stage2
    stage_width,stage_height = 480,700
    sidebar_width = 140 # sidebar displays statistics
    wall_gap = 5 # space between the walls and the edge of the window
    gap_size = 300.0 # how big the gap in the middle is
    padding = 5.0 # segment padding
    gravity = (0.0, -100.0)
    bound_color = "lightgray" # boundary walls color
    bg_color = "black" # window background color
    ball_spacing = 10 # used to space initially fixed balls
    ball_radius = 15.0
    bullet_color = "yellow"
    step_size = 1/60.0
    
    pygame.init()
    screen = pygame.display.set_mode((2*stage_width+sidebar_width+wall_gap,stage_height))
    clock = pygame.time.Clock()
    running = True
    
    pm.init_pymunk()
    
    player1 = Player("Rob",0)
    player2 = Player("Matt",1)
    
    stage1 = Stage(player1,screen,K_a,K_d,K_w,stage_width,stage_height,wall_gap,gap_size,padding,bound_color,gravity,0,sidebar_width,bullet_color)
    stage2 = Stage(player2,screen,K_LEFT,K_RIGHT,K_UP,stage_width,stage_height,wall_gap,gap_size,padding,bound_color,gravity,stage_width+sidebar_width,sidebar_width,bullet_color)
    
    stages = [stage1,stage2]
    
    poly_swing1 = Polyswing(stage1,100,600,1,10,10,500,1,10,20,1,3, None, 3, 1, "orange")
    poly_swing2 = Polyswing(stage1,275,600,1,10,10,500,1,10,20,1,3, None, 3, 1, "red")
    poly_swing1 = Polyswing(stage2,100,600,1,10,10,500,1,10,20,1,3, None, 3, 1, "orange")
    poly_swing2 = Polyswing(stage2,275,600,1,10,10,500,1,10,20,1,3, None, 3, 1, "red")

    #pygame.mixer.music.load("asian.wav")
    #pygame.mixer.music.play(5,0.0)
    
    last_swing_spawn = 0 # last swing spawn
    ball_spawn_interval = 2
    
    while running: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            for stage in stages:
                if stage.running == True:
                    if event.type == KEYDOWN and event.key == stage.shoot_key:
                        stage.gun.shoot(1500)
        
        screen.fill(THECOLORS[bg_color])
        
        # use modulo arithmetic for spawning events, but use seconds not ticks as ticks are CPU-dependent
        time = pygame.time.get_ticks()/1000
        if time%ball_spawn_interval == 0 and last_swing_spawn != time:
            last_swing_spawn = time
            for stage in stages:
                stage.spawn_swing()
        
        for stage in stages:
            stage.process_input()
            if stage.running == True:
                stage.bullet_reload(time)
                stage.space.step(step_size)
            stage.draw_self()
        
        pygame.display.flip()
        clock.tick(60)
        pygame.display.set_caption("FPS: " + str(clock.get_fps()))

if __name__ == '__main__':
    sys.exit(main())