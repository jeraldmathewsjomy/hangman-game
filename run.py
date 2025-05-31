#!/usr/bin/env python3
"""
Simple launcher script for the Hangman game.
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import pygame
        print(f"Pygame version {pygame.__version__} found.")
        return True
    except ImportError:
        print("Pygame not found. Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please install them manually:")
            print("pip install -r requirements.txt")
            return False

def main():
    """Run the Hangman game."""
    if not check_dependencies():
        return 1

    # Find the main game file
    if os.path.exists("hangman.py"):
        game_file = "hangman.py"
    elif os.path.exists("fullscreen_hangman_with_improved_parallax.py"):
        game_file = "fullscreen_hangman_with_improved_parallax.py"
    else:
        print("Error: Could not find the main game file.")
        return 1

    # Run the game
    print(f"Starting Hangman game from {game_file}...")
    os.execv(sys.executable, [sys.executable, game_file])
    return 0

if __name__ == "__main__":
    sys.exit(main())
