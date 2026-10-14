import random
import time
# stephan
def get_move(grid, my_pos, opp_pos, turn_info):
    """
    A simple bot that tries to move to any adjacent empty cell.
    If multiple cells are empty, it picks randomly.
    """
    moves = {
        "NORD": (0, -1),
        "SUD": (0, 1),
        "EST": (1, 0),
        "OUEST": (-1, 0)
    }
    x,y = my_pos
    print("x = " + str(x))
    isOust = False
    n = 2 
    # nextMove= []
    # for i in range(n):
        
    #     valid_moves = []
    #     for name, (dx, dy) in moves.items():
    #         nx, ny = x + dx, y + dy
    #         if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
    #             if grid[ny][nx] == 0:
    #                 valid_moves.append(name)
    #     if isOust == True:
    #             isOust = False
    #             for name in valid_moves:
    #                 if name == "EST":
    #                     return "EST"
    #     for name in valid_moves:
    #         if name == "NORD":
    #             return "NORD"

    #     for name in valid_moves:
    #         if name == "OUEST":
    #             isOust = True
    #             return "OUEST"
    #     for name in valid_moves:
    #         if name == "SUD":
    #             return "SUD"
    #     for name in valid_moves:
    #         if name == "EST":
    #             return "EST"
        

    
    valid_moves = []
    x, y = my_pos
    for name, (dx, dy) in moves.items():
       nx, ny = x + dx, y + dy
       if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
           if grid[ny][nx] == 0:
               valid_moves.append(name)
               
    if valid_moves:
      return random.choice(valid_moves)
    return "REPOS"
