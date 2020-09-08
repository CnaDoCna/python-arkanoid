import pygame
import random
import math

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 250)

FPS = 25 #można zmieniać
screen_size = [500, 500] #można zmieniac
block_size = [50, 10] #można zmieniać
block_rows = 6 #mozna zmieniac
plate_size = [70, 5] #można zmieniać
ball_size = 10 #można zmieniać
speed = 10 #można zmieniać

pygame.init()
gameDisplay = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.display.set_caption('Game - Snake')
font1 = pygame.font.SysFont('Arial', 20)
font2 = pygame.font.SysFont('Arial', 40)
font3 = pygame.font.SysFont('Arialbold', 30)
background_image = pygame.image.load("space.png").convert()
background_image = pygame.transform.scale(background_image, (screen_size[0], screen_size[1]))
clock = pygame.time.Clock()



def positionBlocks():
    blocks_positions = []
    n = int(math.floor(screen_size[0] / (block_size[0]))) #liczba klockow mieszcząca sie w wierszu
    for y in range(5, block_rows*block_size[1], block_size[1]):
        for x in range(5, n*block_size[0], block_size[0]):
            blocks_positions.append([x,y])
    return blocks_positions


def scoresDisplay(pkt):
    score_text = font1.render("Score: " + str(pkt), True, WHITE)
    gameDisplay.blit(score_text,
        (screen_size[0]/2 - score_text.get_width()/2, screen_size[1]/3))


def playAgainButton():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_text = font3.render("Play Again", False, BLUE)
    button_rect = button_text.get_rect(center = (screen_size[0]/2, screen_size[1]*(9/10)))

    if mouse[0] > button_rect[0] and mouse[0] < (button_rect[0]+button_text.get_width()) and mouse[1] > button_rect[1] and  mouse[1] < (button_rect[1]+button_text.get_height()):
        pygame.draw.rect(gameDisplay, WHITE, button_rect)
        if click[0]:
            Game()

    gameDisplay.blit(button_text, button_rect)


def Game():
    pkt = 0
    gameOver = False
    odbita = True
    pressed_left = False
    pressed_right = False

    ball_movement = [random.choice([-speed, speed]), -speed]
    ball_position = [random.randint(10, screen_size[0]-10), random.randint(block_size[1]*block_rows, screen_size[1]*(9/10)-10)]
    plate_position = [screen_size[0]/2 - plate_size[0]/2, screen_size[1]*(9/10)]
    blocks_positions = positionBlocks()




    while True:
        gameDisplay.blit(background_image, (0,0))
        scoresDisplay(pkt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            plate_position[0] -= speed
        if keys[pygame.K_RIGHT]:
            plate_position[0] += speed
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        pygame.event.pump()


        if not gameOver:
            ball_position[0] += ball_movement[0]
            ball_position[1] += ball_movement[1]

            ball = pygame.draw.rect(gameDisplay, RED, (ball_position[0], ball_position[1], ball_size, ball_size))
            plate = pygame.draw.line(gameDisplay, WHITE, [plate_position[0], plate_position[1]], [plate_position[0]+plate_size[0], plate_position[1]], plate_size[1])
            left_wall = pygame.draw.line(gameDisplay, WHITE, [0,screen_size[1]], [0,0], 5)
            upper_wall = pygame.draw.line(gameDisplay, WHITE, [0,0], [screen_size[0],0], 5)
            right_wall = pygame.draw.line(gameDisplay, WHITE, [screen_size[0]-2,0], [screen_size[0]-2,screen_size[1]-2], 5)

            for position in blocks_positions:
                block = pygame.draw.rect(gameDisplay, WHITE, (position[0], position[1], block_size[0], block_size[1]), 1)
                if ball.colliderect(block):
                    if odbita:
                        ball_movement[1] *= -1
                        blocks_positions.remove(position)
                        pkt +=542
                        odbita = False
                    else: ball_movement[0] *= -1


            if ball.colliderect(plate) or ball.colliderect(upper_wall):
                ball_movement[1] *= -1
                odbita = True
            if ball.colliderect(left_wall) or ball.colliderect(right_wall):
                ball_movement[0] *= -1
                odbita = True
            if ball_position[1] > screen_size[1]:
                gameOver = True


            pygame.display.update()
            clock.tick(FPS)

        else:
            gameDisplay.fill(RED)
            scoresDisplay(pkt)
            playAgainButton()

            for position in blocks_positions:
                block = pygame.draw.rect(gameDisplay, WHITE, (position[0], position[1], block_size[0], block_size[1]))

            gameOver_text = font2.render("Game Over", True, WHITE)
            gameDisplay.blit(gameOver_text,
                (screen_size[0]/2 - gameOver_text.get_width()/2, screen_size[1]/2))

            pygame.display.update()
            clock.tick(FPS)

Game()
