import pygame
import model
from eventmanager import *

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
                
        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, InitializeEvent):
            self.initialize(self.model.width, self.model.rows)
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()

        elif isinstance(event, TickEvent):
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

        elif isinstance(event, DrawBlankEvent):
            self.drawblank(event.ls)

        elif isinstance(event, DrawWinEvent):
            self.drawwin()

    #function create message when there is a winner
    def drawwin(self):
        somewords = self.smallfont.render(
            'GAME OVER',
            True,
            (0, 255, 0))
        self.screen.blit(somewords, (250, 250))
        pygame.display.update()

    #Function to draw animation on the board
    def drawblank(self, ls):
        self.screen.fill((0, 0, 0))
        print('this is ls {}'.format(ls))
        self.draw_line()
        for image in ls:
            x, y, IMAGE = image
            self.screen.blit(IMAGE, (x - (500 // 5 // 2), y - (500 // 5 // 2)))
        pygame.display.update()

    # Function to create line on the board
    def draw_line(self):
        gap = 500 // 5
        x = 0
        y = 0
        for i in range(5):
            x = i * gap
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, 500), 5)
            pygame.draw.line(self.screen, GRAY, (0, x), (500, x), 5)
        pygame.display.update()

    # Initialize the screen
    def initialize(self, c, r):

        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((c, c))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
        self.screen.fill((0, 0, 0))

        gap = c // r

        x = 0
        y = 0

        for i in range(r):
            x = i * gap
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, c), r)
            pygame.draw.line(self.screen, GRAY, (0, x), (c, x), r)

        pygame.display.update()
