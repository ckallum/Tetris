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

    def getShapeCoordinates(self):
        pic = self.shape[self.rotation]
        coordinates = []
        for i, line in enumerate(pic):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    coordinates.append((self.x + j, self.y + i))

        return coordinates

    def drawShape(self, surface, shape):
        pass


class Grid(object):
    def __init__(self):
        self.rows = 20
        self.columns = 10
        self.width = 300
        self.height = 600
        self.grid = [[[0, 0, 0] for _ in range(self.columns)] for _ in range(self.rows)]
        self.occupied = []
        self.cell = 30

    def isOccupied(self, x, y):
        if (x, y) in self.occupied:
            return True
        return False

    def addOccupied(self, x, y):
        self.occupied.append((x, y))

    def drawGrid(self, surface, originX, originY):
        sx = originX
        sy = originY

        for i in range(len(self.grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx, sy + (i * self.cell)),
                             (sx + self.width, sy + (i * self.cell)))
            for j in range(len(self.grid[i]) + 1):
                pygame.draw.line(surface, (128, 128, 128), (sx + j * self.cell, sy),
                                 (sx + j * self.cell, sy + self.height))

    def drawShapes(self, surface, originX, originY):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(surface, self.grid[i][j],
                                 ((originX + j * self.cell), (originY + j * self.cell), self.cell, self.cell))

    def fillGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.occupied:
                    block = self.occupied[self.occupied.index((j, i))]
                    self.grid[i][j] = block

    def clearLine(self):
        pass
    # clear the line, move all occupied blocks above down one y position


def getNextShape():
    return Shape(5, 0, choice(shapes))


def drawLabel(surface, grid, originX, originY):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('\'comicsans\'', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (originX + grid.width / 2 - (label.get_width() / 2), 30))


def update():
    pygame.display.update()


def gameOver(grid):
    pass


def displayNextShape(shape, surface):
    pass


# function to display the next shape on the side


def validMove(grid, x, y):
    return not ((x, y) in grid.occupied)


def gameLost(coordinates):
    for coord in coordinates:
        x, y = coord
        if y < 1:
            return True
    return False


def drawTest(surface):
    s = Shape(10, 20, S7)
    coords = s.getShapeCoordinates()
    print(coords)
    for j, i in enumerate(coords):
        (x, y) = i
        pygame.draw.rect(surface, s.colour, (x*30,
                                             y*30, 30, 30))


class Tetris(object):
    def __init__(self):
        self.width = 800
        self.height = 700
        self.window = pygame.display.set_mode((self.width, self.height))
        self.grid = Grid()
        self.gridOriginX = (self.width - self.grid.width) // 2
        self.gridOriginY = (self.height - self.grid.height)
        self.currentShape = getNextShape()
        self.nextShape = getNextShape()
        self.difficulty = 1
        self.clock = pygame.time.Clock()
        self.speed = 0.2

    def run(self):
        run = True
        pygame.init()
        pygame.display.set_caption('Tetris by Callum Ke')

        while run:
            drawLabel(self.window, self.grid, self.gridOriginX, self.gridOriginY)
            self.grid.drawGrid(self.window, self.gridOriginX, self.gridOriginY)
            self.grid.fillGrid()

            drawTest(self.window)
            pygame.time.delay(100)
            fallTime = self.clock.get_rawtime()
            self.clock.tick()

            if fallTime / 1000 >= self.speed:
                fallTime = 0
                self.currentShape.y += 1
                if not (validMove(self.grid, self.currentShape.x, self.currentShape.y)):
                    self.currentShape.y -= 1
                    self.currentShape = self.nextShape
                    self.nextShape = getNextShape()

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

            self.grid.drawShapes(self.window, self.gridOriginX, self.gridOriginY)
            update()

        pygame.quit()


def main():
    applet = Tetris()
    applet.run()


if __name__ == '__main__':
    main()
