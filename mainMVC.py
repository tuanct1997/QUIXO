import eventmanager
import model
import view
import controller
from copy import deepcopy
# Screen
WIDTH = 500
ROWS = 5
INDEX_LAST_ROW = ROWS - 1
INDEX_LAST_COL = ROWS - 1

def run():
    evManager = eventmanager.EventManager()
    gamemodel = model.GameEngine(evManager,WIDTH,ROWS)
    keyboard = controller.Keyboard(evManager, gamemodel)
    graphics = view.GraphicalView(evManager, gamemodel)
    gamemodel.run()

def is_movable_tile(x, y):
    return x == 0 or y == 0 or x == N_ROWS - 1 or y == N_COLS - 1
def get_possibles_destinations(board, x, y):
    destinations = []

    if x == 0 or x == INDEX_LAST_ROW:
        if y != 0:
            destinations.append((x, 0))
        if y != INDEX_LAST_COL:
            destinations.append((x, INDEX_LAST_COL))
        opposite = 0 if x == INDEX_LAST_ROW else INDEX_LAST_ROW
        destinations.append((opposite, y))

    if (y == 0 or y == INDEX_LAST_COL) and (x != 0 and x != INDEX_LAST_ROW):
        if x != 0:
            destinations.append((0, y))
        if x != INDEX_LAST_ROW:
            destinations.append((INDEX_LAST_COL, y))
        opposite = 0 if y == INDEX_LAST_COL else INDEX_LAST_COL
        destinations.append((x, opposite))

    return destinations

def move_col(board, line, x_start, x_end, value):
    board_copy = deepcopy(board)

    step = -1 if x_end > x_start else 1
    index_start = x_start - 1 if x_end > x_start else x_start + 1
    for x in range(x_end, index_start, step):
        prev_val = board_copy[x][line]
        board_copy[x][line] = value
        value = prev_val

    return board_copy



if __name__ == '__main__':
    run()
    # N_ROWS =5 
    # N_COLS = 5
    # # ls = [[0 for j in range(N_COLS)] for i in range(N_ROWS)]
    # ls = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
    # movable = []
    # for x in range(len(ls)):
    #     for y in range(len(ls[x])):
    #         value = ls[x][y]
    #         if is_movable_tile(x, y) and (value == 0 ):
    #             movable.append((x, y))
    # print('-------------------')

    # print(movable)
    # movables_choices = list(range(1, len(movable) + 1))
    # destinations = get_possibles_destinations(ls, 3, 0)
    # ls_cp = deepcopy(ls)
    # board = move_col(ls_cp, 3, 3, 4, value)

    # print('-------------------')
    # print(movables_choices)
    # print('-------------------')

    # print(board)