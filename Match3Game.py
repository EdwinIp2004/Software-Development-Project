import pygame
import random

# 1. Basic Configuration
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
COLORS = [
    (255, 50, 50),   # Red
    (255, 255, 50),  # Yellow
    (50, 50, 255),   # Blue
    (50, 255, 50)    # Green
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match3Game")
pygame.font.init()
score = 0
combo = 0
score_font = pygame.font.SysFont('Arial', 24, bold=True)

# Initialize the mesh
grid = [[random.randint(0, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# --- Core Plotting Auxiliary Functions ---
def draw_shape(shape_type, x, y, size_scale=1.0):
    """Draw a graphic at specified coordinates"""
    if shape_type == -1: return
    color = COLORS[shape_type]
    size = (CELL_SIZE // 1.5) * size_scale
    
    if shape_type == 0: # Circle
        pygame.draw.circle(screen, color, (int(x), int(y)), int(size // 2))
    elif shape_type == 1: # Square
        pygame.draw.rect(screen, color, (int(x - size//2), int(y - size//2), int(size), int(size)))
    elif shape_type == 2: # Triangle
        pts = [(x, y - size//2), (x - size//2, y + size//2), (x + size//2, y + size//2)]
        pygame.draw.polygon(screen, color, pts)
    elif shape_type == 3: # Hexagon
        pts = []
        for i in range(6):
            angle = i * 3.14159 / 3
            pts.append((x + (size//2) * pygame.math.Vector2(1, 0).rotate_rad(angle).x, 
                        y + (size//2) * pygame.math.Vector2(1, 0).rotate_rad(angle).y))
        pygame.draw.polygon(screen, color, pts)

def draw_background(ignore_cells=None):
    """Draw background lines and non-animated blocks"""
    if ignore_cells is None: ignore_cells = []
    screen.fill((30, 30, 30))

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 50))
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    combo_text = score_font.render(f"Combo: x{combo}", True, (255, 215, 0))
    screen.blit(score_text, (20, 15))
    screen.blit(combo_text, (450, 15))
    
    
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect_x, rect_y = c * CELL_SIZE, r * CELL_SIZE
            pygame.draw.rect(screen, (50, 50, 50), (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)
            if (r, c) not in ignore_cells:
                draw_shape(grid[r][c], rect_x + CELL_SIZE//2, rect_y + CELL_SIZE//2)

# --- Core Algorithm Functions ---
def check_matches():
    matches = set()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 2):
            if grid[r][c] != -1 and grid[r][c] == grid[r][c+1] == grid[r][c+2]:
                matches.update([(r, c), (r, c+1), (r, c+2)])
    for r in range(GRID_SIZE - 2):
        for c in range(GRID_SIZE):
            if grid[r][c] != -1 and grid[r][c] == grid[r+1][c] == grid[r+2][c]:
                matches.update([(r, c), (r+1, c), (r+2, c)])
    return list(matches)

def has_possible_moves():
    """Check if a solution exists"""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            for dr, dc in [(0,1), (1,0)]:
                nr, nc = r + dr, c + dc
                if nr < GRID_SIZE and nc < GRID_SIZE:
                    grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]
                    found = check_matches()
                    grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]
                    if found: return True
    return False

# --- Animation Functions ---
def animate_swap(r1, c1, r2, c2):
    frames = 10
    for i in range(frames + 1):
        p = i / frames
        draw_background(ignore_cells=[(r1, c1), (r2, c2)])
        # Block 1 coordinates
        x1 = (c1 + (c2 - c1) * p) * CELL_SIZE + CELL_SIZE // 2
        y1 = (r1 + (r2 - r1) * p) * CELL_SIZE + CELL_SIZE // 2
        # Block 2 coordinates
        x2 = (c2 + (c1 - c2) * p) * CELL_SIZE + CELL_SIZE // 2
        y2 = (r2 + (r1 - r2) * p) * CELL_SIZE + CELL_SIZE // 2
        draw_shape(grid[r1][c1], x1, y1)
        draw_shape(grid[r2][c2], x2, y2)
        pygame.display.flip()
        pygame.time.delay(20)

def process_matches_and_gravity():
    global score, combo  
    """Handling combo, flashing white animation, and falling animations"""
    current_combo = 0
    while True:
        matched = check_matches()
        if not matched: break

        current_combo += 1
        combo = current_combo
        match_count = len(matched)
        if match_count == 3:
            add_score = 30
        elif match_count == 4:
            add_score = 80
        elif match_count == 5:
            add_score = 150
        else:
            add_score = 30 * (match_count // 3)  
        add_score *= current_combo
        score += add_score
        
        
       # 1. White flash animation
        draw_background()
        for (r, c) in matched:
            pygame.draw.rect(screen, (255, 255, 255), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(150)
        
        # 2. Logic eliminated and briefly turns black
        for (r, c) in matched: grid[r][c] = -1
        draw_background()
        pygame.display.flip()
        pygame.time.delay(100)
        
        #3. Drop Logic and Supplements
        for c in range(GRID_SIZE):
            col_data = [grid[r][c] for r in range(GRID_SIZE) if grid[r][c] != -1]
            missing = GRID_SIZE - len(col_data)
            new_elements = [random.randint(0, 3) for _ in range(missing)]
            final_col = new_elements + col_data
            for r in range(GRID_SIZE): grid[r][c] = final_col[r]
            
        draw_background()
        pygame.display.flip()
        pygame.time.delay(200)

# --- Main Loop ---
selected = None
running = True
while running:
    draw_background()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            c, r = x // CELL_SIZE, y // CELL_SIZE
            
            if selected is None:
                selected = (r, c)
            else:
                r1, c1 = selected
                r2, c2 = r, c
                if abs(r1-r2) + abs(c1-c2) == 1:
                    # Perform swap animation
                    animate_swap(r1, c1, r2, c2)
                    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
                    
                    if check_matches():
                        process_matches_and_gravity()
                    else:
                        animate_swap(r1, c1, r2, c2)
                        grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
                selected = None
    
    # Dead End Reset Detection
    if not has_possible_moves():
        grid = [[random.randint(0, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        process_matches_and_gravity()

pygame.quit()
