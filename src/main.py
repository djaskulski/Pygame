import pygame
import random
import math
from pygame import mixer

# init function
pygame.init()

# game window, and background image
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.jpg')

# background music
mixer.music.load('background_music.ogg')
mixer.music.play(-1)

# title, icon
pygame.display.set_caption('Work Invaders')
icon = pygame.image.load('helmet.png')
pygame.display.set_icon(icon)

# player - initial state
player_img = pygame.image.load('nerd.png')
player_X = 370
player_Y = 480
player_X_change = 0

# value - initial state
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_X = 10
text_Y = 10

# game over font
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Enemies - random spawn
enemy_img = []
enemy_X = []
enemy_Y = []
enemy_X_change = []
enemy_Y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('soldier.png'))
    enemy_X.append(random.randint(0, 735))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_change.append(1)
    enemy_Y_change.append(40)

# bullet - ready state
bullet_img = pygame.image.load('tomato.png')
bullet_X = 0
bullet_Y = 480
bullet_X_change = 0
bullet_Y_change = 3
bullet_state = 'ready'


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt(((enemy_X - bullet_X) ** 2) + ((enemy_Y - bullet_Y) ** 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB
    screen.fill((0, 128, 128))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_X_change = -1
            if event.key == pygame.K_RIGHT:
                player_X_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # current player's location
                    bullet_X = player_X
                    fire_bullet(player_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_X_change = 0

    # window boundaries
    # player
    player_X += player_X_change

    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    # enemies
    for i in range(num_of_enemies):

        # end game
        if enemy_Y[i] > 440:
            for j in range(num_of_enemies):
                enemy_Y[j] = 2000
            game_over_text()
            break

        enemy_X[i] += enemy_X_change[i]
        if enemy_X[i] <= 0:
            enemy_X_change[i] = 1
            enemy_Y[i] += enemy_Y_change[i]
        elif enemy_X[i] >= 736:
            enemy_X_change[i] = -1
            enemy_Y[i] += enemy_Y_change[i]

        # collision
        collision = is_collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_Y = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemy_X[i] = random.randint(0, 735)
            enemy_Y[i] = random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change

    player(player_X, player_Y)
    show_score(text_X, text_Y)
    pygame.display.update()
