import random

class TremauxsSolve:
    def __init__(self, maze) -> None:
        self.maze = maze
        # Set the demensions of the maze 
        self.height = len(maze)
        self.width = len(maze[0])

        #Washere is the cell of the maze that we have explored
        self.wasHere = []
        #path is the short path to solve the maze
        self.path = []

        def solve(self, start, end):
            self.start = start
            self.end = end

            found = False 

            #Add the start
            self.wasHere.append(self.start)

            while not found:

                pass


        #Check to see if the point we moved to has more than option 
        #return True if you can move two or more option otherwise false
        def isJunction(self, x, y):

            if maze[x][y] != 1: 
                pass
            if maze[x][y] != 1: 
                pass
            if maze[x][y] != 1: 
                pass
            if maze[x][y] != 1: 
                pass
            

            return False 
        

        #If all direction are dead return true
        def isDedend(self,x,y):
            totalWall = 0
            if x != 0 :
                if maze[x-1][y] == 1: 
                    totalWall +=1 
            
            if x != self.height-1 :
                if maze[x-1][y] != 1: 
                    totalWall +=1 
            
            if y != self.width-1 :
                if maze[x][y+1] != 1: 
                    totalWall +=1 

            if y != 0 :
                if maze[x][y-1] != 1: 
                    totalWall +=1 

            #if we can't move any direction, the point behind us should be open 
            #so the max wall we can hit is 3 at dead end
            if totalWall == 3:
                return True
            
            return False
            
