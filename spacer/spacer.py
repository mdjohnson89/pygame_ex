import pygame, sys, random
from pygame import mixer

#Part of the coding logic was provided by Matthew Johnson

#Spaceship's class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.damage = 0
        self.kills = 0
    
    def update (self, movement):
        self.movement(movement)

        #Limit the ship to the screen's border 
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
    #Changes the player's avatar, used for animations
    def new_image(self, new_image):
        self.image = pygame.transform.scale(new_image, (75, 75))

    #Gets the positions of the player
    def get_pos(self):
        return self.rect.center

    #Controls the player's movements
    def movement(self, movement):
        #Code provided by M.J.
        key = pygame.key.get_pressed()
        dist = movement # distance moved in 1 frame
        if key[pygame.K_DOWN] or key[pygame.K_s]: # down key and s
            self.rect.y += dist # move down
        elif key[pygame.K_UP] or key[pygame.K_w]: # up key and w
            self.rect.y -= dist # move up
        if key[pygame.K_RIGHT] or key[pygame.K_d]: # right key and d
            self.rect.x += dist # move right
        elif key[pygame.K_LEFT] or key[pygame.K_a]: # left key and a
            self.rect.x -= dist # move left

#Laser's class
class Laser(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Assets/laserBullet.png'), (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = ship.get_pos()
    
    def update(self, speed):
        self.remove_extra()
        self.rect.y -= speed

    def remove_extra(self):
        #Removes the extra lasers that are off-screen so that they won't bloat the program
        #-30 so that it looks like the laser is going off screen before killing
        if self.rect.y < -30:
            self.kill()

#Enemy's class
class Enemy(pygame.sprite.Sprite):
    '''Enemy sprite -- essentially just moves down the screen. '''
    def __init__(self, picture_path, pos_x):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, 0]

    def update(self, x_pos, x_speed, y_speed): #x = 5, y = 4
        self.back_to_top()

        self.rect.y += y_speed
        if self.rect.x < x_pos:
            self.rect.x += x_speed
        if self.rect.x > x_pos:
            self.rect.x -= x_speed

    def back_to_top(self):
        #Teleport the enemies that went past the player back to the top of the screen
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(0, SCREEN_WIDTH)

#Function to check for laser-enemy collitions
def check_laser(laser, enemy, player):
    ''' Checks for laser / enemy collisions '''
    for l in laser:
        for e in enemy:
            if pygame.sprite.collide_rect(e, l):
                pygame.mixer.Sound('Assets/explode.mp3').play()
                e.kill()
                l.kill()

                #Add +1 kill to player's stats
                for p in player:
                    p.kills += 1

#Function to check for player-enemy collitions
def check_enemy(player, enemy):
    for p in player:
        for e in enemy:
            if pygame.sprite.collide_rect(e, p):
                pygame.mixer.Sound('Assets/hit.wav').play()
                e.kill()
                p.damage += 1
                if p.damage >= 3:
                    pygame.event.post(pygame.event.Event(DEAD))

#Function to get the player's health from player obj
def get_health(player):
    for p in player:
        return 3 - p.damage

#Function to get the x value of the obj
def get_x_pos(sprite_group):
    for i in sprite_group:
        return i.get_pos()[0]
    
#Function to get the # of kills from the player obj
def get_kills(player):
    for p in player:
        return p.kills

#Game draw and update function
def draw_n_update(spaceship_group, screen, enemy_group, laser_group, heart, heart_rect, level):
    #Get the x position of the player's ship
    ship_x_pos = get_x_pos(spaceship_group)

    # Updating the window (This could, in theory, be a function. )
    pygame.display.flip()
    screen.blit(game_background, (0,0))

    #Makes the different assets appear on screen
    spaceship_group.draw(screen)
    enemy_group.draw(screen)
    laser_group.draw(screen)

    spaceship_group.update(player_speed)
    laser_group.update(laser_speed)
    #Makes the asteroid goes towards the player
    enemy_group.update(ship_x_pos, enemy_x_speed, enemy_y_speed)

    #Draw heart
    screen.blit(heart, heart_rect)
    draw_text(f"x{get_health(spaceship_group)}", small_font, (255,255,255), screen, 110, 40)
    draw_text(f"Level:{level}", small_font, (255,255,255), screen, 1150, 40)

#Function that draw texts
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

#Function that gets the high score from a file
def open_file(file):
    high_score = open(file, "r")
    return int(high_score.read().replace("\n", ""))
    high_score.close()

#Function that writes the new high score into a file
def write_file(file, high_score):
    high_score_file = open(file, "w")
    high_score_file.write(str(high_score))
    high_score_file.close()

#Game setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Custom Events
DEAD = pygame.USEREVENT + 1

#Screen Setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Spacer')
start_background = pygame.image.load("Assets/start_bg.jpg")
game_background = pygame.image.load("Assets/game_bg.png")

#Bg_sound
mixer.music.load("Assets/bg_music.mp3")
mixer.music.play(-1)

#Global vars
click = False
walkCount = 0
ship_x_pos = 0
SPAWN_COUNT = 0
player_speed = 4
enemy_x_speed = 5
enemy_y_speed = 4
laser_speed = 5
#number of ships, increase for less enemies
N = 80
enemy_count = 0
level = 1
big_font = pygame.font.Font("Assets/zx_spectrum.ttf", 70)
small_font = pygame.font.Font("Assets/zx_spectrum.ttf", 45)
x_small_font = pygame.font.Font("Assets/zx_spectrum.ttf", 30)

#Menu Screen
def menu(click, message, top_button, bottom_button):
    pygame.mouse.set_visible(True)

    #High score value
    high_score = open_file("high_score.txt")

    #Rects for the two buttons
    start_button = pygame.Rect(SCREEN_WIDTH/2 - 185, SCREEN_HEIGHT/2 - 80, 370, 80)
    quit_button = pygame.Rect(SCREEN_WIDTH/2 - 185, SCREEN_HEIGHT/2 + 40, 370, 80)

    while True:
        screen.blit(start_background, (0,0))

        mx, my = pygame.mouse.get_pos()

        #Check for mouse over and mouse click on the start button, button changes color on mouse over
        if start_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (64, 128, 230), start_button, 0, 5)
            if click:
                pygame.mixer.Sound('Assets/button.mp3').play()
                #Starts the game
                main_game(walkCount, ship_x_pos, SPAWN_COUNT, N, enemy_count, level)
        else:
            pygame.draw.rect(screen, (46, 102, 191), start_button, 0, 5)

        #Check for mouse over and mouse click on the quit button, button changes color on mouse over
        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (240, 20, 20), quit_button, 0, 5)
            if click:
                pygame.mixer.Sound('Assets/button.mp3').play()
                quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, (196, 16, 16), quit_button, 0, 5)

        #Draws the # of kills if the menu is not the the starting menu with the game's name
        if message != "SPACER":
            if kills > high_score:
                draw_text(f"New High Score! {kills} Kills!", x_small_font, (255,255,255), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 110)
                write_file("high_score.txt", kills)
            else:
                draw_text(f"High Score: {high_score} Kills | {kills} Kills", x_small_font, (255,255,255), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 110)

        #Draws text on the menu screen
        draw_text(message, big_font, (255,255,255), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 170)
        draw_text(top_button, small_font, (255,255,255), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40)
        draw_text(bottom_button, small_font, (255,255,255), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80)

        click = False

        #Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

#Function for the main game, takes in some of the global var
def main_game(walkCount, ship_x_pos, SPAWN_COUNT, N, enemy_count, level):
    global kills
    pygame.mouse.set_visible(False)

    #Spaceship
    spaceship = Spaceship('Assets/ship/ship_straight.png')
    spaceship_group = pygame.sprite.Group()
    spaceship_group.add(spaceship)

    #Enemies
    enemy = Enemy('Assets/enemy.png', random.randrange(0, SCREEN_WIDTH))
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

    #Laser 
    laser_group = pygame.sprite.Group()

    #Heart
    heart = pygame.image.load("Assets/heart.png")
    heart_rect = heart.get_rect()
    heart_rect.center = (40, 40)
    
    #Ship animation assets
    shipLeft = [pygame.image.load("Assets/ship/ship_left1.png"), pygame.image.load("Assets/ship/ship_left2.png"), pygame.image.load("Assets/ship/ship_left3.png"), pygame.image.load("Assets/ship/ship_left4.png"), pygame.image.load("Assets/ship/ship_left5.png")]
    shipRight = [pygame.image.load("Assets/ship/ship_right1.png"), pygame.image.load("Assets/ship/ship_right2.png"), pygame.image.load("Assets/ship/ship_right3.png"), pygame.image.load("Assets/ship/ship_right4.png"), pygame.image.load("Assets/ship/ship_right5.png")]

    #Indicates direction of the ship
    left = False
    right = False

    while True:
        #No more spawns, player wins the game
        if N == 0:
            menu(click, "YOU WIN!", "Restart", "Quit")

        #Gets the amount of kills the player has and store it in a global var
        kills = get_kills(spaceship_group)

        #Deals with the spawning of enemies | SPAWN_COUNT deals with spawn rate | enemy_count deals with the # of enemies
        SPAWN_COUNT += 1
        if SPAWN_COUNT % N == 0:
            enemy_group.add(Enemy('Assets/enemy.png', random.randrange(0, SCREEN_WIDTH)))
            enemy_count += 1
        if enemy_count >= 20:
            SPAWN_COUNT = 0
            enemy_count = 0
            N -= 10
            level += 1

        #Handling input (EVENTS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == DEAD:
                menu(click, "GAME OVER", "Retry", "Quit")

            #Controls the firing of lasers and movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound('Assets/lazer.mp3').play()
                    laser_group.add(Laser(spaceship))

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = True
                    right = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    left = False
                    right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = False
                    walkCount = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = False
                    walkCount = 0

        # Drawing Collisions
        check_laser(laser_group, enemy_group, spaceship_group)
        check_enemy(spaceship_group, enemy_group)

        #Ship turning animations
        #walkCount + 1 must be less than 5 * n. 5 because there are 5 frames of the animation. The bigger n is, the longer the animation is.
        if walkCount + 1 <= 40:
            if left:
                for s in spaceship_group:
                    s.new_image(shipLeft[walkCount//8])
                    walkCount += 1
            elif right:
                for s in spaceship_group:
                    s.new_image(shipRight[walkCount//8])
                    walkCount += 1
            else:
                for s in spaceship_group:
                    s.new_image(pygame.image.load('Assets/ship/ship_straight.png'))

        #Draw and update the different sprites and rects
        draw_n_update(spaceship_group, screen, enemy_group, laser_group, heart, heart_rect, level)

        clock.tick(60)

#Starts the game
menu(click, "SPACER", "Start", "Quit")