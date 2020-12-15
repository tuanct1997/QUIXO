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
    board = deepcopy(game_array)

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

    def create_board(self):
    	return [[0 for j in range(self.rows)] for i in range(self.rows)]

    def is_movable_tile(self,i, j):
        if i in range(1,self.rows-1) and (j == 0 or j == self.rows-1):
            return True
        elif (i == 0 or i == self.rows-1 ) and j in range(0,self.rows):
            return True
        else:
            return False

    def get_possibles_destinations(board, x, y):
	    destinations = []

	    if x == 0 or x == self.rows-1:
	        if y != 0:
	            destinations.append((x, 0))
	        if y != self.rows-1:
	            destinations.append((x, self.rows-1))
	        opposite = 0 if x == self.rows-1 else self.rows-1
	        destinations.append((opposite, y))

	    if (y == 0 or y == self.rows-1) and (x != 0 and x != self.rows-1):
	        if x != 0:
	            destinations.append((0, y))
	        if x != self.rows-1:
	            destinations.append((self.rows-1, y))
	        opposite = 0 if y == self.rows-1 else self.rows-1
	        destinations.append((x, opposite))

	    return destinations

    def grid(self):
        dis_to_cent = self.width // self.rows // 2
        game_array = []
        array_temp = []
        for i in range(self.rows):
            for j in range(self.rows):
            	x = dis_to_cent*(2*j+1)
            	y = dis_to_cent*(2*i+1)

            	array_temp.append((x,y,"",True))
            game_array.append(array_temp)
            array_temp = []

        return game_array, dis_to_cent

    def is_available(self,game_array,mx,my, dis_to_cent):
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x,y,char = game_array[i][j]
                dis = math.sqrt((x-mx)**2 + (y-my) ** 2)
                if dis <= dis_to_cent:
                    if self.is_movable_tile(i,j):
                        if self.x_turn:
                            if char == 0 or char == 1:
                                game_array[i][j] = (x,y,0)
                                return True,x,y
                        else:
                            if char == 0 or char == -1:
                                game_array[i][j] = (x,y,0)
                                return True,x,y
                    # else:
                    #     print("This is {}".format(x))
        return False,x,y

    def update_col(self,game_array,xstart):
        print("BEFORE {}".format(game_array))
        temp = deepcopy(game_array)
        for z in range(len(game_array)):
            for d in range(len(game_array[z])):
                print("this is DDDDD {}".format(d))
                x1,y1,char = game_array[z][d]
                if d == 4:
                    print('mommmmmm')
                if x1 == xstart and d!=4:
                    y1+= 100
                    temp[z][d] =(x1,y1,char)
                elif x1 ==xstart and d==4:
                    y1 -=400
                    print("LOLL")
                    temp[z][d] = (x1,y1,char)
        game_array = temp
        print(game_array)

    def update_row(self,game_array,ystart):
        temp = deepcopy(game_array)
        for z in range(len(game_array)):
            for d in range(len(game_array[z])):
                x1,y1,char = game_array[z][d]
                if y1 == ystart and z!=4:
                    x1+= 100
                    temp[z][d] =(x1,y1,char)
                elif y1 ==ystart and z==4:
                    x1 -=400
                    temp[z][d] =(x1,y1,char)
        game_array = temp

    def putxlist(self,game_array,temp):
        xcheck,ycheck,char = temp
        print("DMCMMMM DAY LA CHAR {}".format(char))
        for z in range(len(game_array)):
            for d in range(len(game_array[z])):
                x,y,char = game_array[z][d]
                if xcheck == x and ycheck == y:
                    print('kkokokokokokokokoko')
                    game_array[z][d] = (xcheck,ycheck,1)
                    return
    def putolist(self,game_array,temp):
        xcheck,ycheck,char = temp
        print("DMCMMMM DAY LA CHAR {}".format(char))
        for z in range(len(game_array)):
            for d in range(len(game_array[z])):
                x,y,char = game_array[z][d]
                if xcheck == x and ycheck == y:
                    game_array[z][d] = (xcheck,ycheck,-1)
                    return

    def is_move(self,game_array,mx,my,dis_to_cent, xstart, ystart):
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x,y,char = game_array[i][j]
                dis = math.sqrt((x-mx)**2 + (y-my)**2)
                if dis<=dis_to_cent:
                    
                    if self.is_movable_tile(i,j):
                        if x == xstart:
                            self.update_col(game_array,xstart)
                            print(game_array)
                            print('=============================================================================')
                            if self.x_turn:
                                tempx= [x,y,1]
                                self.putxlist(game_array,tempx)
                                self.x_turn = False
                                print("THIS IS TRUE game_array {}".format(game_array))
                                return True,x,y
                            else:
                                tempx = [x,y,-1]
                                self.putolist(game_array,tempx)
                                print("THIS IS TRUE game_array {}".format(game_array))
                                self.x_turn = True
                                return True,x,y
                            
                        elif y == ystart:
                            print(game_array)
                            print('=============================================================================')
                            self.update_row(game_array,ystart)
                            if self.x_turn:
                                game_array[i][j] = (x,y,1)
                                return True,x,y
                            else:
                                game_array[i][j] = (x,y,-1)
                                return True,x,y
        return False,x,y



    def notify(self, event):
        """
        Called by an event in the message queue. 
        """

        if isinstance(event,ClickEvent):
            m_x, m_y = event.clickpos
            print("========{}=========".format(m_x))
            print("========{}=========".format(m_y))
            print("this is game_array{}".format(game_array))
            is_a,x,y= self.is_available(game_array, m_x,m_y,dis_to_cent)
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
                if is_place:
                    self.draw = 1
                    self.mx = m_x
                    self.my = m_y
                    image_xo.clear()
                    for i in range(len(game_array)):
                        for j in range(len(game_array[i])):
                            x,y,char = game_array[i][j]
                            if char == 1:
                                image_xo.append([x,y,X_IMAGE])
                            elif char == -1:
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






