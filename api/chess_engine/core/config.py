# config.py

import os

# Get the directory of the current file (config.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the project root
project_root = os.path.dirname(current_dir)

# Path to your trained model
MODEL_PATH = os.path.join(project_root, 'core', 'chess_evaluation_model_cnnpuzzles_legacy.keras')

# Other configuration variables
DEPTH = 1