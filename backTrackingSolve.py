import random

class backTrackingSolve:
    def __init__(self, maze) -> None:
        self.maze = maze
        # Get the dimensions of the maze
        self.height = len(maze)
        self.width = len(maze[0])

        self.wasHere = []
        self.path = []

    def solve(self, start, end):
        self.start = start
        self.end = end
        return self.step(start[0], start[1])

    def step(self, x, y):
        #Check to see if found the end of the maze!
        if x  == self.end[0] and y == self.end[1]:
            return True

        #Check to see if we are in open spot (Not a wall)
        if self.maze[x][y] != 1: 
            return False
        
        #Check we have have already beed here. 
        if (x,y) in self.wasHere:
            return False
        
        self.wasHere.append((x,y))

        if x != 0 :
            if self.step(x-1,y):
                self.path.append((x,y))
                return True

        if x != self.height-1 :
            if self.step(x+1,y):
                self.path.append((x,y))
                return True
            
        if y != 0 :
            if self.step(x,y-1):
                self.path.append((x,y))
                return True
            
        if y != self.width-1 :
            if self.step(x,y+1):
                self.path.append((x,y))
                return True
        
        return False