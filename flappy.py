import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_WIDTH = 60
PIPE_GAP = 150

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
bird_img = pygame.image.load("bird.jpg")  # Replace with your bird image file path
bird_img = pygame.transform.scale(bird_img, (40, 40))

pipe_img = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
pipe_img.fill((0, 255, 0))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
bird_x = SCREEN_WIDTH // 4
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5

pipes = []
pipe_speed = -3

score = 0

def start_menu(screen):
    """Displays the start menu and waits for the player to press space."""
    font_title = pygame.font.Font(None, 36)  # Changed font size to 36

    font_creator = pygame.font.Font(None, 36)

    title_text = font_title.render("Press SPACE to Start", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    creator_text = font_creator.render("Made by Daksh Joshi", True, BLACK)
    creator_rect = creator_text.get_rect(topleft=(10, SCREEN_HEIGHT - 50))

    while True:
        screen.fill(WHITE)
        screen.blit(title_text, title_rect)
        screen.blit(creator_text, creator_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Exit the menu and start the game

        pygame.display.flip()

def create_pipe():
    """Generates a new pipe pair."""
    pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    return [
        {"x": SCREEN_WIDTH, "y": pipe_height - SCREEN_HEIGHT},  # Top pipe
        {"x": SCREEN_WIDTH, "y": pipe_height + PIPE_GAP},       # Bottom pipe
    ]

def draw_pipes(pipes):
    """Draws pipes on the screen."""
    for pipe in pipes:
        if pipe["y"] < 0:  # Top pipe
            screen.blit(pipe_img, (pipe["x"], pipe["y"]))
        else:              # Bottom pipe
            screen.blit(pipe_img, (pipe["x"], pipe["y"]))

def check_collision(bird_rect, pipes):
    """Checks if the bird collides with any pipe or goes out of bounds."""
    for pipe in pipes:
        pipe_rect = pygame.Rect(pipe["x"], pipe["y"], PIPE_WIDTH, SCREEN_HEIGHT)
        if bird_rect.colliderect(pipe_rect):
            return True

    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True

    return False

def draw_score(score):
    """Displays the current score."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Show the start menu before starting the game
start_menu(screen)

# Main game loop
pipes.extend(create_pipe())  # Add initial pipes

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = -8

    # Bird movement and gravity effect
    bird_velocity += gravity
    bird_y += bird_velocity

    # Update pipes and check for collisions
    for pipe in pipes:
        pipe["x"] += pipe_speed

    if pipes[0]["x"] + PIPE_WIDTH < 0:  # Remove off-screen pipes and add new ones
        pipes = pipes[2:]              # Remove first two off-screen pipes (top and bottom pair)
        pipes.extend(create_pipe())     # Add new pair of pipes at the end of the list
        score += 1                      # Increment score when passing a pair of pipes

    # Draw bird and pipes
    bird_rect = pygame.Rect(bird_x, bird_y, bird_img.get_width(), bird_img.get_height())
    screen.blit(bird_img, (bird_x, bird_y))
    
    draw_pipes(pipes)

    # Check collisions and end game if necessary
    if check_collision(bird_rect, pipes):
        running = False

    # Draw score on screen
    draw_score(score)

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
