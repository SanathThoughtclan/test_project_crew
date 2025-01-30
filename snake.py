import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = RIGHT
food = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
score = 0
game_over = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for displaying the score
font = pygame.font.Font(None, 36)

# Sound effects
try:
    eat_sound = pygame.mixer.Sound("ra.wav")  # Replace with your sound file
    game_over_sound = pygame.mixer.Sound("rb.wav")  # Replace with your sound file
except pygame.error:
    print("Sound files not found. Continuing without sound.")
    eat_sound = None
    game_over_sound = None


# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != RIGHT:
                snake_direction = RIGHT

    # Move the snake
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    snake.insert(0, new_head)

    # Check for collisions
    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
        or new_head in snake[1:]
    ):
        game_over = True
        if game_over_sound:
            game_over_sound.play()


    # Check for food consumption
    if new_head == food:
        score += 10
        if eat_sound:
            eat_sound.play()
        food = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        while food in snake:
            food = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )
    pygame.draw.rect(
        screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Control game speed
    clock.tick(SNAKE_SPEED)


# Game Over screen (outside the main loop)
if game_over:
    font = pygame.font.Font(None, 72)  # Larger font for Game Over
    game_over_text = font.render("Game Over", True, RED)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds


pygame.quit()