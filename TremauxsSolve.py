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

    #Check to see if the point we moved to has more than option 
    #return True if you can move two or more option otherwise false
    def isJunction(self, x, y):

        openSpace  = 0

        if x != 0 :
            if self.maze[x-1][y] != 0: 
                openSpace +=1 
            
        if x != self.height-1 :
            if self.maze[x+1][y] != 0: 
                openSpace +=1
            
        if y != self.width-1 :
            if self.maze[x][y+1] != 0: 
                openSpace +=1

        if y != 0 :
            if self.maze[x][y-1] != 0: 
                openSpace +=1

        if openSpace > 2:
            return True
            
        return False 
        
        #If all direction are dead return true
    def isDedend(self,x,y):
            totalWall = 0
            if x != 0 :
                if self.maze[x-1][y] == 0: 
                    totalWall +=1 
            
            if x != self.height-1 :
                if self.maze[x+1][y] == 0: 
                    totalWall +=1 
            
            if y != self.width-1 :
                if self.maze[x][y+1] == 0: 
                    totalWall +=1 

            if y != 0 :
                if self.maze[x][y-1] == 0: 
                    totalWall +=1 

            #if we can't move any direction, the point behind us should be open 
            #so the max wall we can hit is 3 at dead end
            if totalWall == 3:
                return True
            
            return False
    
    def goBackToLastJuctionOne(self):

        if len(self.junctions) == 0:
            print("No junctions in the list")
            return 
        
        self.junctions.pop()
        lastJunction = self.junctions[len(self.junctions)-1]

        isJuction = False

        while not isJuction:

            if len(self.path) == 0:
                print("Path is empty")
                return

            backStep = self.path.pop() 

            if lastJunction == backStep:
                isJuction = True
                self.path.append(backStep)
                print("went back to ",backStep)
            else:
                print("not at junction keep going back")
                self.maze[backStep[0]][backStep[1]] = 0

    def goBackToLastJuction(self):
        lastJunction = self.junctions.pop()

        isJuction = False

        while not isJuction:

            if len(self.path) == 0:
                print("Path is empty")
                return

            backStep = self.path.pop() 

            if lastJunction == backStep:
                isJuction = True
                self.path.append(self.junctions[len(self.junctions)-1])
                print("went back to ",backStep)
            else:
                print("not the junction keep going back")
                self.maze[backStep[0]][backStep[1]] = 0             

    # Helper function to check if a cell is within the maze boundaries
    def isInside(self, x, y):
        return 0 <= x < self.width-1 and 0 <= y < self.height-1
                
    def  solve(self, start, end):
            self.start = start
            self.end = end

            print("Start ", start)

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
                    print("Has neighbors", neighbors)

                    unvisited_neighbors = [neighbor for neighbor in neighbors if self.maze[neighbor[1]][neighbor[0]] != 0 and neighbor not in self.wasHere ]

                    print("unvisited neighbors", unvisited_neighbors)

                    if unvisited_neighbors:
                        print(len(unvisited_neighbors)," neighbors open")

                        #STEP: We have more than option we are at junction 
                        if len(unvisited_neighbors) > 1:
                            self.junctions += unvisited_neighbors
                            x,y = self.junctions[len(self.junctions)-1]
                            print(self.junctions)
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
                                print("Crap i failed")
                                return False
                            previousDirection = None
                            print("No options going back")
                            continue

                    
                    #STEP: Did we find the end of the maze
                    if end[0] == x and end[1] == y:
                        found = True
                        print("found path")
                        return True
                    
                    print(x,y, "is a open cell")
                    #STEP: We have a valid space to be in, move forward
                    self.wasHere.append((x,y))
                    self.path.append((x,y))
                    
                    steps += 1
                    if steps > maxStep:
                        print("Failed to find exit")
                        return False

                    
                    


                    


                
            
