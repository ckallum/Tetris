import pygame
from random import choice

dimensions = {'blockSize': 20, 'winHeight': 900, 'winWidth': 600, 'rows': 16, 'cols': 8}

S1 = [['.....',
       '......',
       '..00..',
       '.00...',
       '.....'],
      ['.....',
       '..0..',
       '..00.',
       '...0.',
       '.....']]

S2 = [['.....',
       '.....',
       '.00..',
       '..00.',
       '.....'],
      ['.....',
       '..0..',
       '.00..',
       '.0...',
       '.....']]

S3 = [['..0..',
       '..0..',
       '..0..',
       '..0..',
       '.....'],
      ['.....',
       '0000.',
       '.....',
       '.....',
       '.....']]

S4 = [['.....',
       '.....',
       '.00..',
       '.00..',
       '.....']]

S5 = [['.....',
       '.0...',
       '.000.',
       '.....',
       '.....'],
      ['.....',
       '..00.',
       '..0..',
       '..0..',
       '.....'],
      ['.....',
       '.....',
       '.000.',
       '...0.',
       '.....'],
      ['.....',
       '..0..',
       '..0..',
       '.00..',
       '.....']]

S6 = [['.....',
       '...0.',
       '.000.',
       '.....',
       '.....'],
      ['.....',
       '..0..',
       '..0..',
       '..00.',
       '.....'],
      ['.....',
       '.....',
       '.000.',
       '.0...',
       '.....'],
      ['.....',
       '.00..',
       '..0..',
       '..0..',
       '.....']]

S7 = [['.....',
       '..0..',
       '.000.',
       '.....',
       '.....'],
      ['.....',
       '..0..',
       '..00.',
       '..0..',
       '.....'],
      ['.....',
       '.....',
       '.000.',
       '..0..',
       '.....'],
      ['.....',
       '..0..',
       '.00..',
       '..0..',
       '.....']]

shapes = [S1, S2, S3, S4, S5, S6, S7]
colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Shape(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.colour = colours[shapes.index(shape)]
        self.rotation = 0
        self.size = len(shape)

    def changeRotation(self):
        self.rotation = (self.rotation + 1) % self.size

    def getShape(self):
        return self.shape


def collision(shape, grid, occupied):
    pass


def clearLine(grid, occupied):
    pass


def getNextShape(current):
    possible = list(filter(lambda x: x != current.getShape(), shapes))
    return choice(possible)


def drawShape(surface, shape):
    pass


def createGrid(occupied={}):
    pass


def drawGame(surface, rows, cols):
    pass


def gameOver(grid):
    pass


def drawNextShape(shape, surface):
    pass


class Tetris(object):
    def __init__(self):
        self.width = 600
        self.height = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        self.grid = ''
        self.cell = 10
        self.posX = 0
        self.posY = self.height - self.cell
        self.vel = 10
        self.currentShape = Shape(0, 0, choice(shapes))
        self.nextShape = getNextShape(self.currentShape)
        self.difficulty = 1

    def run(self):
        run = True
        pygame.init()
        pygame.display.set_caption('Tetris')

        while run:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.posX > 1:
                self.posX -= self.vel

            if keys[pygame.K_RIGHT] and self.posX < self.width - self.cell:
                self.posX += self.vel

            if keys[pygame.K_UP]:
                self.currentShape = self.nextShape
                self.nextShape = getNextShape(self.currentShape)

            if keys[pygame.K_DOWN] and self.posY < self.height - self.cell:
                self.posY += self.vel

            self.window.fill((0, 0, 0))
            pygame.draw.rect(self.window, (255, 0, 0), (self.posX, self.posY, self.cell, self.cell))
            pygame.display.update()

        pygame.quit()


def main():
    applet = Tetris()
    applet.run()


if __name__ == '__main__':
    main()
