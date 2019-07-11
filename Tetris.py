import pygame
from collections import deque
from random import choice
from copy import copy

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

    def getShapeCoordinates(self):
        pic = self.shape[self.rotation % self.size]
        coordinates = []
        for i, line in enumerate(pic):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    coordinates.append((self.x + j, self.y + i))

        for i, coord in enumerate(coordinates):
            coordinates[i] = (coord[0] - 2, coord[1] - 4)

        return coordinates

    def drawNextShape(self, surface, gridOriginX, gridOriginY, windowWidth, windowHeight):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))
        x = gridOriginX + windowWidth + 50
        y = gridOriginY + windowHeight / 2 - 100
        pic = self.shape[self.rotation % self.size]
        pygame.draw.rect(surface, (0, 0, 0), (x, y, 200, 150), 0)

        for i, line in enumerate(pic):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, self.colour, (x + j * 30, y + i * 30, 30, 30), 0)
        surface.blit(label, (x + 10, y - 30))


class Grid(object):
    def __init__(self):
        self.rows = 20
        self.columns = 10
        self.width = 300
        self.height = 600
        self.grid = [[(0, 0, 0) for _ in range(self.columns)] for _ in range(self.rows)]
        self.occupied = {}
        self.cell = 30

    def isValidSpace(self, coords):
        validSpaces = [(j, i) for j in range(self.columns) for i in range(self.rows) if self.grid[i][j] == (0, 0, 0)]
        for coord in coords:
            if coord not in validSpaces:
                if coord[1] > -1:
                    return False
        return True

    def addOccupied(self, shape):
        for coord in shape.getShapeCoordinates():
            x, y = coord
            self.occupied[(x, y)] = shape.colour

    def drawGrid(self, surface, originX, originY):
        sx = originX
        sy = originY

        for i in range(len(self.grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx, sy + (i * self.cell)),
                             (sx + self.width, sy + (i * self.cell)))
            for j in range(len(self.grid[i]) + 1):
                pygame.draw.line(surface, (128, 128, 128), (sx + j * self.cell, sy),
                                 (sx + j * self.cell, sy + self.height))

    def drawShapesInGrid(self, surface, originX, originY):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                pygame.draw.rect(surface, self.grid[row][col],
                                 (originX + col * self.cell, originY + row * self.cell, self.cell, self.cell), 0)

    def fillGrid(self):
        self.grid = [[(0, 0, 0) for _ in range(self.columns)] for _ in range(self.rows)]
        for coord in self.occupied:
            col, row = coord
            self.grid[row][col] = self.occupied[coord]

    def clearLine(self):
        # Queue for which rows that were deleted first -> filled first
        rowsDeleted = deque()
        for y in range(len(self.grid)):
            row = self.grid[y]
            if (0, 0, 0) not in row:
                rowsDeleted.appendleft(y)
                for x in range(len(row)):
                    try:
                        del self.occupied[(x, y)]
                    except:
                        continue
        increment = len(rowsDeleted)
        if increment > 0:
            while rowsDeleted:
                current = rowsDeleted.pop()
                # Sorting occupied by y values, largest to smallest: largest = first available row in occupied
                for key in sorted(list(self.occupied), key=lambda c: c[1])[::-1]:
                    x, y = key
                    if y < current:
                        self.occupied[(x, current)] = self.occupied.pop((x, y))

        # clear the line, move all occupied blocks above down one y position
        # clear rows from occupied, first row deleted = first row in occupied, second = second in occupied etc.
        # Sort occupied by row coordinates, current row = all occupied coordinates with the same row coordinate


def getNextShape():
    return Shape(5, 0, choice(shapes))


def drawLabel(surface, grid, originX):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('\'comicsans\'', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (originX + grid.width / 2 - (label.get_width() / 2), 30))


def update():
    pygame.display.update()


def drawGame(surface, grid, gridOriginX, gridOriginY, nextShape):
    grid.drawShapesInGrid(surface, gridOriginX, gridOriginY)
    grid.drawGrid(surface, gridOriginX, gridOriginY)
    nextShape.drawNextShape(surface, gridOriginX, gridOriginY, grid.width, grid.height)
    update()


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
        self.clock = pygame.time.Clock()
        self.fallTime = 0
        self.fallSpeed = 0.25
        self.difficultyTime = 0
        self.change = False

    def gameOver(self):
        for coord in self.grid.occupied:
            if coord[1] < 1:
                return True
        return False

    def printGameOver(self):
        font = pygame.font.SysFont("comicsans", 80, bold=True)
        label = font.render("Game Over", 1, (255, 255, 255))

        self.window.blit(label, (
            self.gridOriginX + self.grid.width / 2 - (label.get_width() / 2),
            self.gridOriginY + self.grid.height / 2 - label.get_height() / 2))

    def run(self):
        run = True
        pygame.init()
        pygame.display.set_caption('Tetris by Callum Ke')
        drawLabel(self.window, self.grid, self.gridOriginX)

        while run:
            self.grid.fillGrid()
            self.fallTime += self.clock.get_rawtime()
            self.difficultyTime += self.clock.get_rawtime()
            self.clock.tick()

            if self.difficultyTime / 1000 > 5:
                self.difficultyTime = 0
                if self.difficultyTime > 0.12:
                    self.difficultyTime -= 0.005

            if self.fallTime / 1000 > self.fallSpeed:
                self.fallTime = 0
                self.currentShape.y += 1
                if not (self.grid.isValidSpace(
                        self.currentShape.getShapeCoordinates())) and self.currentShape.y > 0:
                    self.currentShape.y -= 1
                    self.change = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    print('Before', self.currentShape.x, self.currentShape.y)

                    if key[pygame.K_LEFT]:
                        self.currentShape.x -= 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.x += 1

                    if key[pygame.K_RIGHT]:
                        self.currentShape.x += 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.x -= 1

                    if key[pygame.K_UP]:
                        temp = copy(self.currentShape)
                        temp.changeRotation()
                        if self.grid.isValidSpace(temp.getShapeCoordinates()):
                            self.currentShape.changeRotation()

                    if key[pygame.K_DOWN]:
                        self.currentShape.y += 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.y -= 1
                    print('After', self.currentShape.x, self.currentShape.y)

            for coord in self.currentShape.getShapeCoordinates():
                col, row = coord
                if row > -1:
                    self.grid.grid[row][col] = self.currentShape.colour

            if self.change:
                self.grid.addOccupied(self.currentShape)
                self.currentShape = self.nextShape
                self.nextShape = getNextShape()
                self.grid.clearLine()
                self.change = False

            drawGame(self.window, self.grid, self.gridOriginX, self.gridOriginY, self.nextShape)

            if self.gameOver():
                self.printGameOver()
                update()
                pygame.time.delay(1000)
                run = False

        pygame.quit()


def main():
    applet = Tetris()
    applet.run()


if __name__ == '__main__':
    main()
