# Installation Instructions

This document provides instructions for installing and running the Hangman game on different operating systems.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. Open Command Prompt and navigate to the game directory:

  cd path\to\hangman-game


3. Install required packages:

  pip install -r requirements.txt


4. Run the game:

  python run.py


### macOS

1. Install Python if not already installed:

  brew install python


   or download from [python.org](https://www.python.org/downloads/)

2. Open Terminal and navigate to the game directory:


  cd path/to/hangman-game


3. Install required packages:

  pip3 install -r requirements.txt


4. Run the game:

  python3 run.py



### Linux (Ubuntu/Debian)

1. Install Python and pip if not already installed:


  sudo apt update
  sudo apt install python3 python3-pip


2. Install Pygame dependencies:

  sudo apt install python3-dev libsdl2-dev libsdl2-image-dev
libsdl2-mixer-dev libsdl2-ttf-dev


3. Navigate to the game directory:

  cd path/to/hangman-game


4. Install required packages:

  pip3 install -r requirements.txt


5. Run the game:

  python3 run.py



## Troubleshooting

If you encounter any issues:

1. Make sure Python is properly installed and in your PATH
2. Try installing Pygame directly:
pip install pygame>=2.5.2

3. Check that your Python version is 3.7 or higher: python --
version

4. For Linux users, ensure you have the necessary development libraries installed

## Controls

- Mouse: Click buttons to navigate and select letters
- Keyboard: Type letters to make guesses during gameplay
- F11 or Alt+Enter: Toggle fullscreen mode
- ESC: Exit fullscreen or pause the game
- P: Toggle parallax animation (when not in gameplay)
