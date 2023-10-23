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

        # this is a list of all junctions, a junction is more than one open space
        self.junctions = []

        self.directions= [(0,1),(0,-1),(1,0),(-1,0)]
     
    # Helper function to check if a cell is within the maze boundaries
    def isInside(self, x, y):
        return 0 <= x < self.width-1 and 0 <= y < self.height-1
                
    def  solve(self, start, end):
            self.start = start
            self.end = end



            #Add the start
            self.wasHere.append(self.start)
            self.path.append(self.start)

            found = False 

            previousDirection = None
            maxStep = 1000
            steps =0

            while not found:
                    x,y = self.path[len(self.path)-1]
                    #STEP: if previousDirection is none pick a new random direction 
                    neighbors = [(x + dx, y + dy) for dx, dy in self.directions if self.isInside(x + dx, y + dy)]

                    unvisited_neighbors = [neighbor for neighbor in neighbors if self.maze[neighbor[0]][neighbor[1]] != 0 and neighbor not in self.wasHere ]

                    if unvisited_neighbors:
                        #STEP: We have more than option we are at junction 
                        if len(unvisited_neighbors) > 1:
                            self.junctions += unvisited_neighbors
                            x,y = self.junctions.pop()
                        else:
                            x,y = unvisited_neighbors[0] 
                    #STEP: No neightbors go back to last junction   
                    else:
                            #STEP: We found a dead end go back to last junction
                            self.maze[x][y] = 0
                            self.wasHere.append((x,y))
                            if len(self.junctions) != 0:
                                self.path.append(self.junctions.pop())
                            else:
                                return False
                            continue

                    
                    #STEP: Did we find the end of the maze
                    if end == (x,y):
                        found = True
                        return True
                    
                    #STEP: We have a valid space to be in, move forward
                    self.wasHere.append((x,y))
                    self.path.append((x,y))
                    
                    steps += 1
                    if steps > maxStep:
                        return False

                    
                    


                    


                
            
