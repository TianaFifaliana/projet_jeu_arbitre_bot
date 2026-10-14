import random

def is_path_possible(grid, size, start, end):
    """Vérifie si un chemin existe entre start et end via BFS."""
    queue = [start]
    visited = {start}
    
    while queue:
        curr_x, curr_y = queue.pop(0)
        
        if (curr_x, curr_y) == end:
            return True
            
        # Directions : Haut, Bas, Droite, Gauche
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            
            if 0 <= nx < size and 0 <= ny < size: # Dans les limites
                if grid[ny][nx] != -1 and (nx, ny) not in visited: # Pas un mur et pas visité
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return False

def generate_balanced_grid(grid_size, pos_a, pos_b, wall_probability=0.05):
    while True:
        # 1. Initialiser une grille vide
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # 2. Générer les murs avec symétrie centrale
        # On ne parcourt que la moitié de la grille (y) pour refléter sur l'autre moitié
        for y in range((grid_size // 2) + 1):
            for x in range(grid_size):
                # Éviter de placer un mur sur les zones de départ (A et B)
                if (x, y) == pos_a or (x, y) == pos_b:
                    continue
                
                if random.random() < wall_probability:
                    # Placer le mur original
                    grid[y][x] = -1
                    
                    # Calculer les coordonnées symétriques (Rotation 180°)
                    sym_x = (grid_size - 1) - x
                    sym_y = (grid_size - 1) - y
                    
                    # Placer le mur symétrique s'il ne touche pas les départs
                    if (sym_x, sym_y) != pos_a and (sym_x, sym_y) != pos_b:
                        grid[sym_y][sym_x] = -1

        # 3. Vérification de l'accessibilité (Breadth-First Search)
        if is_path_possible(grid, grid_size, pos_a, pos_b):
            return grid

def generate_fixed_grid(grid_size, pos_a, pos_b):
    """Génère une grille au design prédéfini (non aléatoire)."""
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    center = grid_size // 2
    
    # Création d'une croix centrale
    for i in range(max(0, center - 4), min(grid_size, center + 5)):
        # Barre horizontale
        if (i, center) != pos_a and (i, center) != pos_b:
            grid[center][i] = -1
        # Barre verticale
        if (center, i) != pos_a and (center, i) != pos_b:
            grid[i][center] = -1
            
    # Ajout de 4 îlots dans les coins
    for cx, cy in [(4, 4), (grid_size-5, 4), (4, grid_size-5), (grid_size-5, grid_size-5)]:
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if (cx, cy) != pos_a and (cx, cy) != pos_b:
                grid[cy][cx] = -1
                
    return grid

class Game:
    def __init__(self, grid_size=20, max_turns=500, use_fixed_grid=False):
        self.size = grid_size
        self.max_turns = max_turns
        
        # Start top-left and bottom-right
        self.pos_A = (0, 0)
        self.pos_B = (grid_size - 1, grid_size - 1)
        
        if use_fixed_grid:
            self.grid = generate_fixed_grid(grid_size, self.pos_A, self.pos_B)
        else:
            # Construction de la carte de manière équitable !
            self.grid = generate_balanced_grid(grid_size, self.pos_A, self.pos_B, wall_probability=0.05)
        
        # Initial paint
        self.grid[self.pos_A[1]][self.pos_A[0]] = 1
        self.grid[self.pos_B[1]][self.pos_B[0]] = 2
        
        self.turn = 1
        self.blocked_A = False
        self.blocked_B = False

    def is_valid_pos(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def get_target(self, pos, move):
        x, y = pos
        if move == "NORD":
            return (x, y - 1)
        if move == "SUD":
            return (x, y + 1)
        if move == "EST":
            return (x + 1, y)
        if move == "OUEST":
            return (x - 1, y)
        return (x, y) # REPOS or invalid

    def check_valid_target(self, pos, move, me_id, opp_id):
        target = self.get_target(pos, move)
        if target == pos: # REPOS or invalid
            return pos
        x, y = target
        if not self.is_valid_pos(x, y):
            return pos
            
        cell = self.grid[y][x]
        # "Vous ne pouvez pas traverser les murs, ni les cases déjà occupées (par vous ou l'adversaire)."
        if cell != 0:
            return pos
            
        return target

    def try_move(self, move_A, move_B):
        # Resolve target positions
        tar_A = self.check_valid_target(self.pos_A, move_A, 1, 2)
        tar_B = self.check_valid_target(self.pos_B, move_B, 2, 1)

        # Handle collisions
        if tar_A == tar_B and tar_A != self.pos_A and tar_A != self.pos_B:
            # Collision! The designated neutral square becomes a wall
            cx, cy = tar_A
            self.grid[cy][cx] = -1
            # Bots stay in place
            tar_A = self.pos_A
            tar_B = self.pos_B

        # Apply moves and color squares
        if tar_A != self.pos_A:
            self.pos_A = tar_A
            self.grid[self.pos_A[1]][self.pos_A[0]] = 1
            
        if tar_B != self.pos_B:
            self.pos_B = tar_B
            self.grid[self.pos_B[1]][self.pos_B[0]] = 2

    def check_blocked(self, pos):
        # Check all N, S, E, W
        possible_moves = ["NORD", "SUD", "EST", "OUEST"]
        for m in possible_moves:
            tx, ty = self.get_target(pos, m)
            if self.is_valid_pos(tx, ty) and self.grid[ty][tx] == 0:
                return False
        return True

    def calculate_scores(self):
        score_A = sum(row.count(1) for row in self.grid)
        score_B = sum(row.count(2) for row in self.grid)
        return score_A, score_B

    def update(self, move_A, move_B):
        self.try_move(move_A, move_B)
        
        self.blocked_A = self.check_blocked(self.pos_A)
        self.blocked_B = self.check_blocked(self.pos_B)
        
        self.turn += 1

    def is_game_over(self):
        if self.turn > self.max_turns:
            return True
        if self.blocked_A and self.blocked_B:
            return True
        return False
