import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

def scale_image(img, factor):
    size = round(img.get_width() * factor), (img.get_height() * factor)
    return pygame.transform.scale(img, size)
# Load background image
BACKGROUND = pygame.image.load("AnimatedRoad.jpg")

# Screen dimensions
SCREEN_WIDTH = BACKGROUND.get_width()
SCREEN_HEIGHT = BACKGROUND.get_height()

FPS = 60
FramePerSec = pygame.time.Clock()

score = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("AnimatedRoad.jpg")

# Load background music
pygame.mixer.music.load('country.mp3')
pygame.mixer.music.play(-1)  # Play music on loop

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT//1.5))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# User-defined events
INC_SPEED = pygame.USEREVENT + 1
SPAWN_ENEMY = pygame.USEREVENT
SPAWN_LUCKY = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_LUCKY, 3000)
pygame.time.set_timer(INC_SPEED, 2000)  # Increase speed event by time
pygame.time.set_timer(SPAWN_ENEMY, 5000)  # Spawn enemy event every 5 seconds


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load("Player.png")
        self.image = scale_image(image, 1/10)
        self.rect = self.image.get_rect()
        self.rect.center = (160, SCREEN_HEIGHT//2)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT//1.5:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load("Enemy.png")
        self.image = scale_image(image, 1/10)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 5)
        global score
        if self.rect.top > SCREEN_HEIGHT//1.5:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#  Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('coin.png')
        self.image = scale_image(image, 1/20)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT//1.5:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Lucky_coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('lucky_coin.png')
        self.image = scale_image(image, 1/20)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top > SCREEN_HEIGHT//1.5:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)



# Create player and enemy sprites groups
player = Player()
coin = Coin()
lucky_coin = Lucky_coin()
enemy = Enemy()

enemies = pygame.sprite.Group()
enemies.add(enemy)
coins = pygame.sprite.Group()
coins.add(coin)

lucky_coins = pygame.sprite.Group()
lucky_coins.add(lucky_coin)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin, lucky_coin)


# Game variables
speed = 5
coin_score = 0

SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 5000)


def spawn_coin():
    new_coin = Coin()
    coins.add(new_coin)
    all_sprites.add(new_coin)
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SPAWN_COIN:
            spawn_coin()
        elif event.type == INC_SPEED:
            speed += 0.5  # Increase speed
        elif event.type == SPAWN_ENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
        elif event.type == SPAWN_LUCKY:
            new = Lucky_coin()
            lucky_coins.add(new)
            all_sprites.add(new)

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(score), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    coin_scorre = font_small.render(f'Coin score: {str(coin_score)}', True, BLACK)
    DISPLAYSURF.blit(coin_scorre, (SCREEN_WIDTH//2.5, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    

    if pygame.sprite.spritecollide(player, coins, True):
        pygame.mixer.Sound('catch.mp3').play()
        coin_score += 5
    if pygame.sprite.spritecollide(player, lucky_coins, True):
        pygame.mixer.Sound('catch.mp3').play()
        coin_score += 10




    if pygame.sprite.spritecollideany(player, enemies):
        # Collision with enemy
        pygame.mixer.music.pause()
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (SCREEN_WIDTH//6, SCREEN_HEIGHT//4))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)