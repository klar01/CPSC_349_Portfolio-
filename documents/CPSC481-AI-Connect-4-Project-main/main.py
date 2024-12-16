import pygame
import sys
from game_board import Board
from player import Player
import time

SQUARE_SIZE = 100
WIDTH = 700
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLUMN_COUNT = 7

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4")

def welcome_screen():

    while True:
        screen.fill((0, 0, 128))

        title = pygame.font.SysFont("impact", 75).render("Welcome to Connect 4", True, (255, 255, 0))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 100))

        solo_option = pygame.font.SysFont("impact", 50).render("Our AI vs Human?", True, (255, 0, 0))
        multiplayer_option = pygame.font.SysFont("impact", 50).render("Human vs Human?", True, (255, 255, 0))
        depth_Three = pygame.font.SysFont("impact", 50).render("Solo: easy (Depth 3)", True, (255, 255, 0))
        depth_Four = pygame.font.SysFont("impact", 50).render("Solo: medium (Depth 4)", True, (255, 255, 0))
        depth_Five = pygame.font.SysFont("impact", 50).render("Solo: expert (Depth 5)", True, (255, 255, 0))

        solo = solo_option.get_rect(center=(WIDTH // 2, 250))
        multiplayer = multiplayer_option.get_rect(center=(WIDTH // 2, 350))
        ai_Three = depth_Three.get_rect(center=(WIDTH // 2, 450))
        ai_Four = depth_Four.get_rect(center=(WIDTH // 2, 550))
        ai_Five = depth_Five.get_rect(center=(WIDTH // 2, 650))

        #screen.blit(solo_option, solo)
        screen.blit(multiplayer_option, multiplayer)
        screen.blit(depth_Three, ai_Three)
        screen.blit(depth_Four, ai_Four)
        screen.blit(depth_Five, ai_Five)

        mouse = pygame.mouse.get_pos()
        if solo.collidepoint(mouse) or multiplayer.collidepoint(mouse):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solo.collidepoint(event.pos):
                    return "solo"
                if multiplayer.collidepoint(event.pos):
                    return "multiplayer"
                if ai_Three.collidepoint(event.pos):
                    return "depth_Three"
                if ai_Four.collidepoint(event.pos):
                    return "depth_Four"
                if ai_Five.collidepoint(event.pos):
                    return "depth_Five"
                
                
#game ended with a WINNER              
def winner(board, players, turn):
    outcome = pygame.font.SysFont("impact", 75).render(
        f"Player {players[turn].get_id()} Wins!!!!", 1, players[turn].get_color()
    )
    screen.blit(outcome, (50, 10))
    pygame.display.update()
    board.draw_board(screen)

    return True #state of gameOver

#game ended with a TIE
def tie(board, players, turn):
    outcome = pygame.font.SysFont("impact", 75).render(
        "It's a tie!", 1, (255, 255, 255)
    )
    screen.blit(outcome, (50, 10))
    pygame.display.update()
    board.draw_board(screen)

    return True #state of gameOver

def restart_game():
    text = pygame.font.SysFont("impact", 50)
    text_Object= text.render("Return to Homescreen?", True, WHITE, BLACK) #create the text surface object, which the text is drawn on
    restart = text_Object.get_rect() # create a rectangular object for the text surface object
    restart.center = (WIDTH // 2, 300)  # set the center of the rectangular object

    #copying the text surface object to the display surface object at the coordinates.
    screen.blit(text_Object , restart)
    
    #displays the options
    pygame.display.update()

    mouse = pygame.mouse.get_pos()
    if restart.collidepoint(mouse):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart.collidepoint(event.pos):
                    main()                  


def main():
    mode = welcome_screen()

    board = Board()
    player1 = Player(1, mode=mode)
    player2 = Player(2, mode=mode)  # Player 2 (AI in solo mode)

    players = [player1, player2]
    game_over = False
    turn = 0

    screen.fill(WHITE)
    board.draw_board(screen)

    #plays human vs human 
    if mode == "multiplayer":
        while not game_over:
            for event in pygame.event.get():

                #player clicks the exit button
                if event.type == pygame.QUIT:
                    sys.exit()

                # the token moves in response where the cursor moves 
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 100))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, players[turn].get_color(), (posx, 50), 40)
                    pygame.display.update()

                #click down on of the columns to place your token
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 100))
                    posx = event.pos[0]
                    col = posx // SQUARE_SIZE

                    #add token to the column if it's not alreadt full
                    if board.is_valid_location(col):
                        row = board.get_next_open_row(col)
                        board.add_token(players[turn], row, col)

                        board.draw_board(screen)
                        pygame.display.update()

                        #checks for the winner and who won
                        if board.winning_move(players[turn].get_id()):
                            game_over = winner(board, players, turn)
                            break
                        
                        #checks for a tie
                        if not any(board.is_valid_location(c) for c in range(COLUMN_COUNT)):
                            game_over = tie(board, players, turn)
                            break
                        
                        #next player's turn 
                        turn = (turn + 1) % 2

            #game ends, return to main screen 
            if game_over:
                restart_game()             
            
    #plays human vs AI 
    else:
        while not game_over:
            for event in pygame.event.get():
                #player clicks the exit button
                if event.type == pygame.QUIT:
                    sys.exit()

                # the token moves in response where the cursor moves 
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 100))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, players[turn].get_color(), (posx, 50), 40)
                    pygame.display.update()

                #HUMAN player 
                if(players[turn].get_id() == 1 and not game_over):

                    #click down on of the columns to place your token
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 100))
                        posx = event.pos[0]
                        col = posx // SQUARE_SIZE

                        #add token to the column if it's not alreadt full
                        if board.is_valid_location(col):
                            row = board.get_next_open_row(col)
                            board.add_token(players[turn], row, col)
                            board.draw_board(screen)
                            pygame.display.update()

                            #check for a winner and who won
                            if board.winning_move(players[turn].get_id()):
                                game_over = winner(board, players, turn)
                                break
                            
                            #check for a tie
                            if not any(board.is_valid_location(c) for c in range(COLUMN_COUNT)):
                                game_over = tie(board, players, turn)
                                break
                            
                            turn = (turn + 1) % 2
                    
            #AI player 
            if players[turn].get_id() == 2 and not game_over:

                #use alpha-beta pruning
                board.reset_counter()
                start = time.time()
                best_col = 0

                #depth used based on mode choosen by user 
                if (mode == "depth_Three"):
                    best_col = board.alpha_beta(players[0], players[1], True, float('-inf'), float('inf'), depth=3) [0]
                elif (mode == "depth_Four"):
                    best_col = board.alpha_beta(players[0], players[1], True, float('-inf'), float('inf'), depth=4) [0]

                elif (mode == "depth_Five"):
                    best_col = board.alpha_beta(players[0], players[1], True, float('-inf'), float('inf'), depth=5) [0]

                end = time.time()
                total_time = (end - start) * 1000
                print(f"AI's runtime: {total_time:.2f} ms")
                print(f"Number of Nodes: {board.counter}")

                #add token to the column if it's not alreadt full
                if board.is_valid_location(best_col):
                    row = board.get_next_open_row(best_col)
                    board.add_token(players[turn], row, best_col)
                    board.draw_board(screen)
                    pygame.display.update()
                
                #check for a winner and who won
                if board.winning_move(players[turn].get_id()):
                    game_over = winner(board, players, turn)
                    break

                #check for a tie   
                if not any(board.is_valid_location(c) for c in range(COLUMN_COUNT)):
                    game_over = tie(board, players, turn)
                    break

                turn = (turn + 1) % 2

        #game ends, return to main screen 
        if game_over:
            restart_game()


if __name__ == "__main__":
    main()
