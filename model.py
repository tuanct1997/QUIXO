import pygame
from eventmanager import *
import math
from constant import game_array, dis_to_cent, image_choice, image_xo, X_IMAGE, O_IMAGE, WHITE_IMAGE, PLACE
from copy import deepcopy
import threading
from multiprocessing import Queue

#ThreadPool Pattern
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        process_data(self.name, self.q)

    def process_data(threadName, q):
       while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
            else:
                queueLock.release()
            time.sleep(1)


# AI CLASS BUT NOT WORKING
class AIPlayer(object):
    def __init__(self, char):
        super().__init__(char)

    def get_move(self, game):
        if len(game.available_moves()) == 25:
            square = random.choice(GameEngine.is_movable_tile())
        else:
            square = self.minmax(game, self.char)['position']
        return square

    def minmax(self, state, player):
        max_player = self.char  # yourself
        other_player = -1 if player == 1 else 1

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minmax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class GameEngine(object):
    """
    Tracks the game state.
    """

    draw = None
    mx = None
    my = None
    # dis_to_cent = 500//5//2
    x_turn = None
    board = [[(50, 50, 0), (150, 50, 0), (250, 50, 0), (350, 50, 0), (450, 50, 0)],
             [(50, 150, 0), (150, 150, 0), (250, 150, 0), (350, 150, 0), (450, 150, 0)],
             [(50, 250, 0), (150, 250, 0), (250, 250, 0), (350, 250, 0), (450, 250, 0)],
             [(50, 350, 0), (150, 350, 0), (250, 350, 0), (350, 350, 0), (450, 350, 0)],
             [(50, 450, 0), (150, 450, 0), (250, 450, 0), (350, 450, 0), (450, 450, 0)]]
    map_check = deepcopy(game_array)


    def __init__(self, evManager, width, rows):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        
        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().

        width, rows (int) : self define size of screen
        draw (int) : Default = 0 do nothing.-1 if that is first choose, 
        1 if that is place action and 2 if that is Gameover

        mx,my (int) : coordinate of mouse
        x_turn (bool) : define which turn is play
        click
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False
        self.width = width
        self.rows = rows
        self.draw = 0
        self.mx = 0
        self.my = 0
        self.x_turn = True
        self.running = True


    # Check if first move is valid ( first choose piece move)
    def is_movable_tile(self, i, j):
        if i in [50, 150, 250, 350, 450] and (j == 50 or j == 450):
            return True
        elif (i == 50 or i == 450) and j in [50, 150, 250, 350, 450]:
            return True
        else:
            return False

    # Check if second move is valid ( if the postion to place is valid )
    def is_placeable_tile(self, i, j, xstart, ystart):
        if xstart == 50 or xstart == 450:
            if (i == xstart) and (j == 50 or j == 450):
                return True
            elif abs(xstart - i) == 400 and j == ystart:
                return True
            else:
                return False
        elif ystart == 50 or ystart == 450:
            if j == ystart and (i == 50 or i == 450):
                return True
            elif abs(ystart - j) == 400 and i == xstart:
                return True
            else:
                return False
        else:
            return False

    """
    A Map has form in a 3D list : [[()]]
    To store the UI of Pygame in true coordiantion from row -> row , col -> col
    Update_map each time we make a move in order to keep track if there is a winner
    """
    def update_map(self, xu, yu, charu, mapx):
        temp = deepcopy(mapx)
        for i in range(len(mapx)):
            for j in range(len(mapx[i])):
                x, y, char = mapx[i][j]
                if x == xu and y == yu:
                    temp[i][j] = (x, y, charu)

        mapx = temp
        return mapx


    # Check if there is a winner -> return bool
    def has_won(self, game_array):
        # Checking rows

        for row in range(len(game_array)):
            if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2] == game_array[row][3][2] ==
                game_array[row][4][2]) and game_array[row][0][2] != 0:
                return True

        # Checking columns
        for col in range(len(game_array)):
            if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2] == game_array[3][col][2] ==
                game_array[4][col][2]) and game_array[0][col][2] != 0:
                return True

        # Checking main diagonal
        if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2] == game_array[3][3][2] ==
            game_array[4][4][2]) and game_array[0][0][2] != 0:
            return True

        # Checking reverse diagonal
        if (game_array[0][4][2] == game_array[1][3][2] == game_array[2][2][2] == game_array[3][1][2] ==
            game_array[4][0][2]) and game_array[0][4][2] != 0:
            return True

        return False

    # Check which box in UI is choose by user in first move
    def is_available(self, game_array1, mx, my, dis_to_cent):
        for i in range(len(game_array1)):
            for j in range(len(game_array1[i])):
                x, y, char = game_array1[i][j]
                dis = math.sqrt((x - mx) ** 2 + (y - my) ** 2)
                if dis <= dis_to_cent:
                    if self.is_movable_tile(x, y):
                        if self.x_turn:
                            if char == 0 or char == 1:
                                return True, x, y
                        else:
                            if char == 0 or char == -1:
                                return True, x, y

        return False, x, y

    # Update by column after we place the piece inside board => column will have change the position of each piece
    """
    For example [1                  [2
                 2                   3
                 3                   4
                 4                   5
                 5] -> new will be   1] This will change the order of board ( but not the map inorder to keep track Pygame)
                 Also we check condition between yend and ystart because sometime they pick from the middle
                 => half of the col will be update and the other not
    """
    def update_col(self, game_array1, xstart, yend, ystart):
        temp = deepcopy(game_array1)
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                x1, y1, char = game_array1[z][d]

                if yend > ystart:
                    if x1 == xstart and y1 > ystart:
                        y1 -= 100
                        temp[z][d] = (x1, y1, char)

                    elif x1 == xstart and y1 == ystart:
                        y1 += yend - ystart

                        temp[z][d] = (x1, y1, char)
                elif yend < ystart:
                    if x1 == xstart and y1 < ystart:
                        y1 += 100
                        temp[z][d] = (x1, y1, char)
                    elif x1 == xstart and y1 == ystart:
                        y1 -= ystart - yend
                        temp[z][d] = (x1, y1, char)
        game_array1 = deepcopy(temp)
        return game_array1


    # Update by row after we place the piece inside board => column will have change the position of each piece
    # Same explaination with update column above
    def update_row(self, game_array1, ystart, xend, xstart):
        temp = deepcopy(game_array1)
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                x1, y1, char = game_array1[z][d]
                if xend > xstart:
                    if y1 == ystart and x1 > xstart:
                        x1 -= 100
                        temp[z][d] = (x1, y1, char)
                    elif y1 == ystart and x1 == xstart:
                        x1 += xend - xstart
                        temp[z][d] = (x1, y1, char)
                elif xend < xstart:
                    if y1 == ystart and x1 < xstart:
                        x1 += 100
                        temp[z][d] = (x1, y1, char)
                    elif y1 == ystart and x1 == xstart:
                        x1 -= xstart - xend
                        temp[z][d] = (x1, y1, char)
        game_array1 = deepcopy(temp)
        return game_array1

    # Update X character into the board
    def putxlist(self, game_array1, temp):
        xcheck, ycheck, char = temp
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                x, y, char = game_array1[z][d]
                if xcheck == x and ycheck == y:
                    game_array1[z][d] = (xcheck, ycheck, 1)
                    return game_array1

    # Update O character into the board
    def putolist(self, game_array1, temp):
        xcheck, ycheck, char = temp
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                x, y, char = game_array1[z][d]
                if xcheck == x and ycheck == y:
                    game_array1[z][d] = (xcheck, ycheck, -1)
                    return game_array1

    # Check which box in UI is choose by user in second move
    def is_move(self, game_array, mx, my, dis_to_cent, xstart, ystart):
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x, y, char = game_array[i][j]
                dis = math.sqrt((x - mx) ** 2 + (y - my) ** 2)
                if dis <= dis_to_cent:
                    # compare the second cordinate of mouse with first one and see if valid
                    if self.is_movable_tile(x, y) and self.is_placeable_tile(x, y, xstart, ystart):
                        if x == xstart:
                            GameEngine.board = self.update_col(GameEngine.board, xstart, y, ystart)
                            if self.x_turn:
                                tempx = [x, y, 1]
                                GameEngine.board = self.putxlist(GameEngine.board, tempx)
                                self.x_turn = False
                                return True, x, y
                            else:
                                tempx = [x, y, -1]
                                GameEngine.board = self.putolist(GameEngine.board, tempx)
                                self.x_turn = True
                                return True, x, y

                        elif y == ystart:
                            GameEngine.board = self.update_row(GameEngine.board, ystart, x, xstart)
                            if self.x_turn:
                                tempx = [x, y, 1]
                                GameEngine.board = self.putxlist(GameEngine.board, tempx)
                                self.x_turn = False
                                return True, x, y
                            else:
                                tempx = (x, y, -1)
                                GameEngine.board = self.putolist(GameEngine.board, tempx)
                                self.x_turn = True
                                return True, x, y
        return False, x, y

    # Called by an event in the Observer Pattern
    # Check what event currently and doing the order
    def notify(self, event):

        if isinstance(event, ClickEvent):
            m_x, m_y = event.clickpos
            is_a, x, y = self.is_available(GameEngine.board, m_x, m_y, dis_to_cent)
            if is_a:
                self.draw = -1
                self.mx = m_x
                self.my = m_y
                image_choice.append([x, y, WHITE_IMAGE])
            else:
                print('Choose again')

        if isinstance(event, PlaceEvent):
            if len(image_choice) > 0:

                xstart, ystart, path = image_choice[0]
                image_choice.clear()
                m_x, m_y = event.clickpos
                is_place, x, y = self.is_move(game_array, m_x, m_y, dis_to_cent, xstart, ystart)
                # game_array = GameEngine.board
                if is_place:
                    self.draw = 1
                    self.mx = m_x
                    self.my = m_y
                    image_xo.clear()
                    # self.map_check = deepcopy(game_array)
                    for i in range(len(GameEngine.board)):
                        for j in range(len(GameEngine.board[i])):
                            x, y, char = GameEngine.board[i][j]
                            if char == 1:
                                self.map_check = self.update_map(x, y, char, self.map_check)
                                image_xo.append([x, y, X_IMAGE])
                            elif char == -1:
                                self.map_check = self.update_map(x, y, char, self.map_check)
                                image_xo.append([x, y, O_IMAGE])

            else:
                print('Choose again')

        if isinstance(event, InputEvent):
            pass

        if isinstance(event, QuitEvent):
            self.running = False

    """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop in order to keep the UI frame.
        The loop ends when this object hears a QuitEvent in notify().
        Each time we check if there is a signal to draw
        """
    def run(self):
        
        self.running = True
        self.evManager.Post(InitializeEvent())
        while self.running:
            newTick = TickEvent()
            self.evManager.Post(newTick)
            if self.draw == -1:
                self.evManager.Post(DrawBlankEvent(image_choice))
                self.draw = 0
            if self.draw == 1:
                self.evManager.Post(DrawBlankEvent(image_xo))
                if self.has_won(self.map_check):
                    self.draw = 2
                else:
                    self.draw = 0
            if self.draw == 2:
                self.evManager.Post(DrawWinEvent())
