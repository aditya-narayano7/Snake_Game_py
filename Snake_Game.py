import pygame
import random
import os

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

# Display setting
screen_width = 800
screen_height = 400
white = (255, 255, 255)
red = (255, 0 ,0)
green = (0, 255 ,0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

window_size = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# background image

bgimg1 = pygame.image.load('welcome.jpg')
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()
bgimg2 = pygame.image.load('play.jpg')
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
bgimg3 = pygame.image.load('gameover.jpg')
bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()
pygame.display.update()

clock = pygame.time.Clock()
fps = 30

font1 = pygame.font.SysFont(None, 53)
font2 = pygame.font.SysFont('arial', 40)
font3 = pygame.font.SysFont('freesansbold', 40)

def text_display(text, color, x, y, font):
    screen_text = font.render(text, True, color)
    window_size.blit(screen_text, [x, y])

def plot_snake(window_size, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(window_size, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    pygame.mixer.music.load('snake_sound.mp3')
    pygame.mixer.music.play()
    while not exit_game:

        window_size.fill((white))
        text_display('Welcome to the Snake Game',blue, 130, 150, font1)
        text_display("Hit 'Space bar' or 'Enter' to PLAY!", green, 125, 250, font2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game = True
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    Game()

        pygame.display.update()
        clock.tick(30)

def Game():

    # Game variable
    exit_game = False
    game_over = False
    snake_x = 15
    snake_y = 40
    snake_size = 25
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    food_x = random.randint(20,700)
    food_y = random.randint(20,300)
    food_size = 7
    score = 0
    sensivity = 13
    snk_list = []
    snk_length = 1

    if(not os.path.exists("high_score.txt")):
        with open("high_score.txt","w") as f:
            f.write("0")
    with open("high_score.txt","r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            window_size.fill(white)
            with open("high_score.txt","w") as f:
                f.write(str(high_score))
                text_display("Game Over Hit Enter or Space to continue and Escpae ",black, 20, 150, font3)
                text_display("to exit continue and Escpae to exit ",black, 120, 180, font3)
                text_display(f"High Score {high_score}",red, 290, 250, font3)
                text_display("Press key 'f' for Suprise! ", green, 200, 350, font1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.music.load("snake_sound.mp3")
                    pygame.mixer.music.play()
                    # pygame.mixer.music.load('lag_gaye.mp3')
                    # pygame.mixer.music.play()

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        welcome()
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True

                    # Cheat Mod
                    if event.key == pygame.K_p:
                        sensivity += 7
                    if event.key == pygame.K_o:
                        score += 20
                    if event.key == pygame.K_l:
                        init_velocity += 4

                    # Button Function
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x =  init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_y =  init_velocity
                        velocity_x = 0
            
            snake_x += velocity_x
            snake_y += velocity_y

            # Snake Eat
            if abs(snake_x - food_x) <= sensivity and abs(snake_y - food_y) <= sensivity:
                score += 10
                food_x = random.randint(20,700)            
                food_y = random.randint(20,300)
                snk_length += 4
                init_velocity += 1
                if score > int(high_score):
                    high_score = score

            # Display
            window_size.fill(white)
            window_size.blit(bgimg1,(0, 0))

            text_display ("High score:"+ str(high_score),red, 500, 5, font1)
            text_display("Score: "+ str(score), black, 5, 5, font1)

            # Snake Food
            pygame.draw.circle(window_size, red, (food_x, food_y), food_size)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if snake_x < 0 or  snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            if head in snk_list[:-1]:
                game_over = True
            plot_snake(window_size, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
