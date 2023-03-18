"""
Tic Tac Toe Player
Authors: 
Alejandro Perez Gonzalez A01746643

"""

import math

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

    
    
    board_copy = deepcopy(board)
    board_copy[i][j] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Diagonal
    if board[0][0] and board[1][1] and board[2][2] == X:
        return X
    if board[0][0] and board[1][1] and board[2][2] == O:
        return O

    #Rows
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O
    #Columns
    cols = ''
    for i in range(3):
        for j in range(3):
            cols += str(board[i][j])
    if cols == 'XXX':
        return X
    if cols == 'OOO':
        return O



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




def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    'X' Player is trying to maximise the score, 'O' Player is trying to minimise it
    """
    raise NotImplementedError

