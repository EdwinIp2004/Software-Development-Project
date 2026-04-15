# SOFTWARE ENGINEERING Project : Match-3 Puzzle Game

## Graphical Abstract
<img width="601" height="712" alt="image" src="https://github.com/user-attachments/assets/3f656383-2f90-4569-bcec-1dfdcacc0a15" />

## How to Play
**Objective**  
Match 3 or more identical gems in a row or column to clear them. Reach the target score before you run out of moves.

**Controls**  
- Click any gem to select it.  
- Click an adjacent gem to swap them.  
- Only horizontal or vertical swaps are allowed.  
- Press **ESC** to quit the game.

**Scoring System**  
- Base score depends on match length:  
  - 3 gems → 30 points  
  - 4 gems → 80 points  
  - 5 gems → 150 points  
  - 6+ gems → 250 points  
- **Combo multiplier**: Every consecutive match in the same cascade multiplies the score (e.g., Combo ×2, ×3, …).  
- New gems fall from the top after each match.

**Target Score & Level Progression**  
- Each level has a specific target score that increases with difficulty.  
- Starting values: Level 1 target = 2000, moves = 20.  
- After completing a level: moves increase by 10 and target score rises using the formula  
  `target = 1500 + (level-1)×3000 + (level-1)²×500`.  
- The game ends when you run out of moves (Game Over).

**Tactics for High Score**  
- **Chain reactions (combos)** are the key to high scores. Try to create swaps that cause multiple matches in a single cascade.
- Don't do simple match 3 moves unless you're planning for a big chain reaction.
- Save powerful longer matches (4+ gems) for moments when they can trigger even bigger combos.

## 1. Purpose of the Software
- **Type**: Casual puzzle game (Match-3).
- **Development process**: Agile
- **Why we chose Agile**: Game design needs frequent testing. With Agile we can build a working version every sprint, test it together, and improve the game immediately. Waterfall would be too rigid because we cannot know the final product until we finish the game.
- **Target market**: Casual players who want quick, relaxing, puzzle games during their spare time.

## 2. Software Development Plan
### Development Process
We use **Agile** process with short sprints.  
Each sprint produces a working version of the game that can be tested.

### Members (Roles & Responsibilities & Portion)
| Name | Role | Responsibilities | Portion |
|------|------|------------------|---------|
| [Coder 1] | Coder | Game engineering | 20% |
| [Coder 2] | Coder | Game engineering | 20% |
| [Writer 1] | Writer | Documentation & README.md | 20% |
| [Writer 2] | Writer | Documentation & README.md | 20% |
| [Video person] | Video & Testing | Demo video + playtesting | 20% |

### Schedule (Agile Sprints)
| Sprint | Goals | Status |
|--------|-------|--------|
| 1      | Basic 3 match grid | Completed |
| 2      | Animation system | Completed |
| 3      | Scoring system | Completed |
| 4      | Level system | Completed |

### Algorithm
**1. Match Detection & Chain Reaction**  
Scans the entire grid for three or more identical gems horizontally or vertically.
```python
def check_matches():
    matches = set()
    # Horizontal check
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 2):
            if grid[r][c] != -1 and grid[r][c] == grid[r][c+1] == grid[r][c+2]:
                matches.update([(r, c), (r, c+1), (r, c+2)])
    # Vertical check
    for r in range(GRID_SIZE - 2):
        for c in range(GRID_SIZE):
            if grid[r][c] != -1 and grid[r][c] == grid[r+1][c] == grid[r+2][c]:
                matches.update([(r, c), (r+1, c), (r+2, c)])
    return list(matches)
```
**2. Scoring Formula**

| Match Length | Base Score | With Combo (×2) |
|--------------|------------|-----------------|
| 3 gems | 30 | 60 |
| 4 gems | 80 | 160 |
| 5 gems | 150 | 300 |
| 6+ gems | 250 | 500 |

**Formula**: `Total Score = Base Score × Current Combo`
```python
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
```
3. Match Processing & Gravity
Removes matched gems, applies gravity, and refills the grid with new gems. Handling combo, flashing white animation, and falling animations.
```python
def process_matches_and_gravity():
    while True:
        matched = check_matches()
        if not matched: break
        # White flash → remove → gravity → refill
        # (full animation and logic implemented)
```

### Current Status of The Software
- Core gameplay loop - Players click and swap adjacent gems to form matches of 3+ identical shapes
- Match detection system - Correctly identifies horizontal and vertical matches of 3, 4, 5, or 6+ gems
- Visual feedback - White flash animation when matches occur, smooth swap animations
- Selection highlight - White border shows currently selected gem
- Scoring and level system - Player reach next level when they hit the target score, and game over when no moves left

### Future Plan
- Add leaderboard system and menu
- Better visual and soundtrack

## 3. Demo
- YouTube URL: [FILL IN LATER]

## 4. Development & Running Environment
- Programming language: Python 3 + Pygame
- Minimum requirements: Any standard laptop with Python 3 installed
- Required packages: pygame

## 5. Declaration
- Game engine / libraries: Pygame (open-source library).
- No other external code was used without declaration.
