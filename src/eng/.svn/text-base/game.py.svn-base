import os,sys, random, time, pygame, pymunk as pm, math, threading
from pygame.locals import *
from pygame.color import *
from pygame.mixer import *
from stage import Stage
from polyswing import Polyswing
from player import Player
from virtual_stage import Virtualstage
from threading import Semaphore

try:
    import psyco
    psyco.profile(0.001)
except ImportError:
    pass

os.environ['SDL_VIDEO_CENTERED'] = '1'

level_music = ["Retrospect.ogg","Harvest Tunes.ogg","Fuer Py.ogg","8 Bit Anthem.ogg","Chip Tune.ogg","Bolo the Brute.ogg"]        

class Game(object):
    def __init__(self,players,fullscreen,songSelect,get_data,send_data): # fullscreen is boolean
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.graphics_path = "../res/graphics/" # should be passed by UI and then passed to stage
        self.sound_path = "../res/sound/" # should be passed by UI and then passed to stage
        self.barellCannonShoot = pygame.mixer.Sound(self.graphics_path+"barrelCannonShoot.ogg")
        self.quitSound = pygame.mixer.Sound(self.sound_path+"gottago.ogg")
        self.lose = pygame.mixer.Sound(self.sound_path+"mescusi.ogg")
        self.sem = threading.Semaphore()
        self.players = players
        self.stage_width,self.stage_height = 550,800
        self.sidebar_width = 180 # sidebar displays statistics
        if len(players) == 1 and get_data == None and send_data == None:
            self.sidebar_width += 10
        self.wall_gap = 10 # space between the walls and the edge of the window
        self.gap_size = 300.0 # how big the gap in the middle is
        self.padding = 10.0 # segment padding
        self.gravity = (0.0, -100.0)
        self.bound_color = "lightgray" # boundary walls color
        self.bg_color = "black" # window background color
        self.bullet_color = "yellow"
        self.step_size = 1/30.0
        self.running = False
        self.stages = []
        self.spawn_rate = 3
        self.spawn_rate_step = 0.25
        self.spawn_rate_interval = 30
        self.swing_y_lower_lim = 0.75 # used in generation of random starting position for swings
        self.swing_y_upper_lim = 0.95
        self.loser = None # pointer to loser player
        self.get_data = get_data
        self.send_data = send_data
        self.virtual_stage = None
        self.opponent_name = None
        self.y_pos = None
        self.game_finished = False
          
        pygame.init()
        
        if songSelect == 0:
            random.seed()
            randNum = random.randint(0,len(level_music)-1)
            pygame.mixer.music.load(self.sound_path+level_music[randNum])
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(USEREVENT)
        else:
            pygame.mixer.music.load(self.sound_path+level_music[int(songSelect)-1])
            pygame.mixer.music.play(-1)

        if get_data != None and send_data != None:
            self.networked_game = True
        else:
            self.networked_game = False
        
        if self.networked_game:
            self.get_data.fun = self.parse_data # register data handling callback
            screen_dim = (2*self.stage_width+self.sidebar_width,self.stage_height)
        else:
            screen_dim = (len(self.players)*self.stage_width+self.sidebar_width,self.stage_height)
        if fullscreen:
            self.screen = pygame.display.set_mode(screen_dim,pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_dim,HWSURFACE)
            
        self.background = pygame.image.load(self.graphics_path+"background.jpg").convert()
        
        if len(players) == 2 or get_data != None: #if its a multiplayer game
            self.gameover = pygame.image.load(self.graphics_path+"2pGameOver.png").convert_alpha()
        else:
            self.gameover = pygame.image.load(self.graphics_path+"1pGameOver.png").convert_alpha()
            
          
        self.clock = pygame.time.Clock()
        pm.init_pymunk()
                
        if self.networked_game: 
            x_offset = 0
            #time.sleep(3)
            name_dict = {"player_name":players[0].name}
            self.send_data.send([name_dict])
            #if it is the host, generate the random y position of the swings and send it to the client
            if self.send_data.comp == "server":
                self.y_pos = [random.randint(self.stage_height*self.swing_y_lower_lim,self.stage_height*self.swing_y_upper_lim),random.randint(self.stage_height*self.swing_y_lower_lim,self.stage_height*self.swing_y_upper_lim),random.randint(self.stage_height*self.swing_y_lower_lim,self.stage_height*self.swing_y_upper_lim)]
                y_pos_dict = {"y_pos" : self.y_pos}
                self.send_data.send([y_pos_dict])
            #otherwise get the data from the host and parse the data
            while(self.y_pos == None or self.opponent_name == None):
                time.sleep(.1)
            
            new_stage = Stage(players[0],self.screen,self.stage_width,self.stage_height,self.wall_gap,self.gap_size,self.padding,self.bound_color,self.gravity,x_offset,self.sidebar_width,self.bullet_color, True,self.graphics_path,self.sound_path)
            x_step = self.stage_width/4
            j = 0
            for i in range(x_step,x_step*4,x_step):
                new_swing = Polyswing(new_stage,i,self.y_pos[j],1,1,10,1500,1,10,20,1,7,None,3,1,"red")
                j += 1
            
            self.stages.append(new_stage)
            
            x_offset += self.stage_width+self.sidebar_width
            
            #set up opponents virtual stage
            self.virtual_stage = Virtualstage(self.screen,self.stage_width,self.stage_height,self.wall_gap,self.gap_size,self.sidebar_width,self.bound_color,x_offset,self.graphics_path,self.sound_path)
            self.virtual_stage.player = Player(self.opponent_name,1,None,None,None,None,None,None,None,None,None,None)
                        
            
        else: #it's not a networked game
            x_offset = 0
            self.y_pos = [random.randint(self.stage_height*self.swing_y_lower_lim,self.stage_height*self.swing_y_upper_lim),random.randint(self.stage_height*self.swing_y_lower_lim,self.stage_height*self.swing_y_upper_lim),random.randint(self.stage_height*self.swing_y_lower_lim,self.stage_height*self.swing_y_upper_lim)]
            if len(self.players) > 1:
                is_multiplayer = True
            else:
                is_multiplayer = False
                
            for player in self.players: # initialize stage for each player
                new_stage = Stage(player,self.screen,self.stage_width,self.stage_height,self.wall_gap,self.gap_size,self.padding,self.bound_color,self.gravity,x_offset,self.sidebar_width,self.bullet_color,is_multiplayer,self.graphics_path,self.sound_path)
                x_step = self.stage_width/4
                j = 0
                for i in range(x_step,x_step*4,x_step):
                    new_swing = Polyswing(new_stage,i,self.y_pos[j],1,1,10,1500,1,10,20,1,7,None,3,1,"red")
                    j += 1
                
                self.stages.append(new_stage)
                x_offset += self.stage_width+self.sidebar_width    
        
        #use player 1's sound volume by default
        self.barellCannonShoot.set_volume(players[0].volume)
        self.quitSound.set_volume(players[0].volume)
        self.lose.set_volume(players[0].volume)
                
    def start(self): # start pymunk, run main loop, and then return stats for each player
        self.running = True
        
        last_swing_spawn = 0 # last swing spawn
        last_spawn_rate_update = 0
        last_net_stat_update = 0
        last_score_sent = 0
        
        while self.running: # main game loop
            game_time = pygame.time.get_ticks()/1000.
            if self.game_finished:
                self.running = False
            if self.networked_game: 
                if game_time-last_net_stat_update >= 0.25:
                    last_net_stat_update = game_time
                    self.send_data.send(self.stages[0].objects_to_send())
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitSound.play()
                    self.running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.quitSound.play()
                    self.running = False
                elif event.type == USEREVENT:
                    randNum = random.randint(0,len(level_music)-1)
                    pygame.mixer.music.load(self.sound_path+level_music[randNum])
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(USEREVENT)
                    
                for stage in self.stages:
                    if stage.running == True:
                        if stage.player.controller:
                            if (event.type==JOYBUTTONDOWN and stage.player.controller.get_button(0)):
                                stage.gun.shoot(1200)
                            elif (event.type==JOYBUTTONDOWN and stage.player.controller.get_button(2)):
                                if len(stage.cannons) > 0:
                                    stage.cannons[0].shoot(1000)
                                    if stage.cannons[0].loaded:
                                        self.barellCannonShoot.play()
                                
                            opponent_stage = None
                            for find_stage in self.stages:
                                if find_stage != stage:
                                    opponent_stage = find_stage
                            
                            if (event.type == JOYBUTTONDOWN and stage.player.controller.get_button(5)):
                                stage.build_down_operation(opponent_stage)
                            if (event.type == JOYBUTTONDOWN and stage.player.controller.get_button(4)):
                                stage.build_up_operation(opponent_stage)
                            if (event.type == JOYBUTTONDOWN and stage.player.controller.get_button(1)):
                                stage.build_operation(opponent_stage)
                            if (event.type == JOYBUTTONDOWN and stage.player.controller.get_button(3)):
                                stage.cancel_operation(opponent_stage)
                                
                        else:                                
                            if event.type == KEYDOWN and event.key == stage.shoot_key:
                               stage.gun.shoot(1200)
                            elif event.type == KEYDOWN and event.key == stage.player.key_barrel_shoot:
                                #there should only be 1 barrel at most... if there are more this needs to be changed
                                if len(stage.cannons) > 0:
                                    stage.cannons[0].shoot(1000)
                                    if stage.cannons[0].loaded:
                                        self.barellCannonShoot.play()
                           
                            opponent_stage = None
                            for find_stage in self.stages:
                                if find_stage != stage:
                                    opponent_stage = find_stage
                        
                            if event.type == KEYDOWN and event.key == stage.player.key_build_down:
                                stage.build_down_operation(opponent_stage)
                        
                            if event.type == KEYDOWN and event.key == stage.player.key_build_up:
                                stage.build_up_operation(opponent_stage)
                        
                            if event.type == KEYDOWN and event.key == stage.player.key_build_confirm:
                                stage.build_operation(opponent_stage)
                        
                            if event.type == KEYDOWN and event.key == stage.player.key_build_cancel:
                                stage.cancel_operation(opponent_stage)
                

            self.screen.blit(self.background, (0, 0))

            if game_time - last_spawn_rate_update >= self.spawn_rate_interval:
                last_spawn_rate_update = game_time
                self.update_spawn_rate()
                    
            if game_time-last_swing_spawn >= self.spawn_rate:
                last_swing_spawn = game_time
                for stage in self.stages:
                    stage.spawn_swing()
            
            for stage in self.stages:
                stage.process_input()
                if stage.running == True:
                    stage.bullet_reload(game_time)
                    stage.move_items()
                    stage.space.step(self.step_size)
                else:
                    for stage2 in self.stages:
                        stage2.set_end_time()
                    if self.virtual_stage != None:
                        self.sem.acquire()
                        self.virtual_stage.set_end_time()
                        self.sem.release()
                    if(self.loser == None):
                        self.loser = stage.player
                    self.game_finished = True
                stage.draw_self()
                    
            if self.virtual_stage != None:
                self.sem.acquire()
                if self.virtual_stage.running == False:
                    print "other player has LOST"
                    self.stages[0].set_end_time()
                    self.virtual_stage.set_end_time()
                    if(self.loser == None):
                        self.loser = self.virtual_stage.player
                    self.game_finished = True
                self.virtual_stage.draw_self()
                self.sem.release()           
                        
            # send network update every two seconds
            

            pygame.display.flip()
            self.clock.tick(1/self.step_size)    
        
        stats = [] # list of stat dictionaries for each player
        for stage in self.stages:
            player_stats = {}
            player_stats['player'] = stage.player
            player_stats['points'] = stage.point_total
            player_stats['purchases_made'] = stage.purchases_made
            player_stats['time_elapsed'] = stage.end_time - stage.start_time
            if(self.loser == stage.player):
                player_stats['won_game'] = False
            else:
                player_stats['won_game'] = True 
            stats.append(player_stats)
        # ADD: virtual stats
        
        if self.game_finished == True:
            self.screen.blit(self.gameover, (0, 0))
            #display who won and how many seconds it was
            # Create a font
            verdana = pygame.font.match_font('Verdana')
            font = pygame.font.Font(verdana, 32)
            
            # Render the text
            if len(self.players) == 1 and self.get_data == None: #message for single player
                message = "You survived " + str(int(self.stages[0].end_time-self.stages[0].start_time)) + " seconds!"
            elif len(self.players) == 2 and self.get_data == None: #local multi
                #find the name of the winner
                winner = None
                for stage in self.stages:
                    if self.loser != stage.player:
                        winner = stage
                message = winner.player.name + " won in " + str(int(winner.end_time-winner.start_time)) + " seconds!"
            elif self.networked_game:
                winner = None
                if self.loser == self.stages[0].player:
                    winner = self.virtual_stage
                else:
                    winner = self.stages[0]
                message = winner.player.name + " won in " + str(int(winner.end_time-winner.start_time)) + " seconds!"
                
            text = font.render(message, True, (255,255, 255))
            
            # Create a rectangle
            textRect = text.get_rect()
            
            # Center the rectangle
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 700
            
            # Blit the text
            self.screen.blit(text, textRect)
            pygame.display.flip()
            
            self.lose.play()
            time.sleep(5)
            return stats            

    def update_spawn_rate(self):
        if self.spawn_rate - self.spawn_rate_step >= 0.5:
            self.spawn_rate -= self.spawn_rate_step
            
    def parse_data(self,data_list):
        # we also need dict to tell both players to start game, and one to signal to the other that they lost
        if self.y_pos == None or self.opponent_name == None:
            for dict in data_list:
                for k,v in dict.iteritems():
                    if k == "y_pos":
                        self.y_pos = v
                    elif k == "player_name":
                        self.opponent_name = v
        else:
            self.sem.acquire()
            if self.virtual_stage != None:        
                self.virtual_stage.ball_prop = data_list[0]              
                self.virtual_stage.bullet_prop = data_list[1]
                self.virtual_stage.swing_prop = data_list[2]
                self.virtual_stage.cannon_prop = data_list[3]
                self.virtual_stage.spinner_prop = data_list[4]
                self.virtual_stage.gun_prop = []
                for i in range(5,8):
                    self.virtual_stage.gun_prop.append(data_list[i])
                self.virtual_stage.point_total = int(data_list[8])
                self.virtual_stage.gun_bullets_curr = int(data_list[9])
                self.virtual_stage.running = data_list[10]
                if self.virtual_stage.running == False:
                    print "IT IS NOW FALSE OMG"
            
            self.sem.release() 