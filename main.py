#First game using Pygame, using Python Crash Course book as a guide.
import pygame
import game_functions as gf
from settings import Settings
from game_stats import GameStats
from button import Button
from pygame.sprite import Group
from ship import Ship
from scoreboard import Scoreboard

def run_game():
    #Initialize game and create a screen object.
    pygame.init()
    
    sa_settings = Settings()
    
    screen = pygame.display.set_mode(
        (sa_settings.screen_width, sa_settings.screen_height))
    
    stats = GameStats(sa_settings)
    sb = Scoreboard(sa_settings, screen, stats)
    
    #Make Play button.
    play_button = Button(sa_settings, screen, "Play")
    
    #Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(sa_settings, screen)
    bullets = Group()
    aliens = Group()
    
    #Create the fleet of aliens.
    gf.create_fleet(sa_settings, screen, ship, aliens)
    
    #Start main game loop.
    while True:
        gf.check_events(sa_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(sa_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(sa_settings, screen, stats, sb, ship, aliens, bullets)
            
        gf.update_screen(sa_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
