import multiprocessing
import multiprocessing.queues
import time
import importlib.util
import os
import sys

def bot_worker(bot_path, input_queue, output_queue):
    # Setup sys path so imports relative to the bot work
    bot_dir = os.path.dirname(os.path.abspath(bot_path))
    if bot_dir not in sys.path:
        sys.path.insert(0, bot_dir)
        
    # Dynamically import the bot file
    bot_name = os.path.basename(bot_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(bot_name, bot_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[bot_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error loading bot {bot_path}: {e}")
        return

    if not hasattr(module, 'get_move'):
        print(f"Error: Bot {bot_path} has no 'get_move' function.")
        return

    while True:
        try:
            # Wait for data from engine
            req = input_queue.get()
            if req == "STOP":
                break
            
            grid, my_pos, opp_pos, turn_info = req
            
            try:
                move = module.get_move(grid, my_pos, opp_pos, turn_info)
            except Exception as e:
                # If there's an error in runtime, fallback to REPOS
                print(f"Error executing bot {bot_path}: {e}")
                move = "REPOS"
            
            output_queue.put(move)
        except Exception as e:
            output_queue.put("REPOS")

class BotHandler:
    def __init__(self, bot_path):
        self.bot_path = bot_path
        self.ctx = multiprocessing.get_context('spawn')
        self.input_queue = self.ctx.Queue()
        self.output_queue = self.ctx.Queue()
        self.process = self.ctx.Process(target=bot_worker, args=(bot_path, self.input_queue, self.output_queue))
        self.process.start()
        
    def get_move(self, grid, my_pos, opp_pos, turn_info, timeout=0.100):
        # Clear output queue just in case there are left-overs from a previous timeout
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except:
                pass
            
        self.input_queue.put((grid, my_pos, opp_pos, turn_info))
        
        try:
            # We enforce a hard timeout based on multiprocessing Queue timeout argument
            move = self.output_queue.get(timeout=timeout)
            return str(move).upper()
        except multiprocessing.queues.Empty:
            return "REPOS"
            
    def close(self):
        try:
            self.input_queue.put("STOP")
        except:
            pass
        self.process.join(timeout=1)
        if self.process.is_alive():
            self.process.terminate()
