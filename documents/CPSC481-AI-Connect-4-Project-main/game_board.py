from player import Player
import math
import pygame
import numpy as np
import sys

COLUMN_COUNT = 7
ROW_COUNT = 6
SQUARE_SIZE = 100

class Board:

    def __init__(self):
        self.NUM_ROWS = ROW_COUNT
        self.NUM_COLS = COLUMN_COUNT
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))  #board must always start empty (when starting new game)
        self.board_image = pygame.image.load("images/board.png")
        self.counter = 0

    #player adds a token to a column if the column isn't full
    def add_token(self, player, row, col):
        self.board[row][col] = player.get_id()
                
    def is_valid_location(self, col):
        return self.board[self.NUM_ROWS - 1][col] == 0  # Check if the top cell is empty

    # Get the next available row in a column
    def get_next_open_row(self, col):
        for row in range(self.NUM_ROWS):
            if self.board[row][col] == 0:  # Find the first empty cell
                return row
        raise ValueError("Column is full!")

    # Check if any of the pieces placed were in a sequence that constitutes a victory; return boolean
    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.NUM_COLS - 3):
            for r in range(self.NUM_ROWS):
                if (self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece):
                    return True

        # Check vertical locations for win
        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS - 3):
                if (self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece):
                    return True

        # Check positively sloped diagonals
        for c in range(self.NUM_COLS - 3):
            for r in range(self.NUM_ROWS - 3):
                if (self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece):
                    return True

        # Check negatively sloped diagonals
        for c in range(self.NUM_COLS - 3):
            for r in range(3, self.NUM_ROWS):
                if (self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece):
                    return True

        return False
    
    def draw_board(self, screen):
        screen.blit(self.board_image, (0, 100))  # Position the image slightly lower to leave space for tokens

        flipped_board = np.flip(self.board, 0)

        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS):
                pos_x = c * 100 + 50
                pos_y = r * 100 + 150  # Adjust for row (start after header)

                if flipped_board[r][c] == 1:  # Player 1
                    pygame.draw.circle(screen, (255, 255, 0), (pos_x, pos_y), 40) 
                elif flipped_board[r][c] == 2:  # Player 2
                    pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), 40)

        pygame.display.update()

    #finds all available columns to place a token for the player's turn at the current state of board
    def valid_locations(self):
        valid_location =[]

        for col in COLUMN_COUNT:
            if(self.boardis_valid_location(col)):
                valid_location.append(col)

        return valid_location
    
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        # AI's moves for 2,3 and for winning
        if window.count(piece) == 4:  # Winning move
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:  # 3-in-a-row with an open slot
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:  # 2-in-a-row with two open slots
            score += 4

        # Opponent has 3 in a row to block
        if window.count(opp_piece) == 3 and window.count(0) == 1:  # Opponent's 3-in-a-row
            score -= 8
        elif window.count(opp_piece) == 2 and window.count(0) == 2:  # Opponent's 2-in-a-row with two open slots
            score -= 4

        if window.count(piece) == 2 and window.count(0) == 2:  #AI's double threat
            score += 6
        if window.count(opp_piece) == 2 and window.count(0) == 2:  # enemies double threat
            score -= 6

        return score

    def score_position(self, piece):

        score = 0
        center_array = [int(i) for i in list(self.board[:, self.NUM_COLS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3  # Higher weight for center column

        # check horizontals
        for r in range(self.NUM_ROWS):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.NUM_COLS - 3):  # Horizontal windows
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # check verticals
        for c in range(self.NUM_COLS):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.NUM_ROWS - 3):  # Vertical windows
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # checks positive diagonols
        for r in range(self.NUM_ROWS - 3):
            for c in range(self.NUM_COLS - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # checks negative diagnol
        for r in range(self.NUM_ROWS - 3):
            for c in range(self.NUM_COLS - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score
        
    # Key points about how alpha-beta pruning works:
    #   MAX - updates the value of alpha.
    #   MIN - updates the value of beta.
    #   CHILD NODES get ONLY the alpha and beta values from the PARENT nodes.
    #   PRUNE for (MAX player) beta <= alpha, or (MIN player) 

    # provide this function the 'board' (the state of the board), 'maxPlayer' (true/false), 
    # and provides the appropraite alpha/beta (-infin or +infin) based on 'maxPlayer'
    # returns (best value, column of best value)
    def alpha_beta(self, playerOne, playerTwo, startMaxPlayer, alpha, beta, depth):
        
        self.counter += 1

        human = playerOne.get_id()
        ai = playerTwo.get_id()
        valid_locations = [col for col in range(self.NUM_COLS) if self.is_valid_location(col)]
        is_terminal = self.is_terminal(playerOne, playerTwo)

        # Base case
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(ai):  # AI wins
                    return (None, 1000000)
                elif self.winning_move(human):  # Human wins
                    return (None, -1000000)
                else:
                    return (None, 0)  # Tie
            return (None, self.score_position(ai))  # Score the board for the AI

        # Maximizing AI
        if startMaxPlayer:
            value = float('-inf')
            best_col = valid_locations[0]

            for col in valid_locations:
                row = self.get_next_open_row(col)
                temp_board = self.board.copy()
                self.add_token(playerTwo, row, col)
                new_score = self.alpha_beta(playerOne, playerTwo, False, alpha, beta, depth - 1)[1]
                self.board = temp_board

                if new_score > value:
                    value = new_score
                    best_col = col
                
                if new_score >= beta:
                    break
                
                alpha = max(alpha, value)

            return best_col, value

        # Minimizing player
        else:
            value = float('inf')
            best_col = valid_locations[0]

            for col in valid_locations:
                row = self.get_next_open_row(col)
                temp_board = self.board.copy()
                self.add_token(playerOne, row, col)
                new_score = self.alpha_beta(playerOne, playerTwo, True, alpha, beta, depth - 1)[1]
                self.board = temp_board

                # STEP 1
                if new_score < value:
                    value = new_score
                    best_col = col
                
                # STEP 2
                if new_score <= alpha:
                    break

                # STEP 3
                beta = min(beta, new_score)

            return best_col, value   #highest value and column associated with it



    #returns a boolean if the node is a leaf node or not 
    def is_terminal(self, playerOne, playerTwo):
        human = playerOne.get_id()
        ai = playerTwo.get_id()

        #human/ai wins or tie 
        if (self.winning_move(human) or self.winning_move(ai) or np.count_nonzero(self.board) == 42):
            return True
        else:
            return False 

    def reset_counter(self):
        self.counter = 0