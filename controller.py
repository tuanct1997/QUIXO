import pygame
import model
from eventmanager import *


class Controller(object):
    """
    Handles keyboard input.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): push messages to the event queue in Observer pattern.
        model (GameEngine): Game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.evManager.Post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.evManager.Post(QuitEvent())
                    else:
                        # post any other keys to the message queue for everyone else to see
                        self.evManager.Post(InputEvent(event.unicode, None))
                # cCheck Mouse button for first move
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.evManager.Post(ClickEvent(event, pygame.mouse.get_pos()))

                # Check release Mouse button for second move
                if event.type == pygame.MOUSEBUTTONUP:
                    self.evManager.Post(PlaceEvent(event, pygame.mouse.get_pos()))
