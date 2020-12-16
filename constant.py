import pygame

width = 500
rows = 5
image_choice = []
image_xo = []
PLACE = 0

X_IMAGE = pygame.image.load("Images/x.png")
X_IMAGE = pygame.transform.scale(X_IMAGE, (500 // 5 // 2, 500 // 5 // 2))
O_IMAGE = pygame.image.load("Images/o.png")
O_IMAGE = pygame.transform.scale(O_IMAGE, (500 // 5 // 2, 500 // 5 // 2))
WHITE_IMAGE = pygame.image.load("Images/white1.jpg")
WHITE_IMAGE = pygame.transform.scale(WHITE_IMAGE, (500 // 5, 500 // 5))

dis_to_cent = width // rows // 2
game_array = [[(50, 50, 0), (150, 50, 0), (250, 50, 0), (350, 50, 0), (450, 50, 0)],
              [(50, 150, 0), (150, 150, 0), (250, 150, 0), (350, 150, 0), (450, 150, 0)],
              [(50, 250, 0), (150, 250, 0), (250, 250, 0), (350, 250, 0), (450, 250, 0)],
              [(50, 350, 0), (150, 350, 0), (250, 350, 0), (350, 350, 0), (450, 350, 0)],
              [(50, 450, 0), (150, 450, 0), (250, 450, 0), (350, 450, 0), (450, 450, 0)]]
