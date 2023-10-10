import pygame
import sys
import random, time
from backTrackingGen import BackTrackingGen
from backTrackingSolve import backTrackingSolve


class MazeSolver:
    def __init__(self):
        # Define maze dimensions and cell size
        self.mazeWidth = 50
        self.mazeHeight = 50
        self.cellSize = 7

        # Define maze matrix (0 for walls, 1 for open paths)
        self.maze = [[0 for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        self.displayMaze = [[0 for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]

        self.endPos = (0,0)
        self.startPos = (0,0)

        # Initialize Pygame
        pygame.init()

        # Create the screen
        self.screen = pygame.display.set_mode((self.mazeWidth * self.cellSize, self.mazeHeight * self.cellSize))
        pygame.display.set_caption("Maze Solver")

        # Define colors
        self.white = (255, 255, 255)
        self.start = (244, 3, 252)
        self.end = (173, 255, 47)
        self.path = (255, 204, 203)
        self.black = (0, 0, 0)

        # Define State for the maze program
        self.BUILD = 0
        self.END = 1
        self.SOLVE = 2
        self.DRAW = 3
        self.PAUSE = 4
        self.currentState = self.BUILD

    def resetMaze(self):
        self.maze = [[0 for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]
        self.displayMaze = [[0 for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]


    def drawMaze(self):
        for y in range(self.mazeHeight):
            for x in range(self.mazeWidth):
                if self.displayMaze[x][y] == 0:
                    pygame.draw.rect(self.screen, self.black, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                elif self.displayMaze[x][y] == 2:
                    pygame.draw.rect(self.screen, self.start, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                elif self.displayMaze[x][y] == 3:
                    pygame.draw.rect(self.screen, self.end, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                elif self.displayMaze[x][y] == 4:
                    pygame.draw.rect(self.screen, self.path, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                else:
                    pygame.draw.rect(self.screen, self.white, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        x = self.startPos[0]
        y = self.startPos[1]
        pygame.draw.rect(self.screen, self.start, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        x = self.endPos[0]
        y = self.endPos[1]
        pygame.draw.rect(self.screen, self.end, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))


    def creatStartAndEnd(self):
        found = False
        while not found :
            pX = random.randrange(self.mazeHeight/2, self.mazeHeight)
            pY = random.randrange(self.mazeWidth/2, self.mazeWidth)

            if self.maze[pX][pY] == 1:
                self.endPos = (pX, pY)
                found = True

        found = False
        while not found :
            pX = random.randrange(1, self.mazeHeight/2)
            pY = random.randrange(1, self.mazeWidth/2)

            if self.maze[pX][pY] == 1:
                self.startPos = (pX, pY)
                found = True
    
    def main(self):

        # Generate the maze just once
        gen = BackTrackingGen(self.mazeHeight, self.mazeWidth)
        steps = gen.generate(self.maze)
        steps.reverse()

        self.creatStartAndEnd()

        print("Start " , self.startPos)
        print("End " , self.endPos)

        solve = backTrackingSolve(self.maze)
        pathFound = solve.solve(self.startPos, self.endPos)
        path = solve.path
        wasHere = solve.wasHere
        wasHere.reverse()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            self.screen.fill(self.black)

            if len(steps) > 0:
                step = steps.pop()
                self.displayMaze[step[0]][step[1]] = 1
            elif len(wasHere) > 0:
                step = wasHere.pop()
                self.displayMaze[step[0]][step[1]] = 4
            elif len(path) > 0:
                step = path.pop()
                self.displayMaze[step[0]][step[1]] = 3
            else:
                time.sleep(1)
                self.resetMaze()
                steps = gen.generate(self.maze)

                self.creatStartAndEnd()
                solve = backTrackingSolve(self.maze)
                pathFound = solve.solve(self.startPos, self.endPos)
                path = solve.path
                wasHere = solve.wasHere
                wasHere.reverse()
    
            # Draw the maze
            self.drawMaze()

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    maze_solver = MazeSolver()
    maze_solver.main()
