#A settings class to store all the settings for SpaceAliens.
class Settings():
    def __init__(self):
        #Initializes game's settings.
        self.screen_width = 1200
        self.screen_height = 600
        
        #Sets windows background color.
        self.bg_color = (230, 230, 230)
        
        #Sets ships speed.
        self.ship_speed_factor = 1
        self.ship_limit = 3
        
        #Bullet settings.
        self.bullet_speed_factor = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowd = 3
        
        #Alien settings
        self.alien_speed_factor = 0.45
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 repesents left.
        self.fleet_direction = 1
        
        #How quickly the game speeds up.
        self.speedup_scale = 1.2
        
        #Howquickly the the alien point values increase
        self.score_scale = 1.1
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        #Initialize settings that change through out the game.
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 2.5
        self.alien_speed_factor = 0.45
        
        #Fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        
        #Scoring
        self.alien_points = 50
        
    def increase_speed(self):
        #Increase speed setting.
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        
        #Increase point values.
        self.alien_points = int(self.alien_points * self.score_scale)