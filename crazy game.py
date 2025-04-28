import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)

# Fonts
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crazy Game")
clock = pygame.time.Clock()

# Highscore file
HIGHSCORE_FILE = "highscores.txt"

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return {"snake": 0, "flappy": 0}
    with open(HIGHSCORE_FILE, "r") as f:
        lines = f.readlines()
        highscores = {"snake": 0, "flappy": 0}
        for line in lines:
            game, score = line.strip().split(":")
            highscores[game] = int(score)
        return highscores

def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        for game, score in highscores.items():
            f.write(f"{game}:{score}\n")

highscores = load_highscores()

def main_menu():
    while True:
        clock.tick(FPS)
        screen.fill(SKY_BLUE)
        title = font_large.render("Choose a Game", True, WHITE)
        option1 = font_medium.render("1. Flappy Bird", True, WHITE)
        option2 = font_medium.render("2. Snake", True, WHITE)
        quit_text = font_small.render("Press ESC to Quit", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, 250))
        screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, 350))
        screen.blit(quit_text, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    flappy_bird()
                if event.key == pygame.K_2:
                    snake_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def snake_game():
    block_size = 20
    snake_speed = 10
    snake = [(100, 100)]
    direction = (block_size, 0)
    food = (random.randrange(0, WIDTH, block_size), random.randrange(0, HEIGHT, block_size))
    score = 0
    game_over = False
    pause = False
    snake_timer = 0

    while True:
        clock.tick(FPS)
        screen.fill(GREEN)

        if not pause and not game_over:
            snake_timer += 1
            if snake_timer >= FPS // snake_speed:
                snake_timer = 0
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])

                if (new_head[0] < 0 or new_head[0] >= WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT or
                    new_head in snake):
                    game_over = True
                else:
                    snake.insert(0, new_head)
                    if new_head == food:
                        score += 1
                        food = (random.randrange(0, WIDTH, block_size), random.randrange(0, HEIGHT, block_size))
                    else:
                        snake.pop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a] and direction[0] == 0:
                    direction = (-block_size, 0)
                if event.key in [pygame.K_RIGHT, pygame.K_d] and direction[0] == 0:
                    direction = (block_size, 0)
                if event.key in [pygame.K_UP, pygame.K_w] and direction[1] == 0:
                    direction = (0, -block_size)
                if event.key in [pygame.K_DOWN, pygame.K_s] and direction[1] == 0:
                    direction = (0, block_size)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_r and game_over:
                    snake_game()
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        # Draw snake
        for i, block in enumerate(snake):
            color = ORANGE if i == 0 else WHITE
            pygame.draw.rect(screen, color, (block[0], block[1], block_size, block_size))

        # Draw food
        pygame.draw.rect(screen, RED, (food[0], food[1], block_size, block_size))

        # Draw UI
        back_text = font_small.render("ESC - Menu", True, BLACK)
        screen.blit(back_text, (10, 10))
        score_text = font_small.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 40))
        highscore_text = font_small.render(f"High Score: {highscores['snake']}", True, BLACK)
        screen.blit(highscore_text, (10, 70))

        if game_over:
            if score > highscores["snake"]:
                highscores["snake"] = score
                save_highscores(highscores)
                message = "New Highscore!"
            else:
                message = "Game Over!"

            game_over_text = font_large.render("Game Over!", True, RED)
            message_text = font_medium.render(message, True, RED)
            restart_text = font_small.render("Press R to Restart", True, WHITE)

            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()

def flappy_bird():
    bird_size = 30
    bird_x = WIDTH // 4
    bird_y = HEIGHT // 2
    bird_velocity = 0
    gravity = 0.5
    jump_strength = -10

    pipes = []
    pipe_width = 70
    pipe_gap = 200
    pipe_frequency = 1500  # milliseconds
    last_pipe = pygame.time.get_ticks()

    background_scroll = 0
    bg_speed = 1

    score = 0
    game_over = False
    pause = False

    while True:
        clock.tick(FPS)
        screen.fill(SKY_BLUE)

        # Scroll background
        background_scroll -= bg_speed
        if background_scroll <= -WIDTH:
            background_scroll = 0

        # Draw background elements
        for x in range(0, WIDTH * 2, 200):
            pygame.draw.rect(screen, BROWN, (x + background_scroll, HEIGHT - 150, 40, 150))  # Tree trunks
            pygame.draw.circle(screen, GREEN, (x + background_scroll + 20, HEIGHT - 170), 50)  # Tree tops
            pygame.draw.circle(screen, WHITE, (x + background_scroll + 100, 100), 30)  # Cloud 1
            pygame.draw.circle(screen, WHITE, (x + background_scroll + 140, 120), 40)  # Cloud 2

        if not pause and not game_over:
            bird_velocity += gravity
            bird_y += bird_velocity

            # Add pipes
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > pipe_frequency:
                pipe_height = random.randint(100, HEIGHT - 300)
                pipes.append((WIDTH, pipe_height))
                last_pipe = current_time

            # Move pipes
            pipes = [(x - 5, h) for (x, h) in pipes]

            # Check for collision
            for x, h in pipes:
                if (bird_x + bird_size > x and bird_x < x + pipe_width):
                    if bird_y < h or bird_y + bird_size > h + pipe_gap:
                        game_over = True

            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if pipe[0] > -pipe_width]

            # Update score
            for pipe in pipes:
                if pipe[0] + pipe_width == bird_x:
                    score += 1

            if bird_y > HEIGHT or bird_y < 0:
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = jump_strength
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_r and game_over:
                    flappy_bird()
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        # Draw bird
        pygame.draw.rect(screen, ORANGE, (bird_x, bird_y, bird_size, bird_size))

        # Draw pipes
        for x, h in pipes:
            pygame.draw.rect(screen, GREEN, (x, 0, pipe_width, h))
            pygame.draw.rect(screen, GREEN, (x, h + pipe_gap, pipe_width, HEIGHT - h - pipe_gap))

        # Draw UI
        back_text = font_small.render("ESC - Menu", True, BLACK)
        screen.blit(back_text, (10, 10))
        score_text = font_small.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 40))
        highscore_text = font_small.render(f"High Score: {highscores['flappy']}", True, BLACK)
        screen.blit(highscore_text, (10, 70))

        if game_over:
            if score > highscores["flappy"]:
                highscores["flappy"] = score
                save_highscores(highscores)
                message = "You Still Suck!"
            else:
                message = "You Suck!"

            game_over_text = font_large.render("Game Over!", True, RED)
            message_text = font_medium.render(message, True, RED)
            restart_text = font_small.render("Press R to Restart", True, WHITE)

            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()

# Run the menu
main_menu()
