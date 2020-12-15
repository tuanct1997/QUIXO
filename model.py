import pygame
from eventmanager import *
import math
from constant import game_array, dis_to_cent,image_choice,image_xo,X_IMAGE,O_IMAGE,WHITE_IMAGE,PLACE
from copy import deepcopy
class GameEngine(object):
    """
    Tracks the game state.
    """

    draw = None
    mx = None
    my = None
    # dis_to_cent = 500//5//2
    x_turn = None
    board = [[(50, 50, 0), (150, 50, 0), (250, 50, 0), (350, 50, 0), (450, 50, 0)], [(50, 150, 0), (150, 150, 0), (250, 150, 0), (350, 150, 0), (450, 150, 0)], [(50, 250, 0), (150, 250, 0), (250, 250, 0), (350, 250, 0), (450, 250, 0)], [(50, 350, 0), (150, 350, 0), (250, 350, 0), (350, 350, 0), (450, 350, 0)], [(50, 450, 0), (150, 450, 0), (250, 450, 0), (350, 450, 0), (450, 450, 0)]]


    # o_turn = None
    

    def __init__(self, evManager,width, rows):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        
        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """
        
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False
        self.width = width
        self.rows = rows
        self.draw = 0
        self.mx = 0
        self.my = 0
        # self.game_array, self.dis_to_cent = self.grid()
        self.x_turn = True
        self.running = True
        self.click = True
        # self.o_turn = False

    # def create_board(self):
    # 	return [[0 for j in range(self.rows)] for i in range(self.rows)]

    def is_movable_tile(self,i, j):
        if i in [50,150,250,350,450] and (j == 50 or j == 450):
            return True
        elif (i == 50 or i == 450 ) and j in [50,150,250,350,450]:
            return True
        else:
            return False

    def is_placeable_tile(self,i, j,xstart,ystart):
        if xstart in [50,450] and ystart in [50,450]:
            if i in [50,450] and j in [50,450] and (i != xstart or j != ystart):
                return True
            else:
                return False
        else:
            return False

    # def have_won(self,game_array1):
    #     for x in range(len(game_array1)):
    #         for j in range(len(game_array1[x])):
    #             if
    #             pass
    #         pass

    def is_available(self,game_array1,mx,my, dis_to_cent):
        for i in range(len(game_array1)):
            for j in range(len(game_array1[i])):
                x,y,char = game_array1[i][j]
                print("THIS IS X {} and Y {} and CHAR {}".format(x,y,char))
                dis = math.sqrt((x-mx)**2 + (y-my) ** 2)
                if dis <= dis_to_cent:
                    print("LOL~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    if self.is_movable_tile(x,y):
                        if self.x_turn:
                            if char == 0 or char == 1:
                                return True,x,y
                        else:
                            if char == 0 or char == -1:
                                return True,x,y
                    # else:
                    #     print("This is {}".format(x))
        return False,x,y

    def update_col(self,game_array1,xstart,yend,ystart):
        print("BEFORE {}".format(game_array1))
        temp = deepcopy(game_array1)
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                print("this is DDDDD {}".format(d))
                x1,y1,char = game_array1[z][d]
                if d == 4:
                    print('mommmmmm')
                    print("y1 là {}".format(y1))
                    print("yend là {}".format(yend))
                if yend > ystart:
                    if x1 == xstart and y1 > ystart:
                        y1-= 100
                        temp[z][d] =(x1,y1,char)
                    elif x1 ==xstart and y1==ystart:
                        y1 += yend - ystart
                        print("y1 là {}".format(y1))
                        print("yend là {}".format(yend))
                        print("LOLL")
                        temp[z][d] = (x1,y1,char)
                elif yend < ystart:
                    if x1 == xstart and y1 < ystart:
                        y1 += 100
                        temp[z][d] =(x1,y1,char)
                    elif x1 ==xstart and y1 == ystart:
                        y1 -= ystart - yend
                        print("LOLL")
                        temp[z][d] = (x1,y1,char)
        game_array1 = deepcopy(temp)
        print("THIS SHITTTTTTT HAHAHAHA {}".format(game_array1))
        return game_array1

    def update_row(self,game_array1,ystart,xend,xstart):
        print("BEFORE {}".format(game_array1))
        temp = deepcopy(game_array1)
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                print("this is DDDDD {}".format(d))
                x1,y1,char = game_array1[z][d]
                if xend > xstart:
                    if y1 == ystart and x1 > xstart:
                        x1-= 100
                        temp[z][d] =(x1,y1,char)
                    elif y1 ==ystart and x1==xstart:
                        x1 += xend - xstart
                        print("y1 là {}".format(y1))
                        print("yend là {}".format(xend))
                        print("LOLL")
                        temp[z][d] = (x1,y1,char)
                elif xend < xstart:
                    if y1 == ystart and x1 < xstart:
                        x1 += 100
                        temp[z][d] =(x1,y1,char)
                    elif y1 ==ystart and x1 == xstart:
                        x1 -= xstart - xend
                        print("LOLL")
                        temp[z][d] = (x1,y1,char)
        game_array1 = deepcopy(temp)
        print("THIS SHITTTTTTT HAHAHAHA {}".format(game_array1))
        return game_array1

    def putxlist(self,game_array1,temp):
        xcheck,ycheck,char = temp
        print("DMCMMMM DAY LA CHAR {}".format(char))
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                x,y,char = game_array1[z][d]
                if xcheck == x and ycheck == y:
                    print('kkokokokokokokokoko')
                    game_array1[z][d] = (xcheck,ycheck,1)
                    return game_array1

    def putolist(self,game_array1,temp):
        xcheck,ycheck,char = temp
        print("DMCMMMM DAY LA CHAR {}".format(char))
        for z in range(len(game_array1)):
            for d in range(len(game_array1[z])):
                x,y,char = game_array1[z][d]
                if xcheck == x and ycheck == y:
                    game_array1[z][d] = (xcheck,ycheck,-1)
                    return game_array1

    def is_move(self,game_array,mx,my,dis_to_cent, xstart, ystart):
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x,y,char = game_array[i][j]
                dis = math.sqrt((x-mx)**2 + (y-my)**2)
                if dis<=dis_to_cent:
                    # ,xstart,ystart
                    if self.is_movable_tile(x,y):
                        if x == xstart:
                            GameEngine.board = self.update_col(GameEngine.board,xstart,y,ystart)
                            print(game_array)
                            print("eqoeioqweioqwieqoweiqwoeiqwoeiqwoeqwieoqwiqwoeiqooeiq")
                            print('=============================================================================')
                            if self.x_turn:
                                print("THIS IS TRUE game_array {}".format(GameEngine.board))
                                tempx= [x,y,1]
                                GameEngine.board = self.putxlist(GameEngine.board,tempx)
                                self.x_turn = False
                                print("THIS IS TRUE game_array {}".format(GameEngine.board))
                                return True,x,y
                            else:
                                print("THIS IS TRUE game_array {}".format(game_array))
                                tempx = [x,y,-1]
                                GameEngine.board = self.putolist(GameEngine.board,tempx)
                                print("THIS IS TRUE game_array {}".format(game_array))
                                self.x_turn = True
                                return True,x,y
                            
                        elif y == ystart:
                            print(game_array)
                            print('=============================================================================')
                            GameEngine.board = self.update_row(GameEngine.board,ystart,x,xstart)
                            if self.x_turn:
                                tempx= [x,y,1]
                                GameEngine.board = self.putxlist(GameEngine.board,tempx)
                                self.x_turn = False
                                return True,x,y
                            else:
                                tempx = (x,y,-1)
                                GameEngine.board = self.putolist(GameEngine.board,tempx)
                                self.x_turn = True
                                return True,x,y
        return False,x,y



    def notify(self, event):
        """
        Called by an event in the message queue. 
        """

        if isinstance(event,ClickEvent):
            m_x, m_y = event.clickpos
            print("FORMAT BOARD LA {}".format(GameEngine.board))
            is_a,x,y= self.is_available(GameEngine.board, m_x,m_y,dis_to_cent)
            print("THIS IS IS_A {}".format(is_a))
            if is_a:
                self.draw = -1
                self.mx = m_x
                self.my = m_y
                image_choice.append([x,y,WHITE_IMAGE])
            else:
                print('Choose again111111')

        if isinstance(event,PlaceEvent):
            if len(image_choice)>0:

                xstart,ystart,path = image_choice[0]
                image_choice.clear()
                m_x,m_y = event.clickpos
                print('PLACE EVENT {}'.format(m_x))
                print("PLACE EVENT 2---{}".format(m_y))
                is_place , x , y = self.is_move(game_array,m_x,m_y,dis_to_cent,xstart,ystart)
                # game_array = GameEngine.board
                if is_place:
                    self.draw = 1
                    self.mx = m_x
                    self.my = m_y
                    image_xo.clear()
                    print("GAME ENGINE {}".format(GameEngine.board))
                    for i in range(len(GameEngine.board)):
                        for j in range(len(GameEngine.board[i])):
                            x,y,char = GameEngine.board[i][j]
                            if char == 1:
                                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                image_xo.append([x,y,X_IMAGE])
                            elif char == -1:
                                print("~~~~~~~~~~~~~~~~~~~~oooo~~~~~~~~~~~~~~~~~~")
                                image_xo.append([x,y,O_IMAGE])
 
            else:
                print('Choose again')


        if isinstance(event,InputEvent):
        	pass

        if isinstance(event, QuitEvent):
            self.running = False

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
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
                self.draw = 0                






