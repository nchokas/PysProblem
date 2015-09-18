import pymunk as pm
import pygame
from pygame.color import *

#this poly is aware of it's container (of any level)

#self.cannon_shape = pm.Poly(self.body,  [(-width,-height), (-width,height),(width,height),(width,-height)] ,(0, 0), False)


class PAPoly(pm.Poly):
    def __init__(self, body, vertices, offset,  auto_order_vertices, container):
        pm.Poly.__init__(self, body, vertices, offset,  auto_order_vertices)
        self.container = container
    