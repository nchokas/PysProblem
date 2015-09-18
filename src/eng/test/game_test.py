import sys
from game import Game
from player import Player
from pygame.locals import *
try:
    import psyco
    psyco.profile(0.0)
except ImportError:
    pass

def main():
    #movements
    #gun controls: left, right, shoot, shoot barrel cannon
    #buy controls: up, down
    #confirm build, cancel build
    
    player1 = Player("Rob",0,K_a,K_d,K_w, K_SPACE,
                      K_r, K_f,
                      K_RETURN, K_RSHIFT )
    
    player2 = Player("Matt",1,K_LEFT,K_RIGHT,K_UP, K_KP0, 
                     K_KP_MINUS, K_KP_PLUS,
                     K_KP_ENTER, K_KP_PERIOD)

    players = [player1]# ,player2]
    
    game = Game(players,False, None, None)
    game.start()
    
if __name__ == '__main__':
    sys.exit(main())