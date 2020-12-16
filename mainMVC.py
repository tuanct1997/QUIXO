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
    gamemodel = model.GameEngine(evManager, WIDTH, ROWS)
    keyboard = controller.Controller(evManager, gamemodel)
    graphics = view.GraphicalView(evManager, gamemodel)
    gamemodel.run()


if __name__ == '__main__':
    run()
