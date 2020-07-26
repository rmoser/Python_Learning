import os
import sys
import pygame
from pygame.locals import *
import pygame.gfxdraw
import random
import time
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Control Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 5

CRASH = pygame.mixer.Sound(r'Materials\crash.wav')

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(r"Materials\AnimatedStreet.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


# Sprites
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"Materials\Enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), -70))
        self.point_scale = 1

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top >= SCREEN_HEIGHT:
            score(int(SPEED * self.point_scale))
            self.reset()

    def reset(self):
        self.__init__()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, shadow=False):
        super().__init__()
        self.width = 44
        self.height = 96
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - self.height // 2

        self.image = pygame.image.load(r"Materials\Player.png")
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(center=(self.x, self.y))

        self.shadow_scale = 0.9
        self.shadow = pygame.Surface((round(self.width * self.shadow_scale), round(self.height * self.shadow_scale)))
        self.shadow.fill(GRAY)
        self.shadow_rect = self.shadow.get_rect(center=(self.x, self.y))

        self.score = 0
        self.health = 3
        self.airborne = False
        self.airtime = 70
        self.airtimer = 0
        self.altitude = 0
        self.altitudes = []
        for t in range(self.airtime+1):
            self.altitudes.append(round(10 * math.sin(t / self.airtime * math.pi)))

    def left(self, n):
        self.x = max(self.x - n, 0)
        self.rect.centerx = self.x
        self.shadow_rect.centerx = self.x

    def right(self, n):
        self.x = min(self.x + n, SCREEN_WIDTH)
        self.rect.centerx = self.x
        self.shadow_rect.centerx = self.x

    def land(self):
        self.airtimer = 1
        self.altitude = 0
        self.move()

    def move(self):
        # Cannot move while airborne
        if self.airborne:
            # Jump car and shrink shadow
            self.airtimer -= 1
            self.altitude = self.altitudes[self.airtimer]
            self.rect.centerx = self.x + self.altitude
            self.rect.centery = self.y + self.altitude
            factor = (100 - self.altitude) / 100.
            self.shadow = pygame.transform.scale(self.shadow, (round(self.width * self.shadow_scale * factor), round(self.height * self.shadow_scale * factor)))
            self.shadow_rect = self.shadow.get_rect(center=(self.x, self.y))

            if self.airtimer == 0:
                self.airborne = False
            return
        else:
            self.rect.centerx = self.x

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and not self.airborne:
            if self.rect.left > 0:
                self.left(5)

        if pressed_keys[K_RIGHT] and not self.airborne:
            if self.rect.right < SCREEN_WIDTH:
                self.right(5)

        if pressed_keys[K_SPACE] and not self.airborne:
            self.airborne = True
            self.airtimer = self.airtime

    def draw(self, surface):
        surface.blit(self.shadow, self.shadow_rect)
        surface.blit(self.image, self.rect)
        # surface.blits((self.shadow, ), (self.image, self.rect))


def score(n):
    P1.score += n


# Init Sprites
P1 = Player()
E1 = Enemy()

# Group Sprites
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)


def update_display():
    pass


# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
# pygame.time.set_timer(INC_SPEED, 1000)


def exit_game():
    for entity in all_sprites:
        entity.kill()

    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over, (30, 250))

    time.sleep(0.5)
    print("Game over, man.")
    print(f"Score: {P1.score}")
    pygame.quit()
    sys.exit()


# Game loop
print("Shall we play a game?")
while True:
    # Event handler
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 1
            continue

        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                SPEED += 5
            elif event.key == K_DOWN:
                SPEED = max(SPEED - 5, 0)

        if event.type == QUIT:
            exit_game()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"SPEED: {SPEED}  ALT: {P1.altitude}  SCORE: {P1.score}  HEALTH: {P1.health}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in enemies:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    for entity in (P1,):
        DISPLAYSURF.blit(entity.shadow, entity.shadow_rect)
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between Player and Enemy
    for enemy in pygame.sprite.spritecollide(P1, enemies, False):
        if P1.altitude > 4:
            # Bonus points for jumping an enemy
            if enemy.point_scale == 1:
                enemy.point_scale = 2
        else:
            # Impact effect
            if enemy.rect.center[0] < P1.rect.center[0]:
                P1.x += 30
                P1.move()
            else:
                P1.x -= 30
                P1.move()

            pygame.display.update()
            CRASH.play()

            enemy.reset()

            time.sleep(0.5)

            pygame.display.update()
            P1.health -= 1
            P1.land()
            if P1.health == 0:
                exit_game()

    pygame.display.update()
    FramePerSec.tick(FPS)

