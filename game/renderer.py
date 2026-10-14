import os



class Renderer:
    COLORS = {
        0: "\033[40m",     # Black (Empty)
        1: "\033[44m\033[37m", # Blue (Team A)
        2: "\033[41m\033[37m", # Red (Team B)
        -1: "\033[47m\033[30m", # Gray (Wall)
    }
    RESET = "\033[0m"

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_grid(self, game):
        print(f"Turn: {game.turn}/{game.max_turns} | Team A: Blue, Team B: Red | Wall: Gray")
        score_A, score_B = game.calculate_scores()
        print(f"Scores -> Team A: {score_A} | Team B: {score_B}")
        
        border = "  " + "".join([f"{i%10} " for i in range(game.size)])
        print(border)
        
        for y in range(game.size):
            line = f"{y%10:2d}"
            for x in range(game.size):
                cell = game.grid[y][x]
                color = self.COLORS.get(cell, self.RESET)
                
                char = "  "
                if (x, y) == game.pos_A:
                    char = " A"
                elif (x, y) == game.pos_B:
                    char = " B"
                elif cell == -1:
                    char = " X"
                    
                line += f"{color}{char}{self.RESET}"
            print(line)
        print("\n")
