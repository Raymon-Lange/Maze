import heapq

class AstarSolve:
    def __init__(self,maze) -> None:
        self.maze = maze
        # Set the demensions of the maze 
        self.height = len(maze)
        self.width = len(maze[0])

        #Washere is the cell of the maze that we have explored
        self.wasHere = []
        #path is the short path to solve the maze
        self.path = []

    def heuristic(self, point, goal):
        # Manhattan distance heuristic
        return abs(point[0] - goal[0]) + abs(point[1] - goal[1])
    
    def solve(self, start ,end):
            openSet = []

            # STEP Priority queue with (F-score, node)
            heapq.heappush(openSet, (0, start))
            cameFrom = {}
            gScore = {start: 0}

            #STEP: open set is not null we are still looking for the path 
            while openSet:
                 #STEP get the current location
                _, current = heapq.heappop(openSet)

                 #STEP: Check if we are at the goal
                if current == end:
                    while current in cameFrom:
                        print(current)
                        self.path.append(current)
                        current = cameFrom[current]
                    
                    #don't forget to add the start OOPs
                    self.path.append(start)
                    self.path.reverse()
                    return True

                #STEP: lets find which gscore is closes to the end.
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    x, y = current[0] + dx, current[1] + dy
                    neighbor = (x, y)

                    tentativeG = gScore[current] + 1

                    #step check if x and y is a open space and with in the maze
                    if 0 <= x < self.height and 0 <= y < self.width and self.maze[x][y] == 1:   
                        if neighbor not in gScore or tentativeG < gScore[neighbor]:
                            gScore[neighbor] = tentativeG
                            fScore = tentativeG + self.heuristic(neighbor, end)
                            heapq.heappush(openSet, (fScore, neighbor))
                            cameFrom[neighbor] = current

            return False
