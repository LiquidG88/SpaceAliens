#Creating the ship.
import pygame
from pygame.sprite import Sprite 

class Ship(Sprite):
    def __init__(self, sa_settings, screen):
        #Initilize the ship and set its starting position.
        super(Ship, self).__init__()
        self.screen = screen
        self.sa_settings = sa_settings
        
        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #Start each new ship at the bottom center of screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #Adding float capabilities.
        self.center = float(self.rect.centerx)
        
        #Movement flag.
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        #Move ship based on movemnet flag.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.sa_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.sa_settings.ship_speed_factor
        
        #Update rect object from self.center.
        self.rect.centerx = self.center
        
    def center_ship(self):
        #Center the ship on screen.
        self.center = self.screen_rect.centerx
        
        
    def blitme(self):
        #Draw ship at current location.
        self.screen.blit(self.image, self.rect)