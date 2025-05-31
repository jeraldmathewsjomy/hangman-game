#!/usr/bin/env python3
import pygame
import sys
import random
import os
import time
import math
import pygame.freetype

# Initialize pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Get the user's screen resolution
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Flag to track fullscreen state
fullscreen = False

# Enhanced color palette - neon/retro theme
DARK_BG = (25, 25, 35)       # Dark background
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
NEON_GREEN = (57, 255, 20)   # Bright green for correct guesses
NEON_PINK = (255, 20, 147)   # Bright pink for highlights
NEON_BLUE = (0, 195, 255)    # Bright blue for UI elements
NEON_YELLOW = (255, 255, 0)  # Bright yellow for emphasis
NEON_PURPLE = (180, 0, 255)  # Bright purple for accents
NEON_RED = (255, 50, 50)     # Bright red for wrong guesses
DARK_GRAY = (40, 40, 50)     # Darker gray for button base
BUTTON_BG = (60, 60, 80)     # Button background color
BUTTON_TEXT = (240, 240, 240) # Button text color - high contrast
GREEN = NEON_GREEN
RED = NEON_RED
BLUE = NEON_BLUE
YELLOW = NEON_YELLOW
PURPLE = NEON_PURPLE
TRANSPARENT = (0, 0, 0, 0)

# Additional colors for parallax background
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
TREE_GREEN = (0, 100, 0)
MOUNTAIN_GRAY = (100, 100, 100)
BROWN = (139, 69, 19)

# Font settings
FONT_COLOR = (240, 240, 240)  # High contrast font color

# Game settings
FPS = 60
GAME_TITLE = "Hangman Game"

# Default window size (for windowed mode)
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

# Create the screen - start in windowed mode
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Function to calculate scale factors based on current screen size
def get_scale_factors():
    current_w, current_h = screen.get_size()
    scale_x = current_w / DEFAULT_WIDTH
    scale_y = current_h / DEFAULT_HEIGHT
    return scale_x, scale_y

# Function to scale a value based on the x-axis scale factor
def scale_x(value):
    scale_x, _ = get_scale_factors()
    return int(value * scale_x)

# Function to scale a value based on the y-axis scale factor
def scale_y(value):
    _, scale_y = get_scale_factors()
    return int(value * scale_y)

# Function to scale both x and y values
def scale_pos(x, y):
    scale_x, scale_y = get_scale_factors()
    return int(x * scale_x), int(y * scale_y)

# Function to scale font size
def scale_font_size(size):
    _, scale_y = get_scale_factors()
    return max(int(size * scale_y), size)

# Load background image
background_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "background.png")
try:
    background_image = pygame.image.load(background_path)
    has_background = True
except:
    print(f"Could not load background image from {background_path}")
    has_background = False

# Function to scale background image to current screen size
def scale_background():
    if has_background:
        current_w, current_h = screen.get_size()
        return pygame.transform.scale(background_image, (current_w, current_h))
    return None

# Function to draw a tree
def draw_tree(surface, x, y, size):
    # Scale based on screen size
    x = scale_x(x)
    y = scale_y(y)
    size = scale_y(size)
    
    # Draw trunk
    trunk_width = size // 5
    trunk_height = size // 2
    trunk_rect = pygame.Rect(x - trunk_width // 2, y - trunk_height, trunk_width, trunk_height)
    pygame.draw.rect(surface, BROWN, trunk_rect)
    
    # Draw foliage (triangle)
    foliage_width = size
    foliage_height = size
    
    # Draw multiple triangles for a fuller tree
    for i in range(3):
        offset_y = i * (foliage_height // 4)
        points = [
            (x, y - trunk_height - foliage_height + offset_y),  # top
            (x - foliage_width // 2, y - trunk_height - foliage_height // 3 + offset_y),  # bottom left
            (x + foliage_width // 2, y - trunk_height - foliage_height // 3 + offset_y)   # bottom right
        ]
        pygame.draw.polygon(surface, TREE_GREEN, points)

# Function to draw a cloud
def draw_cloud(surface, x, y, size):
    # Scale based on screen size
    x = scale_x(x)
    y = scale_y(y)
    size = scale_y(size)
    
    # Draw multiple overlapping circles for a cloud shape
    pygame.draw.circle(surface, WHITE, (x, y), size)
    pygame.draw.circle(surface, WHITE, (x + size, y), int(size * 0.8))
    pygame.draw.circle(surface, WHITE, (x - size, y), int(size * 0.7))
    pygame.draw.circle(surface, WHITE, (x + size // 2, y - size // 2), int(size * 0.6))
    pygame.draw.circle(surface, WHITE, (x - size // 2, y - size // 2), int(size * 0.5))

# Function to draw a bird
def draw_bird(surface, x, y, size, flap_state):
    # Scale based on screen size
    x = scale_x(x)
    y = scale_y(y)
    size = scale_y(size)
    
    # Simple bird shape with flapping wings
    wing_angle = math.sin(flap_state) * 0.5  # Wing flap animation
    
    # Bird body
    pygame.draw.ellipse(surface, BLACK, (x - size // 2, y - size // 4, size, size // 2))
    
    # Bird head
    pygame.draw.circle(surface, BLACK, (x + size // 2 - size // 8, y - size // 4), size // 4)
    
    # Bird wings
    wing_points1 = [
        (x, y - size // 4),  # Wing joint
        (x - size // 2, y - size // 2 - int(size * wing_angle)),  # Wing tip
        (x, y)  # Wing back
    ]
    wing_points2 = [
        (x, y - size // 4),  # Wing joint
        (x + size // 2, y - size // 2 + int(size * wing_angle)),  # Wing tip
        (x, y)  # Wing back
    ]
    pygame.draw.polygon(surface, BLACK, wing_points1)
    pygame.draw.polygon(surface, BLACK, wing_points2)

# Function to draw a mountain
def draw_mountain(surface, x, y, width, height):
    # Scale based on screen size
    x = scale_x(x)
    y = scale_y(y)
    width = scale_x(width)
    height = scale_y(height)
    
    # Mountain shape
    points = [
        (x, y),  # base left
        (x + width // 2, y - height),  # peak
        (x + width, y)  # base right
    ]
    
    # Draw mountain with gradient
    pygame.draw.polygon(surface, MOUNTAIN_GRAY, points)
    
    # Add snow cap
    snow_points = [
        (x + width // 2, y - height),  # peak
        (x + width // 2 - width // 6, y - height + height // 5),
        (x + width // 2 + width // 6, y - height + height // 5)
    ]
    pygame.draw.polygon(surface, WHITE, snow_points)

# Function to draw a bush
def draw_bush(surface, x, y, size):
    # Scale based on screen size
    x = scale_x(x)
    y = scale_y(y)
    size = scale_y(size)
    
    # Draw multiple overlapping circles for a bush shape
    for i in range(5):
        offset_x = random.randint(-size // 2, size // 2)
        offset_y = random.randint(-size // 3, size // 3)
        pygame.draw.circle(surface, TREE_GREEN, (x + offset_x, y + offset_y), size // 2)

# Background element class
class BackgroundElement:
    def __init__(self, element_type, x, y, size, speed):
        self.element_type = element_type  # 'tree', 'cloud', 'bird', 'mountain', 'bush'
        self.base_x = x  # Store original positions for scaling
        self.base_y = y
        self.base_size = size
        self.speed = speed
        self.flap_state = random.random() * 6.28  # Random start position for bird wing flap
        
        # For mountains
        if element_type == 'mountain':
            self.width = size * 3
            self.height = size * 2
    
    def update(self):
        # Move element from right to left
        self.base_x -= self.speed
        
        # Reset position if it moves off screen
        if self.base_x < -self.base_size * 3:
            self.base_x = DEFAULT_WIDTH + self.base_size
            
        # Update bird wing flap animation
        if self.element_type == 'bird':
            self.flap_state += 0.2
    
    def draw(self, surface):
        # Draw the appropriate element type
        if self.element_type == 'tree':
            draw_tree(surface, self.base_x, self.base_y, self.base_size)
        elif self.element_type == 'cloud':
            draw_cloud(surface, self.base_x, self.base_y, self.base_size)
        elif self.element_type == 'bird':
            draw_bird(surface, self.base_x, self.base_y, self.base_size, self.flap_state)
        elif self.element_type == 'mountain':
            draw_mountain(surface, self.base_x, self.base_y, self.width, self.height)
        elif self.element_type == 'bush':
            draw_bush(surface, self.base_x, self.base_y, self.base_size)

# Improved parallax background class
class ImprovedParallaxBackground:
    def __init__(self):
        self.elements = []
        self.active = True
        
        # Create background elements
        self.create_elements()
    
    def create_elements(self):
        # Mountains (very slow)
        for i in range(5):
            mountain_size = random.randint(100, 200)
            mountain_x = random.randint(0, DEFAULT_WIDTH)
            mountain_y = int(DEFAULT_HEIGHT * 0.7)  # Ground level
            self.elements.append(BackgroundElement('mountain', mountain_x, mountain_y, mountain_size, 0.2))
        
        # Far trees (slow)
        for i in range(15):
            tree_size = random.randint(50, 80)
            tree_x = random.randint(0, DEFAULT_WIDTH)
            tree_y = int(DEFAULT_HEIGHT * 0.7)  # Ground level
            self.elements.append(BackgroundElement('tree', tree_x, tree_y, tree_size, 0.5))
        
        # Bushes (medium speed)
        for i in range(10):
            bush_size = random.randint(20, 40)
            bush_x = random.randint(0, DEFAULT_WIDTH)
            bush_y = int(DEFAULT_HEIGHT * 0.7) + bush_size // 2  # Ground level
            self.elements.append(BackgroundElement('bush', bush_x, bush_y, bush_size, 1))
        
        # Medium trees (medium speed)
        for i in range(10):
            tree_size = random.randint(80, 120)
            tree_x = random.randint(0, DEFAULT_WIDTH)
            tree_y = int(DEFAULT_HEIGHT * 0.7)  # Ground level
            self.elements.append(BackgroundElement('tree', tree_x, tree_y, tree_size, 1.5))
        
        # Near trees (fast)
        for i in range(8):
            tree_size = random.randint(120, 180)
            tree_x = random.randint(0, DEFAULT_WIDTH)
            tree_y = int(DEFAULT_HEIGHT * 0.7)  # Ground level
            self.elements.append(BackgroundElement('tree', tree_x, tree_y, tree_size, 2.5))
        
        # Clouds (very slow)
        for i in range(8):
            cloud_size = random.randint(20, 40)
            cloud_x = random.randint(0, DEFAULT_WIDTH)
            cloud_y = random.randint(50, int(DEFAULT_HEIGHT * 0.4))
            self.elements.append(BackgroundElement('cloud', cloud_x, cloud_y, cloud_size, 0.3))
        
        # Birds (medium speed)
        for i in range(5):
            bird_size = random.randint(15, 30)
            bird_x = random.randint(0, DEFAULT_WIDTH)
            bird_y = random.randint(100, int(DEFAULT_HEIGHT * 0.5))
            self.elements.append(BackgroundElement('bird', bird_x, bird_y, bird_size, 1.8))
        
        # Sort elements by speed (for proper layering)
        self.elements.sort(key=lambda x: x.speed)
    
    def update(self):
        if not self.active:
            return
            
        # Update all elements
        for element in self.elements:
            element.update()
    
    def draw(self, surface):
        # Draw sky
        sky_rect = pygame.Rect(0, 0, surface.get_width(), scale_y(DEFAULT_HEIGHT * 0.7))
        pygame.draw.rect(surface, SKY_BLUE, sky_rect)
        
        # Draw ground
        ground_rect = pygame.Rect(0, scale_y(DEFAULT_HEIGHT * 0.7), surface.get_width(), surface.get_height() - scale_y(DEFAULT_HEIGHT * 0.7))
        pygame.draw.rect(surface, GROUND_GREEN, ground_rect)
        
        # Draw all elements in order (background to foreground)
        for element in self.elements:
            element.draw(surface)
    
    def toggle(self):
        self.active = not self.active
    
    def resize(self):
        # No specific resize needed as all drawing functions use scale_x and scale_y
        pass
# Try to load a pixel/arcade style font
try:
    # Check for the Press Start 2P font first (a pixel font perfect for games)
    press_start_font = os.path.join(os.path.expanduser("~"), "fonts", "PressStart2P-Regular.ttf")
    if os.path.exists(press_start_font):
        # Create font loading function that considers screen scaling
        def get_title_font():
            return pygame.font.Font(press_start_font, scale_font_size(36))
        def get_large_font():
            return pygame.font.Font(press_start_font, scale_font_size(24))
        def get_medium_font():
            return pygame.font.Font(press_start_font, scale_font_size(16))
        def get_small_font():
            return pygame.font.Font(press_start_font, scale_font_size(12))
        print("Using Press Start 2P font")
    else:
        # Check if a pixel font exists in the directory
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pixel_font.ttf")
        if os.path.exists(font_path):
            def get_title_font():
                return pygame.font.Font(font_path, scale_font_size(48))
            def get_large_font():
                return pygame.font.Font(font_path, scale_font_size(36))
            def get_medium_font():
                return pygame.font.Font(font_path, scale_font_size(28))
            def get_small_font():
                return pygame.font.Font(font_path, scale_font_size(20))
        else:
            # Fall back to system fonts with bold style for arcade feel
            def get_title_font():
                return pygame.font.SysFont('Arial', scale_font_size(48), bold=True)
            def get_large_font():
                return pygame.font.SysFont('Arial', scale_font_size(36), bold=True)
            def get_medium_font():
                return pygame.font.SysFont('Arial', scale_font_size(28), bold=True)
            def get_small_font():
                return pygame.font.SysFont('Arial', scale_font_size(20), bold=True)
except:
    # Fallback if font loading fails
    def get_title_font():
        return pygame.font.SysFont('Arial', scale_font_size(48), bold=True)
    def get_large_font():
        return pygame.font.SysFont('Arial', scale_font_size(36), bold=True)
    def get_medium_font():
        return pygame.font.SysFont('Arial', scale_font_size(28), bold=True)
    def get_small_font():
        return pygame.font.SysFont('Arial', scale_font_size(20), bold=True)

# Sound effects
def create_beep_sound(frequency, duration, volume=0.3):
    """Create a simple beep sound with the given frequency and duration"""
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate))
    
    # Generate a numpy array of sound samples
    buf = pygame.mixer.Sound(buffer=bytes(bytearray(
        int(32767.0 * volume * math.sin(2.0 * math.pi * frequency * i / sample_rate))
        & 0xFF for i in range(n_samples)
    )))
    return buf

# Create sound effects
correct_sound = create_beep_sound(440, 0.2)  # Higher pitched beep for correct guess
wrong_sound = create_beep_sound(220, 0.3)    # Lower pitched beep for wrong guess
win_sound = create_beep_sound(880, 0.5)      # High pitched beep for win
lose_sound = create_beep_sound(110, 0.7)     # Low pitched beep for lose
click_sound = create_beep_sound(660, 0.1)    # Medium pitched short beep for clicks
# Game data - categorized by difficulty
categories = {
    "Animals": {
        "easy": ["dog", "cat", "pig", "fox", "cow", "rat", "bat", "hen", "bee", "ant"],
        "medium": ["tiger", "zebra", "koala", "panda", "camel", "eagle", "shark", "snake", "horse", "sheep"],
        "hard": ["elephant", "giraffe", "penguin", "kangaroo", "dolphin", "rhinoceros", "crocodile", "octopus", "cheetah", "panther"]
    },
    "Movies": {
        "easy": ["jaws", "star", "cars", "up", "toy", "lion", "wall", "bolt", "soul", "nemo"],
        "medium": ["frozen", "avatar", "matrix", "aliens", "psycho", "shrek", "titanic", "batman", "joker", "rocky"],
        "hard": ["inception", "gladiator", "interstellar", "casablanca", "godfather", "parasite", "whiplash", "braveheart", "goodfellas", "apocalypse"]
    },
    "Countries": {
        "easy": ["usa", "cuba", "peru", "mali", "fiji", "iran", "iraq", "chad", "togo", "laos"],
        "medium": ["japan", "india", "china", "spain", "italy", "kenya", "egypt", "chile", "sudan", "nepal"],
        "hard": ["australia", "argentina", "singapore", "switzerland", "kazakhstan", "mozambique", "bangladesh", "madagascar", "azerbaijan", "kyrgyzstan"]
    },
    "Sports": {
        "easy": ["golf", "swim", "run", "ski", "surf", "bike", "judo", "yoga", "polo", "bowl"],
        "medium": ["soccer", "tennis", "hockey", "boxing", "karate", "rowing", "diving", "cricket", "cycling", "fencing"],
        "hard": ["basketball", "volleyball", "gymnastics", "wrestling", "badminton", "skateboard", "snowboard", "waterpolo", "taekwondo", "equestrian"]
    },
    "Fruits": {
        "easy": ["pear", "plum", "lime", "kiwi", "fig", "date", "apple", "grape", "melon", "mango"],
        "medium": ["orange", "banana", "cherry", "papaya", "guava", "lychee", "apricot", "peach", "lemon", "coconut"],
        "hard": ["pineapple", "watermelon", "strawberry", "blueberry", "blackberry", "raspberry", "cranberry", "dragonfruit", "passionfruit", "pomegranate"]
    },
    "Cars": {
        "easy": ["ford", "audi", "jeep", "kia", "mini", "seat", "fiat", "bmw", "saab", "opel"],
        "medium": ["toyota", "nissan", "honda", "mazda", "subaru", "volvo", "lexus", "jaguar", "tesla", "porsche"],
        "hard": ["mercedes", "lamborghini", "maserati", "bentley", "ferrari", "bugatti", "chevrolet", "mitsubishi", "volkswagen", "rolls-royce"]
    }
}

# Game states
STATE_MENU = 0
STATE_DIFFICULTY = 1
STATE_CATEGORY = 2
STATE_GAME = 3
STATE_WIN = 4
STATE_LOSE = 5
STATE_PAUSE = 6  # New pause state

# Difficulty levels
DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BUTTON_TEXT, font_func=get_medium_font, button_type="default"):
        self.base_x = x  # Store original positions for scaling
        self.base_y = y
        self.base_width = width
        self.base_height = height
        self.text = text
        self.button_type = button_type
        
        # Set colors based on button type
        if button_type == "play":
            self.color = NEON_GREEN
            self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        elif button_type == "hint":
            self.color = NEON_BLUE
            self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        elif button_type == "reset":
            self.color = NEON_RED
            self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        else:
            self.color = color
            self.hover_color = hover_color
            
        self.text_color = text_color
        self.font_func = font_func
        self.is_hovered = False
        self.is_disabled = False
        self.click_effect = 0  # For click animation
        
        # Update the rect based on current scale
        self.update_rect()
    
    def update_rect(self):
        """Update button rectangle based on current screen scale"""
        x = scale_x(self.base_x)
        y = scale_y(self.base_y)
        width = scale_x(self.base_width)
        height = scale_y(self.base_height)
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, surface):
        # Update rect in case screen has been resized
        self.update_rect()
        
        # Determine button color based on state
        if self.is_disabled:
            color = DARK_GRAY  # Disabled color
        else:
            color = self.hover_color if self.is_hovered else self.color
        
        # Create button shadow for depth
        shadow_rect = self.rect.copy()
        shadow_rect.x += scale_x(4)
        shadow_rect.y += scale_y(4)
        pygame.draw.rect(surface, (0, 0, 0, 128), shadow_rect, border_radius=scale_y(15))
        
        # Draw button with rounded corners
        pygame.draw.rect(surface, color, self.rect, border_radius=scale_y(15))
        
        # Add a glowing border effect when hovered
        if self.is_hovered and not self.is_disabled:
            glow_rect = self.rect.copy()
            glow_rect.inflate_ip(scale_x(4), scale_y(4))
            pygame.draw.rect(surface, NEON_YELLOW, glow_rect, scale_y(3), border_radius=scale_y(17))
        else:
            # Regular border
            pygame.draw.rect(surface, (255, 255, 255, 150), self.rect, scale_y(2), border_radius=scale_y(15))
        
        # Click animation effect
        if self.click_effect > 0:
            click_rect = self.rect.copy()
            click_rect.inflate_ip(-self.click_effect * scale_x(4), -self.click_effect * scale_y(4))
            pygame.draw.rect(surface, (255, 255, 255, 100), click_rect, border_radius=scale_y(15))
            self.click_effect -= 0.2
            if self.click_effect <= 0:
                self.click_effect = 0
        
        # Render text with slight offset for pressed effect when clicked
        # Add text shadow for better visibility
        font = self.font_func()
        shadow_offset = scale_y(1)
        text_shadow = font.render(self.text, True, BLACK)
        text_shadow_rect = text_shadow.get_rect(center=self.rect.center)
        text_shadow_rect.x += shadow_offset
        text_shadow_rect.y += shadow_offset
        
        if self.click_effect > 0:
            text_shadow_rect.y += scale_y(2)  # Move shadow down slightly when clicked
        
        surface.blit(text_shadow, text_shadow_rect)
        
        # Render main text
        text_surface = font.render(self.text, True, self.text_color if not self.is_disabled else (100, 100, 100))
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        if self.click_effect > 0:
            text_rect.y += scale_y(2)  # Move text down slightly when clicked
            
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        if not self.is_disabled:
            self.is_hovered = self.rect.collidepoint(pos)
        else:
            self.is_hovered = False
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.is_disabled:
            if self.rect.collidepoint(pos):
                self.click_effect = 5  # Start click animation
                click_sound.play()  # Play click sound
                return True
        return False
class HangmanAnimation:
    def __init__(self):
        # Animation parameters
        self.animation_speed = 5  # pixels per frame
        self.current_part = 0
        self.animating = False
        self.animation_progress = 0
        
        # Pendulum swing animation parameters
        self.swinging = False
        self.swing_angle = 0
        self.max_swing_angle = math.pi / 6  # 30 degrees
        self.swing_speed = 0.1
        self.swing_damping = 0.98  # Damping factor to slow down swing
        self.swing_direction = 1
        self.swing_time = 0
        self.swing_duration = 3.0  # seconds
        
        # Define the hangman parts for animation - using base positions that will be scaled
        self.parts = [
            {"type": "line", "start": (150, 400), "end": (250, 400), "thickness": 10},  # Base
            {"type": "line", "start": (200, 400), "end": (200, 100), "thickness": 10},  # Pole
            {"type": "line", "start": (200, 100), "end": (300, 100), "thickness": 10},  # Top
            {"type": "line", "start": (300, 100), "end": (300, 150), "thickness": 10},  # Rope
            {"type": "circle", "center": (300, 180), "radius": 30, "thickness": 3},     # Head
            {"type": "line", "start": (300, 210), "end": (300, 290), "thickness": 3},   # Body
            {"type": "line", "start": (300, 230), "end": (260, 260), "thickness": 3},   # Left arm
            {"type": "line", "start": (300, 230), "end": (340, 260), "thickness": 3},   # Right arm
            {"type": "line", "start": (300, 290), "end": (260, 340), "thickness": 3},   # Left leg
            {"type": "line", "start": (300, 290), "end": (340, 340), "thickness": 3}    # Right leg
        ]
        
        # Pivot point for swinging (top of rope)
        self.pivot_point = (300, 100)
        
        # Scaffold parts (always drawn)
        self.scaffold_parts = 4
        
        # Wrong guess parts (drawn based on wrong guesses)
        self.wrong_parts = 6
        
        # Animation state for each part
        self.part_animations = [{"complete": False, "progress": 0} for _ in range(len(self.parts))]
        
        # Complete the scaffold parts initially
        for i in range(self.scaffold_parts):
            self.part_animations[i]["complete"] = True
            self.part_animations[i]["progress"] = 1.0
    
    def start_animation(self, part_index):
        """Start animating a specific part"""
        if part_index < len(self.parts) and not self.part_animations[part_index]["complete"]:
            self.current_part = part_index
            self.animating = True
            self.animation_progress = 0
    
    def start_swing_animation(self):
        """Start the pendulum swing animation"""
        self.swinging = True
        self.swing_angle = self.max_swing_angle  # Start at maximum angle
        self.swing_time = 0
    
    def update(self):
        """Update the animation state"""
        # Update part drawing animations
        if self.animating:
            part = self.parts[self.current_part]
            anim_state = self.part_animations[self.current_part]
            
            if part["type"] == "line":
                # For lines, progress from start to end
                anim_state["progress"] += 0.02
                if anim_state["progress"] >= 1.0:
                    anim_state["progress"] = 1.0
                    anim_state["complete"] = True
                    self.animating = False
            
            elif part["type"] == "circle":
                # For circles, progress through the arc
                anim_state["progress"] += 0.02
                if anim_state["progress"] >= 1.0:
                    anim_state["progress"] = 1.0
                    anim_state["complete"] = True
                    self.animating = False
        
        # Update pendulum swing animation
        if self.swinging:
            self.swing_time += 1/60  # Assuming 60 FPS
            
            # Calculate swing angle using damped harmonic motion
            # A * e^(-damping * t) * cos(frequency * t)
            damping_factor = math.exp(-1.5 * self.swing_time / self.swing_duration)
            self.swing_angle = self.max_swing_angle * damping_factor * math.cos(4 * self.swing_time)
            
            # Stop swinging when amplitude becomes very small
            if damping_factor < 0.05:
                self.swinging = False
                self.swing_angle = 0
    
    def draw(self, surface, wrong_guesses):
        """Draw the hangman with animations"""
        # Draw scaffold parts (always visible)
        for i in range(self.scaffold_parts):
            self.draw_part(surface, i)
        
        # If we have body parts to draw and we're swinging, draw the swinging hangman
        if wrong_guesses > 0 and self.swinging and all(self.part_animations[i]["complete"] for i in range(self.scaffold_parts, self.scaffold_parts + min(wrong_guesses, self.wrong_parts))):
            self.draw_swinging_hangman(surface, wrong_guesses)
        else:
            # Draw wrong guess parts based on wrong guesses
            for i in range(self.scaffold_parts, self.scaffold_parts + min(wrong_guesses, self.wrong_parts)):
                # Start animation for this part if not already animating or complete
                if not self.part_animations[i]["complete"] and not self.animating:
                    self.start_animation(i)
                
                # Draw the part with current animation progress
                self.draw_part(surface, i)
    
    def draw_part(self, surface, part_index):
        """Draw a specific part with animation"""
        if part_index >= len(self.parts):
            return
            
        part = self.parts[part_index]
        anim_state = self.part_animations[part_index]
        progress = anim_state["progress"]
        
        if part["type"] == "line":
            # Scale the coordinates
            start_x, start_y = scale_pos(part["start"][0], part["start"][1])
            end_x, end_y = scale_pos(part["end"][0], part["end"][1])
            thickness = scale_y(part["thickness"])
            
            # Calculate the end point based on animation progress
            current_end_x = start_x + (end_x - start_x) * progress
            current_end_y = start_y + (end_y - start_y) * progress
            
            pygame.draw.line(surface, BLACK, (start_x, start_y), (current_end_x, current_end_y), thickness)
            
        elif part["type"] == "circle" and progress > 0:
            # Scale the coordinates and radius
            center_x, center_y = scale_pos(part["center"][0], part["center"][1])
            radius = scale_y(part["radius"])
            thickness = scale_y(part["thickness"])
            
            # Draw circle with arc based on progress
            if progress < 1.0:
                # Draw partial circle (arc)
                rect = pygame.Rect(
                    center_x - radius, 
                    center_y - radius,
                    radius * 2, 
                    radius * 2
                )
                # Arc from 0 to progress * 360 degrees
                pygame.draw.arc(surface, BLACK, rect, 0, progress * 2 * math.pi, thickness)
            else:
                # Draw complete circle
                pygame.draw.circle(surface, BLACK, (center_x, center_y), radius, thickness)
                
    def draw_swinging_hangman(self, surface, wrong_guesses):
        """Draw the hangman figure swinging like a pendulum"""
        # Scale the pivot point
        pivot_x, pivot_y = scale_pos(self.pivot_point[0], self.pivot_point[1])
        
        # Calculate the rope length
        rope_length = scale_y(50)  # Length from pivot to head center
        
        # Calculate the position of the head based on swing angle
        head_x = pivot_x + rope_length * math.sin(self.swing_angle)
        head_y = pivot_y + rope_length * math.cos(self.swing_angle)
        
        # Draw the rope
        pygame.draw.line(surface, BLACK, (pivot_x, pivot_y), (head_x, head_y), scale_y(3))
        
        # Draw the head (circle)
        pygame.draw.circle(surface, BLACK, (int(head_x), int(head_y)), scale_y(30), scale_y(3))
        
        # Only draw body parts if they should be visible based on wrong guesses
        if wrong_guesses >= 2:  # Body
            body_length = scale_y(80)
            body_x = head_x
            body_y = head_y + scale_y(30)  # 30 is head radius
            body_end_x = head_x + body_length * math.sin(self.swing_angle)
            body_end_y = head_y + scale_y(30) + body_length * math.cos(self.swing_angle)
            pygame.draw.line(surface, BLACK, (body_x, body_y), (body_end_x, body_end_y), scale_y(3))
            
            if wrong_guesses >= 3:  # Left arm
                arm_length = scale_y(40)
                arm_angle = self.swing_angle - math.pi/4  # 45 degrees left
                arm_x = head_x + scale_y(20) * math.sin(self.swing_angle)  # Offset from body
                arm_y = head_y + scale_y(50) * math.cos(self.swing_angle)  # Offset from head
                arm_end_x = arm_x + arm_length * math.sin(arm_angle)
                arm_end_y = arm_y + arm_length * math.cos(arm_angle)
                pygame.draw.line(surface, BLACK, (arm_x, arm_y), (arm_end_x, arm_end_y), scale_y(3))
            
            if wrong_guesses >= 4:  # Right arm
                arm_length = scale_y(40)
                arm_angle = self.swing_angle + math.pi/4  # 45 degrees right
                arm_x = head_x + scale_y(20) * math.sin(self.swing_angle)  # Offset from body
                arm_y = head_y + scale_y(50) * math.cos(self.swing_angle)  # Offset from head
                arm_end_x = arm_x + arm_length * math.sin(arm_angle)
                arm_end_y = arm_y + arm_length * math.cos(arm_angle)
                pygame.draw.line(surface, BLACK, (arm_x, arm_y), (arm_end_x, arm_end_y), scale_y(3))
            
            if wrong_guesses >= 5:  # Left leg
                leg_length = scale_y(50)
                leg_angle = self.swing_angle - math.pi/8  # Slight angle left
                leg_x = body_end_x
                leg_y = body_end_y
                leg_end_x = leg_x + leg_length * math.sin(leg_angle)
                leg_end_y = leg_y + leg_length * math.cos(leg_angle)
                pygame.draw.line(surface, BLACK, (leg_x, leg_y), (leg_end_x, leg_end_y), scale_y(3))
            
            if wrong_guesses >= 6:  # Right leg
                leg_length = scale_y(50)
                leg_angle = self.swing_angle + math.pi/8  # Slight angle right
                leg_x = body_end_x
                leg_y = body_end_y
                leg_end_x = leg_x + leg_length * math.sin(leg_angle)
                leg_end_y = leg_y + leg_length * math.cos(leg_angle)
                pygame.draw.line(surface, BLACK, (leg_x, leg_y), (leg_end_x, leg_end_y), scale_y(3))
class HangmanGame:
    def __init__(self):
        self.state = STATE_MENU
        self.category = None
        self.word = ""
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.wins = 0
        self.losses = 0
        self.difficulty = DIFFICULTY_EASY
        self.timer_enabled = False
        self.timer_start = 0
        self.timer_duration = 0  # in seconds
        self.time_remaining = 0
        self.previous_state = None  # For pause menu to return to previous state
        
        # Create improved parallax background
        self.parallax_background = ImprovedParallaxBackground()
        
        # Create hangman animation
        self.hangman_animation = HangmanAnimation()
        
        # Helper function to calculate button width based on text
        def calculate_button_width(text, font_func, min_width=120, padding=40):
            font = font_func()
            text_width = font.size(text)[0]
            return max(min_width, text_width + padding)
        
        # Create menu buttons with dynamic width
        play_width = calculate_button_width("Play Game", get_medium_font, 200)
        quit_width = calculate_button_width("Quit", get_medium_font, 200)
        menu_button_width = max(play_width, quit_width)
        
        self.menu_buttons = [
            Button(DEFAULT_WIDTH//2 - menu_button_width//2, 200, menu_button_width, 60, "Play Game", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(DEFAULT_WIDTH//2 - menu_button_width//2, 300, menu_button_width, 60, "Quit", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font)
        ]
        
        # Create difficulty buttons with dynamic width
        easy_width = calculate_button_width("Easy", get_medium_font, 200)
        medium_width = calculate_button_width("Medium", get_medium_font, 200)
        hard_width = calculate_button_width("Hard", get_medium_font, 200)
        diff_button_width = max(easy_width, medium_width, hard_width)
        
        self.difficulty_buttons = [
            Button(DEFAULT_WIDTH//2 - diff_button_width//2, 150, diff_button_width, 60, "Easy", BUTTON_BG, (100, 255, 100), BUTTON_TEXT, get_medium_font),
            Button(DEFAULT_WIDTH//2 - diff_button_width//2, 250, diff_button_width, 60, "Medium", BUTTON_BG, (255, 255, 100), BUTTON_TEXT, get_medium_font),
            Button(DEFAULT_WIDTH//2 - diff_button_width//2, 350, diff_button_width, 60, "Hard", BUTTON_BG, (255, 100, 100), BUTTON_TEXT, get_medium_font)
        ]
        
        # Create back button for difficulty screen
        back_width = calculate_button_width("Back", get_medium_font, 100)
        self.back_button = Button(50, DEFAULT_HEIGHT - 80, back_width, 50, "Back", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font)
        
        # Create category buttons with dynamic width and better spacing
        category_names = ["Animals", "Movies", "Countries", "Sports", "Fruits", "Cars"]
        category_widths = [calculate_button_width(name, get_medium_font, 140) for name in category_names]
        max_category_width = max(category_widths)
        button_gap = 30  # Gap between buttons
        
        # Calculate total width needed for two buttons plus gap
        total_width = max_category_width * 2 + button_gap
        left_start = DEFAULT_WIDTH//2 - total_width//2
        right_start = left_start + max_category_width + button_gap
        
        self.category_buttons = [
            Button(left_start, 120, max_category_width, 50, "Animals", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(right_start, 120, max_category_width, 50, "Movies", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(left_start, 190, max_category_width, 50, "Countries", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(right_start, 190, max_category_width, 50, "Sports", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(left_start, 260, max_category_width, 50, "Fruits", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(right_start, 260, max_category_width, 50, "Cars", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font)
        ]
        
        # Create keyboard buttons with better spacing - REDUCED SIZE
        self.keyboard_buttons = []
        letters = "abcdefghijklmnopqrstuvwxyz"
        
        # Calculate optimal button size based on screen width and font - SMALLER BUTTONS
        button_width = 35  # Reduced from 45
        button_height = 35  # Reduced from 45
        button_margin = 6   # Reduced from 8
        
        # First row (a-m) - 13 letters
        row1_letters = letters[:13]
        total_row1_width = (button_width + button_margin) * len(row1_letters) - button_margin
        x_start = (DEFAULT_WIDTH - total_row1_width) // 2
        y_pos = DEFAULT_HEIGHT - 120  # Moved up more
        
        for i, letter in enumerate(row1_letters):
            x = x_start + i * (button_width + button_margin)
            self.keyboard_buttons.append(Button(x, y_pos, button_width, button_height, letter, BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_small_font))
        
        # Second row (n-z) - 13 letters
        row2_letters = letters[13:]
        total_row2_width = (button_width + button_margin) * len(row2_letters) - button_margin
        x_start = (DEFAULT_WIDTH - total_row2_width) // 2
        y_pos = DEFAULT_HEIGHT - 75  # Moved up slightly
        
        for i, letter in enumerate(row2_letters):
            x = x_start + i * (button_width + button_margin)
            self.keyboard_buttons.append(Button(x, y_pos, button_width, button_height, letter, BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_small_font))
        
        # Game over buttons with dynamic width
        play_again_width = calculate_button_width("Play Again", get_medium_font, 140)
        main_menu_width = calculate_button_width("Main Menu", get_medium_font, 140)
        game_over_button_width = max(play_again_width, main_menu_width)
        button_gap = 30  # Gap between buttons
        
        # Calculate positions for centered buttons with proper gap
        total_width = game_over_button_width * 2 + button_gap
        left_start = DEFAULT_WIDTH//2 - total_width//2
        right_start = left_start + game_over_button_width + button_gap
        
        self.game_over_buttons = [
            Button(left_start, DEFAULT_HEIGHT - 100, game_over_button_width, 50, "Play Again", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font),
            Button(right_start, DEFAULT_HEIGHT - 100, game_over_button_width, 50, "Main Menu", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font)
        ]
        
        # Create pause button for game screen - positioned at bottom left corner
        self.pause_button = Button(10, DEFAULT_HEIGHT - 50, 40, 40, "||", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_medium_font)
        
        # Create pause menu buttons
        continue_width = calculate_button_width("Continue", get_medium_font, 200)
        quit_width = calculate_button_width("Quit to Menu", get_medium_font, 200)
        pause_button_width = max(continue_width, quit_width)
        
        self.pause_menu_buttons = [
            Button(DEFAULT_WIDTH//2 - pause_button_width//2, 200, pause_button_width, 60, "Continue", BUTTON_BG, (100, 255, 100), BUTTON_TEXT, get_medium_font),
            Button(DEFAULT_WIDTH//2 - pause_button_width//2, 300, pause_button_width, 60, "Quit to Menu", BUTTON_BG, (255, 100, 100), BUTTON_TEXT, get_medium_font)
        ]
        
        # Add fullscreen toggle button - positioned in bottom right corner
        self.fullscreen_button = Button(DEFAULT_WIDTH - 50, DEFAULT_HEIGHT - 50, 40, 40, "F", BUTTON_BG, (80, 80, 100), BUTTON_TEXT, get_small_font)
    def start_new_game(self, category_name):
        self.category = category_name
        
        # Select word based on difficulty
        if self.difficulty == DIFFICULTY_EASY:
            difficulty_key = "easy"
            self.max_wrong_guesses = 8  # More guesses for easy mode
            self.timer_enabled = False
        elif self.difficulty == DIFFICULTY_MEDIUM:
            difficulty_key = "medium"
            self.max_wrong_guesses = 6  # Standard guesses for medium
            self.timer_enabled = True
            self.timer_duration = 120  # 2 minutes for medium
        else:  # Hard
            difficulty_key = "hard"
            self.max_wrong_guesses = 4  # Fewer guesses for hard mode
            self.timer_enabled = True
            self.timer_duration = 60  # 1 minute for hard
        
        # Get word from appropriate difficulty level
        self.word = random.choice(categories[category_name][difficulty_key]).lower()
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.state = STATE_GAME
        
        # Start timer if enabled
        if self.timer_enabled:
            self.timer_start = time.time()
            self.time_remaining = self.timer_duration
        
        # Reset hangman animation
        self.hangman_animation = HangmanAnimation()
        
        # Reset keyboard buttons
        for button in self.keyboard_buttons:
            button.color = BUTTON_BG
            button.is_hovered = False
            button.is_disabled = False
            button.text_color = BUTTON_TEXT
    
    def guess_letter(self, letter):
        if letter not in self.guessed_letters:
            self.guessed_letters.append(letter)
            
            # Update keyboard button color and state
            for button in self.keyboard_buttons:
                if button.text == letter:
                    button.is_disabled = True
                    if letter in self.word:
                        button.color = GREEN  # Use NEON_GREEN for correct guesses
                        button.text_color = BLACK  # Black text on green for better visibility
                        correct_sound.play()  # Play correct sound
                    else:
                        button.color = RED  # Use NEON_RED for wrong guesses
                        button.text_color = WHITE  # White text on red for better visibility
                        wrong_sound.play()  # Play wrong sound
                        self.wrong_guesses += 1
            
            # Check if game is lost
            if self.wrong_guesses >= self.max_wrong_guesses:
                self.state = STATE_LOSE
                self.losses += 1
                lose_sound.play()  # Play lose sound
            
            # Check if game is won
            elif all(letter in self.guessed_letters for letter in self.word):
                self.state = STATE_WIN
                self.wins += 1
                win_sound.play()  # Play win sound
    def draw_word(self):
        word_display = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                word_display += letter + " "
            else:
                word_display += "_ "
        
        # Draw text shadow for better visibility
        shadow_text = get_large_font().render(word_display, True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(450) + scale_y(2)))
        screen.blit(shadow_text, shadow_rect)
        
        # Draw the text
        text = get_large_font().render(word_display, True, NEON_BLUE)
        text_rect = text.get_rect(center=(screen.get_width()//2, scale_y(450)))
        screen.blit(text, text_rect)
    
    def draw_menu(self):
        # Draw title with shadow for better visibility
        shadow_offset = scale_y(2)
        title_shadow = get_title_font().render("HANGMAN GAME", True, BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(screen.get_width()//2 + shadow_offset, scale_y(100) + shadow_offset))
        screen.blit(title_shadow, title_shadow_rect)
        
        title = get_title_font().render("HANGMAN GAME", True, PURPLE)
        title_rect = title.get_rect(center=(screen.get_width()//2, scale_y(100)))
        screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(screen)
            
        # Draw fullscreen toggle button
        self.fullscreen_button.draw(screen)
    
    def draw_difficulty_selection(self):
        # Draw title with shadow
        shadow_offset = scale_y(2)
        title_shadow = get_title_font().render("SELECT DIFFICULTY", True, BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(screen.get_width()//2 + shadow_offset, scale_y(80) + shadow_offset))
        screen.blit(title_shadow, title_shadow_rect)
        
        title = get_title_font().render("SELECT DIFFICULTY", True, BLUE)
        title_rect = title.get_rect(center=(screen.get_width()//2, scale_y(80)))
        screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.difficulty_buttons:
            button.draw(screen)
            
        # Draw difficulty descriptions with proper spacing
        descriptions = [
            "Easier words, 8 lives, no time limit",
            "Medium words, 6 lives, 2 minute limit",
            "Hard words, 4 lives, 1 minute limit"
        ]
        
        # Calculate positions based on button positions
        for i, desc in enumerate(descriptions):
            # Get the corresponding button's position
            button = self.difficulty_buttons[i]
            button_bottom = button.rect.bottom
            
            # Add shadow for better visibility
            desc_shadow = get_small_font().render(desc, True, BLACK)
            desc_shadow_rect = desc_shadow.get_rect(center=(screen.get_width()//2 + scale_x(1), button_bottom + scale_y(25) + scale_y(1)))
            screen.blit(desc_shadow, desc_shadow_rect)
            
            # Draw the description text with consistent spacing from button
            desc_text = get_small_font().render(desc, True, WHITE)
            desc_rect = desc_text.get_rect(center=(screen.get_width()//2, button_bottom + scale_y(25)))
            screen.blit(desc_text, desc_rect)
        
        # Draw back button
        self.back_button.draw(screen)
            
        # Draw fullscreen toggle button
        self.fullscreen_button.draw(screen)
    
    def draw_category_selection(self):
        # Draw title with shadow
        shadow_offset = scale_y(2)
        title_shadow = get_title_font().render("SELECT CATEGORY", True, BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(screen.get_width()//2 + shadow_offset, scale_y(80) + shadow_offset))
        screen.blit(title_shadow, title_shadow_rect)
        
        title = get_title_font().render("SELECT CATEGORY", True, BLUE)
        title_rect = title.get_rect(center=(screen.get_width()//2, scale_y(80)))
        screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.category_buttons:
            button.draw(screen)
        
        # Draw back button
        self.back_button.draw(screen)
            
        # Draw fullscreen toggle button
        self.fullscreen_button.draw(screen)
    
    def draw_heart(self, x, y, size, fill_percent=1.0):
        """Draw a heart shape with fill percentage (0.0 to 1.0)"""
        # Heart shape points
        heart_color = (255, 0, 0)  # Red color for heart
        faded_color = (150, 150, 150)  # Gray color for faded heart
        
        # Calculate color based on fill percentage
        if fill_percent < 1.0:
            r = int(255 - (255 - 150) * (1 - fill_percent))
            g = int(0 + 150 * (1 - fill_percent))
            b = int(0 + 150 * (1 - fill_percent))
            heart_color = (r, g, b)
        
        # Draw the heart
        radius = int(size / 4)
        pygame.draw.circle(screen, heart_color, (x - radius, y - radius), radius)
        pygame.draw.circle(screen, heart_color, (x + radius, y - radius), radius)
        
        # Draw the bottom triangle of the heart
        points = [
            (x - radius * 2, y - radius),
            (x, y + radius * 2),
            (x + radius * 2, y - radius)
        ]
        pygame.draw.polygon(screen, heart_color, points)
    def draw_timer(self, x, y):
        """Draw the timer with a visual representation"""
        if not self.timer_enabled:
            return
            
        # Scale the position - center horizontally, fixed position vertically
        x = screen.get_width() // 2
        y = scale_y(40)
            
        # Calculate minutes and seconds
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        
        # Determine color based on time remaining
        if self.time_remaining > self.timer_duration * 0.6:  # More than 60% time left
            timer_color = GREEN
        elif self.time_remaining > self.timer_duration * 0.3:  # More than 30% time left
            timer_color = YELLOW
        else:  # Less than 30% time left
            timer_color = RED
        
        # Create a semi-transparent background for better visibility
        timer_text = get_medium_font().render(f"{minutes:02d}:{seconds:02d}", True, timer_color)
        timer_rect = timer_text.get_rect(center=(x, y))
        bg_rect = timer_rect.copy()
        bg_rect.inflate_ip(scale_x(20), scale_y(10))
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((40, 40, 60, 180))
        screen.blit(bg_surface, bg_rect)
            
        # Draw timer text with shadow for better visibility
        shadow_text = get_medium_font().render(f"{minutes:02d}:{seconds:02d}", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(x + scale_x(2), y + scale_y(2)))
        screen.blit(shadow_text, shadow_rect)
        
        # Draw the main timer text
        screen.blit(timer_text, timer_rect)
        
        # Draw a progress bar
        bar_width = scale_x(100)
        bar_height = scale_y(10)
        bar_x = x - bar_width // 2
        bar_y = y + scale_y(20)
        
        # Background bar (empty)
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Filled portion
        fill_width = int((self.time_remaining / self.timer_duration) * bar_width)
        pygame.draw.rect(screen, timer_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
    
    def draw_game_screen(self):
        # Draw category text with shadow for better visibility
        shadow_text = get_medium_font().render(f"Category: {self.category}", True, BLACK)
        shadow_rect = shadow_text.get_rect(topleft=(scale_x(22), scale_y(22)))
        screen.blit(shadow_text, shadow_rect)
        
        category_text = get_medium_font().render(f"Category: {self.category}", True, BLUE)
        category_rect = category_text.get_rect(topleft=(scale_x(20), scale_y(20)))
        screen.blit(category_text, category_rect)
        
        # Draw difficulty level with shadow
        difficulty_names = ["Easy", "Medium", "Hard"]
        difficulty_colors = [GREEN, YELLOW, RED]
        
        shadow_text = get_small_font().render(f"Difficulty: {difficulty_names[self.difficulty]}", True, BLACK)
        shadow_rect = shadow_text.get_rect(topleft=(scale_x(22), scale_y(62)))
        screen.blit(shadow_text, shadow_rect)
        
        difficulty_text = get_small_font().render(f"Difficulty: {difficulty_names[self.difficulty]}", True, difficulty_colors[self.difficulty])
        difficulty_rect = difficulty_text.get_rect(topleft=(scale_x(20), scale_y(60)))
        screen.blit(difficulty_text, difficulty_rect)
        
        # Draw hearts for lives - ensure they're visible at the top
        heart_size = scale_y(20)
        heart_spacing = scale_x(30)
        heart_y = scale_y(30)
        
        # Calculate heart positions to be on the right side with proper spacing
        total_hearts_width = (self.max_wrong_guesses * heart_spacing)
        heart_start_x = screen.get_width() - total_hearts_width - scale_x(30)
        
        # Draw hearts without background
        for i in range(self.max_wrong_guesses):
            heart_x = heart_start_x + (i * heart_spacing)
            
            # Determine heart fill status
            if i >= self.max_wrong_guesses - self.wrong_guesses:
                # Faded heart (lost life)
                fill_percent = 0.0
            else:
                # Full heart (remaining life)
                fill_percent = 1.0
            
            self.draw_heart(heart_x, heart_y, heart_size, fill_percent)
        
        # Draw timer if enabled - now handled in the draw_timer method with proper positioning
        if self.timer_enabled:
            self.draw_timer(0, 0)  # Parameters are ignored in the updated method
        
        # Draw stats with shadow - position on right side but below hearts
        shadow_text = get_small_font().render(f"Wins: {self.wins}  Losses: {self.losses}", True, BLACK)
        shadow_rect = shadow_text.get_rect(topright=(screen.get_width() - scale_x(18), scale_y(62)))
        screen.blit(shadow_text, shadow_rect)
        
        stats_text = get_small_font().render(f"Wins: {self.wins}  Losses: {self.losses}", True, WHITE)
        stats_rect = stats_text.get_rect(topright=(screen.get_width() - scale_x(20), scale_y(60)))
        screen.blit(stats_text, stats_rect)
        
        # Calculate how many parts of the hangman to draw based on wrong guesses and max wrong guesses
        # This ensures the hangman is fully drawn only when all lives are lost
        wrong_parts_to_draw = int(self.wrong_guesses * 6 / self.max_wrong_guesses)
        
        # Draw animated hangman (no background) with synchronized parts
        self.hangman_animation.draw(screen, wrong_parts_to_draw)
        
        # Draw word
        self.draw_word()
        
        # Draw keyboard (no background)
        for button in self.keyboard_buttons:
            button.draw(screen)
        
        # Draw pause button in top-left corner
        self.pause_button.draw(screen)
            
        # Draw fullscreen toggle button - now positioned in bottom right corner
        self.fullscreen_button.draw(screen)
        
    def draw_pause_screen(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Draw pause title with shadow
        shadow_offset = scale_y(3)
        pause_shadow = get_title_font().render("GAME PAUSED", True, BLACK)
        pause_shadow_rect = pause_shadow.get_rect(center=(screen.get_width()//2 + shadow_offset, scale_y(150) + shadow_offset))
        screen.blit(pause_shadow, pause_shadow_rect)
        
        pause_text = get_title_font().render("GAME PAUSED", True, NEON_BLUE)
        pause_rect = pause_text.get_rect(center=(screen.get_width()//2, scale_y(150)))
        screen.blit(pause_text, pause_rect)
        
        # Draw keyboard controls hint
        hint_shadow = get_small_font().render("Tip: You can also use your keyboard to type letters", True, BLACK)
        hint_shadow_rect = hint_shadow.get_rect(center=(screen.get_width()//2 + scale_x(1), scale_y(400) + scale_y(1)))
        screen.blit(hint_shadow, hint_shadow_rect)
        
        hint_text = get_small_font().render("Tip: You can also use your keyboard to type letters", True, NEON_YELLOW)
        hint_rect = hint_text.get_rect(center=(screen.get_width()//2, scale_y(400)))
        screen.blit(hint_text, hint_rect)
        
        # Draw pause menu buttons
        for button in self.pause_menu_buttons:
            button.draw(screen)
            
        # Draw fullscreen toggle button
        self.fullscreen_button.draw(screen)
    def draw_win_screen(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 100, 0, 150))  # Semi-transparent green
        screen.blit(overlay, (0, 0))
        
        # Draw win message with shadow
        shadow_offset = scale_y(3)
        win_shadow = get_title_font().render("YOU WIN!", True, BLACK)
        win_shadow_rect = win_shadow.get_rect(center=(screen.get_width()//2 + shadow_offset, scale_y(150) + shadow_offset))
        screen.blit(win_shadow, win_shadow_rect)
        
        win_text = get_title_font().render("YOU WIN!", True, NEON_GREEN)
        win_rect = win_text.get_rect(center=(screen.get_width()//2, scale_y(150)))
        screen.blit(win_text, win_rect)
        
        # Draw the word
        word_shadow = get_large_font().render(f"The word was: {self.word}", True, BLACK)
        word_shadow_rect = word_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(250) + scale_y(2)))
        screen.blit(word_shadow, word_shadow_rect)
        
        word_text = get_large_font().render(f"The word was: {self.word}", True, WHITE)
        word_rect = word_text.get_rect(center=(screen.get_width()//2, scale_y(250)))
        screen.blit(word_text, word_rect)
        
        # Draw difficulty
        difficulty_names = ["Easy", "Medium", "Hard"]
        
        diff_shadow = get_medium_font().render(f"Difficulty: {difficulty_names[self.difficulty]}", True, BLACK)
        diff_shadow_rect = diff_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(290) + scale_y(2)))
        screen.blit(diff_shadow, diff_shadow_rect)
        
        difficulty_text = get_medium_font().render(f"Difficulty: {difficulty_names[self.difficulty]}", True, WHITE)
        difficulty_rect = difficulty_text.get_rect(center=(screen.get_width()//2, scale_y(290)))
        screen.blit(difficulty_text, difficulty_rect)
        
        # Draw stats
        stats_shadow = get_medium_font().render(f"Wins: {self.wins}  Losses: {self.losses}", True, BLACK)
        stats_shadow_rect = stats_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(330) + scale_y(2)))
        screen.blit(stats_shadow, stats_shadow_rect)
        
        stats_text = get_medium_font().render(f"Wins: {self.wins}  Losses: {self.losses}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(screen.get_width()//2, scale_y(330)))
        screen.blit(stats_text, stats_rect)
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(screen)
            
        # Draw fullscreen toggle button
        self.fullscreen_button.draw(screen)
    
    def draw_lose_screen(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((100, 0, 0, 150))  # Semi-transparent red
        screen.blit(overlay, (0, 0))
        
        # Draw lose message with shadow
        shadow_offset = scale_y(3)
        lose_shadow = get_title_font().render("GAME OVER", True, BLACK)
        lose_shadow_rect = lose_shadow.get_rect(center=(screen.get_width()//2 + shadow_offset, scale_y(150) + shadow_offset))
        screen.blit(lose_shadow, lose_shadow_rect)
        
        lose_text = get_title_font().render("GAME OVER", True, NEON_RED)
        lose_rect = lose_text.get_rect(center=(screen.get_width()//2, scale_y(150)))
        screen.blit(lose_text, lose_rect)
        
        # Draw the word
        word_shadow = get_large_font().render(f"The word was: {self.word}", True, BLACK)
        word_shadow_rect = word_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(250) + scale_y(2)))
        screen.blit(word_shadow, word_shadow_rect)
        
        word_text = get_large_font().render(f"The word was: {self.word}", True, WHITE)
        word_rect = word_text.get_rect(center=(screen.get_width()//2, scale_y(250)))
        screen.blit(word_text, word_rect)
        
        # Draw difficulty
        difficulty_names = ["Easy", "Medium", "Hard"]
        
        diff_shadow = get_medium_font().render(f"Difficulty: {difficulty_names[self.difficulty]}", True, BLACK)
        diff_shadow_rect = diff_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(290) + scale_y(2)))
        screen.blit(diff_shadow, diff_shadow_rect)
        
        difficulty_text = get_medium_font().render(f"Difficulty: {difficulty_names[self.difficulty]}", True, WHITE)
        difficulty_rect = difficulty_text.get_rect(center=(screen.get_width()//2, scale_y(290)))
        screen.blit(difficulty_text, difficulty_rect)
        
        # Draw reason for loss
        if self.timer_enabled and self.time_remaining <= 0:
            reason_shadow = get_medium_font().render("Time's up!", True, BLACK)
            reason_shadow_rect = reason_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(330) + scale_y(2)))
            screen.blit(reason_shadow, reason_shadow_rect)
            
            reason_text = get_medium_font().render("Time's up!", True, NEON_RED)
        else:
            reason_shadow = get_medium_font().render("Out of lives!", True, BLACK)
            reason_shadow_rect = reason_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(330) + scale_y(2)))
            screen.blit(reason_shadow, reason_shadow_rect)
            
            reason_text = get_medium_font().render("Out of lives!", True, NEON_RED)
            
        reason_rect = reason_text.get_rect(center=(screen.get_width()//2, scale_y(330)))
        screen.blit(reason_text, reason_rect)
        
        # Draw stats
        stats_shadow = get_medium_font().render(f"Wins: {self.wins}  Losses: {self.losses}", True, BLACK)
        stats_shadow_rect = stats_shadow.get_rect(center=(screen.get_width()//2 + scale_x(2), scale_y(370) + scale_y(2)))
        screen.blit(stats_shadow, stats_shadow_rect)
        
        stats_text = get_medium_font().render(f"Wins: {self.wins}  Losses: {self.losses}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(screen.get_width()//2, scale_y(370)))
        screen.blit(stats_text, stats_rect)
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(screen)
            
        # Draw fullscreen toggle button
        self.fullscreen_button.draw(screen)
    def handle_events(self):
        global fullscreen
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle window resize events
            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:  # Only handle resize if not in fullscreen mode
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    # Update parallax background for new screen size
                    self.parallax_background.resize()
            
            # Handle fullscreen toggle button
            self.fullscreen_button.check_hover(mouse_pos)
            if self.fullscreen_button.is_clicked(mouse_pos, event):
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
                # Update parallax background for new screen size
                self.parallax_background.resize()
            
            # Handle keyboard shortcuts for fullscreen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
                    # Update parallax background for new screen size
                    self.parallax_background.resize()
                elif event.key == pygame.K_ESCAPE:
                    if fullscreen:
                        fullscreen = False
                        screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
                        # Update parallax background for new screen size
                        self.parallax_background.resize()
                    elif self.state == STATE_GAME:
                        # Pause the game when ESC is pressed during gameplay
                        self.previous_state = self.state
                        self.state = STATE_PAUSE
                # Toggle parallax animation with 'P' key
                elif event.key == pygame.K_p and self.state != STATE_GAME:
                    self.parallax_background.toggle()
                
                # Handle keyboard letter input during gameplay
                if self.state == STATE_GAME and event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key)
                    if letter not in self.guessed_letters:
                        self.guess_letter(letter)
            
            # Menu state
            if self.state == STATE_MENU:
                for i, button in enumerate(self.menu_buttons):
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        if i == 0:  # Play Game
                            self.state = STATE_DIFFICULTY
                        elif i == 1:  # Quit
                            pygame.quit()
                            sys.exit()
            
            # Difficulty selection state
            elif self.state == STATE_DIFFICULTY:
                for i, button in enumerate(self.difficulty_buttons):
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        self.difficulty = i  # Set difficulty level
                        self.state = STATE_CATEGORY
                
                # Handle back button
                self.back_button.check_hover(mouse_pos)
                if self.back_button.is_clicked(mouse_pos, event):
                    self.state = STATE_MENU
            
            # Category selection state
            elif self.state == STATE_CATEGORY:
                for i, button in enumerate(self.category_buttons):
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        self.start_new_game(button.text)
                
                # Handle back button
                self.back_button.check_hover(mouse_pos)
                if self.back_button.is_clicked(mouse_pos, event):
                    self.state = STATE_DIFFICULTY
            
            # Game state
            elif self.state == STATE_GAME:
                for button in self.keyboard_buttons:
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event) and button.text not in self.guessed_letters:
                        self.guess_letter(button.text)
                
                # Handle pause button
                self.pause_button.check_hover(mouse_pos)
                if self.pause_button.is_clicked(mouse_pos, event):
                    self.previous_state = self.state
                    self.state = STATE_PAUSE
            
            # Pause state
            elif self.state == STATE_PAUSE:
                for i, button in enumerate(self.pause_menu_buttons):
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        if i == 0:  # Continue
                            self.state = self.previous_state
                        elif i == 1:  # Quit to Menu
                            self.state = STATE_MENU
            
            # Win or Lose state
            elif self.state == STATE_WIN or self.state == STATE_LOSE:
                for i, button in enumerate(self.game_over_buttons):
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        if i == 0:  # Play Again
                            self.state = STATE_DIFFICULTY
                        elif i == 1:  # Main Menu
                            self.state = STATE_MENU
    
    def update(self):
        """Update game logic"""
        # Update parallax background if not in game state
        if self.state != STATE_GAME:
            self.parallax_background.update()
        
        # Update hangman animation
        if self.state == STATE_GAME:
            self.hangman_animation.update()
            
            # Update timer if enabled
            if self.timer_enabled:
                elapsed = time.time() - self.timer_start
                self.time_remaining = max(0, self.timer_duration - elapsed)
                
                # Check if time is up
                if self.time_remaining <= 0:
                    self.state = STATE_LOSE
                    self.losses += 1
                    lose_sound.play()  # Play lose sound
    
    def run(self):
        while True:
            # Handle events
            self.handle_events()
            
            # Update game logic
            self.update()
            
            # Draw background
            if self.state != STATE_GAME:
                # Use parallax background for non-game states
                self.parallax_background.draw(screen)
            else:
                # Use static background for game state
                if has_background:
                    scaled_bg = scale_background()
                    screen.blit(scaled_bg, (0, 0))
                else:
                    screen.fill(DARK_BG)
            
            # Draw current state
            if self.state == STATE_MENU:
                self.draw_menu()
            elif self.state == STATE_DIFFICULTY:
                self.draw_difficulty_selection()
            elif self.state == STATE_CATEGORY:
                self.draw_category_selection()
            elif self.state == STATE_GAME:
                self.draw_game_screen()
            elif self.state == STATE_WIN:
                self.draw_win_screen()
            elif self.state == STATE_LOSE:
                self.draw_lose_screen()
            elif self.state == STATE_PAUSE:
                # First draw the game screen (as background)
                self.draw_game_screen()
                # Then overlay the pause screen
                self.draw_pause_screen()
            
            # Update display
            pygame.display.flip()
            clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    game = HangmanGame()
    game.run()
