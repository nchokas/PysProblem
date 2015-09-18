import pymunk as pm, pygame
from pygame.color import *
from new_circle import NewCircle

class Ball(object):
	
	#1: stage
	#2: the x position 
	#3: the y position
	#4: the mass of the ball
	#5: the radius of the ball
	#6: the elasticity of the ball
	#7: the color of the ball 
	
	def __init__(self, stage, pos_x, pos_y, circle_mass, radius, circle_elasticity, color):
		self.stage = stage
		self.color = color
		self.radius = radius
		self.inertia = pm.moment_for_circle(circle_mass, 0, radius, (0,0))
		self.body = pm.Body(circle_mass, self.inertia)
		self.body.position = pos_x, pos_y
		self.circle = NewCircle(self.stage, self, self.body, self.radius, (0,0))
		self.circle.collision_type = 2 # 2 is ball
		self.circle.elasticity = circle_elasticity
		self.stage.space.add(self.body, self.circle)
		#self.stage.balls.append(self)
		self.stage.add_ball(self)
		self.colors = ["red","orange","yellow","green","blue","purple"]
		self.point_values = {"red":(0,600),"orange":(1,500),"yellow":(2,400),"green":(3,300),"blue":(4,200),"purple":(5,100)}
		self.color_index = self.point_values[self.color][0]
		self.point_value = self.point_values[self.color][1]
		self.point_multiplier = 1.0
		#all the ball graphics
		self.red_nut = pygame.image.load(self.stage.graphics_path + "nut1.png").convert_alpha()
		self.orange_nut = pygame.image.load(self.stage.graphics_path + "nut2.png").convert_alpha()
		self.yellow_nut = pygame.image.load(self.stage.graphics_path + "nut3.png").convert_alpha()
		self.green_nut = pygame.image.load(self.stage.graphics_path + "nut4.png").convert_alpha()
		self.blue_nut = pygame.image.load(self.stage.graphics_path + "nut5.png").convert_alpha()
		self.purple_nut = pygame.image.load(self.stage.graphics_path + "nut6.png").convert_alpha()
		
		self.gun_bullet = pygame.image.load(self.stage.graphics_path + "gunbullet.png").convert_alpha()
		self.cannon_bullet = pygame.image.load(self.stage.graphics_path + "cannonbullet.png").convert_alpha()
		 
		
	def destroy_self(self):
		self.stage.space.remove(self.circle, self.circle.body)
		self.stage.remove_ball(self)
		
	def change_color(self):
		if self.color_index == len(self.colors)-1:
			return False
		else:
			self.color_index += 1
		self.color = self.colors[self.color_index]
		return True
	
	def draw_self(self):
		#decide which color it is
		if self.color == "red":
			current_image = self.red_nut
		elif self.color == "orange":
			current_image = self.orange_nut
		elif self.color == "yellow":
			current_image = self.yellow_nut
		elif self.color == "green":
			current_image = self.green_nut
		elif self.color == "blue":
			current_image = self.blue_nut
		else:
			current_image = self.purple_nut
			
		current_image = pygame.transform.scale(current_image,(2+self.radius * 2, 2+self.radius * 2))

		new_pos_y = self.stage.display_height-int(self.body.position.y)-self.radius -2 
		p = int(self.body.position.x+self.stage.x_offset-self.radius - 2), new_pos_y
        
		self.stage.screen.blit(current_image, p)
		  
#		new_pos_y = self.stage.display_height-int(self.body.position.y)
#		p = int(self.body.position.x+self.stage.x_offset), new_pos_y
#		pygame.draw.circle(self.stage.screen, THECOLORS[self.color], p, int(self.radius), 2)
		
	   