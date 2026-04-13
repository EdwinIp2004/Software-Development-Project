# SOFTWARE ENGINEERING Project : Match-3 Puzzle Game

## Graphical Abstract
<img width="598" height="692" alt="image" src="https://github.com/user-attachments/assets/b23da503-255d-4fca-9154-815396def52f" />


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
| 3      | Scoring system and meun | Completed |
| 4      | Polish, bug fixing, final assets and testing | Planned |

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

2. Match Processing & Gravity
Removes matched gems, applies gravity, and refills the grid with new gems. Handling combo, flashing white animation, and falling animations.
```python
def process_matches_and_gravity():
    """Handling combo, flashing white animation, and falling animations"""
    while True:
        matched = check_matches()
        if not matched: break
        # White flash → remove → gravity → refill
        # (full animation and logic implemented)
```

### Current Status of The Software
The pilot/demo version is complete and fully playable. The game has an 8×8 grid with clickable gems, swap mechanics, match detection, removal animations, gravity, and automatic refilling. The core gameplay loop works smoothly.

### Future Plan
- Add scoring system and level progression
- Add main menu, level select, etc.

## 3. Demo
- YouTube URL: [FILL IN LATER]

## 4. Development & Running Environment
- Programming language: Python 3 + Pygame
- Minimum requirements: Any standard laptop with Python 3 installed
- Required packages: pygame

## 5. Declaration
- [FILL IN LATER]
