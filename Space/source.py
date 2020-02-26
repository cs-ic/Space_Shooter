import pygame
import math
import random
from pygame import mixer


# Intialiae the module
pygame.init()

# Create the Screen
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")

# icon of the game
programIcon = pygame.image.load("icon_2.png")
pygame.display.set_icon(programIcon)

# player image
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
num_of_enemies = 3
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)

# Enemy
BackImg = pygame.image.load("background.png")

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
fire = False

# Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score_val = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_val, (x, y))


def game_over():
    over_font = pygame.font.Font("freesansbold.ttf", 64)
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    )
    if distance < 36:
        return True


# running window
running = True

while running:

    # screen.fill(BackImg)
    screen.blit(BackImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                continue
            if event.key == pygame.K_DOWN:
                continue
            if event.key == pygame.K_SPACE and fire == False:
                bulletX = playerX + 16
                bulletY = playerY + 10
                fire = True

        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change
    if playerX >= 736:
        playerX = 0
    elif playerX <= 0:
        playerX = 736

    # for random moment
    # if random.randrange(1, 50, 3) == 18:
    #     enemyX_change *= -1

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 0
            bulletX = 0
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            print(score)

        bulletY -= 10
        if bulletY <= 0:
            fire = False

        if fire == True:
            bullet(bulletX, bulletY)

        enemy(enemyX[i], enemyY[i], i)

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
