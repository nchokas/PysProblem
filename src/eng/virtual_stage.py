import pygame
import time
from pygame.color import *

class Virtualstage(object):
    def __init__(self,screen,width,height,wall_gap,gap_size,sidebar_width,bound_color,x_offset,graphics_path,sound_path):
        
        self.screen = screen
        self.width = width
        self.height = height 
        self.wall_gap = wall_gap
        self.gap_size = gap_size
        self.sidebar_width = sidebar_width
        self.bound_color = bound_color
        self.x_offset = x_offset
        self.graphics_path = graphics_path
        self.sound_path = sound_path
        
        self.end_time_set = False
        self.end_time = 0
        self.start_time = time.time()
        self.player = None
        
        #stats window
        self.gun_bullets_curr = 0
        self.point_total = 0
        
        self.running = True
        self.ball_colors = ["red","orange","yellow","green","blue","purple"]
        
        #objects from network
        self.ball_prop = []
        self.bullet_prop = []
        self.swing_prop = []
        self.cannon_prop = []
        self.spinner_prop = []
        self.gun_prop = [] 
        
        self.stage_image = pygame.image.load(self.graphics_path + "stage.png").convert_alpha()
        self.gun_base = pygame.image.load(self.graphics_path + "cannonbase.png").convert_alpha()
        
        #all the ball graphics
        self.red_nut = pygame.image.load(self.graphics_path + "nut1.png").convert_alpha()
        self.orange_nut = pygame.image.load(self.graphics_path + "nut2.png").convert_alpha()
        self.yellow_nut = pygame.image.load(self.graphics_path + "nut3.png").convert_alpha()
        self.green_nut = pygame.image.load(self.graphics_path + "nut4.png").convert_alpha()
        self.blue_nut = pygame.image.load(self.graphics_path + "nut5.png").convert_alpha()
        self.purple_nut = pygame.image.load(self.graphics_path + "nut6.png").convert_alpha()
        
        self.gun_bullet = pygame.image.load(self.graphics_path + "gunbullet.png").convert_alpha()
        self.cannon_bullet = pygame.image.load(self.graphics_path + "cannonbullet.png").convert_alpha()  
        
        self.BC_unloaded = pygame.image.load(self.graphics_path + "bc.png").convert_alpha()
        self.BC_loaded = pygame.image.load(self.graphics_path + "bcloaded.png").convert_alpha()
        
        self.vine_top = pygame.image.load(self.graphics_path + "vinetop.png").convert_alpha()
        self.vine_mid = pygame.image.load(self.graphics_path + "vinemid.png").convert_alpha()
        self.vine_bot = pygame.image.load(self.graphics_path + "vinebot.png").convert_alpha()
        
        self.vine_short = pygame.image.load(self.graphics_path + "vineshort.png").convert_alpha()
        
        self.gun = pygame.image.load(self.graphics_path + "cannon2.png").convert_alpha() 
        
    def draw_self(self):
        #this is a static image
        self.screen.blit(self.stage_image, (self.x_offset + self.wall_gap, self.wall_gap))
        
#        p0 = ((self.width/2) - (self.gap_size/2)+self.x_offset,(-self.wall_gap+20)+self.height)
#        p1 = (self.wall_gap+self.x_offset, (-self.wall_gap)+self.height)
#        p2 = (self.wall_gap+self.x_offset, -(self.height-self.wall_gap)+self.height)
#        p3 = (-self.wall_gap+self.x_offset + self.width, -(self.height-self.wall_gap)+self.height)
#        p4 = (-self.wall_gap+self.x_offset + self.width,(-self.wall_gap)+self.height)
#        p5 = ((self.width/2) + (self.gap_size/2)+self.x_offset,(-self.wall_gap+20)+self.height)
#
#        wall_points = [p0,p1,p2,p3,p4,p5]
#        pygame.draw.lines(self.screen,THECOLORS[self.bound_color], False, wall_points)
                    
        for i in range(0,len(self.ball_prop),4):
                    #decide which color it is
            if self.ball_prop[i+2] == 0:
                current_image = self.red_nut
            elif self.ball_prop[i+2] == 1:
                current_image = self.orange_nut
            elif self.ball_prop[i+2] == 2:
                current_image = self.yellow_nut
            elif self.ball_prop[i+2] == 3:
                current_image = self.green_nut
            elif self.ball_prop[i+2] == 4:
                current_image = self.blue_nut
            else:
                current_image = self.purple_nut
                
            current_image = pygame.transform.scale(current_image,(2+int(self.ball_prop[i+3]) * 2, 2+int(self.ball_prop[i+3]) * 2))
               
            self.screen.blit(current_image, (self.ball_prop[i]-(2+int(self.ball_prop[i+3])),self.ball_prop[i+1]-(2+int(self.ball_prop[i+3]))))
            #pygame.draw.circle(self.screen, THECOLORS[self.ball_colors[self.ball_prop[i+2]]], (self.ball_prop[i], self.ball_prop[i+1]), int(self.ball_prop[i+3]), 2)
        for i in range(0,len(self.bullet_prop),3):            
            if self.bullet_prop[i+2] == 2: #this is a gun bullet
                self.screen.blit(self.gun_bullet, (self.bullet_prop[i] - 10, self.bullet_prop[i+1] - 10))
            if self.bullet_prop[i+2] == 3: #this is a gun bullet
                self.screen.blit(self.cannon_bullet, (self.bullet_prop[i] - 10, self.bullet_prop[i+1] - 10))
                
            #pygame.draw.circle(self.screen, THECOLORS[self.ball_colors[self.bullet_prop[i+2]]], (self.bullet_prop[i], self.bullet_prop[i+1]), int(self.bullet_prop[i+3]), 2)
        for i in range(0,len(self.swing_prop),5):
            
            if self.swing_prop[i] == 0: 
                vine_scaled = pygame.transform.scale(self.vine_short, (6, int(self.swing_prop[4] + 2)))
            elif self.swing_prop[i] == 1: 
                vine_scaled = pygame.transform.scale(self.vine_top, (6, int(self.swing_prop[4] + 2)))
            elif self.swing_prop[i] == 2: 
                vine_scaled = pygame.transform.scale(self.vine_bot, (6, int(self.swing_prop[4] + 2)))
            else: 
                vine_scaled = pygame.transform.scale(self.vine_mid, (6, int(self.swing_prop[4] + 2)))
            
            vine_turned = pygame.transform.rotate(vine_scaled, self.swing_prop[i+3])

            self.screen.blit(vine_turned, (self.swing_prop[i+1], self.swing_prop[i+2]))
            #pygame.draw.circle(self.screen, THECOLORS["red"], (self.swing_prop[i], self.swing_prop[i+1]), 2 , 2)
        
        
        for i in range(0,len(self.cannon_prop),4):
            if self.cannon_prop[i+3]:
                cannon_turned = pygame.transform.rotate(self.BC_loaded, self.cannon_prop[i+2])
            else: 
                cannon_turned = pygame.transform.rotate(self.BC_unloaded, self.cannon_prop[i+2])
            
            cannon_flipped = pygame.transform.flip(cannon_turned, True, True)
            self.screen.blit(cannon_flipped, (self.cannon_prop[i], self.cannon_prop[i+1]))
#######################################            
#            cannon_flipped = pygame.transform.flip(cannon_turned, True, True)
#                p1 = self.cannon_prop[i], self.cannon_prop[i+1]
#                p2 = self.cannon_prop[i+2], self.cannon_prop[i+3]
#                p3 = self.cannon_prop[i+4], self.cannon_prop[i+5]
#                p4 = self.cannon_prop[i+6], self.cannon_prop[i+7]
#            
#            if self.cannon_prop[i+8]:
#                pygame.draw.lines(self.screen,THECOLORS["green"], False, [p1,p2,p3,p4])
#            else:
#                pygame.draw.lines(self.screen,THECOLORS["red"], False, [p1,p2,p3,p4])
#######################################
        for i in range(0,len(self.spinner_prop),8):
            
            seg1p1 = self.spinner_prop[i], self.spinner_prop[i+1]
            seg1p2 = self.spinner_prop[i+2], self.spinner_prop[i+3]
            seg2p1 = self.spinner_prop[i+5], self.spinner_prop[i+5]
            seg2p2 = self.spinner_prop[i+6], self.spinner_prop[i+7]
            
            pygame.draw.lines(self.screen,THECOLORS["lightgray"], False, [seg1p1,seg1p2])
            pygame.draw.lines(self.screen,THECOLORS["lightgray"], False, [seg2p1,seg2p2])
        
        #this is a static image
        self.screen.blit(self.gun_base, (self.x_offset + self.width/2 - self.gun_base.get_width()/2, self.height - self.gun_base.get_height() + 3))
        
        for i in range(0,len(self.gun_prop),3):
            gun_turned = pygame.transform.rotate(self.gun, self.gun_prop[i+2])
            gun_flipped = pygame.transform.flip(gun_turned, True, True)
            
            self.screen.blit(gun_flipped, (self.gun_prop[i], self.gun_prop[i+1]))
#            p1 = self.gun_prop[i], self.gun_prop[i+1]
#            p2 = self.gun_prop[i+2], self.gun_prop[i+3]
#            p3 = self.gun_prop[i+4], self.gun_prop[i+5]
#            p4 = self.gun_prop[i+6], self.gun_prop[i+7]     
#            
#            pygame.draw.lines(self.screen,THECOLORS["green"], False, [p1,p2,p3,p4])      
        
        self.draw_stats()
        
    def draw_stats(self):
        player_name_str = "Player: "+str(self.player.name)
        bullet_count_str = "Bullets Available: "+ str(self.gun_bullets_curr) #+str(len(self.bullets))
        point_total_str = "Points: "+str(int(self.point_total))
        game_over_str = "Game Over!"
        
#        if self.running:
#            time_str = "Time: "+str(time.time() - self.start_time)[:4]
#        else:
#            time_str = "Time: "+str(self.end_time - self.start_time)[:4] 
            
        stats = [player_name_str,bullet_count_str,point_total_str]        
        
        verdana = pygame.font.match_font('Verdana')
        verdana_font = pygame.font.Font(verdana,10)
        text_color = (255,255,255)
        text_bg = (0,0,0)
        
        y_offset = self.height/2
        #TODO: add background
        for stat in stats:
            text = verdana_font.render(stat,1,text_color,text_bg)
            rect = text.get_rect()
            rect.centerx, rect.y = self.width+self.sidebar_width/2.0,y_offset + 20
        
            self.screen.blit(text,rect)
            y_offset += rect.height       
            
    def set_end_time(self):
        if self.end_time_set == False:
            self.end_time = time.time()
            self.end_time_set = True
        
        
    