import pygame
import random

# 1. Basic Configuration
WIDTH, HEIGHT = 600, 660  
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

def check_matches(grid=None):
    # 未传grid时，自动使用全局grid，100%兼容你原来的调用
    if grid is None:
        grid = globals()['grid']
    matches = set()
    match_lengths = []  
    
    
    for r in range(GRID_SIZE):
        current_color = grid[r][0]
        count = 1
        for c in range(1, GRID_SIZE):
            if grid[r][c] == current_color and current_color != -1:
                count += 1
            else:
                if count >= 3:
                    match_lengths.append(count)
                    for i in range(c - count, c):
                        matches.add((r, i))
                current_color = grid[r][c]
                count = 1
       
        if count >= 3:
            match_lengths.append(count)
            for i in range(GRID_SIZE - count, GRID_SIZE):
                matches.add((r, i))
    
   
    for c in range(GRID_SIZE):
        current_color = grid[0][c]
        count = 1
        for r in range(1, GRID_SIZE):
            if grid[r][c] == current_color and current_color != -1:
                count += 1
            else:
                if count >= 3:
                    match_lengths.append(count)
                    for i in range(r - count, r):
                        matches.add((i, c))
                current_color = grid[r][c]
                count = 1
        # 处理列尾的连续匹配
        if count >= 3:
            match_lengths.append(count)
            for i in range(GRID_SIZE - count, GRID_SIZE):
                matches.add((i, c))
    
    return list(matches), match_lengths


def has_possible_moves(grid=None):
    if grid is None:
        grid = globals()['grid']
    """Check if a solution exists"""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            for dr, dc in [(0,1), (1,0)]:
                nr, nc = r + dr, c + dc
                if nr < GRID_SIZE and nc < GRID_SIZE:
                    # 交换两个元素
                    grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]
                    # 检查匹配（取check_matches第一个返回值）
                    found, _ = check_matches(grid)
                    # 交换回来
                    grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]
                    if found:
                        return True
    return False


def generate_valid_grid(max_attempts=1000):
    """
    生成一个完全没有可消除匹配、且有可玩步骤的8x8网格
    加最大重试次数，避免极端情况无限循环
    """
    for _ in range(max_attempts):
        # 1. 生成随机网格
        grid = [[random.randint(0, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # 2. 检查是否有匹配，无匹配才继续
        matched, _ = check_matches(grid)
        if not matched:
            
            if has_possible_moves(grid):
                return grid

    return [[(i+j)%4 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

def draw_shape(shape_type, x, y, size_scale=1.0):
    """Draw a graphic at specified coordinates"""
    if shape_type == -1: return
    color = COLORS[shape_type]
    size = (CELL_SIZE // 1.5) * size_scale

    if shape_type == 0: # Circle
        pygame.draw.circle(screen, color, (int(x), int(y)), int(size // 2))
    elif shape_type == 1: # Square
        pygame.draw.rect(screen, color, (int(x - size/2), int(y - size/2), int(size), int(size)))
    elif shape_type == 2: # Triangle
        pts = [(x, y - size/2), (x - size/2, y + size/2), (x + size/2, y + size/2)]
        pygame.draw.polygon(screen, color, pts)
    elif shape_type == 3: # Hexagon
        pts = []
        for i in range(6):
            angle = i * 3.14159 / 3
            pts.append((x + (size/2) * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
                        y + (size/2) * pygame.math.Vector2(1, 0).rotate_rad(angle).y))
        pygame.draw.polygon(screen, color, pts)

UI_HEIGHT = 60
def draw_background(ignore_cells=None):
    """Draw background lines and non-animated blocks"""
    if ignore_cells is None:
        ignore_cells = []
    screen.fill((30, 30, 30))


    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, UI_HEIGHT))

    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    combo_text = score_font.render(f"Combo: x {combo}", True, (255, 215, 0))
    screen.blit(score_text, (20, 15))
    screen.blit(combo_text, (450, 15))

  
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect_x = c * CELL_SIZE
            rect_y = r * CELL_SIZE + UI_HEIGHT
            pygame.draw.rect(screen, (50, 50, 50), (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)
            if (r, c) not in ignore_cells:
                draw_shape(grid[r][c], rect_x + CELL_SIZE//2, rect_y + CELL_SIZE//2)

def animate_swap(r1, c1, r2, c2):
    frames = 10
    for i in range(frames + 1):
        p = i / frames
        draw_background(ignore_cells=[(r1, c1), (r2, c2)])

        x1 = (c1 + (c2 - c1) * p) * CELL_SIZE + CELL_SIZE // 2
        y1 = (r1 + (r2 - r1) * p) * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
        
        x2 = (c2 + (c1 - c2) * p) * CELL_SIZE + CELL_SIZE // 2
        y2 = (r2 + (r1 - r2) * p) * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT

        draw_shape(grid[r1][c1], x1, y1)
        draw_shape(grid[r2][c2], x2, y2)
        pygame.display.flip()
        pygame.time.delay(20)

def process_matches_and_gravity():
    global score, combo
    """Handling combo, flashing white animation, and falling animations"""
    current_combo = 0
    while True:
        # 现在check_matches返回两个值：matched坐标列表 + match_lengths连续段长度列表
        matched, match_lengths = check_matches()
        if not matched:
            break

        current_combo += 1
        combo = current_combo

        
        add_score = 0
        for length in match_lengths:
            if length == 3:
                add_score += 30    
            elif length == 4:
                add_score += 80   
            elif length == 5:
                add_score += 150   
            elif length >= 6:
                add_score += 250   
    
        add_score *= current_combo
    
        score += add_score

    
        draw_background()
        for (r, c) in matched:
            pygame.draw.rect(screen, (255, 255, 255), (c*CELL_SIZE, r*CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(150)

       
        for (r, c) in matched:
            grid[r][c] = -1
        draw_background()
        pygame.display.flip()
        pygame.time.delay(100)

        for c in range(GRID_SIZE):
            col_data = [grid[r][c] for r in range(GRID_SIZE) if grid[r][c] != -1]
            missing = GRID_SIZE - len(col_data)
            new_elements = [random.randint(0, 3) for _ in range(missing)]
            final_col = new_elements + col_data
            for r in range(GRID_SIZE):
                grid[r][c] = final_col[r]

        draw_background()
        pygame.display.flip()
        pygame.time.delay(200)
    
    if current_combo == 0:
        combo = 0

grid = generate_valid_grid()

selected = None
running = True

while running:
    draw_background()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
                # 按下 ESC 键 (K_ESCAPE)退出
                if event.key == pygame.K_ESCAPE:
                    running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # 计算点击的网格坐标（完全保留你原来的代码，无修改）
            c = x // CELL_SIZE
            r = (y - UI_HEIGHT) // CELL_SIZE

            if selected is None:
                selected = (r, c)
            else:
                r1, c1 = selected
                r2, c2 = r, c
                if abs(r1-r2) + abs(c1-c2) == 1:
                    # Perform swap animation（完全保留你原来的代码，无修改）
                    animate_swap(r1, c1, r2, c2)
                    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

                    
                    if check_matches()[0]:
                        process_matches_and_gravity()
                    else:
                        animate_swap(r1, c1, r2, c2)
                        grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

                selected = None
    # ==============================================
    if not has_possible_moves():
        # 原来的随机生成，替换成generate_valid_grid
        # grid = [[random.randint(0, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # process_matches_and_gravity()
        grid = generate_valid_grid()
        score = 0  
        combo = 0  

pygame.quit()
