import pygame
from random import choice
from copy import copy

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


def getNextShape():
    return Shape(5, 0, choice(shapes))


def drawShape(surface, shape):
    pass


def drawGame(surface, grid, width, height):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('\'comicsans\'', 60)
    label = font.render('\'TETRIS\'', 1, (255, 255, 255))
    surface.blit(label, (width + grid.width / 2 - (label.get_width() / 2), 30))

    pygame.draw.rect(surface, (255, 0, 0), (width, height, grid.width, grid.height))
    pygame.display.update()


def gameOver(grid):
    pass


def displayNextShape(shape, surface):
    pass
# function to display the next shape on the side


class Grid(object):
    def __init__(self, occupied={}):
        self.rows = 20
        self.columns = 10
        self.width = 0
        self.height = 0
        self.grid = [[[0, 0, 0] for x in range(self.columns)] for x in range(self.rows)]
        self.occupied = occupied

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in occupied:
                    block = occupied[(j, i)]
                    self.grid[i][j] = block

    def getGrid(self):
        return self.grid

    def isOccupied(self, x, y):
        if (x, y) in self.occupied:
            return True
        return False

    def drawGrid(self, surface, width, height):
        pass

    def clearLine(self):
        pass
    # clear the line, move all occupied blocks above down one y position


def validMove(grid, x, y):
    return (x, y) in grid.occupied


class Tetris(object):
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.window = pygame.display.set_mode((self.width, self.height))
        self.grid = Grid()
        self.cell = 10
        self.currentShape = getNextShape()
        self.nextShape = getNextShape()
        self.difficulty = 1
        self.clock = pygame.time.Clock()

    def run(self):
        run = True
        pygame.init()
        pygame.display.set_caption('Tetris by Callum Ke')

        while run:
            self.grid.drawGrid(self.window, self.width, self.height)
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and validMove(self.grid, self.currentShape.x - 1, self.currentShape.y):
                self.currentShape.x -= 1

            if keys[pygame.K_RIGHT] and validMove(self.grid, self.currentShape.x - 1, self.currentShape.y):
                self.currentShape.x += 1

            if keys[pygame.K_UP]:
                temp = copy(self.currentShape)
                temp.changeRotation()
                if validMove(self.grid, temp.x, temp.y):
                    self.currentShape.changeRotation()

            if keys[pygame.K_DOWN] and validMove(self.grid, self.currentShape.x, self.currentShape.y + 1):
                self.currentShape.y += 1

            drawGame(self.window, self.grid, self.width, self.height)

        pygame.quit()


def main():
    applet = Tetris()
    applet.run()


if __name__ == '__main__':
    main()
