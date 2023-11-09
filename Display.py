import sys
import os
import random
import pygame
from backTrackingGen import BackTrackingGen
from backTrackingSolve import backTrackingSolve
from TremauxsSolve import TremauxsSolve
from aStarSolve import AstarSolve

class MazeSolver:
    # Constants for state
    BUILD = 0
    END = 1
    SOLVE = 2
    DRAW = 3
    PAUSE = 4

    def __init__(self):
        # Define maze dimensions and cell size
        self.mazeWidth = 50
        self.mazeHeight = 50
        self.cellSize = 7

        # Define maze matrix (0 for walls, 1 for open paths)
        self.maze = [[0] * self.mazeWidth for _ in range(self.mazeHeight)]
        self.displayMaze = [[0] * self.mazeWidth for _ in range(self.mazeHeight)]

        self.endPos = (0, 0)
        self.startPos = (0, 0)

        # Initialize Pygame
        pygame.init()

        # Create the screen
        self.screen = pygame.display.set_mode((self.mazeWidth * self.cellSize, self.mazeHeight * self.cellSize))
        pygame.display.set_caption("Maze Solver")

        # Define colors
        self.colors = {
            "white": (255, 255, 255),
            "start": (244, 3, 252),
            "end": (173, 255, 47),
            "path": (255, 204, 203),
            "black": (0, 0, 0)
        }

        self.currentState = self.BUILD
        self.explored = 0
        self.shortestPath = 0

        self.loadAssets()

    def resetMaze(self):
        self.maze = [[0] * self.mazeWidth for _ in range(self.mazeHeight)]
        self.displayMaze = [[0] * self.mazeWidth for _ in range(self.mazeHeight)]

    def drawMaze(self):
        for y in range(self.mazeHeight):
            for x in range(self.mazeWidth):
                cell_value = self.displayMaze[x][y]
                color = self.colors["black"]
                if cell_value == 1:
                    color = self.colors["white"]
                elif cell_value == 2:
                    color = self.colors["start"]
                elif cell_value == 3:
                    color = self.colors["end"]
                elif cell_value == 4:
                    color = self.colors["path"]
                pygame.draw.rect(self.screen, color, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        self.drawStartAndEnd()

    def drawStartAndEnd(self):
        self.drawCell(self.startPos, self.colors["start"])
        self.drawCell(self.endPos, self.colors["end"])

    def drawCell(self, position, color):
        x, y = position
        pygame.draw.rect(self.screen, color, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

    def createStartAndEnd(self):
        self.endPos = self.getRandomOpenCell(int(self.mazeHeight / 2), self.mazeHeight)
        self.startPos = self.getRandomOpenCell(1, int(self.mazeHeight / 2))

    def getRandomOpenCell(self, start, end):
        while True:
            pX = random.randrange(start, end)
            pY = random.randrange(start, end)
            if self.maze[pX][pY] == 1:
                return (pX, pY)

    def drawMenu(self, name):
        pygame.draw.rect(self.screen, self.colors["black"], pygame.Rect(20, 20, 300, 300), 2, 10)
        pygame.draw.rect(self.screen, self.colors["white"], pygame.Rect(20, 20, 298, 298))

        menu_items = [
            f"Generation: Backtracking",
            f"Solving: {name}",
            f'Cells Explored: {self.explored}',
            f'Shortest Path: {self.shortestPath}'
        ]

        self.drawTexts(menu_items, 150, [40, 80, 120, 170])

    def drawTexts(self, texts, x, y_values):
        for i, text in enumerate(texts):
            y = y_values[i]
            self.drawText(text, self.colors["black"], x, y)

    def drawText(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def loadAssets(self):
        self.assets_dir = os.path.join("assets")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 16)

    def main(self):
        clock = pygame.time.Clock()

        # Generate the maze just once
        gen = BackTrackingGen(self.mazeHeight, self.mazeWidth)
        steps = gen.generate(self.maze)
        steps.reverse()

        self.createStartAndEnd()

        Astar = AstarSolve(self.maze)
        Astar.solve(self.startPos, self.endPos)

        backtracking = backTrackingSolve(self.maze)
        backtracking.solve(self.startPos, self.endPos)

        tremauxs = TremauxsSolve(self.maze)
        tremauxs.solve(self.startPos, self.endPos)

        count = 200
        mazeSolved = 0
        wasHere = []
        path = []
        name = "Foobar"

        running = True
        while running:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.colors["black"])

            if len(steps) > 0:
                step = steps.pop()
                self.displayMaze[step[0]][step[1]] = 1
            elif len(wasHere) > 0:
                step = wasHere.pop()
                self.displayMaze[step[0]][step[1]] = 4
            elif len(path) > 0:
                step = path.pop()
                self.displayMaze[step[0]][step[1]] = 3
            elif count > 0:
                count -= 1
                self.currentState = self.END
            else:
                if mazeSolved == 0:
                    path = Astar.path
                    wasHere = Astar.wasHere
                    self.displayMaze = Astar.maze
                    wasHere.reverse()
                    mazeSolved += 1
                    name = "A Star"
                elif mazeSolved == 1:
                    path = backtracking.path
                    wasHere = backtracking.wasHere
                    wasHere.reverse()
                    mazeSolved += 1
                    name = "Backtracking"
                else:
                    path = tremauxs.path
                    wasHere = tremauxs.wasHere
                    wasHere.reverse()
                    mazeSolved = 0
                    name = "Tremaux"

                self.explored = len(wasHere)
                self.shortestPath = len(path)
                self.currentState = self.SOLVE
                self.displayMaze = self.maze
                count = 200

            self.drawMaze()

            if self.currentState == self.END:
                self.drawMenu(name)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    maze_solver = MazeSolver()
    maze_solver.main()
