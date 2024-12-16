# https://github.com/jayanam/connect4_python 
class Player: 

    def __init__(self, player_id, mode="multiplayer"):
        self.id = player_id
        self.mode = mode

    def get_id(self):
        return self.id 
    
    def get_color(self):
        if(self.id == 1):
            return (255, 255, 0)  #yellow
        else:
            return (255, 0, 0)  #red
        
    def is_ai(self):

        return self.mode == "solo" and self.id == 2
        
    