import pygame
from pygame.sprite import Sprite

#A class to manage bullets fired from the ship.
class Bullet(Sprite):
    def __init__(self, sa_settings, screen, ship):
        #Create a bullet object at the ship's current position.
        super(Bullet, self).__init__()
        self.screen = screen
        
        #creat bullet at (0, 0) then set correct position.
        self.rect = pygame.Rect(0, 0, sa_settings.bullet_width, sa_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #Store bullets value as a float.
        self.y = float(self.rect.y)
        
        self.color = sa_settings.bullet_color
        self.speed_factor = sa_settings.bullet_speed_factor
    
    def update(self):
        #Move the bullets up the screen.
        #Update the position of the bullet.
        self.y -= self.speed_factor
        #Update the rect position.
        self.rect.y = self.y
    
    def draw_bullet(self):
        #Draw the bullet to the screen.
        pygame.draw.rect(self.screen, self.color, self.rect)
        