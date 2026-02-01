import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Chicken!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images and sounds
try:
    chicken_image = pygame.image.load("chicken.png").convert_alpha()
    chicken_image = pygame.transform.scale(chicken_image, (50, 50))
except pygame.error as e:
    print(f"Could not load chicken image: {e}")
    pygame.quit()
    sys.exit()

try:
    catch_sound = pygame.mixer.Sound("catch_sound.wav")
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    background_music = pygame.mixer.Sound("background_music.wav")
except pygame.error as e:
    print(f"Could not load sound files: {e}")
    pygame.quit()
    sys.exit()
 
# Create chicken's rectangle for positioning
def reset_chicken():
    chicken_rect.x = random.randint(0, screen_width - chicken_rect.width)
    chicken_rect.y = random.randint(0, screen_height - chicken_rect.height)

chicken_rect = chicken_image.get_rect()
reset_chicken()

# Define variables
score = 0
game_active = False
game_over = False
chicken_timer = 5  # Chicken catch timer in seconds
game_timer = 45      # Game timer in seconds
start_chicken_time = 0
start_game_time = 0

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Leaderboard file
leaderboard_file = "leaderboard.txt"

# Load highest score
def load_high_score():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as file:
            return int(file.read().strip())
    return 0

# Save highest score
def save_high_score(high_score):
    with open(leaderboard_file, "w") as file:
        file.write(str(high_score))

highest_score = load_high_score()
new_high_score = False  # Flag to check if a new high score is achieved
message_displayed = False  # Flag to track if the message has been displayed
new_high_score_time = None  # Time when the new high score was achieved

# Click counter for outside clicks
click_count = 0
max_clicks = 3

# Function to display text on the screen
def display_text(text, position):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, position)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not game_active and not game_over:  # Start game
                game_active = True
                game_over = False
                score = 0
                game_timer = 45
                reset_chicken()
                start_chicken_time = pygame.time.get_ticks()  # Start chicken timer
                start_game_time = pygame.time.get_ticks()      # Start game timer
                background_music.play(-1)  # Loop background music
                new_high_score = False
                message_displayed = False  # Reset message displayed flag
                click_count = 0  # Reset click count

            if event.key == pygame.K_r and game_over:  # Restart game
                game_active = True
                game_over = False
                score = 0
                game_timer = 45
                reset_chicken()
                start_chicken_time = pygame.time.get_ticks()
                start_game_time = pygame.time.get_ticks()
                background_music.play(-1)
                new_high_score = False
                message_displayed = False  # Reset message displayed flag
                click_count = 0  # Reset click count

            if event.key == pygame.K_p and game_active:  # Pause game
                game_active = False
                background_music.stop()

            if event.key == pygame.K_q and game_over:  # Quit game
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button clicked
            if not game_over and not chicken_rect.collidepoint(pygame.mouse.get_pos()):
                click_count += 1
                if click_count >= max_clicks:
                    game_over = True
                    game_active = False
                    background_music.stop()
                    game_over_sound.play()
            else:
                click_count = 0  # Reset count if clicked on the chicken

    if game_active:
        # Calculate elapsed time for chicken timer and game timer
        current_time = pygame.time.get_ticks()
        elapsed_chicken_time = (current_time - start_chicken_time) / 1000  # in seconds
        elapsed_game_time = (current_time - start_game_time) / 1000  # in seconds

        # Check for chicken catch
        if chicken_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            score += 1
            catch_sound.play()
            reset_chicken()
            start_chicken_time = current_time  # Reset chicken timer

            # Increase game timer for every 10 successful catches
            if score % 10 == 0:
                game_timer += 10

            # Check if a new high score is achieved
            if score > highest_score and not message_displayed:
                highest_score = score
                new_high_score = True
                new_high_score_time = current_time  # Set the time for the new high score
                message_displayed = True  # Mark message as displayed

        # Check for game over conditions
        if elapsed_chicken_time >= chicken_timer:
            game_over = True
            game_active = False
            background_music.stop()
            game_over_sound.play()

        if elapsed_game_time >= game_timer:
            game_over = True
            game_active = False
            background_music.stop()
            game_over_sound.play()

        # Move the chicken randomly every 5 seconds
        if int(elapsed_chicken_time) % 3 == 0 and elapsed_chicken_time > 0:
            reset_chicken()

    # Fill screen with white color
    screen.fill(WHITE)

    if game_active:
        # Vibration effect: Small random offset
        vibrate_offset_x = random.randint(-15, 15)
        vibrate_offset_y = random.randint(-15, 15)

        # Draw chicken with vibration effect
        screen.blit(chicken_image, (chicken_rect.x + vibrate_offset_x, chicken_rect.y + vibrate_offset_y))

        # Draw highest score above current score
        display_text(f"Highest Score: {highest_score}", (10, 30))
        display_text(f"Score: {score}", (10, 60))

        # Draw remaining game timer
        remaining_game_time = max(0, game_timer - int(elapsed_game_time))
        display_text(f"Game Time Left: {remaining_game_time}s", (screen_width - 250, 10))
        
        # Draw chicken timer
        remaining_chicken_time = max(0, chicken_timer - int(elapsed_chicken_time))
        display_text(f"Chicken Time Left: {remaining_chicken_time}s", (screen_width - 250, 40))

        # Display the special message if a new high score is achieved
        if new_high_score and new_high_score_time is not None and (current_time - new_high_score_time) <= 3000:
            display_text("Winner winner chicken dinner!", (screen_width // 2 - 150, screen_height // 2 - 50))

    elif game_over:
        display_text("Game Over!", (screen_width // 2 - 50, screen_height // 2 - 20))
        display_text("Press 'R' to Restart", (screen_width // 2 - 100, screen_height // 2 + 10))
        display_text("Press 'Q' to Quit", (screen_width // 2 - 100, screen_height // 2 + 40))

        # Display highest score at game over screen
        display_text(f"Highest Score: {highest_score}", (screen_width // 2 - 100, screen_height // 2 + 70))

        # Save new high score if achieved
        if new_high_score:
            save_high_score(highest_score)

    else:
        display_text("Welcome to Chicken Catcher!", (screen_width // 2 - 150, screen_height // 2 - 60))
        display_text("Press 'Enter' to Start", (screen_width // 2 - 100, screen_height // 2 - 20))
        display_text("Press 'P' to Pause", (screen_width // 2 - 100, screen_height // 2 + 10))

    # Update display
    pygame.display.flip()

    # Set frame rate
    clock.tick(30)
