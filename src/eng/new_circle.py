import pymunk as pm, pygame
from pygame.color import *

class NewCircle(pm.Circle):
    def __init__(self, stage, ball, body, radius, offset):
        self.ball = ball
        self.stage = stage
        pm.Circle.__init__(self, body, radius, offset)
    
    def destroy_self(self):
        self.body.position.y = -100