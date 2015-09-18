import pymunk as pm

class Lineswing(object):
#needs to use new ball class
 
#    1: the space the lineswing will belong to
#    2: the x position of the top 
#    3: the y position of the top
#    4: the length of the line
#    5: the mass of the line
#    6: the mass of the circle
#    7: the radius of the circle
#    8: the elasticity of the circle
#    9: the padding on the segment
#    10: the inertia of the segment
#    11: the elasticity of the segment
    
    def __init__(self, space, pos_x, pos_y, seg_length, seg_mass, circle_mass, radius, circle_elasticity, seg_padding, seg_inertia, seg_elasticity):        
        
        self.rotation_center_body = pm.Body(pm.inf, pm.inf) # 1
        self.rotation_center_body.position = (pos_x,pos_y)
            
        self.body = pm.Body(seg_mass, seg_inertia) # 2
        self.body.position = (pos_x,pos_y)    
            
        self.s1 = pm.Segment(self.body, (0, 0), (0.0, -seg_length), seg_padding)
        self.s1.elasticty = seg_elasticity
        
        inertia = pm.moment_for_circle(circle_mass, 0, radius, (0,0))
        self.ballBody = pm.Body(circle_mass, inertia)
        self.ballBody.position = (pos_x, pos_y - (seg_length + radius) )
        
        self.circle = pm.Circle(self.ballBody, radius, (0,0))
        self.circle.elasticity = circle_elasticity
#        
        self.rotation_center_joint = pm.PinJoint(self.body, self.rotation_center_body, (0,0), (0,0)) # 3
        self.rotation_center_joint2 = pm.PinJoint(self.ballBody, self.body, (0,0), (0,-seg_length))    

        space.add(self.s1, self.circle, self.ballBody, self.body, self.rotation_center_joint, self.rotation_center_joint2)