class GameStats():
    #Tracks statistics for Space Alien.
    
    def __init__(self, sa_settings):
        #Initilize statistics.
        self.sa_settings = sa_settings
        self.reset_stats()
        
        #Start SpaceAlien in an inactive state.
        self.game_active = False
        
        #High score should never be reset.
        self.high_score = 0
        
    def reset_stats(self):
        #Initiliza statistics that can change during the game.
        self.ships_left = self.sa_settings.ship_limit
        self.score = 0
        self.level = 1