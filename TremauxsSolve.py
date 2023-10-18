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
            if self.maze[x-1][y] != 1: 
                openSpace +=1 
            
        if x != self.height-1 :
            if self.maze[x-1][y] != 1: 
                openSpace +=1
            
        if y != self.width-1 :
            if self.maze[x][y+1] != 1: 
                openSpace +=1

        if y != 0 :
            if self.maze[x][y-1] != 1: 
                openSpace +=1

        if openSpace >= 2:
            return True
            
        return False 
        

        #If all direction are dead return true
    def isDedend(self,x,y):
            totalWall = 0
            if x != 0 :
                if self.maze[x-1][y] == 1: 
                    totalWall +=1 
            
            if x != self.height-1 :
                if self.maze[x-1][y] == 1: 
                    totalWall +=1 
            
            if y != self.width-1 :
                if self.maze[x][y+1] == 1: 
                    totalWall +=1 

            if y != 0 :
                if self.maze[x][y-1] == 1: 
                    totalWall +=1 

            #if we can't move any direction, the point behind us should be open 
            #so the max wall we can hit is 3 at dead end
            if totalWall == 3:
                return True
            
            return False
    
    def goBackToLastJuction(self):
        lastJunction = self.junctions[len(self.junctions)]


        isJuction = False

        while not isJuction:

            backStep = self.path.pop() 

            if lastJunction == backStep:
                isJuction = True
            else:
                self.maze[backStep[0]][backStep[1]] = 1

                
        
    def solve(self, start, end):
            self.start = start
            self.end = end

            found = False 

            #Add the start
            self.wasHere.append(self.start)
            self.path.append(self.start)

            count = 0 

            while not found:
                direction = self.directions[random.randint(0,3)]
                currentPos = self.wasHere[len(self.wasHere)-1]
                x = currentPos[0] + direction[0]
                y = currentPos[1] + direction[1]

                if end[0] == x and end[1] == y:
                    found = True
                    self.path.append((x,y))
                    return True


                if self.maze[x][y] != 1 and (x,y) in self.wasHere:
                    
                    if self.isJunction(x,y):
 
                        if (x,y) in self.junctions:
                        #Get the last  postion i came from and mark in as wall 
                            point = self.wasHere.pop()
                            self.maze[point[0]][point[1]] = 1
                        
                            self.goBackToLastJuction()
                        else: 
                            #add the junction to the list of junctions 
                            self.junctions.append((x,y))

                    elif self.isDeadEnd():
                        self.goBackToLastJuction()

                    else:
                        self.wasHere.append((x,y))
                        self.path.append((x,y))

                count += 1
                if count > 100:
                    return False

                    



                    


                
            
