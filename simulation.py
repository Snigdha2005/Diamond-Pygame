import pygame
import os
import random
import sys

# Pygame initialization
pygame.init()

# Set up the screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diamond Card Auction Game")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define font
font = pygame.font.SysFont(None, 56)
# Load card images

CARD_FOLDER = "Cards/Playing Cards/PNG-cards-1.3/"
card_images = {}
all_cards = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
scores = [0, 0]
player1_bids = []
player2_bids = []

card_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['hearts', 'diamonds', 'clubs', 'spades']
for suit in suits:
    card_images[suit] = []
    for i in card_list:
        card_image = pygame.image.load(os.path.join(CARD_FOLDER, f"{suit}/{i}.png"))
        card_images[suit].append(pygame.transform.scale(card_image, (170, 240)))

# Player input functions
def get_player_options(screen, font, player):
    option = None
    if player == 1:
        screen.fill(GREEN)
        player1_text = font.render("Player 1 Options", True, WHITE)
        player1_rect = player1_text.get_rect(midtop=(640, 120))
        screen.blit(player1_text, player1_rect)
        opt = ['Adaptive', 'Balanced', 'Dynamic', 'Random', 'Equal']
        button_width = 200
        button_height = 50
        option1_buttons = [font.render(f"{opt[i]}", True, BLACK) for i in range(5)]
        for i, button in enumerate(option1_buttons):
                button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 250 + i * 60), (button_width, button_height))
                pygame.draw.rect(screen, WHITE, button_rect)
                button_text_rect = button.get_rect(center=button_rect.center)  # Get text rectangle
                screen.blit(button, button_text_rect)
    else:
        screen.fill(GREEN)
        player2_text = font.render("Player 2 Options", True, WHITE)
        player2_rect = player2_text.get_rect(midtop=(640, 120))
        screen.blit(player2_text, player2_rect)
        opt = ['Maximum', 'Minimum', 'Adaptive', 'Balanced', 'Dynamic', 'Random', 'Equal']
        button_width = 200
        button_height = 50
        option2_buttons = [font.render(f"{opt[i]}", True, BLACK) for i in range(7)]
        for i, button in enumerate(option2_buttons):
                button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 200 + i * 60), (button_width, button_height))
                pygame.draw.rect(screen, WHITE, button_rect)
                button_text_rect = button.get_rect(center=button_rect.center)  # Get text rectangle
                screen.blit(button, button_text_rect)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if player == 1:
                    for i, option_text in enumerate(option1_buttons):
                        button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 250 + i * 60), (button_width, button_height))
                        if button_rect.collidepoint(mouse_pos):
                            option = i + 1  # Option numbers start from 1
                            running = False
                            break
                else:
                    for i, option_text in enumerate(option2_buttons):
                        button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 250 + i * 60), (button_width, button_height))
                        if button_rect.collidepoint(mouse_pos):
                            option = i + 1  # Option numbers start from 1
                            running = False
                            break

    return option
    
# Countdown function
def countdown():
    font = pygame.font.SysFont(None, 100)
    for i in range(3, 0, -1):
        screen.fill(GREEN)
        text = font.render(str(i), True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

# Shuffling animation
diamond_card_images = card_images['diamonds']

def pick_diamond(cards):
    return random.choice(cards)
#print(pick_diamond(cards))

def bid_solver(diamond_card, player_cards, option, opponent_bids, scores):
    if option == 1:
        return adaptive_bidding_strategy(diamond_card, player_cards, opponent_bids)
    elif option == 2:
        return balanced_bidding_strategy(diamond_card, player_cards)
    elif option == 3:
        return dynamic_adaptation_strategy(diamond_card, player_cards, "aggressive", scores[0])
    elif option == 4:
        return random.choice(player_cards)
    else:
        return diamond_card

# Player 2 bid function
def player2_bid(diamond_card, player_cards, option, opponent_bids, scores, sub_option):
    if option == 1:
        return max(player_cards)
    elif option == 2:
        return min(player_cards)
    else:
        return bid_solver(diamond_card, player_cards, sub_option, opponent_bids, scores)

# Adaptive bidding strategy function
def adaptive_bidding_strategy(diamond_card, player_cards, opponent_bids):
    aggressiveness_threshold = 8

    if len(opponent_bids) != 0 and max([all_cards[_] for _ in opponent_bids]) > aggressiveness_threshold:
        return max(player_cards)
    elif all_cards[diamond_card] < 8:
        return min(player_cards)
    else:
        return max(player_cards)

# Balanced bidding strategy function
def balanced_bidding_strategy(diamond_card, player_cards):
    if all_cards[diamond_card] >= 10:
        return max(player_cards)
    elif all_cards[diamond_card] <= 5:
        return min(player_cards)
    else:
        return max(player_cards)

# Dynamic adaptation strategy function
def dynamic_adaptation_strategy(diamond_card, player_cards, opponent_aggressiveness, player_score):
    if opponent_aggressiveness == "aggressive" and player_score < 50:
        return min(player_cards)
    elif opponent_aggressiveness == "conservative" and player_score >= 50:
        return max(player_cards)
    else:
        return max(player_cards)

# Remove card from suit function
def remove_card_from_suit(suit, card):
    suit.remove(card)
    return suit

# Update suit function
def update_suit(suits, cards):
    for i in range(len(suits)):
        #print(suits[i], cards[i])
        suits[i].remove(cards[i])
    return suits

# Scoreboard function
def scoreboard(diamond_card, bid1, bid2):
    global scores
    if all_cards[bid1] > all_cards[bid2]:
        scores[0] = scores[0] + all_cards[diamond_card]
    elif all_cards[bid2] > all_cards[bid1]:
        scores[1] = scores[1] + all_cards[diamond_card]
    else:
        scores = [scores[_] + all_cards[diamond_card] / 2 for _ in range(2)]
    return 

# Winner function
def winner():
    m = max(scores)
    if m == scores[0] and m != scores[1]:
        return "Player 1"
    elif m == scores[1] and m != scores[0]:
        return "Player 2"
    return "Draw"

# Main game loop
def main_game(screen, font, option1, option2, sub_option2):
    global scores
    player1_bids = []
    player2_bids = []
    cards = list(all_cards.keys())
    player1_cards = list(all_cards.keys())
    player2_cards = list(all_cards.keys())
    for i in range(13):
        diamond_card = pick_diamond(cards)
        bid1 = bid_solver(diamond_card, player1_cards, option1, player2_bids, scores)
        player1_bids.append(bid1)
        bid2 = player2_bid(diamond_card, player2_cards, option2, player1_bids, scores, sub_option2)
        player2_bids.append(bid2)
        #print(diamond_card, bid1, bid2)
        screen.fill(GREEN)
        print(diamond_card, bid1, bid2, end=" ")
        # Display diamond card
        player_text = font.render(f"Player 1 Cards: ", True, WHITE)
        screen.blit(player_text, (20, 400))
        player_text = font.render(f"Player 2 Cards: ", True, WHITE)
        screen.blit(player_text, (20, 520))
        for i in player1_cards:
            #print(len(card_images['hearts']))
            #print(all_cards[i] - 2)
            screen.blit(card_images['hearts'][all_cards[i] - 2], (300+((all_cards[i]-2)*60), 350))
        for i in player2_cards:
            screen.blit(card_images['spades'][all_cards[i] - 2], (300+((all_cards[i]-2)*60), 450))
        pygame.display.flip()
        pygame.time.delay(2000)
        screen.fill(GREEN)
        screen.blit(card_images['diamonds'][all_cards[diamond_card] - 2], (150, 40))
        # Display player 1 cards
        [cards, player1_cards, player2_cards] = update_suit([cards, player1_cards, player2_cards], [diamond_card, bid1, bid2])
        player_text = font.render(f"Player 1 Cards: ", True, WHITE)
        screen.blit(player_text, (20, 400))
        player_text = font.render(f"Player 2 Cards: ", True, WHITE)
        screen.blit(player_text, (20, 520))
        for i in player1_cards:
            #print(len(card_images['hearts']))
            #print(all_cards[i] - 2)
            screen.blit(card_images['hearts'][all_cards[i] - 2], (300+((all_cards[i]-2)*60), 350))
        for i in player2_cards:
            screen.blit(card_images['spades'][all_cards[i] - 2], (300+((all_cards[i]-2)*60), 450))
        # Display bids
        bid_text = font.render(f"Player 1 Bid: ", True, WHITE)
        screen.blit(bid_text, (450, 100))
        screen.blit(card_images['hearts'][all_cards[bid1] - 2], (650, 40))
        bid_text = font.render(f"Player 2 Bid: ", True, WHITE)
        screen.blit(bid_text, (850, 100))
        screen.blit(card_images['spades'][all_cards[bid2] - 2], (1050, 40))
        pygame.display.flip()
        pygame.time.delay(4000)
        scoreboard(diamond_card, bid1, bid2)
        print(scores)
        # Display scoreboard
        screen.fill(GREEN)
        scoreboard_text = font.render(f"Scores: {scores[0]} - {scores[1]}", True, WHITE)
        scoreboard_rect = scoreboard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(scoreboard_text, scoreboard_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    # Display winner
    screen.fill(GREEN)
    winner_text = font.render(f"Winner: {winner()}", True, WHITE)
    winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(winner_text, winner_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

# Bid solver function

# Main function
def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Diamond Card Auction Game")

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Define font
    font = pygame.font.SysFont(None, 46)

    option1 = get_player_options(screen, font, 1)
    option2 = get_player_options(screen, font, 2)
    countdown()
    if option2 < 2:
        main_game(screen, font, option1, option2, 0)
    else:
        main_game(screen, font, option1, 3, option2 - 2)

    # Quit Pygame
    pygame.quit()
# Execute main function
main()