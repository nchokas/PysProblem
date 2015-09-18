class Player(object):
    def __init__(self,name,number,key_cannon_left,key_cannon_right,key_shoot, barrel_shoot, build_up, build_down, build_confirm, build_cancel,controller,volume):
        self.name = name
        self.number = number
        self.key_cannon_left = key_cannon_left
        self.key_cannon_right = key_cannon_right
        self.key_cannon_shoot = key_shoot
        self.key_barrel_shoot = barrel_shoot
        self.key_build_up = build_up
        self.key_build_down = build_down
        self.key_build_confirm = build_confirm
        self.key_build_cancel = build_cancel
        self.controller = controller
        self.volume = volume
        