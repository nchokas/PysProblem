import pymunk as pm

class Lineswing(object):
    
    def __init__(self, bod_x, bod_y, space):
        
        linelength = 50 #can make this a parameter 
        self.rotation_center_body = pm.Body(pm.inf, pm.inf) # rigid center of rotation
        self.rotation_center_body.position = (bod_x,bod_y)
            
        self.body = pm.Body(60, 5000) # this will be the body for the line
        self.body.position = (bod_x,bod_y)    
            
        self.l1 = pm.Segment(self.body, (0, 0), (0.0, -linelength), 5.0)
        
        #create the ball
        mass = 10
        radius = 20 
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        self.ballBody = pm.Body(mass, inertia)
        self.ballBody.position = (bod_x, bod_y - (linelength + radius) )
        
        self.circle = pm.Circle(self.ballBody, radius, (0,0))
        self.circle.elasticity = 1
   
        #connect the line to the center of rotation and then the ball to the line
        self.rotation_center_joint = pm.PinJoint(self.body, self.rotation_center_body, (0,0), (0,0))
        self.rotation_center_joint2 = pm.PinJoint(self.body, self.ballBody, (0,-linelength), (0,0))    


        space.add(self.l1, self.circle, self.ballBody, self.body, self.rotation_center_joint, self.rotation_center_joint2)
     
            