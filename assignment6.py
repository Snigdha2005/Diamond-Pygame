import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Function to display text
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to draw buttons
def draw_button(text, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, BLACK, x + width / 2, y + height / 2)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.selected = False

    def image(self):
        return f"cards/{self.rank}_of_{self.suit}.png"

def game_loop():
    # Define points for each card rank
    points_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # Define all suits excluding diamonds
    suits = ['hearts', 'clubs', 'spades']

    # Assign suits to player and computer
    player_suit, computer_suit = random.sample(suits, k=2)

    # Create player's deck with assigned suit
    player_deck = []
    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        player_deck.append(Card(rank, player_suit))

    # Create computer's deck with assigned suit
    computer_deck = []
    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        computer_deck.append(Card(rank, computer_suit))

    # Shuffle the computer's deck
    random.shuffle(computer_deck)
    computer_previous_card = None

    # Shuffle the diamond cards
    diamond_cards = [Card(rank, 'diamonds') for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
    random.shuffle(diamond_cards)

    # Initialize player and computer scores
    player_score = 0
    computer_score = 0

    # Define font and font size for the scores
    font = pygame.font.SysFont(None, 30)

    # Calculate the width and height of each card based on screen dimensions
    num_cards = 13  # Number of cards to display
    card_spacing = 10  # Spacing between cards
    card_width = (WIDTH - (num_cards + 1) * card_spacing) // num_cards  # Calculate width to fit cards with spacing
    card_height = int(card_width * 1.5)  # Maintain aspect ratio (1.5 times the width)

    # Define the positions of each card based on a consistent pattern
    card_positions = []
    initial_x = 20  # Adjust as needed
    for i, card in enumerate(player_deck):
        card_x = initial_x + i * (card_width + card_spacing)
        card_y = HEIGHT - card_height - 20  # Adjust as needed
        card_positions.append((card_x, card_y))

    running = True
    selected_card = None  # Variable to store the selected card

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a card was clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (card_x, card_y) in enumerate(card_positions):
                    if card_x <= mouse_x <= card_x + card_width and card_y <= mouse_y <= card_y + card_height:
                        # Mark the clicked card as selected
                        if selected_card:
                            selected_card.selected = False
                            if computer_deck:
                                computer_previous_card = computer_deck.pop(0)  # Update computer_previous_card with a new card
                            else:
                                computer_previous_card = None  # If computer_deck is empty, set computer_previous_card to None
                            selected_card = player_deck.pop(i)  # Remove the clicked card from the deck
                            selected_card.selected = True

                        if not diamond_cards:
                            running = False  # End the game if no diamond cards left
                        else:
                            diamond_card = diamond_cards.pop(0)  # Pop a diamond card
                            print(f"Player selected: {selected_card.rank} of {selected_card.suit}")
                            if computer_previous_card:
    

                                print(f"Computer selected: {computer_previous_card.rank} of {computer_previous_card.suit}")
                            print(f"Diamond card: {diamond_card.rank} of {diamond_card.suit}")
                            # Compare ranks and update scores
                            if computer_previous_card:
                                if points_dict[selected_card.rank] > points_dict[computer_previous_card.rank]:
                                    player_score += points_dict[diamond_card.rank]
                                elif points_dict[selected_card.rank] < points_dict[computer_previous_card.rank]:
                                    computer_score += points_dict[diamond_card.rank]
                                else:
                                    player_score += points_dict[diamond_card.rank] / 2
                                    computer_score += points_dict[diamond_card.rank] / 2

        # Pop the computer's card if available
        if computer_deck:
            computer_previous_card = computer_deck.pop(0)
        else:
            computer_previous_card = None

        # Drawing code
        screen.fill(GREEN)  # Fill screen with green color


        # Display player's cards at the bottom of the screen
        for i, card in enumerate(player_deck):
            card_x, card_y = card_positions[i]
            card_image = pygame.image.load(card.image())
            if card.selected:
                card_image.fill(BLACK, special_flags=pygame.BLEND_RGB_MULT)  # Change color to black
            card_image = pygame.transform.scale(card_image, (card_width, card_height))
            screen.blit(card_image, (card_x, card_y))

        # Display computer's card (if not None) on the right side of the screen
        if computer_previous_card:
            computer_card_image = pygame.image.load(computer_previous_card.image())
            computer_card_image = pygame.transform.scale(computer_card_image, (card_width, card_height))
            screen.blit(computer_card_image, (WIDTH - card_width - 20, HEIGHT // 2 - card_height // 2))

        # Display player score in the upper right corner
        draw_text(f"Your Score: {player_score}", BLACK, WIDTH - 150, 20)

        # Display computer score in the lower right corner
        # Display computer score in the lower left corner
        draw_text(f"Computer Score: {computer_score}", BLACK, WIDTH - 150, 40)


        # Display diamond card in the center of the screen
        if diamond_cards:
            diamond_card = diamond_cards[0]  # Get the top diamond card
            diamond_card_image = pygame.image.load(diamond_card.image())
            diamond_card_image = pygame.transform.scale(diamond_card_image, (card_width, card_height))
            screen.blit(diamond_card_image, (WIDTH // 2 - card_width // 2, HEIGHT // 2 - card_height // 2))

        pygame.display.flip()

# Start the game loop
game_loop()

# Quit Pygame when the game loop ends
pygame.quit()

