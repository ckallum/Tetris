import pygame
from random import choice

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
            coordinates[i] = (coord[0], coord[1])

        return coordinates

    def drawNextShape(self, surface, shape):
        pass


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
        # validSpaces = [xy for subList in validSpaces for xy in subList]
        for coord in coords:
            if coord not in validSpaces:
                if coord[1] > -1:
                    return False
        return True

    def addOccupied(self, coords, colour):
        for coord in coords:
            x, y = coord
            self.occupied[(x, y)] = colour

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
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.occupied:
                    self.grid[i][j] = self.occupied[(j, i)]

    def clearLine(self):
        count = 0
        for i in range(len(self.grid) - 1, -1, -1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                count += 1
                for j in range(len(row)):
                    try:
                        del self.occupied[(j, i)]
                    except:
                        continue

        if count > 0:
            for key in sorted(list(self.occupied), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < count:
                    newKey = (x, y + count)
                    self.occupied[newKey] = self.occupied.pop(key)

        return count

    # clear the line, move all occupied blocks above down one y position


def getNextShape():
    return Shape(6, 0, choice(shapes))


def drawLabel(surface, grid, originX):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('\'comicsans\'', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (originX + grid.width / 2 - (label.get_width() / 2), 30))


def update():
    pygame.display.update()


# function to display the next shape on the side


def drawGame(surface, grid, gridOriginX, gridOriginY):
    grid.drawShapesInGrid(surface, gridOriginX, gridOriginY)
    grid.drawGrid(surface, gridOriginX, gridOriginY)
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
        self.difficulty = 1
        self.clock = pygame.time.Clock()
        self.fallTime = 0
        self.speed = 0.25
        self.change = False

    def gameOver(self):
        for coord in self.grid.occupied:
            if coord[1] < 1:
                return True
        return False

    def run(self):
        run = True
        pygame.init()

        while run:
            self.grid.fillGrid()
            pygame.display.set_caption('Tetris by Callum Ke')
            drawLabel(self.window, self.grid, self.gridOriginX)
            self.fallTime += self.clock.get_rawtime()
            self.clock.tick()

            if self.fallTime / 1000 > self.speed:
                self.fallTime = 0
                self.currentShape.y += 1
                if not (self.grid.isValidSpace(
                        self.currentShape.getShapeCoordinates())) and self.currentShape.y > self.grid.rows:
                    self.currentShape.y -= 1
                    self.change = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT:
                        self.currentShape.x -= 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.x += 1

                    if event.type == pygame.K_RIGHT:
                        self.currentShape.x += 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.x -= 1

                    if event.type == pygame.K_UP:
                        self.currentShape.rotation += 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.rotation -= 1

                    if event.type == pygame.K_DOWN:
                        self.currentShape.y += 1
                        if not (self.grid.isValidSpace(self.currentShape.getShapeCoordinates())):
                            self.currentShape.y -= 1

            for coord in self.currentShape.getShapeCoordinates():
                col, row = coord
                if -1 < row < self.grid.rows:
                    self.grid.grid[row][col] = self.currentShape.colour

            if self.change:
                self.grid.addOccupied(self.currentShape.getShapeCoordinates(), self.currentShape.colour)
                self.currentShape = self.nextShape
                self.nextShape = getNextShape()
                self.change = False
                score = self.grid.clearLine()

            drawGame(self.window, self.grid, self.gridOriginX, self.gridOriginY)

            if self.gameOver():
                # display game over
                update()
                pygame.time.delay(1500)
                print("hi")
                run = False
                # update score

        pygame.quit()


def main():
    applet = Tetris()
    applet.run()


if __name__ == '__main__':
    main()
