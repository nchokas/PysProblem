import pygame

class Buildblock(object):
    
    def __init__(self, stage, pos_x, pos_y, height, width, color):
        self.stage = stage
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = height
        self.width = width
        self.color = color
        self.occupancy_index = 0
    
    def move_up(self):
        if self.pos_y - self.height > self.stage.height/2 - 60:
            self.pos_y = self.pos_y - self.height
            self.occupancy_index = self.occupancy_index - 1
            
    
    def move_down(self):
        if self.pos_y - self.height < self.stage.height/2 + 180:
            self.pos_y = self.pos_y + self.height
            self.occupancy_index = self.occupancy_index + 1
    
    def get_occupancy_index(self):
        return self.occupancy_index
    
    def draw_self(self):
        
        p1 = self.pos_x + self.stage.x_offset + self.stage.wall_gap, self.pos_y + self.stage.wall_gap
        p2 = self.pos_x + self.stage.x_offset + self.stage.wall_gap + (self.width - 2*self.stage.wall_gap),self.pos_y + self.stage.wall_gap
        p3 = self.pos_x + self.stage.x_offset + self.stage.wall_gap + (self.width - 2*self.stage.wall_gap), self.pos_y + self.stage.wall_gap + self.height
        p4 = self.pos_x + self.stage.x_offset + self.stage.wall_gap, self.pos_y + self.stage.wall_gap + self.height
        pointlist = [p1, p2, p3, p4]
   
        pygame.draw.lines(self.stage.screen, self.color, True, pointlist)
        