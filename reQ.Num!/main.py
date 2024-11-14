import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_LARGE = pygame.font.SysFont('Arial', 32)  # Decreased font size
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Function to load words from a file
def load_words(filename):
    absolute_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(absolute_path, 'r') as file:
            words = [line.strip() for line in file.readlines() if line.strip()]
        if not words:
            raise ValueError(f"The word list in {filename} is empty.")
        return words
    except FileNotFoundError:
        print(f"Warning: The file {absolute_path} was not found. Using a fallback word list.")
        return ["python", "javascript", "hangman", "developer", "programming", "computer"]
    except ValueError as ve:
        print(f"Error: {ve}")
        return ["python", "javascript", "hangman", "developer", "programming", "computer"]

# Function to choose a random word
def choose_word():
    words = load_words('words.txt')
    return random.choice(words)

# Function to format the word with spaces between each dash or letter
def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# Function to draw the hangman based on the number of attempts left
def draw_hangman(attempts):
    pygame.draw.line(screen, BLACK, (150, 500), (150, 200), 5)
    pygame.draw.line(screen, BLACK, (100, 500), (200, 500), 5)
    pygame.draw.line(screen, BLACK, (150, 200), (300, 200), 5)
    pygame.draw.line(screen, BLACK, (300, 200), (300, 250), 5)
    if attempts <= 5:
        pygame.draw.circle(screen, BLACK, (300, 275), 25, 3)
    if attempts <= 4:
        pygame.draw.line(screen, BLACK, (300, 300), (300, 400), 3)
    if attempts <= 3:
        pygame.draw.line(screen, BLACK, (300, 325), (270, 375), 3)
    if attempts <= 2:
        pygame.draw.line(screen, BLACK, (300, 325), (330, 375), 3)
    if attempts <= 1:
        pygame.draw.line(screen, BLACK, (300, 400), (270, 450), 3)
    if attempts == 0:
        pygame.draw.line(screen, BLACK, (300, 400), (330, 450), 3)

# Draw buttons for Play Again and Exit with borders
def draw_buttons():
    play_again_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 120, 50)
    exit_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT - 100, 120, 50)

    # Fill buttons
    pygame.draw.rect(screen, GREEN, play_again_button)
    pygame.draw.rect(screen, RED, exit_button)

    # Draw borders
    pygame.draw.rect(screen, BLACK, play_again_button, 3)  # Border around play again button
    pygame.draw.rect(screen, BLACK, exit_button, 3)  # Border around exit button

    # Add text to buttons
    play_text = FONT_SMALL.render("Play Again", True, WHITE)
    exit_text = FONT_SMALL.render("Exit", True, WHITE)
    screen.blit(play_text, (play_again_button.x + 10, play_again_button.y + 10))
    screen.blit(exit_text, (exit_button.x + 30, exit_button.y + 10))

    return play_again_button, exit_button

# Hangman game function
def hangman():
    word = choose_word()
    guessed_letters = set()
    attempts = 6
    game_over = False

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)

        current_word = display_word(word, guessed_letters)
        word_text = FONT_LARGE.render(current_word, True, BLACK)
        screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 4))

        guessed_letters_text = "Guessed Letters: " + ', '.join(sorted(guessed_letters))
        guessed_text = FONT_SMALL.render(guessed_letters_text, True, BLACK)
        screen.blit(guessed_text, (WIDTH - guessed_text.get_width() - 20, HEIGHT - 60))

        attempts_text = FONT_SMALL.render(f"Remaining Attempts: {attempts}", True, RED)
        screen.blit(attempts_text, (WIDTH - attempts_text.get_width() - 20, HEIGHT - 90))

        draw_hangman(attempts)

        if all(letter in guessed_letters for letter in word):
            win_text = FONT_LARGE.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH - win_text.get_width() - 20, HEIGHT // 2))
            game_over = True
        elif attempts == 0:
            lose_text = FONT_LARGE.render(f"You Lose! The word was: {word}", True, RED)
            screen.blit(lose_text, (WIDTH - lose_text.get_width() - 20, HEIGHT // 2))
            game_over = True

        if game_over:
            play_again_button, exit_button = draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    guess = pygame.key.name(event.key)
                    if guess.isalpha() and len(guess) == 1 and guess not in guessed_letters:
                        guessed_letters.add(guess)
                        if guess not in word:
                            attempts -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    hangman()
                    return
                elif exit_button.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    hangman()
    pygame.quit()
