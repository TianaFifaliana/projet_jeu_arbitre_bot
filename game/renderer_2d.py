import pygame
import sys

class PygameRenderer:
    COLORS = {
        "bg": (30, 30, 30),        # Dark background
        "grid": (50, 50, 50),      # Grid lines
        "empty": (40, 40, 40),     # Empty cells
        "team_a": (41, 128, 185),  # Blue
        "team_b": (192, 57, 43),   # Red
        "wall": (149, 165, 166),   # Gray collision wall
        "text": (236, 240, 241)    # White text
    }

    def __init__(self, window_size=800):
        pygame.init()
        self.window_size = window_size
        self.info_panel_height = 80
        self.screen_width = window_size
        self.screen_height = window_size + self.info_panel_height
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Territoires Algorithmiques : Le Duel")
        
        self.font_large = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 20)

    def process_events(self):
        # We need to process events so the OS doesn't think the app is frozen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

    def clear(self):
        # Not strictly needed since we fill screen in draw_grid, but keeps API compatible
        pass

    def draw_grid(self, game):
        self.process_events()
        
        self.screen.fill(self.COLORS["bg"])
        
        # Calculate cell size
        cell_size = self.window_size // game.size
        
        # Draw the grid cells
        for y in range(game.size):
            for x in range(game.size):
                cell_val = game.grid[y][x]
                
                rect = pygame.Rect(x * cell_size, y * cell_size + self.info_panel_height, cell_size, cell_size)
                
                if cell_val == 0:
                    color = self.COLORS["empty"]
                elif cell_val == 1:
                    color = self.COLORS["team_a"]
                elif cell_val == 2:
                    color = self.COLORS["team_b"]
                elif cell_val == -1:
                    color = self.COLORS["wall"]
                else:
                    color = self.COLORS["empty"]
                    
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.COLORS["grid"], rect, 1) # border
                
                # Draw collision mark cross
                if cell_val == -1:
                    pygame.draw.line(self.screen, (100, 100, 100), rect.topleft, rect.bottomright, 3)
                    pygame.draw.line(self.screen, (100, 100, 100), rect.bottomleft, rect.topright, 3)

        # Draw the bots as circles
        bot_radius = int(cell_size * 0.4)
        # 🤖 Affichage du Bot de l'équipe A
        ax, ay = game.pos_A
        a_center = (int((ax + 0.5) * cell_size), int((ay + 0.5) * cell_size) + self.info_panel_height)
        pygame.draw.circle(self.screen, (255, 255, 255), a_center, bot_radius, 3) # Highlight ring
        pygame.draw.circle(self.screen, self.COLORS["team_a"], a_center, bot_radius - 2)
        
        # 🤖 Affichage du Bot de l'équipe B
        bx, by = game.pos_B
        b_center = (int((bx + 0.5) * cell_size), int((by + 0.5) * cell_size) + self.info_panel_height)
        pygame.draw.circle(self.screen, (255, 255, 255), b_center, bot_radius, 3) # Highlight ring
        pygame.draw.circle(self.screen, self.COLORS["team_b"], b_center, bot_radius - 2)

        # Draw Info Panel
        score_A, score_B = game.calculate_scores()
        
        # Turn Text
        turn_text = self.font_large.render(f"TOUR: {game.turn} / {game.max_turns}", True, self.COLORS["text"])
        self.screen.blit(turn_text, (20, 20))
        
        # Score Text
        score_text_a = self.font_large.render(f"Équipe A : {score_A}", True, self.COLORS["team_a"])
        score_text_b = self.font_large.render(f"Équipe B : {score_B}", True, self.COLORS["team_b"])
        
        # Align right
        self.screen.blit(score_text_a, (self.screen_width - 400, 20))
        self.screen.blit(score_text_b, (self.screen_width - 200, 20))

        pygame.display.flip()

    def show_game_over(self, game):
        # Keep window active after game reaches turn limit or both blocked
        score_A, score_B = game.calculate_scores()
        
        # Draw final state
        self.draw_grid(game)
        
        # Draw dark overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))
        
        if score_A > score_B:
            msg = "VICTOIRE DE L'ÉQUIPE A !"
            col = self.COLORS["team_a"]
        elif score_B > score_A:
            msg = "VICTOIRE DE L'ÉQUIPE B !"
            col = self.COLORS["team_b"]
        else:
            msg = "ÉGALITÉ !"
            col = self.COLORS["text"]
            
        go_font = pygame.font.SysFont("Arial", 50, bold=True)
        text_surf = go_font.render(msg, True, col)
        text_rect = text_surf.get_rect(center=(self.screen_width/2, self.screen_height/2 - 30))
        
        # Add shadow text
        shadow_surf = go_font.render(msg, True, (0,0,0))
        shadow_rect = shadow_surf.get_rect(center=(self.screen_width/2 + 3, self.screen_height/2 - 27))
        
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(text_surf, text_rect)
        
        sub_msg = f"Score final : {score_A} - {score_B}"
        sub_font = pygame.font.SysFont("Arial", 30)
        sub_surf = sub_font.render(sub_msg, True, self.COLORS["text"])
        sub_rect = sub_surf.get_rect(center=(self.screen_width/2, self.screen_height/2 + 30))
        self.screen.blit(sub_surf, sub_rect)
        
        pygame.display.flip()
        
        import threading
        
        # Loop until manually closed by the user
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.time.wait(100)
            
        pygame.quit()
