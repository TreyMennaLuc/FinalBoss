#Trey Menna
import pygame
from pygame.locals import *
import random
import time
import threading


pygame.font.init()  # initialize the font module


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

keys_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False, pygame.K_c: False}

platforms = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.jump_speed = -10  # vertical speed for jumping
        self.vertical_speed = 0  # vertical speed for falling/gravity
        self.num_jumps = 0  # number of consecutive jumps
        self.attack = False  # flag to indicate if the player is attacking
        self.health = 5
        self.health_size = 20  # size of each health square
        self.health_spacing = 5  # spacing between each health square
        self.immune_timer = 300  # timer for how long the player is immune after taking damage
        self.cannotBeDamaged = False

    
    def draw_health(self, surface):
        # draw a row of squares to represent the player's health
        health_rect = pygame.Rect(10, 10, self.health_size, self.health_size)
        for i in range(self.health):
            pygame.draw.rect(surface, GREEN, health_rect)
            health_rect.move_ip(self.health_size + self.health_spacing, 0)


    def swing_attack(self):
            # update the screen to see attack hitbox
            hitbox = pygame.Rect(self.rect.x + self.rect.width, self.rect.y - self.rect.height / 2, 150, 100)
            pygame.draw.rect(screen, BLUE, hitbox)
            pygame.display.update()
            
            if hitbox.colliderect(boss.rect):
                boss.health -= 10 
                keys_pressed[K_SPACE] = False           
            pygame.display.update()

    def damagePlayer(player):
        global boss, keys_pressed
        if player.cannotBeDamaged:
            return
        else:
            player.health -=1
            player.cannotBeDamagedTimer()
            player.cannotBeDamaged = True  # set the player to immune
    
    def canBeDamaged(self):
            self.cannotBeDamaged = False 

    def cannotBeDamagedTimer(self):
            t = threading.Timer(3.0, self.canBeDamaged)
            t.start()
    

    def update(self):
        global keys_pressed  # use global keyword to access global variable
        self.draw_health(screen)    # update the player's health display

        if keys_pressed[K_LEFT]:
            self.rect.x -= 5
        if keys_pressed[K_RIGHT]:
            self.rect.x += 5

         # handle jumping
        if keys_pressed[K_UP] and self.vertical_speed == 0:
            if self.num_jumps < 1:  # allow jump if less than 2 consecutive jumps
                self.vertical_speed = self.jump_speed
                self.num_jumps += 1
        
        # handle attacking
        if keys_pressed[K_SPACE]:
            self.swing_attack()
        
        #Handle shuriken
        if keys_pressed[K_c]:
            self.throw_shuriken()
            keys_pressed[K_c] = False
        
        # apply gravity
        self.vertical_speed += 0.4
        self.rect.y += self.vertical_speed

          # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
            self.vertical_speed = 0  # stop vertical speed if hitting top of screen
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vertical_speed = 0  # stop vertical speed if hitting bottom of screen
            self.num_jumps = 0  # reset consecutive jumps if landed on bottom of screen

        
       # Check for collision with platforms
        for platform in pygame.sprite.spritecollide(self, platforms, False):
            if self.rect.bottom > platform.rect.top and self.rect.bottom < platform.rect.bottom:
                self.rect.bottom = platform.rect.top
                self.vertical_speed = 0  # stop falling if hitting platform from above
                self.num_jumps = 0  # reset consecutive jumps if landed on a platform
    def throw_shuriken(self):
        shuriken = Shuriken(self.rect)
        shurikens.add(shuriken)
             
            
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
        self.health = 100
        self.last_firing_time = time.monotonic()
        self.firing_interval = 2 # seconds

    def fire_projectile(self):
        x = self.rect.x - 50  # adjust this value to control the horizontal position of the projectile
        y = self.rect.centery  # adjust this value to control the vertical position of the projectile
        projectile = Projectile(self.rect)
        projectiles.add(projectile)
    
    def randomTrigger(self):
        # Get the current time
        current_time = time.monotonic()

        # Check if enough time has elapsed since the last firing
        if current_time - self.last_firing_time >= self.firing_interval:
            # If enough time has elapsed, randomly decide whether to fire
            if random.random() < 0.5: # 50% chance of firing
                self.fire_projectile()
                # Update the last firing time
                self.last_firing_time = current_time

       

    def draw_health(self, surface):
        # draw a red bar to represent the boss's health
        health_rect = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 10)
        pygame.draw.rect(surface, RED, health_rect)
        health_rect.width = max(0, (self.health / 100) * health_rect.width)
        pygame.draw.rect(surface, GREEN, health_rect)

    
    def update(self):
        self.draw_health_bar(screen)
        self.check_shuriken_collision(shurikens)
        self.randomTrigger()
        

    def draw_health_bar(self, surface):
        # Draw health bar
        health_bar_width = 150
        health_bar_height = 10
        health_bar_border_width = 2
        health_bar_border_rect = pygame.Rect(self.rect.x, self.rect.y - health_bar_height - health_bar_border_width, health_bar_width + health_bar_border_width * 2, health_bar_height + health_bar_border_width * 2)
        pygame.draw.rect(surface, WHITE, health_bar_border_rect)
        health_bar_rect = pygame.Rect(self.rect.x + health_bar_border_width, self.rect.y - health_bar_height, health_bar_width * (self.health / 100), health_bar_height)
        pygame.draw.rect(surface, GREEN, health_bar_rect)

        
        #Code for red health bar
        #health_bar_rect = pygame.Rect(self.rect.x + health_bar_border_width, self.rect.y - health_bar_height, health_bar_width * (self.health / 100), health_bar_height)
        #pygame.draw.rect(surface, RED, health_bar_rect)

    def check_shuriken_collision(self, shurikens):
        for shuriken in shurikens:
            if self.rect.colliderect(shuriken.rect):
                self.health -= 3
                shuriken.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, boss_rect):
        super().__init__()
        self.image = pygame.Surface((50, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = boss_rect.x
        self.rect.y = boss_rect.y
        self.speed = 2  # adjust this value to control the speed of the projectile

    def update(self):
        self.rect.x -= self.speed

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Platform, self).__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Shuriken(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super(Shuriken, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x + player_rect.width
        self.rect.y = player_rect.y + player_rect.height / 2 - self.rect.height / 2
        self.speed = 10
    
    def update(self):
        self.rect.x += self.speed

def display_win_message():
    font = pygame.font.SysFont(None, 64)
    text = font.render("You Win!", True, GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
    screen.blit(text, text_rect)
    pygame.display.update()

def display_loss_message():
    font = pygame.font.SysFont(None, 64)
    text = font.render("You Lose", True, GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
    screen.blit(text, text_rect)
    pygame.display.update()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, boss_rect):
        super(Projectile, self).__init__()
        self.image = pygame.Surface((30, 200))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = boss_rect.x + 130
        self.rect.y = boss_rect.y #+ boss_rect.height / 2 - self.rect.height / 2
        self.speed = 1
    
    def update(self):
        self.rect.x -= self.speed


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boss Fight")

clock = pygame.time.Clock()

player = Player()
boss = Boss()
platform1 = Platform(350, 400)
platform2 = Platform(350, 220)
Platform3 = Platform(200, 300)
Platform4 = Platform(530, 160)
Platform5 = Platform(100, 180)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(Platform3)
platforms.add(Platform4)
platforms.add(Platform5)

projectiles = pygame.sprite.Group()
shurikens = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(boss)
all_sprites.add(platform1)
all_sprites.add(platform2)
all_sprites.add(Platform3)
all_sprites.add(Platform4)
all_sprites.add(Platform5)



game_over = False

while not game_over:
  # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                keys_pressed[K_LEFT] = True
            elif event.key == K_RIGHT:
                keys_pressed[K_RIGHT] = True
            elif event.key == K_UP:
                keys_pressed[K_UP] = True
            elif event.key == K_DOWN:
                keys_pressed[K_DOWN] = True
            elif event.key == K_SPACE:
                keys_pressed[K_SPACE] = True
            elif event.key == K_c:
                keys_pressed[K_c] = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                keys_pressed[K_LEFT] = False
            elif event.key == K_RIGHT:
                keys_pressed[K_RIGHT] = False
            elif event.key == K_UP:
                keys_pressed[K_UP] = False
            elif event.key == K_DOWN:
                keys_pressed[K_DOWN] = False
            elif event.key == K_SPACE:
                keys_pressed[K_SPACE] = False
            elif event.key == K_c:
                keys_pressed[K_c] = False 

    # Handle player input
    player.update()
    boss.check_shuriken_collision(shurikens)


    # Update game objects
    shurikens.update()
    all_sprites.update()
    platforms.update()
    projectiles.update()
    

 # check if player is attacking and swing attack
    if player.attack:
        player.swing_attack()

   
    # Draw game objects
    screen.fill(BLACK)
    all_sprites.draw(screen)
    boss.draw_health_bar(screen)
    shurikens.draw(screen)
    player.draw_health(screen)
    projectiles.draw(screen)


    # Update display
    pygame.display.flip()

    # Set game FPS
    clock.tick(60)

    # update projectiles
    for projectile in projectiles:
        projectile.update()
        if projectile.rect.right < 0:
            projectile.kill()  # remove projectile if it goes off the left edge of the screen
        elif projectile.rect.colliderect(player.rect):
            player.damagePlayer()  # damage the player if a projectile hits them
    
   # Check for player collision with boss
    if pygame.sprite.collide_rect(player, boss):
        boss.health -= 3
        player.damagePlayer()

   # Check if player has defeated boss
    if boss.health <= 0:
        display_win_message()
        start_time = pygame.time.get_ticks()
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            if elapsed_time >= 5000:
                game_over = True
                print("Thank you for playing!")
                break

    # Check if boss has defeated player
    if player.health <= 0:
        display_loss_message()
        start_time = pygame.time.get_ticks()
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            if elapsed_time >= 5000:
                game_over = True
                print("Thank you for playing!")
                break

pygame.quit()