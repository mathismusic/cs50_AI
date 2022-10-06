"""
Tic Tac Toe Player
"""

import math
import copy

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

    if terminal(board):
        return 1
    count = 0
    for row in board:
        count += row.count(X)  # the variable X = 'X', so it's list.count('X') only.
        count -= row.count(O)
    if count == 0:
        return X
    else:
        return O


def actions(board):

    if terminal(board):
        return 1
    set_of_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_actions.add((i, j))
    return set_of_actions  # set_of_actions is a set of 2-tuples, an action is a tuple


def result(board, action):

    if board[action[0]][action[1]] != EMPTY:
        raise Exception
    new_board = copy.deepcopy(board)  # https://www.youtube.com/watch?v=naG4uXpmVAU
    new_board[action[0]][action[1]] = player(board)  # initially EMPTY, now set to X/O
    return new_board


def winner(board):

    # centre_player = board[1][1] Not correct as centre player could be empty, checking three emptys in a row is not correct
    if board[1][1] != EMPTY:
        if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0] or board[0][1] == board[1][1] == board[2][1] or board[1][0] == board[1][1] == board[1][2]:
            return board[1][1]
    if board[0][0] != EMPTY:
        # no need to count 00 11 22 case again, as if 00 11 22 did happen, then it's counted above as 11 != EMPTY
        if board[0][0] == board[1][0] == board[2][0] or board[0][0] == board[0][1] == board[0][2]:
            return board[0][0]
    if board[2][2] != EMPTY:
        if board[2][0] == board[2][1] == board[2][2] or board[0][2] == board[1][2] == board[2][2]:
            return board[2][2]
    # in cases 1, 2, 3 all 8 winning possibilities are counted. if program made it till here, then game is unfinished/draw
    return None


def terminal(board):

    # terminal state if game is won/ no more cells left to fill
    if winner(board) != None:
        return True
    for row in board:
        if row.count(EMPTY) != 0:
            return False
    return True


def utility(board):

    # it is given that input is a terminal board ie that terminal(board) is True. No need to check it.
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':  # here '' is req. board[a][b] returns element of a list in a ''
        return -1
    elif winner(board) == None:
        return 0


def minimax(board):

    if terminal(board):
        return None
    if player(board) == X:
        u = -2
        for action in actions(board):
            u = max(u, min_val(result(board, action)))
        for action in actions(board):
            if min_val(result(board, action)) == u:
                return action
    if player(board) == O:
        u = 2
        for action in actions(board):
            u = min(u, max_val(result(board, action)))
        for action in actions(board):
            if max_val(result(board, action)) == u:
                return action


def max_val(board):

    # find max over stuff X could play
    if terminal(board):
        return utility(board)
    u = -2
    for action in actions(board):
        u = max(u, min_val(result(board, action)))
    return u


def min_val(board):

    # find min over stuff O can play
    if terminal(board):
        return utility(board)
    u = 2
    for action in actions(board):
        u = min(u, max_val(result(board, action)))
    return u
