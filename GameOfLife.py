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
        #print("evolve me -- col: " + str(self.index[0]) + " row: " + str(self.index[1]))

        oldAliveState = self.alive

        # cylce through the 8 surrounding neighbours
        aliveFound = 0
        for i in range(3):
            col = (self.index[0] + i) - 1
            if 0 <= col < Field.countX:
                for n in range(3):
                    row = (self.index[1] + n) - 1
                    if 0 <= row < Field.countY:
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


# a field of cells, either dead or alive
class Field:
    cellRows = []
    oldCellRows = []
    countX = 100
    countY = 100
    randomAliveChance = 0.04

    #update
    updateClock = 0
    updateDelay = 1    # delay in ticks --- 60 ticks = 1 sec

    @staticmethod
    def fillRandom():
        Field.cellRows = []
        Field.oldCellRows = []

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
                else:
                    Field.cellRows[row].append(Cell(False, x, y, col, row, cellWidth, cellHeight))

    @staticmethod
    # draw the field by drawing all cells
    def draw():
        for row in range(len(Field.cellRows)):
            for cell in Field.cellRows[row]:
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
#print(Field.getAliveCount())


# game loop
running = True
while running:

    # erase the
    screen.fill((0, 0, 0))
    delay = clock.tick(60)


    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                Field.fillRandom()
                Field.evolve()


    # evolve field
    Field.updateClock += 1
    if Field.updateClock == Field.updateDelay:
        Field.evolve()
    if not 0 <= Field.updateClock <= Field.updateDelay:
        Field.updateClock = 0


    # draw field
    Field.draw()

    # pygame display update
    pygame.display.update()

pygame.quit()