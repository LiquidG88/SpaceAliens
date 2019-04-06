import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
#A class to represent a single alien in the fleet.

    def __init__(self, sa_settings, screen):
        #Initilize the alien and set its starting position.
        super(Alien, self).__init__()
        self.screen = screen
        self.sa_settings = sa_settings
        
        #Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect() #???
        
        #Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store the alien's exact position.
        self.x = float(self.rect.x)
    
    def check_edges(self):
        #return true if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        #Move the alien to the right.
        self.x += (self.sa_settings.alien_speed_factor * self.sa_settings.fleet_direction)
        self.rect.x = self.x
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)