import time
import os
from game.engine import Game
from game.player import BotHandler
from game.renderer_2d import PygameRenderer

# --- CONFIGURATION DE L'ARBITRE ---
BOT_1_PATH = "bots/bot_equipe_01.py"
BOT_2_PATH = "bots/bot_equipe_02.py"
GRID_SIZE = 30
MAX_TURNS = 500
TIMEOUT_SEC = 0.100  # 100ms
FPS = 10  # Vitesse d'affichage (0 pour voir le résultat instantanément)
USE_FIXED_GRID = False # Mettre sur True pour jouer sur une carte statique de tournoi
# ----------------------------------

def main():
    bot1_path = os.path.abspath(BOT_1_PATH)
    bot2_path = os.path.abspath(BOT_2_PATH)
    
    game = Game(grid_size=GRID_SIZE, max_turns=MAX_TURNS, use_fixed_grid=USE_FIXED_GRID)
    renderer = PygameRenderer(window_size=800)
    
    # Initialize bot handlers
    print("Loading bots...")
    botA_handler = BotHandler(bot1_path)
    botB_handler = BotHandler(bot2_path)
    
    # Give them a moment to start the processes
    time.sleep(0.5)
    
    try:
        renderer.clear()
        renderer.draw_grid(game)
        
        while not game.is_game_over():
            turn_info = {"turn": game.turn, "time_left_ms": TIMEOUT_SEC * 1000}
            
            # Request moves using the wrapper, with strict timeout
            t0 = time.time()
            move_A = "REPOS" if game.blocked_A else botA_handler.get_move(game.grid, game.pos_A, game.pos_B, turn_info, timeout=TIMEOUT_SEC)
            
            move_B = "REPOS" if game.blocked_B else botB_handler.get_move(game.grid, game.pos_B, game.pos_A, turn_info, timeout=TIMEOUT_SEC)
            
            game.update(move_A, move_B)
            
            renderer.clear()
            print(f"Move A: {move_A} | Move B: {move_B}")
            renderer.draw_grid(game)
            
            if FPS > 0:
                time.sleep(1.0 / FPS)
                
        score_A, score_B = game.calculate_scores()
        print("Game Over!")
        print(f"Final Score: Team A: {score_A} - Team B: {score_B}")
        if score_A > score_B:
            print("Winner: Team A")
        elif score_B > score_A:
            print("Winner: Team B")
        else:
            print("Draw!")
            
        print("Affichage de l'écran de fin. Fermez la fenêtre graphique pour terminer.")
        renderer.show_game_over(game)
    finally:
        # Stop bot processes safely
        botA_handler.close()
        botB_handler.close()

if __name__ == "__main__":
    main()
