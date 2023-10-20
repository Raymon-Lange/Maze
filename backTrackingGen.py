import random

class BackTrackingGen:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def generate(self, maze):
        stack = [(random.randrange(1, self.width, 2), random.randrange(1, self.height, 2))]
        steps = [stack[0]]

         # Define directions (up, down, left, right)
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

        # Helper function to check if a cell is within the maze boundaries
        def isInside(x, y):
            return 0 <= x < self.width-2 and 0 <= y < self.height-2


        while stack:
            x, y = stack[-1]  # Current cell
            neighbors = [(x + dx, y + dy) for dx, dy in directions if isInside(x + dx, y + dy)]

            unvisited_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] == 0]
        
            if unvisited_neighbors:
                # Choose a random unvisited neighbor
                nx, ny = random.choice(unvisited_neighbors)
                maze[ny][nx] = 1  # Mark the cell as visited
                steps.append((ny,nx))
                maze[y + (ny - y) // 2][x + (nx - x) // 2] = 1  # Remove the wall between current and neighbor
                steps.append((y + (ny - y) // 2, x + (nx - x) // 2))
                stack.append((nx, ny))
            else:
                # If there are no unvisited neighbors, backtrack
                stack.pop()

        return steps
