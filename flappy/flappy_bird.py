import pygame, sys, random

#Sprites/Classes
class Bird(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load('flappybird.png')
        self.rect = self.image.get_rect()
        self.rect.center = [200, 415]

    def falling(self):
        self.rect.y += 5

    def flying(self):
        self.rect.y -= 90

class Obstacle1(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load('obstacle2.png')
        self.rect = self.image.get_rect()
        self.rect.center = [500, random.randrange(0,150)]

    def update(self):
        self.rect.x -= 6
        

class Obstacle2(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.rect.center = [500, random.randrange(850,960)]

    def update(self):
        self.rect.x -= 6 

# General setup  
pygame.init()
clock = pygame.time.Clock()

#Custom events
GAME_OVER = pygame.USEREVENT
SCORE = pygame.USEREVENT +1

# Setting up the main window
screen_width = 500
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy Bird')
background = pygame.image.load('background.png')

#Bird
bird = Bird('flappybird.png')
bird_group = pygame.sprite.Group()
bird_group.add(bird)

#Obstacles
obstacle1 = Obstacle1('obstacle2.png')
obstacle1_group = pygame.sprite.Group()
obstacle1_group.add(obstacle1)
obstacle2 = Obstacle2('obstacle.png')
obstacle2_group = pygame.sprite.Group()
obstacle2_group.add(obstacle2)

#Collision
def collision(bird, obstacle1):
    for b in bird:
        for o in obstacle1:
            if pygame.sprite.collide_rect(b, o):
                b.kill()
                pygame.event.post(pygame.event.Event(GAME_OVER))
def collision2(bird, obstacle2):
    for b in bird:
        for o in obstacle2:
            if pygame.sprite.collide_rect(b, o):
                b.kill()
                pygame.event.post(pygame.event.Event(GAME_OVER))

def scoring():
    for b in bird_group:
        for o in obstacle2_group:
            if o.rect.x > b.rect.x:
                pygame.event.post(pygame.event.Event(SCORE))

obstacle_count = 0
N = 60
score = 0
font = pygame.font.SysFont(None, 24)
font2 = pygame.font.SysFont(None, 50)


#Loop

while True:
    #Makes obstacles reappear   
    obstacle_count += 1
    if obstacle_count % N == 0:
        obstacle1_group.add(Obstacle1('obstacle2.png'))
        obstacle2_group.add(Obstacle2(obstacle1))

    #Handling input(EVENTS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flying()
        
        if event.type == SCORE:
            score += 0.01666

        if event.type == GAME_OVER:
                background = pygame.image.load('background.png')
                screen.blit(background, (0,0))
                text2 = font2.render('Game Over', True, 'White')
                text3 = font2.render(f'Score: {round(score)}', True, 'White') 
                screen.blit(text2, (170, 400))
                screen.blit(text3, (190, 460))
                pygame.display.update()
                pygame.time.delay(6000)
                quit()
                sys.exit()
        
    #draws collisions 
    collision(bird_group, obstacle1_group)
    collision2(bird_group, obstacle2_group)
    scoring()
    
    text = font.render(f'Score: {round(score)}', True, 'White')


    # Updating the window 
    pygame.display.flip()
    screen.blit(background, (0,0))
    bird_group.draw(screen) 
    obstacle1_group.draw(screen)
    obstacle2_group.draw(screen)
    screen.blit(text, (20,20))
    bird.falling()
    obstacle1_group.update()
    obstacle2_group.update()
    
    clock.tick(60)
    