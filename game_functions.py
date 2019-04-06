#Function for events.
import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_events(sa_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    #Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, sa_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(sa_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(sa_settings, screen, stats, sb, play_button, ship, aliens, bullets,
                       mouse_x, mouse_y):
    #Start a new game when the player clickes the button.
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        #Start a new game when the player clickes the button.
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            #Hide mouse cursor.
            pygame.mouse.set_visible(False)
            
            #Reset game settings.
            sa_settings.initialize_dynamic_settings()
            
            #Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True
            
            #Reset scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            
            #Empty the list f aliens and bullets.
            aliens.empty()
            bullets.empty()
            
            #Createa new fleet and center the ship.
            create_fleet(sa_settings, screen, ship, aliens)
            ship.center_ship()

def check_keydown_events(event, sa_settings, screen, ship, bullets):
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(sa_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(sa_settings, screen, ship, bullets):
    if len(bullets) < sa_settings.bullets_allowd:
            #Creat new bullet and add it to bullet group.
            new_bullet = Bullet(sa_settings, screen, ship)
            bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False

def update_screen(sa_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #Redraw the screen during each pass through the loop.
        screen.fill(sa_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        
        #Draw scoreboard.
        sb.show_score()
        
        #Draw play button if game is inactive.
        if not stats.game_active:
            play_button.draw_button()
        
        #Redraw all bullets.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        
        #Make the most recently drawn screen visible.
        pygame.display.flip()

def update_bullets(sa_settings, screen, stats, sb, ship, aliens, bullets):
    #Update position of bullets.
    bullets.update()
    
    #Get rid of bullets that have gone off screen.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        
    check_bullet_alien_collisions(sa_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(sa_settings, screen, stats, sb, ship, aliens, bullets):
    #Check for bullets that hit aliens.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += sa_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #Destroy existin bullets then make a new alien fleet and speed up game.
        bullets.empty()
        sa_settings.increase_speed()
        create_fleet(sa_settings, screen, ship, aliens)
        
        #Start a new level when the fleet is destroyed.
        stats.level += 1
        sb.prep_level()
            
def create_fleet(sa_settings, screen, ship, aliens):
    #Create a full fleet of aliens.
    alien = Alien(sa_settings, screen)
    number_aliens_x = get_number_aliens_x(sa_settings, alien.rect.width)
    number_rows = get_number_rows(sa_settings, ship.rect.height, alien.rect.height)
    
    #Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(sa_settings, screen, aliens, alien_number, row_number)
    
def get_number_rows(sa_settings, ship_height, alien_height):
    #Determine the number of aliens that fit on the screen.
    avalible_space_y = (sa_settings.screen_height -
                        (3 * alien_height) - ship_height)
    number_rows = int(avalible_space_y / (2 * alien_height))
    return number_rows
        
def get_number_aliens_x(sa_settings, alien_width):
    #Determine the number of aliens that fit in a row.
    avalible_space_x = sa_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avalible_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(sa_settings, screen, aliens, alien_number, row_number):
    #Create alien and place it in a row
    alien = Alien(sa_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def update_aliens(sa_settings, screen, stats, sb, ship, aliens, bullets):
    #Update the positions of all aliesn in the fleet.
    check_fleet_edges(sa_settings, aliens)
    aliens.update()
    
    #Look for alien/ship contact.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(sa_settings, screen, stats, sb, ship, aliens, bullets)
        
    #Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(sa_settings, screen, stats, sb, ship, aliens, bullets)
    
def check_fleet_edges(sa_settings, aliens):
    #Respond if aliens hit an edge.
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(sa_settings, aliens)
            break
        
def change_fleet_direction(sa_settings, aliens):
    #Drop the entire fleet.
    for alien in aliens.sprites():
        alien.rect.y += sa_settings.fleet_drop_speed
    sa_settings.fleet_direction *= -1
    
def ship_hit(sa_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        #Respond to ship getting hit by alien.
        stats.ships_left -= 1
        
        #Update scoreboard
        sb.prep_ships()
    
        #Empty the list of bullets.
        aliens.empty()
        bullets.empty()
    
        #Create a new fleet and canter the ship.
        create_fleet(sa_settings, screen, ship, aliens)
        ship.center_ship()
    
        #Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(sa_settings, screen, stats, sb, ship, aliens, bullets):
    #Check if aliens hit the bottom of the screen.
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this the same as if the ship got hit.
            ship_hit(sa_settings, screen, stats, sb, ship, aliens, bullets)
            break
        
def check_high_score(stats, sb):
    #Check if there is a new high score.
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
       
