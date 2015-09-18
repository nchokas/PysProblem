import pymunk as pm
from ball import Ball

class SwingBall(Ball):
    def __init__(self, stage, swing, pos_x, pos_y, circle_mass, radius, circle_elasticity, color):
        Ball.__init__(self, stage, pos_x, pos_y, circle_mass, radius, circle_elasticity, color)
        self.swing = swing
        self.detached = False