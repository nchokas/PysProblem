import pymunk as pm

class Lineswing(object):
    
    def __init__(self, space, pos_x, pos_y, seg_length, seg_mass, circle_mass, radius, elasticity, seg_padding, seg_inertia):        
        
        self.rotation_center_body = pm.Body(pm.inf, pm.inf) # 1
        self.rotation_center_body.position = (pos_x,pos_y)
            
        self.body = pm.Body(seg_mass, seg_inertia) # 2
        self.body.position = (pos_x,pos_y)    
            
        self.s1 = pm.Segment(self.body, (0, 0), (0.0, -seg_length), seg_padding)

        inertia = pm.moment_for_circle(circle_mass, 0, radius, (0,0))
        self.ballBody = pm.Body(circle_mass, inertia)
        self.ballBody.position = (pos_x, pos_y - (seg_length + radius) )
        
        self.circle = pm.Circle(self.ballBody, radius, (0,0))
        self.circle.elasticity = elasticity
#        
        self.rotation_center_joint = pm.PinJoint(self.body, self.rotation_center_body, (0,0), (0,0)) # 3
        self.rotation_center_joint2 = pm.PinJoint(self.ballBody, self.body, (0,0), (0,-seg_length))    

        space.add(self.s1, self.circle, self.ballBody, self.body, self.rotation_center_joint, self.rotation_center_joint2)