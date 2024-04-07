def main_game(screen, font, option1, option2, sub_option2):
    global scores
    player1_bids = []
    player2_bids = []
    cards = list(all_cards.keys())
    player1_cards = list(all_cards.keys())
    player2_cards = list(all_cards.keys())



    for i in range(13):
        
        diamond_card =  pick_diamond(cards)

      

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Define rects for player 1 cards
        player1_card_rects = []
        for i in range(len(player1_cards)):
            card_value = all_cards[player1_cards[i]]
            x = 300 + ((card_value - 2) * 60)  # Adjust offset and spacing as needed
            y = 350
            width = 70  # Card width
            height = 100  # Card height
            player1_card_rects.append(pygame.Rect(x, y, width, height))

        # Check for click on player 1 cards
        clicked_card = None
        for event in pygame.event.get():  # Get all events
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                if event.button == 1:  # Check for left click
                    if player1_card_rects:  # Check if rects exist (avoid potential errors)
                        for i, rect in enumerate(player1_card_rects):
                            if rect.collidepoint(mouse_pos):
                                clicked_card = player1_cards[i]
                                break
                              

        # Set bid1 based on click or original logic
        if clicked_card is not None:
            bid1 = clicked_card
        else:
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