# Hangman Game – Built with Amazon Q CLI in Under 10 Minutes

A feature-rich Hangman game with fullscreen support, parallax scrolling background, multiple difficulty levels, and various word categories - created with the help of Amazon Q CLI under 10 minutes with single prompt.


https://github.com/user-attachments/assets/53b16713-5748-4199-bb5a-365b20df56c6



## About This Project

This Hangman game was developed using Python and Pygame, with assistance from Amazon Q CLI. It features a modern, responsive design with animated elements, multiple difficulty levels, and a variety of word categories to choose from.

## Game Features

- Three difficulty levels:
  - Easy: 8 lives, shorter words, no time limit
  - Medium: 6 lives, medium-length words, 2-minute time limit
  - Hard: 4 lives, longer/complex words, 1-minute time limit

- Six word categories:
  - Animals
  - Movies
  - Countries
  - Sports
  - Fruits
  - Cars

- Dynamic parallax background: Multi-layered scrolling background with trees, mountains, birds, and clouds that creates a sense of depth

- Animated hangman drawing: Progressive drawing that synchronizes with the number of lives remaining

- Responsive design: Adapts to different screen sizes with fullscreen support

- Sound effects: Audio feedback for correct/incorrect guesses and game outcomes

- Keyboard support: Use physical keyboard or on-screen buttons to make guesses

- Pause functionality: Pause the game at any time and resume when ready

## How to Play

1. Select a difficulty level (Easy, Medium, or Hard)
2. Choose a word category
3. Guess letters using your keyboard or the on-screen buttons
4. Try to guess the word before running out of lives!

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. Clone this repository:
   git clone https://github.com/jeraldmathewsjomy/hangman-game.git
   cd hangman-game

2. Install required packages:
   pip install -r requirements.txt

3. Run the game:
   python run.py

For detailed installation instructions for different operating systems, see INSTALL.md.

## Controls

- Mouse: Click buttons to navigate and select letters
- Keyboard: Type letters to make guesses during gameplay
- F11 or Alt+Enter: Toggle fullscreen mode
- ESC: Exit fullscreen or pause the game
- P: Toggle parallax animation (when not in gameplay)

## Created with Amazon Q CLI

This game was developed with assistance from Amazon Q CLI, an AI-powered assistant built by AWS that helps developers with coding tasks, answering questions, and providing recommendations.

### About Amazon Q CLI

Amazon Q CLI brings IDE-style autocomplete and agentic capabilities directly to your terminal, offering:
- Code suggestions and completions
- Answers to questions about AWS services and best practices
- Code snippet generation
- Debugging assistance
- Codebase exploration and understanding

## 🧠 Amazon Q CLI Setup

Amazon Q CLI is an AI-powered assistant that helps you code, debug, and build projects directly from your terminal.

### 🪟 Windows (via WSL - Recommended)

Amazon Q CLI doesn’t have a native Windows installer yet, but you can install it easily using WSL (Windows Subsystem for Linux).

#### Quick Installation Steps (WSL with Ubuntu):

```bash
# Launch Ubuntu via WSL
wsl -d Ubuntu

# Navigate to your home directory
cd

# Download Amazon Q CLI
curl --proto '=https' --tlsv1.2 -sSf https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip -o q.zip

# Install unzip if needed
sudo apt install unzip

# Unzip and install
unzip q.zip
cd q
chmod +x install.sh
./install.sh
```

🧠 Choose **"Use for Free with Builder ID"** and complete authentication in your browser.

✔️ After installation, start chatting:
```bash
q chat
```

---

### 🐧 Ubuntu / Linux

```bash
sudo apt update
sudo apt install python3 python3-pip unzip
curl --proto '=https' --tlsv1.2 -sSf https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip -o q.zip
unzip q.zip
cd q
chmod +x install.sh
./install.sh
q chat
```

---

### 🍏 macOS

```bash
brew install amazon-q
# OR
pip3 install amazon-q
aws configure
q chat
```

## Requirements

- Python 3.7 or later
- Pygame 2.5.2 or later

## 🧠 Prompt Used to Generate This Game

This fully working Hangman game was generated in under **10 minutes** using the following prompt in **Amazon Q CLI**:

```
Hi Amazon Q CLI, I want to build a fully working clone of my Hangman game that includes everything I had in my completed version. Please create the complete codebase for the game in Python using Pygame.

Here’s what I need in the game without missing any detail:

1. Classic Hangman gameplay with rules, lives, and win/lose conditions.
2. Category selection (Animals, Movies, Countries, Sports, Fruits, Cars), each with easy, medium, and hard difficulty (10 words each).
3. Difficulty levels with different lives and time limits:
   - Easy: 8 lives, no timer
   - Medium: 6 lives, 2-minute timer
   - Hard: 4 lives, 1-minute timer
4. On-screen and physical keyboard support with button states, input logic, and visual feedback.
5. Game flow from menu - difficulty - category - game screen - win/lose - restart or quit.
6. Scoring system that tracks wins/losses per session and displays them on game over screens.
7. Animated hangman drawing, with 10 parts shown based on wrong guesses.
8. Parallax animated background (sky, mountains, trees, birds, clouds) on menu screens.
9. Swinging hangman pendulum animation when player loses.
10. Clean UI design with centered layout, hover/click effects on buttons, “Press Start 2P” font, neon color scheme (dark background with vibrant neon buttons and text).
11. Word display with underscore for hidden letters and real-time letter reveal.
12. Color-coded timer with a countdown bar and visual urgency feedback (green > yellow > red).
13. Pause menu with resume/quit, activated by ESC key.
14. Fullscreen support, toggle with F or F11 keys.
15. Sound effects for correct, wrong, win, lose, and button clicks (sine-wave generated).
16. Visual effects like button flashes, overlays on win/loss/pause.
17. Responsive design that adjusts to any screen size.
18. No external image or audio assets, everything should be generated with code.
19. Use Python 3 and Pygame (with `pygame.freetype`), and standard libraries only.

Please write everything in a single project folder. Make sure it runs without errors. Provide the full working code with all modules, assets, and comments included.
```

> ✨ This prompt was executed using **Amazon Q CLI**, and the complete game was auto-generated from it!


## Acknowledgments

- This game was created using Amazon Q CLI as part of the [Build Games with Amazon Q CLI](https://community.aws/content/2xIoduO0xhkhUApQpVUIqBFGmAc/build-games-with-amazon-q-cli-and-score-a-t-shirt?lang=en) campaign.
- Pygame library for game development
- "Press Start 2P" font for the retro arcade feel
