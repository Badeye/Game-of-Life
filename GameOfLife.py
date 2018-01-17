# florian wolf - 16.01.2017
import pygame
from pygame.locals import *
import random

pygame.init()
pygame.display.set_caption("Florian Wolf's - Game of Life")

res = (800, 800)
width = 800
height = 800

screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

infoScreen = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32)

# font
infoFont = pygame.font.SysFont('Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New', 14)
instructionFont = pygame.font.SysFont('Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New', 14)


# cells can either be dead or alive. They die/live depending on how many neighbours they have
class Cell:

    # constructor
    def __init__(self, alive, x, y, col, row, cellWidth, cellHeight):
        self.index = (col, row)
        self.x = x
        self.y = y
        self.width = cellWidth
        self.height = cellHeight

        self.alive = False
        self.color = (0, 0, 0)
        if alive:
            self.alive = True
            self.color = (255, 255, 255)
        self.previousAliveStates = []

    # draw this cell
    def draw(self):
        if self.alive:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)
        pygame.draw.rect(screen, self.color, (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))

    # check the neighbouring cells to kill/revive this one accordingly
    def evolve(self):
        oldAliveState = self.alive

        # cylce through the 8 surrounding neighbours
        aliveFound = 0
        for i in range(3):
            col = (self.index[0] + i) - 1
            if 0 <= col < Field.countX:
                for n in range(3):
                    row = (self.index[1] + n) - 1
                    if 0 <= row < Field.countY and not (row == self.index[1] and col == self.index[0]):
                        # check the neighbour for deadness *kek*
                        if Field.oldCellRows[row][col].alive:
                            aliveFound += 1

        # rule #1   --- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        if aliveFound < 2 and self.alive:
            self.alive = False

        # rule #2   --- Any live cell with two or three live neighbours lives on to the next generation.
        if 1 < aliveFound < 4 and self.alive:
            self.alive = True

        # rule #3   --- Any live cell with more than three live neighbours dies, as if by overpopulation.
        if 3 < aliveFound and self.alive:
            self.alive = False

        # rule #4   --- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        if aliveFound == 3 and not self.alive:
            self.alive = True

        # register/log the change
        if oldAliveState != self.alive:
            self.previousAliveStates.append(oldAliveState)
            if self.alive:
                Field.cellsAlive += 1
            else:
                Field.cellsAlive -= 1


# a field of cells, either dead or alive
class Field:
    cellRows = []
    oldCellRows = []
    countX = 100
    countY = 100
    randomAliveChance = 0.05

    # cell alive counters
    cellsAlive = 0
    oldCellsAlive = 0
    stillEvolving = True

    # update variables
    updateClock = 0
    updateDelay = 1    # delay in ticks --- 60 ticks = 1 sec

    @staticmethod
    def fillRandom():
        Field.cellRows = []
        Field.oldCellRows = []
        Field.cellsAlive = 0
        Field.oldCellsAlive = 0

        cellWidth = width/Field.countX
        cellHeight = height/Field.countY

        for row in range(Field.countX):
            Field.cellRows.append([])
            for col in range(Field.countY):
                r = random.random()
                x = (height/Field.countX) * col + (height/Field.countX)/2
                y = (width / Field.countY) * row + (width / Field.countY) / 2

                # spawn a cell that is alive
                if r <= Field.randomAliveChance:
                    Field.cellRows[row].append(Cell(True, x, y, col, row, cellWidth, cellHeight))
                    Field.cellsAlive += 1
                else:
                    Field.cellRows[row].append(Cell(False, x, y, col, row, cellWidth, cellHeight))

    @staticmethod
    # draw the field by drawing all cells and evolve them if needed
    def draw():
        # evolve field check
        evolve = False
        Field.updateClock += 1
        if Field.updateClock == Field.updateDelay:
            evolve = True
        if not 0 <= Field.updateClock <= Field.updateDelay:
            Field.updateClock = 0

        Field.oldCellsAlive = Field.cellsAlive

        for row in range(len(Field.cellRows)):
            for cell in Field.cellRows[row]:

                # switch dead/alive depending on the amount of alive neighbours
                if evolve:
                    Field.oldCellRows = Field.cellRows
                    cell.evolve()
                    if Field.oldCellsAlive != Field.cellsAlive:
                        Field.stillEvolving = True
                    else:
                        Field.stillEvolving = False
                cell.draw()

    @staticmethod
    # switch dead/alive depending on the amount of alive neighbours
    def evolve():
        Field.oldCellRows = Field.cellRows
        for row in range(len(Field.cellRows)):
            for cell in Field.cellRows[row]:
                cell.evolve()

    @staticmethod
    # get the cell underneath the cursor on a click
    def getCellByClick(x, y):
        print("fillthis")

    @staticmethod
    # debug alive count
    def getAliveCount():
        alives = 0
        for row in range(len(Field.cellRows)):
            for cell in Field.cellRows[row]:
                if cell.alive:
                    alives += 1
        return alives


# set up the Field by filling it with new, random cells
Field.fillRandom()


# info box filled with content (text)
class InfoBox:
    width = 165
    height = 105
    backgroundColor = (0, 0, 0, 200)
    textColor = (255, 255, 255)

    textPaddingTop = 10

    @staticmethod
    def draw():
        pygame.draw.rect(infoScreen, InfoBox.backgroundColor, (0, 0, InfoBox.width, InfoBox.height))

        # instruction
        instrText = instructionFont.render("SPACE to randomize", False, InfoBox.textColor)
        infoScreen.blit(instrText, (InfoBox.textPaddingTop, InfoBox.textPaddingTop))

        # alive count
        infoText = infoFont.render("Alive: " + str(Field.cellsAlive), False, InfoBox.textColor)
        infoScreen.blit(infoText, (InfoBox.textPaddingTop, InfoBox.textPaddingTop + 30))

        # evolving
        evolvingText = infoFont.render("Evolving: " + str(Field.stillEvolving), False, InfoBox.textColor)
        infoScreen.blit(evolvingText, (InfoBox.textPaddingTop, InfoBox.textPaddingTop + 50))

        # fps
        fpsText = infoFont.render("FPS: " + str(int(clock.get_fps())), False, InfoBox.textColor)
        infoScreen.blit(fpsText, (InfoBox.textPaddingTop, InfoBox.textPaddingTop + 70))

        screen.blit(infoScreen, (0, 0))


# game loop
running = True
while running:

    # erase the screen to prepare for the redraw
    screen.fill((0, 0, 0))

    # set the frame rate
    delay = clock.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                Field.fillRandom()
                Field.evolve()

    # draw and evolve the field
    Field.draw()

    # draw info boxes
    InfoBox.draw()

    # pygame display update
    pygame.display.update()

pygame.quit()