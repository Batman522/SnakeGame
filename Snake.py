import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 8  # Decreased FPS to reduce snake speed

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
title_font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 50)
game_over_font = pygame.font.SysFont(None, 70)
score_font = pygame.font.SysFont(None, 35)

# Game variables
initial_snake_length = 3
snake = [(GRID_WIDTH // 2 - i, GRID_HEIGHT // 2) for i in range(initial_snake_length)]
snake_direction = 'RIGHT'
snake_speed = GRID_SIZE
snake_grow = False
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

# Functions
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def move_snake():
    global snake_direction, snake_grow

    head = snake[0]
    if snake_direction == 'UP':
        new_head = (head[0], head[1] - 1)
    elif snake_direction == 'DOWN':
        new_head = (head[0], head[1] + 1)
    elif snake_direction == 'LEFT':
        new_head = (head[0] - 1, head[1])
    elif snake_direction == 'RIGHT':
        new_head = (head[0] + 1, head[1])

    snake.insert(0, new_head)

    if not snake_grow:
        snake.pop()
    else:
        snake_grow = False

def draw_food():
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision():
    global snake, snake_grow, food, score

    head = snake[0]

    # Check if snake collides with itself
    if head in snake[1:]:
        return True

    # Check if snake eats food
    if head == food:
        snake_grow = True
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score += 1

    # Check if snake hits the boundary
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True

    return False

def draw_score():
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_button(text, pos):
    button_text = button_font.render(text, True, WHITE)
    button_rect = button_text.get_rect(center=pos)
    pygame.draw.rect(screen, BLUE, button_rect.inflate(20, 20))
    screen.blit(button_text, button_rect)
    return button_rect

def main_menu():
    while True:
        screen.fill(BLACK)

        # Draw title
        title_text = title_font.render("Snake Game", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)

        # Draw button
        button_rect = draw_button("Play Game", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

def game_over_menu():
    while True:
        screen.fill(BLACK)

        # Draw Game Over text
        game_over_text = game_over_font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_text, game_over_rect)

        # Draw final score
        final_score_text = score_font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(final_score_text, final_score_rect)

        # Draw Play Again button
        play_again_rect = draw_button("Play Again", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        # Draw Quit button
        quit_rect = draw_button("Quit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    main_game()
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Main loop
def main_game():
    global running, snake, snake_direction, snake_grow, food, score
    running = True
    clock = pygame.time.Clock()

    # Reset game variables
    snake = [(GRID_WIDTH // 2 - i, GRID_HEIGHT // 2) for i in range(initial_snake_length)]
    snake_direction = 'RIGHT'
    snake_grow = False
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    snake_direction = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    snake_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    snake_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    snake_direction = 'RIGHT'

        # Update
        move_snake()

        # Check collisions
        if check_collision():
            running = False

        # Clear screen
        screen.fill(BLACK)

        # Draw
        draw_snake()
        draw_food()
        draw_score()

        # Update display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(FPS)

    # Show game over menu
    game_over_menu()

# Run the main menu
main_menu()

# Start the game
main_game()

# Quit Pygame
pygame.quit()
sys.exit()
