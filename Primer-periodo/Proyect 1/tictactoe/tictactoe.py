"""
Tic Tac Toe Player
Authors: 
Alejandro Perez Gonzalez A01746643
Lizbeth Paulina Ayala Parra A01747237

"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    NumberOfX = 0
    NumberOfO = 0
    

    for row in board:
        NumberOfX += row.count(X)
        NumberOfO += row.count(O)


    if NumberOfX > NumberOfO:
        return O
    else:
        return X

    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    playerMoves = []
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                playerMoves.append((i,j))
    
    return playerMoves

   # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """    
    Board = [row[:] for row in board]

    if Board[action[0]][action[1]] != EMPTY:
        raise ValueError("Position already occupied")

    
    boardcopy = deepcopy(board)

    boardcopy[action[0]][action[1]] = player(board)

    return boardcopy




def winner(board):

    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == X:
            return X
        if board[i][0] and board[i][1] and board[i][2] == O:
            return O
        
    for j in range(3):
        if board[0][j] and board[1][j] and board[2][j] == X:
            return X
        if board[0][j] and board[1][j] and board[2][j] == O:
            return O

    if board[0][0] and board[1][1] and board[2][2] or board[0][2] and board[1][1] and board[2][1] == X:
        return X
    if board[0][0] and board[1][1] and board[2][2] or board[0][2] and board[1][1] and board[2][1] == O:
        return O
    
    #No winner found
    return EMPTY




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check winner function to determine if there is a winner
    if winner(board):
        return True

    # Check if the board is empty
    for row in board:
        if EMPTY in row:
            return False
        else:
            return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0




def minimax_max(board):
    """
    Returns the maximum possible score for X player.
    """
    if terminal(board):
        return utility(board)

    best_score = -math.inf
    for action in actions(board):
        score = minimax_min(result(board, action))
        best_score = max(best_score, score)
    return best_score


def minimax_min(board):
    """
    Returns the minimum possible score for O player.
    """
    if terminal(board):
        return utility(board)

    best_score = math.inf
    for action in actions(board):
        score = minimax_max(result(board, action))
        best_score = min(best_score, score)
    return best_score

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    'X' Player is trying to maximise the score, 'O' Player is trying to minimise it
    """
    current_player = player(board)

    # If the game is over, return None as there is no action to take
    if terminal(board):
        return None

    if current_player == X:
        # Maximize the score
        best_score = -math.inf
        best_action = None
        for action in actions(board):
            score = minimax_min(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    else:
        # Minimize the score
        best_score = math.inf
        best_action = None
        for action in actions(board):
            score = minimax_max(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action
        return best_action

