import pygame
import random
import math

# Initialization settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define colors (R, G, B)
COLORS = [(255, 0, 0), (255, 255, 0), (0, 0, 255), (0, 255, 0)]

# Initialize the map: Randomly generate numbers from 0 to 3
grid = [[random.randint(0, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    # Traverse an 8x8 grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # 1. Calculate the coordinates of the top-left corner of the current cell, used to draw the background line.
            rect_x = col * CELL_SIZE
            rect_y = row * CELL_SIZE
            
            # Draw dark gray grid lines (set the color to (50, 50, 50))
            # Parameter 1 represents the line width, so only the outline is drawn and no fill is applied.
            pygame.draw.rect(screen, (50, 50, 50), (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)
            
            # 2. Calculate the center point of the square shape.
            x = rect_x + CELL_SIZE // 2
            y = rect_y + CELL_SIZE // 2
            
            # Get the color and shape type of the current cell
            color = COLORS[grid[row][col]]
            shape_type = grid[row][col]
            
            # 3. Draw the shape according to your required functional specifications [cite: 36, 40]
            if shape_type == 0: # Red - Circle
                pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)
                
            elif shape_type == 1: # Yellow - Square
                size = CELL_SIZE // 1.5
                pygame.draw.rect(screen, color, (x - size//2, y - size//2, size, size))
                
            elif shape_type == 2: # Blue - Triangle
                # Calculate the three vertices of a triangle
                points = [
                    (x, y - CELL_SIZE//3),                # Top
                    (x - CELL_SIZE//3, y + CELL_SIZE//3), # Bottom Left
                    (x + CELL_SIZE//3, y + CELL_SIZE//3)  # Bottom right
                ]
                pygame.draw.polygon(screen, color, points)
                
            elif shape_type == 3: # Green - Regular Hexagon
                points = []
                for i in range(6):
                    # One vertex every 60 degrees
                    angle = i * math.pi / 3
                    px = x + (CELL_SIZE // 3) * math.cos(angle)
                    py = y + (CELL_SIZE // 3) * math.sin(angle)
                    points.append((px, py))
                pygame.draw.polygon(screen, color, points)
            
# Define variables before the while loop
selected_cell = None  # Record the first click (row, col)

running = True
while running:
    screen.fill((30, 30, 30))
    draw_grid()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # --- Mouse Click Logic ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            
            # If this is your first time clicking
            if selected_cell is None:
                selected_cell = (row, col)
            else:
                # If it's the second click, try swapping.
                r1, c1 = selected_cell
                r2, c2 = row, col
                
                # Determine if they are adjacent (the sum of their distances is 1 if they are adjacent)
                if abs(r1 - r2) + abs(c1 - c2) == 1:
                    # Swap the positions in the array
                    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
                
                # Reset selection regardless of success or failure
                selected_cell = None

pygame.quit()