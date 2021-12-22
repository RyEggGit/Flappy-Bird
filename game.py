# Import and initialize the pygame library and radnom library
import pygame
from random import randint, seed
from random import random

from pygame.constants import K_UP
pygame.init()


#seed for random number generator
seed(4)

# Set up the drawing window
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Player Variables
playerX = 200
playerY = 100
playerW = 50
playerH = 40

velocity_multiplyer = 0.5
playerVel = 0
gravity = 0.0002

#draws player
bird1 = pygame.image.load(r'C:\Users\RyEgg\OneDrive\Desktop\Python Project\Flappy-Bird\images\bird_1.png')
bird2 = pygame.image.load(r'C:\Users\RyEgg\OneDrive\Desktop\Python Project\Flappy-Bird\images\bird_2.png')
bird3 = pygame.image.load(r'C:\Users\RyEgg\OneDrive\Desktop\Python Project\Flappy-Bird\images\bird_3.png')

bird_sprite = [bird1, bird2, bird3]
bird_index = 0
bird_index_delay = 0

# Home Screen Images
title = pygame.image.load(r'C:\Users\RyEgg\OneDrive\Desktop\Python Project\Flappy-Bird\images\title.png')
play_norm = pygame.image.load(r'C:\Users\RyEgg\OneDrive\Desktop\Python Project\Flappy-Bird\images\play.png')
play_hover = pygame.image.load(r'C:\Users\RyEgg\OneDrive\Desktop\Python Project\Flappy-Bird\images\play_hover.png')

hover = False

play_width = 150
play_height = 100
play_rect = pygame.Rect(SCREEN_WIDTH // 2 - play_width / 2 , SCREEN_HEIGHT//2 - play_height /2 + 50, play_width, play_height)


# Colors
color_player = (138,43,226)
color_red = (255, 0,0)
color_white = (255, 255, 255)
color_green = (0, 255, 0)
color_blue = (0, 0, 128)
color_black = (0, 0, 0)


pillar_speed = 0.1

#pillar class
class pillar ():
    
    def __init__(self,w = 40, h = 100, offset = SCREEN_HEIGHT - SCREEN_HEIGHT/2, x = SCREEN_WIDTH):
        self.height_top = h
        self.height_bot = SCREEN_HEIGHT - h + offset
        self.width = w
        self.x = x

    def drawpillars(self):
        pygame.draw.rect(screen, color_red , pygame.Rect(self.x, 0, self.width, self.height_top))
        pygame.draw.rect(screen, color_red , pygame.Rect(self.x, self.height_bot, self.width, self.height_top))
        return self.check_out_of_screen()

    def check_out_of_screen(self):
        if(self.x + self.width < 0 ):
            self.x = SCREEN_WIDTH + self.width
            return False
        else:
            self.x -= pillar_speed
            return True
    def checkcollsion(self, playerY, playerX, playerW, score):
        if(playerX < self.x + self.width and playerX + playerW > self.x):
            if(playerY < self.height_top or playerY > self.height_bot):
                return True
        else:
            return False


# Create the pillar array
"""         w    h   o         x        """
p0 = pillar(40, 200, 100, SCREEN_WIDTH + 40)
p1 = pillar(40, 250, 100, SCREEN_WIDTH + 40)
p2 = pillar(40, 200, 150, SCREEN_WIDTH + 40)
p3 = pillar(40, 200, 100, SCREEN_WIDTH + 40)
p4 = pillar(40, 200, 100, SCREEN_WIDTH + 40)
p5 = pillar(40, 150, 75, SCREEN_WIDTH + 40)
p6 = pillar(40, 200, 100, SCREEN_WIDTH + 40)
p7 = pillar(40, 300, 150, SCREEN_WIDTH + 40)


a_pillar = [p0,p1,p2,p3,p4,p5,p6,p7]
a_draw = [True,False, False, False, False,False, False, False]
pillar_index = 0

# Score 
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(str(score), True, color_black, color_white)
textRect = text.get_rect()  
textRect.center = (SCREEN_WIDTH -15, 15)

#Screen Variables
home_screen = True
game_screen = False
running = True



while running:
    # Fill the background with white
    screen.fill((255, 255, 255))

    # HomeScreen Code
    if(home_screen == True):
        playerY = 100
        playerVel = 0

        a_draw[pillar_index] = False
        pillar_index = randint(0, len(a_pillar) - 1)
        a_draw[pillar_index] = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                if (play_rect.collidepoint(mouse_position)):
                    hover = True
                else:
                    hover = False
                
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if (play_rect.collidepoint(mouse_position)):
                    home_screen = False
                    game_screen = True
                    print(home_screen)
                    break
                    #hover = False
                                    
        screen.blit(title, (SCREEN_WIDTH // 2 - 150 , SCREEN_HEIGHT//2 - 200))    
        #pygame.draw.rect(screen, color_green, play_rect)
        if(hover == True):
            screen.blit(play_hover, (SCREEN_WIDTH // 2 - play_width / 2 , SCREEN_HEIGHT//2 - play_height /2 + 50))
        else:
            screen.blit(play_norm, (SCREEN_WIDTH // 2 - play_width / 2 , SCREEN_HEIGHT//2 - play_height /2 + 50))
        
    # Game loop Code   
    else:
        # User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    playerVel -= velocity_multiplyer
        #moves player
        playerY +=  playerVel
        playerVel += gravity

        #upper and lower bound checks
        if(playerY + playerH > SCREEN_HEIGHT):
            #playerVel = 0
            #playerY = SCREEN_HEIGHT - playerH
            home_screen = True
            game_screen = False
        elif(playerY < 0):
            #playerVel = 0
            #playerY = 0
            home_screen = True
            game_screen = False
        else:
            playerVel += gravity
        #print("Y: " +str(playerY))
        #print("Vel: " +str(playerVel))

        
            
        # draw pillars
        if(a_draw[pillar_index] == True): 
            a_draw[pillar_index] = a_pillar[pillar_index].drawpillars()
            if(a_pillar[pillar_index].checkcollsion(playerY, playerX, playerW, score) == True):
                home_screen = True
                game_screen = False  
        else:
            pillar_speed += 0.005
            score += 1
            a_draw[pillar_index] = False
            pillar_index = randint(0, len(a_pillar) - 1)
            a_draw[pillar_index] = True
            print("Drawing: p" + str(pillar_index))
        
        #draw score
        text = font.render(str(score), True, color_green, color_white)
        screen.blit(text, textRect)

        # Draw player
        #pygame.draw.rect(screen, color_red, pygame.Rect(playerX+10, playerY + 12, playerW, playerH)) 
        screen.blit(bird_sprite[bird_index], (playerX, playerY))   
        if( bird_index_delay == 120):
            bird_index_delay = 0
            if(bird_index == 2):
                bird_index = -1
            bird_index +=1
        bird_index_delay += 1

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()