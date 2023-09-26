import pygame
import random
import math
from pygame import mixer

# initiating pygame
pygame.init()

# creating screen - width, height
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('space_bg.png')
# background sound
#mixer.music.load()
# play on loop
#mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# player spaceship
playerImg = pygame.image.load('ufo64.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien_normal.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# missile
missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 10
# state:ready - can't see the bullet on screen
# state:fire - bullet currently moving
missile_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(text,(200,250))


def player(x, y):
    # "drawing" image onto screen - image, coords
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit((enemyImg[i]), (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - missileX, 2)) + (math.pow(enemyY - missileY, 2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score_display = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(score_display, (x, y))

# game loop
running = True

while running:

    # rgb values 0-255
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (-300, 0))

    # check if close button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if keys pressed
        if event.type == pygame.KEYDOWN:
            # print("a key stroke is pressed")

            if event.key == pygame.K_LEFT:
                # print("left arrow pressed")
                playerX_change = -5
                # print(playerX_change)

            if event.key == pygame.K_RIGHT:
                # print("right arrow pressed")
                playerX_change = 5
                # print(playerX_change)

            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missile_sound = mixer.Sound('laser.wav')
                    missile_sound.play()
                    # fires missile only when state is ready - fixes glitching missile
                    missileX = playerX
                    # original player X coord stored so missile doesn't move with player
                    fire_missile(missileX, missileY)

        # check if keys released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("key released")
                playerX_change = 0
                # print(playerX_change)

    # player coord calculation
    playerX += playerX_change
    # boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # upon hitting left side, moves right
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        # upon hitting right side, moves left
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision calculation for every enemy
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            missileY = 480
            missile_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    # missile movement
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    # to draw player after screen so it appears on top of background
    player(playerX, playerY)
    # update score
    show_score(textX, textY)
    # updates screen
    pygame.display.update()
