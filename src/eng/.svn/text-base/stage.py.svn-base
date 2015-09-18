import pymunk as pm, pygame, math, random
#from ball import Ball
from bullet import Bullet
from gun import Gun
from polyswing import Polyswing
from pygame.color import *
import time
from buildblock import Buildblock
from spinner import Spinner
from barrelcannon import Barrelcannon

class Stage(object):
    def __init__(self,player,screen,width,height,wall_gap,gap_size,seg_padding,bound_color,gravity,x_offset,sidebar_width,bullet_color,is_multiplayer,graphics_path,sound_path):
        self.graphics_path = graphics_path
        self.sound_path = sound_path
        self.player = player
        self.left_key = player.key_cannon_left
        self.right_key = player.key_cannon_right
        self.shoot_key = player.key_cannon_shoot
        self.bullet_color = bullet_color
        self.screen = screen
        self.space = pm.Space()
        self.space.gravity = gravity
        self.space._space.contents.elasticIterations = 10
        self.width = width
        self.height = height
        self.sidebar_width = sidebar_width
        self.wall_gap = wall_gap
        self.gap_size = gap_size
        self.seg_padding = seg_padding
        self.bound_color = bound_color
        self.gravity = gravity
        self.x_offset = x_offset
        self.balls_destroyed = 0
        self.point_total = 0
        self.bullet_limit = 5
        self.space.add_collisionpair_func(1,2,bullet_collision)
        self.space.add_collisionpair_func(1, 3, barrelcannon_load)
        self.swing_limit = 30 # turn this into calculation
        self.child_bonus = 1.5
        self.grandchild_bonus = 2.0
        self.running = True
        self.start_time = time.time()
        self.end_time = 0
        self.end_time_set = False
#        self.spinner_mode = False
        self.spinner_size = 25
        self.spinner_block = None #Buildblock(self,0,self.height/2,60,self.width,(255,0,0))
#        self.barrel_cannon_mode = False
        self.barrel_cannon_block = None
#        self.spinner_count = 0
        self.spinner_limit = 3
        self.spinner_upgrade_level = 0
        self.spinner_max_upgrade_level = 3
        self.barrel_cannon_limit = 1
        self.occupancy_of_blocks = [False, False, False, False, False]
        self.cannon_selected = False
        self.spinner_selected = False
        
        self.is_multiplayer = is_multiplayer
        self.bc_price = 15000
        self.spinner_price = 30000
        self.upgrade_capacity_price = 20000
        self.upgrade_reload_rate_price = 30000
        self.upgrade_spinner_price = 30000
        self.upgrade_bc_price = 25000
        self.upgrade_force_price = 10000
        self.purchases_made = 0
        
        self.virt_x_offset = self.width+self.sidebar_width
        
        display_info = pygame.display.Info()
        self.display_height = display_info.current_h    

        
        # init gun
        self.gun = Gun(self, self.width/2, -10, 15, 30, 1, 1, math.pi/120)
        self.gun.body.angle = math.pi
        self.space.add(self.gun.cannon_shape)
        
        self.balls = []
        self.bullets = []
        self.cannons = []
        self.spinners = []
#===============================================================================
#        swings contains both the connected and disconnected swings and is for drawing them
#        connected swings are the ones that are still connected to the tier1 swing
#        if the connected swing number reaches the maximum and each one has a ball, end game
#        Note: tier1 swings are ALWAYS connected
#===============================================================================
        self.swings = []
        self.connected_swings = []
        
        
        self.buy_index = 0 # current position in buying menu
        #available,upgrade level,(text name,cost),buy action 
        self.max_upgrades = [self.gun.capacity_upgrade_level_max,self.gun.rate_upgrade_level_max,3,3,self.spinner_limit,3]# corresponds to below positions in buy_info
        capacity = [1,self.gun.capacity_upgrade_level_max,[("Bullet Capacity",self.upgrade_capacity_price)],0]
        reload_rate = [1,self.gun.rate_upgrade_level_max,[("Reload Rate",self.upgrade_reload_rate_price)],0]
        impulse = [1,self.gun.impulse_upgrade_level_max,[("Gun Force",self.upgrade_force_price)],0]
        barrel_cannon = [1,3,[("Barrel Cannon",self.bc_price),("Upgrade Barrel Cannon",self.upgrade_bc_price)],0]   
        spinner_available = 0
        if self.is_multiplayer:
            spinner_available = 1
        spinner = [spinner_available,self.spinner_limit,[("Spinner",self.spinner_price)],0]
        spinner_upgrade = [0,3,[("Upgrade Spinners",self.upgrade_spinner_price)],0]
    
        self.buy_info = [capacity,reload_rate,impulse,barrel_cannon,spinner,spinner_upgrade]
        
        vert_wall_height = height-2.0*wall_gap
        horiz_wall_width = (width-(gap_size+2*wall_gap))/2.0 # width of bottom walls
        horiz_top_wall_width = (width-2*wall_gap) # width of top wall
        
        seg1_pos = (wall_gap,height/2.0) # seg1 is left vertical wall
        seg1_start = (0,-vert_wall_height/2.0)
        seg1_end = (0,vert_wall_height/2.0)
    
        seg2_pos = (width-wall_gap,height/2.0) # seg2 is right vertical wall
        seg2_start = (0,-vert_wall_height/2.0) 
        seg2_end = (0,vert_wall_height/2.0)
    
        seg3_pos = (horiz_wall_width/2.0+wall_gap,wall_gap) # seg3 is left horizontal wall
        seg3_start = (-horiz_wall_width/2.0,0)
        seg3_end =  (horiz_wall_width/2.0,-20.0)
    
        seg4_pos = (width-(horiz_wall_width/2.0+wall_gap),wall_gap) # seg4 is right horizontal wall
        seg4_start = (-horiz_wall_width/2.0,-20.0)
        seg4_end = (horiz_wall_width/2.0,0)
    
        seg5_pos = (width/2.0,height-wall_gap)
        seg5_start = (-horiz_top_wall_width/2.0,0)
        seg5_end =  (horiz_top_wall_width/2.0,0)
    
        body1 = pm.Body(pm.inf,pm.inf)
        body1.position = seg1_pos
        seg1 = pm.Segment(body1,seg1_start,seg1_end,seg_padding)
        seg1.elasticity = 1
    
        body2 = pm.Body(pm.inf,pm.inf)
        body2.position = seg2_pos
        seg2 = pm.Segment(body2,seg2_start,seg2_end,seg_padding)
        seg2.elasticity = 1
    
        body3 = pm.Body(pm.inf,pm.inf)
        body3.position = seg3_pos
        seg3 = pm.Segment(body3,seg3_start,seg3_end,seg_padding)
        seg3.elasticity = 1
    
        body4 = pm.Body(pm.inf,pm.inf)
        body4.position = seg4_pos
        seg4 = pm.Segment(body4,seg4_start,seg4_end,seg_padding)
        seg4.elasticity = 1
    
        body5 = pm.Body(pm.inf,pm.inf)
        body5.position = seg5_pos
        seg5 = pm.Segment(body5,seg5_start,seg5_end,seg_padding)
        seg5.elasticity = 1

        self.space.add(seg1,seg2,seg3,seg4,seg5)
        self.segs = [seg1,seg2,seg3,seg4,seg5]
        
        self.stage_image = pygame.image.load(self.graphics_path + "stage.png").convert_alpha()
        self.gun_base = pygame.image.load(self.graphics_path + "cannonbase.png").convert_alpha()
        self.stats_back = pygame.image.load(self.graphics_path + "statbg.png").convert_alpha()
        self.stats_back2 = pygame.image.load(self.graphics_path + "statbg2.png").convert_alpha()
        
    def to_pygame(self, p):
        return int(p.x)+self.x_offset, int(-p.y+self.height)
    
    def draw_self(self):
        #draw the stage area
        self.screen.blit(self.stage_image, (self.x_offset + self.wall_gap, self.wall_gap))

        
        #draw the base of the gun
        
        
#        for seg in self.segs:
#            body = seg.body
#            pv1 = body.position + seg.a.rotated(math.degrees(body.angle))
#            pv2 = body.position + seg.b.rotated(math.degrees(body.angle))
#            p1 = self.to_pygame(pv1)
#            p2 = self.to_pygame(pv2)
#            pygame.draw.lines(self.screen,THECOLORS[self.bound_color], False, [p1,p2])

        for ball in self.balls+self.bullets:
            if ball.body.position.y < 0-ball.radius:
                self.point_total += ball.point_value * ball.point_multiplier
                if(ball.point_value > 0):
                    self.balls_destroyed += 1
                ball.destroy_self()
            else: ball.draw_self()
        for swing in self.swings:
            swing.draw_self()
        for cannon in self.cannons:
            cannon.draw_self()
            
        self.gun.draw_self(self.player.number)
        self.screen.blit(self.gun_base, (self.x_offset + self.width/2 - self.gun_base.get_width()/2, self.height - self.gun_base.get_height() + 3))
        
        for spinner in self.spinners:
            spinner.draw_self()
            
        self.draw_stats()
        self.draw_buy_menu()
        if self.spinner_block != None:
            self.spinner_block.draw_self()
        if self.barrel_cannon_block != None:
             self.barrel_cannon_block.draw_self()
       
        
    def draw_build_zone(self):
        pygame.draw.rect(self.screen, (255,55,0), (self.width/2.0, self.height/2.0, self.width, 60))
    
    def move_items(self):
        for spinner in self.spinners:
            spinner.move()
        for cannon in self.cannons:
            cannon.move()
        
    def draw_stats(self): 
        player_name_str = "Player: "+str(self.player.name)
        bullet_count_str = "Bullets Available: "+ str(self.gun.bullets_curr) #+str(len(self.bullets))
        point_total_str = "Points: "+str(int(self.point_total))
        
        if self.running:
            time_str = "Time: "+str(int(time.time() - self.start_time))
        else:
            time_str = "Time: "+str(int(self.end_time - self.start_time))
            
        stats = [player_name_str,bullet_count_str,point_total_str,time_str]            
        
        verdana = pygame.font.match_font('Verdana')
        verdana_font = pygame.font.Font(verdana,10)
        text_color = (255,255,255)
        
        y_offset = self.height/2*self.player.number
        
        if self.player.number == 0:
            self.screen.blit(self.stats_back, (self.width - 5,y_offset + 10))
        else:
            self.screen.blit(self.stats_back2, (self.width - 5,y_offset + 10))
        
        for stat in stats:
            text = verdana_font.render(stat,1,text_color)
            rect = text.get_rect()
            rect.centerx, rect.y = self.width+self.sidebar_width/2.0,y_offset + 20
        
            self.screen.blit(text,rect)
            y_offset += rect.height
            
    def draw_buy_menu(self):
        verdana = pygame.font.match_font('Verdana')
        verdana_font = pygame.font.Font(verdana,10)
        text_color_active = (255,255,255)
        text_color_inactive = (127,127,127)
        text_bg = (0,0,0)
        
        y_offset = self.height/2*self.player.number + 80
        
        for i in range(len(self.buy_info)):
            item = self.buy_info[i]
            if item[0]:
                if self.buy_index == i:
                    text_color = text_color_active
                else:
                    text_color = text_color_inactive
                text = verdana_font.render(item[2][item[3]][0]+" L"+str(abs(self.max_upgrades[i]-item[1])+1)+": "+str(item[2][item[3]][1]),1,text_color) # item[3] holds switch 
            else:
                continue
            
            rect = text.get_rect()
            rect.centerx, rect.y = self.width+self.sidebar_width/2.0,y_offset
        
            self.screen.blit(text,rect)
            y_offset += rect.height
    
    def build_down_operation(self, opponent_stage):
        if self.buy_index < len(self.buy_info)-1:
            if self.barrel_cannon_block != None:
                self.barrel_cannon_block.move_down()  
                return
            if opponent_stage != None and opponent_stage.spinner_block != None:
                opponent_stage.spinner_block.move_down()
                return
            next_index = self.buy_index+1
            while(next_index < len(self.buy_info)):
                if self.buy_info[next_index][0]:
                    self.buy_index = next_index
                    break
                else:
                    next_index = next_index+1 
               
    def build_up_operation(self, opponent_stage):
        if self.buy_index > 0:
            if self.barrel_cannon_block != None:
                self.barrel_cannon_block.move_up()
                return   
            if opponent_stage != None and opponent_stage.spinner_block != None:
                opponent_stage.spinner_block.move_up()
                return
            next_index = self.buy_index-1
            while next_index >= 0:
                if self.buy_info[next_index][0]:
                    self.buy_index = next_index
                    break
                else:
                    next_index = next_index-1
        elif self.barrel_cannon_block != None:
            self.barrel_cannon_block.move_up()   
        elif opponent_stage != None and opponent_stage.spinner_block != None:
            opponent_stage.spinner_block.move_up()             
    
    def build_operation(self, opponent_stage):
        if self.buy_index == 0: # bullet capacity
            self.buy_capacity()
        elif self.buy_index == 1: # reload rate
            self.buy_reload_rate()
        elif self.buy_index == 2:
            self.buy_gun_force()
        elif self.buy_index == 3: # barrel cannon + upgrade
            self.buy_barrel_cannon(opponent_stage)
        elif self.buy_index == 4: # spinner
            self.buy_spinner(opponent_stage)
        elif self.buy_index == 5: # spinner upgrade
            self.buy_spinner_upgrade(opponent_stage)    

                             
    def cancel_operation(self, opponent_stage):
        self.barrel_cannon_block = None        
        if opponent_stage != None:
            opponent_stage.spinner_block = None   

    def add_ball(self, ball):
        if(isinstance(ball,Bullet)):
           self.bullets.append(ball)
        else:
           self.balls.append(ball)
    
    def remove_ball(self, ball): 
       if(isinstance(ball,Bullet)):
           self.bullets.remove(ball)
       else:
           self.balls.remove(ball)
           
    def process_input(self):
        if self.player.controller:
            if (self.player.controller.get_axis(0) > 0.5):
                self.gun.move_right()
            elif (self.player.controller.get_axis(0) < -0.5):
                self.gun.move_left()
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[self.left_key]:
                self.gun.move_left()
            elif pressed_keys[self.right_key]:
                self.gun.move_right()
    
    def bullet_reload(self,time): #this is time independent with each gun
        if time-self.gun.last_reload_time >= self.gun.reload_rate:
            self.gun.last_reload_time = time
            if self.gun.bullets_curr < self.gun.max_bullets:
                self.gun.bullets_curr += 1
    
    def spawn_spinner(self):
#        print "spawn spin"
        if len(self.spinners)%2 == 0:
            direction = 2
        else:
            direction = -2
            
        new_spinner = Spinner(self, .5*self.width, -(self.spinner_block.pos_y + self.wall_gap + 30) + self.height, self.spinner_size, self.spinner_size, 0, 1, -math.pi/60, direction, .1*self.width, .9*self.width)
        self.spinners.append(new_spinner)
        
    def spawn_barrel_cannon(self):
        new_barrel_cannon = Barrelcannon(self, .5*self.width, -(self.barrel_cannon_block.pos_y + self.wall_gap + 30) + self.height, 20, 30, 1, 1, -math.pi/60, 2, .2*self.width, .8*self.width)
        
    def spawn_swing(self): # set running to False if no more swings can be spawned, signaling endgame
        if len(self.connected_swings) >= self.swing_limit: #all swings are connected
            all_have_balls = True # all the connected swings have balls
            for swing in self.connected_swings:
                if swing.ball == None:
                    all_have_balls = False
                    break

            if all_have_balls:    
                self.running = False
        else:
            init_swing_cnt = len(self.connected_swings)
            spawned = False
            while spawned == False:
                rand_swing_index = random.randint(0,len(self.connected_swings)-1)
                sel_swing = self.connected_swings[rand_swing_index]
                
                ball_spawn = False
                if sel_swing.ball == None:
                    ball_spawn = sel_swing.respawn_ball(sel_swing.circle_mass,sel_swing.radius,1, "red")
                else:
                    new_tier = sel_swing.tier + 1
                        
                    if new_tier == 2:
                        new_swing = Polyswing(self,200,550,1,1,.33*sel_swing.section_mass,500,1,.33*sel_swing.circle_mass,15,1,4,sel_swing,2,new_tier,"red")
                    else: #its tier 3
                        new_swing = Polyswing(self,200,550,1,1,.5*sel_swing.section_mass,500,1,.5*sel_swing.circle_mass,10,1,2,sel_swing,0,new_tier, "red")         
              
                if ball_spawn or len(self.connected_swings) > init_swing_cnt:
                    spawned = True
                    
    def set_end_time(self):
        if self.end_time_set == False:
            self.end_time = time.time()
            self.end_time_set = True
            
    def set_spinner_block(self):
        self.spinner_block = Buildblock(self,0,self.height/2,60,self.width,(255,0,0))
    
    def set_barrel_cannon_block(self):
        self.barrel_cannon_block = Buildblock(self,0,self.height/2,60,self.width,(0,255,0))
        
    def objects_to_send(self):
        master_list = [] # list of dictionaries
        # go through balls, swings, cannons, guns, spinners
        ball_list = []
        for ball in self.balls: # each ball takes up four slots
            ball_list.append(int(ball.body.position.x+self.virt_x_offset))
            ball_list.append(int(self.display_height-int(ball.body.position.y)))
            ball_list.append(ball.color_index)
            ball_list.append(ball.radius)
        master_list.append(ball_list)
        
        bullet_list = []
        for bullet in self.bullets: # each bullet takes up four slots
            bullet_list.append(int(bullet.body.position.x+self.virt_x_offset))
            bullet_list.append(int(self.display_height-int(bullet.body.position.y)))
            bullet_list.append(bullet.color_index)
            #bullet_list.append(bullet.radius)
        master_list.append(bullet_list)
        
        swing_list = []    
        for swing in self.swings:
            for section in swing.sections: 
                if section != swing.sections[-1]:
                    length = self.distance(section.body.position, swing.sections[swing.sections.index(section)+1].body.position)
                    angle = self.angle(section.body.position, swing.sections[swing.sections.index(section)+1].body.position)
#                    print angle
                    
                    if len(swing.sections) == 2:
                        image = 0
                        #vine_scaled = pygame.transform.scale(self.vine_short, (6, int(length + 2)))
                    else: #its longer than 2
                        if section == swing.sections[0]: #first section
                            image = 1
                            #vine_scaled = pygame.transform.scale(self.vine_top, (6, int(length + 2)))
                        elif section == swing.sections[-2]: # second to last section
                            image = 2
                            #vine_scaled = pygame.transform.scale(self.vine_bot, (6, int(length + 2)))
                        else: #everything else
                            image = 3
                            #vine_scaled = pygame.transform.scale(self.vine_mid, (6, int(length + 2)))
                    
                    vine_angle = int(90 + (angle*180)/math.pi)
                    #vine_turned = pygame.transform.rotate(vine_scaled, 90 + (angle*180)/math.pi)
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

                    swing_list.append(image)
                    swing_list.append(int(section.body.position.x+self.virt_x_offset + xpos))
                    swing_list.append(int(self.display_height - section.body.position.y + ypos))
                    swing_list.append(vine_angle)
                    swing_list.append(int(length))
                    
#                    self.stage.screen.blit(vine_turned, (section.body.position.x+self.stage.x_offset + xpos, self.stage.display_height - section.body.position.y + ypos))                
#                swing_list.append(int(section.body.position.x+self.virt_x_offset))
#                swing_list.append(int(self.display_height-int(section.body.position.y)))
        master_list.append(swing_list)
        
        cannon_list = []
        for cannon in self.cannons: # each cannon takes up 9 slots
            
            if cannon.body.angle <= 0 and cannon.body.angle > -math.pi/2:
                #print "down to left"
                xpos = math.cos(cannon.body.angle) * (-cannon.width) + -math.sin(cannon.body.angle) * (-cannon.height) 
                ypos = -math.sin(cannon.body.angle) * (-cannon.width) + -math.cos(cannon.body.angle) * (cannon.height) 
            elif cannon.body.angle <= -math.pi/2 and cannon.body.angle > -math.pi:
                #print "left to up"
                xpos = -math.cos(cannon.body.angle) * (-cannon.width) + -math.sin(cannon.body.angle) * (-cannon.height) 
                ypos = -math.sin(cannon.body.angle) * (-cannon.width) + -math.cos(cannon.body.angle) * (-cannon.height) 
            elif cannon.body.angle <= -math.pi and cannon.body.angle > -3*math.pi/2:
                #print "up to right"
                xpos = -math.cos(cannon.body.angle) * (-cannon.width) + math.sin(cannon.body.angle) * (-cannon.height) 
                ypos = math.sin(cannon.body.angle) * (-cannon.width) + -math.cos(cannon.body.angle) * (-cannon.height)
            else:
                #print "right to down"
                xpos = math.cos(cannon.body.angle) * (-cannon.width) + math.sin(cannon.body.angle) * (-cannon.height) 
                ypos = math.sin(cannon.body.angle) * (-cannon.width) + math.cos(cannon.body.angle) * (-cannon.height)
            
            x = cannon.body.position.x+self.virt_x_offset + xpos
            y = self.display_height - cannon.body.position.y + ypos
            angle = int((cannon.body.angle*180)/math.pi)
            
            if(cannon.loaded):
                isLoaded = 1
            else:
                isLoaded = 0
            cannon_list.append(int(x))
            cannon_list.append(int(y))
            cannon_list.append(angle)
            cannon_list.append(isLoaded)
        master_list.append(cannon_list)
        
        spinner_list = []
        for spinner in self.spinners: # each spinner takes up 8 slots
            seg1_pt1 = spinner.seg1.body.position+spinner.seg1.a.rotated(math.degrees(spinner.seg1.body.angle))
            seg1_pt2 = spinner.seg1.body.position+spinner.seg1.b.rotated(math.degrees(spinner.seg1.body.angle))
            seg1_pt1_x = self.virt_x_offset+seg1_pt1.x
            seg1_pt1_y = -seg1_pt1.y+self.height
            seg1_pt2_x = self.virt_x_offset+seg1_pt2.x
            seg1_pt2_y = -seg1_pt2.y+self.height
            
            seg2_pt1 = spinner.seg2.body.position+spinner.seg2.a.rotated(math.degrees(spinner.seg1.body.angle))
            seg2_pt2 = spinner.seg2.body.position+spinner.seg2.b.rotated(math.degrees(spinner.seg1.body.angle))
            seg2_pt1_x = self.virt_x_offset+seg2_pt1.x
            seg2_pt1_y = -seg2_pt1.y+self.height
            seg2_pt2_x = self.virt_x_offset+seg2_pt2.x
            seg2_pt2_y = -seg2_pt2.y+self.height
                      
            seg1_pts = [seg1_pt1_x,seg1_pt1_y,seg1_pt2_x,seg1_pt2_y]
            seg2_pts = [seg2_pt1_x,seg2_pt1_y,seg2_pt2_x,seg2_pt2_y]
            
            spinner_list.append(seg1_pts[0])
            spinner_list.append(seg1_pts[1])
            spinner_list.append(seg1_pts[2])
            spinner_list.append(seg1_pts[3])
            spinner_list.append(seg2_pts[0])
            spinner_list.append(seg2_pts[1])
            spinner_list.append(seg2_pts[2])
            spinner_list.append(seg2_pts[3])
        master_list.append(spinner_list)
        
        #gun
        if self.gun.body.angle > math.pi:
            xpos = -math.cos(self.gun.body.angle) * (-self.gun.width - 3) + -math.sin(self.gun.body.angle) * (-3*self.gun.height - 3) 
            ypos = -math.sin(self.gun.body.angle) * (-self.gun.width - 3) + -math.cos(self.gun.body.angle) * (-3*self.gun.height - 3) 
        else:
            xpos = -math.cos(self.gun.body.angle) * (-self.gun.width - 3) + -math.sin(self.gun.body.angle) * (-self.gun.height + 3) 
            ypos = -math.sin(self.gun.body.angle) * (self.gun.width + 3) + -math.cos(self.gun.body.angle) * (-3*self.gun.height - 3) 
        
        x = self.gun.cannon_shape.body.position.x + self.virt_x_offset + xpos
        y = self.display_height - self.gun.cannon_shape.body.position.y + ypos
        gun_angle = int((self.gun.body.angle*180)/math.pi)
        
        master_list.append(int(x))
        master_list.append(int(y))
        master_list.append(gun_angle)
        #    TODO: add block occupancy info too
        master_list.append(self.point_total)
        master_list.append(self.gun.bullets_curr)
        master_list.append(self.running)
        
        return master_list

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
   
    def buy_capacity(self):
        # capacity = [1,self.gun.capacity_upgrade_level_max,[("Upgrade Capacity",self.upgrade_capacity_price)],self.buy_capacity]
        info = self.buy_info[0]
        upgrade_price = info[2][0][1]
        upgrade_level = info[1]
        if self.point_total >= upgrade_price and upgrade_level > 0:
            info[1] -= 1
            self.gun.max_bullets += 1
            self.point_total -= upgrade_price
            self.purchases_made += 1
        if info[1] == 0: # if no more upgrades are possible
            info[0] = 0
            self.build_up_operation(None)
            
    def buy_reload_rate(self):
        # reload_rate = [1,self.gun.rate_upgrade_level_max,[("Reload Rate",self.upgrade_reload_rate_price)],self.buy_reload_rate]
        info = self.buy_info[1]
        upgrade_price = info[2][0][1]
        upgrade_level = info[1]
        if self.point_total >= upgrade_price and upgrade_level > 0:
            info[1] -= 1
            self.gun.reload_rate -= 0.2
            self.point_total -= upgrade_price
            self.purchases_made += 1
        if info[1] == 0: # if no more upgrades are possible
            info[0] = 0
            self.build_up_operation(None)
            
    def buy_gun_force(self):
        info = self.buy_info[2]
        upgrade_price = info[2][0][1]
        upgrade_level = info[1]
        if self.point_total >= upgrade_price and upgrade_level > 0:
            info[1] -= 1
            self.gun.impulse_upgrade_level += 1
            self.point_total -= upgrade_price
            self.purchases_made += 1
        if info[1] == 0: # if no more upgrades are possible
            info[0] = 0
            self.build_up_operation(None)
            
    def buy_barrel_cannon(self,opponent_stage):
        # barrel_cannon = [1,3,[("Barrel Cannon",self.bc_price),("Upgrade Barrel Cannon",self.upgrade_bc_price)],self.buy_barrel_cannon]
        info = self.buy_info[3]
        upgrade_level = info[1]
        if len(self.cannons) == 0: # if building cannon
            upgrade_price = info[2][0][1]
            if self.barrel_cannon_block == None and (opponent_stage == None or opponent_stage.spinner_block == None):
                if self.point_total >= upgrade_price and upgrade_level > 0:
                    self.set_barrel_cannon_block()
            elif self.barrel_cannon_block and self.occupancy_of_blocks[self.barrel_cannon_block.get_occupancy_index()] == False:
                info[1] -= 1
                self.spawn_barrel_cannon()
                self.occupancy_of_blocks[self.barrel_cannon_block.get_occupancy_index()] = True
                self.barrel_cannon_block = None
                self.point_total -= upgrade_price
                self.purchases_made += 1
                self.buy_info[3][3] = 1 # switch to display Cannon Upgrade
        else: # if upgrading cannon
            upgrade_price = info[2][1][1]
            if self.point_total >= upgrade_price and upgrade_level > 0:
                for cannon in self.cannons:
                    if cannon.upgrade < cannon.upgrade_max:
                        info[1] -= 1
                        cannon.upgrade += 1 
                        self.point_total -= upgrade_price
                        self.purchases_made += 1
                if info[1] == 0: # if no more upgrades are possible
                    info[0] = 0
                    self.build_up_operation(None) 
            
    def buy_spinner(self,opponent_stage):
        info = self.buy_info[4]
        upgrade_level = info[1]
        upgrade_price = info[2][0][1]
        if self.barrel_cannon_block == None and opponent_stage.spinner_block == None:
            if len(opponent_stage.spinners) < opponent_stage.spinner_limit and self.point_total >= upgrade_price and upgrade_level:
                opponent_stage.set_spinner_block()
        elif opponent_stage.spinner_block != None and opponent_stage.occupancy_of_blocks[opponent_stage.spinner_block.get_occupancy_index()] == False:
            info[1] -= 1
            opponent_stage.spawn_spinner()
            opponent_stage.occupancy_of_blocks[opponent_stage.spinner_block.get_occupancy_index()] = True
            opponent_stage.spinner_block = None
            self.point_total -= upgrade_price
            self.purchases_made += 1
            if len(opponent_stage.spinners) >= opponent_stage.spinner_limit:
                info[0] = 0 # disable display on buy menu
                self.build_up_operation(None)
            if self.buy_info[5][1] != 0:
                self.buy_info[5][0] = 1 # enable display for spinner upgrades

    def buy_spinner_upgrade(self,opponent_stage):
        info = self.buy_info[5]
        upgrade_level = info[1]
        upgrade_price = info[2][0][1]
        if self.point_total >= upgrade_price and upgrade_level > 0:
            info[1] -=1
            self.point_total -= upgrade_price
            self.purchases_made += 1
            
            opponent_stage.spinner_size += 10
            for spinner in opponent_stage.spinners:
                opponent_stage.space.remove(spinner.seg1,spinner.seg2)      
                spinner.seg1 = pm.Segment(spinner.body, (-opponent_stage.spinner_size/2,0), (opponent_stage.spinner_size/2,0), 5)
                spinner.seg2 = pm.Segment(spinner.body, (0,-opponent_stage.spinner_size/2), (0,opponent_stage.spinner_size/2), 5)              
                opponent_stage.space.add(spinner.seg1,spinner.seg2)
            
            if info[1] == 0: # if no more upgrades are possible
                info[0] = 0
                self.build_up_operation(None)
            

    
def bullet_collision(shapeA, shapeB, contacts, normal_coef, data=None):
    if shapeB.ball.change_color() == False and shapeB.ball.detached != True:
        shapeB.ball.swing.destroy_joint(shapeA.stage.child_bonus,shapeB.stage.grandchild_bonus)
        shapeB.ball.detached = True # should not affect the swing if it is detached.
    return True

def barrelcannon_load(shapeA, shapeB, contacts, normal_coef, data=None):
    if shapeB.container.loaded == False and shapeA.ball.color == "yellow":
        shapeA.body.position.y = -1000 #clears the bullet
        shapeB.container.collect() #loads the cannon
    return True