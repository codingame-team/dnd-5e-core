# Migration Guide: From dao_classes.py to dnd-5e-core

This guide helps you migrate from using `dao_classes.py` directly to using the `dnd-5e-core` package.

## Before (dao_classes.py)

```python
# All in one file
from dao_classes import Monster, Character, Weapon, Spell, CombatSystem
import pygame  # Mixed with UI code

# UI and logic mixed together
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.player = Character(...)

    def run(self):
        # Game loop with mixed UI and logic
        pass
```

## After (dnd-5e-core)

```python
# Separated concerns
from dnd_5e_core.entities import Monster, Character
from dnd_5e_core.equipment import Weapon
from dnd_5e_core.spells import Spell
from dnd_5e_core.combat import CombatSystem

import pygame  # UI code separate

# Clear separation: UI vs Logic
class GameLogic:
    def __init__(self):
        self.player = Character(...)
        self.combat = CombatSystem()

    def update(self):
        # Pure game logic, no UI
        pass

class GameUI:
    def __init__(self, logic: GameLogic):
        self.logic = logic
        self.screen = pygame.display.set_mode((800, 600))

    def render(self):
        # Pure UI rendering
        pass

    def run(self):
        while running:
            self.logic.update()
            self.render()
```

## Key Changes

### Import Paths

| Old (dao_classes.py) | New (dnd-5e-core) |
|---------------------|-------------------|
| `from dao_classes import Monster` | `from dnd_5e_core.entities import Monster` |
| `from dao_classes import Character` | `from dnd_5e_core.entities import Character` |
| `from dao_classes import Weapon` | `from dnd_5e_core.equipment import Weapon` |
| `from dao_classes import Spell` | `from dnd_5e_core.spells import Spell` |
| `from dao_classes import Race` | `from dnd_5e_core.races import Race` |

### No UI Dependencies

The package has NO pygame, ncurses, or other UI dependencies.

Remove all `cprint()`, `color.RED`, pygame rendering from game logic.

### Example: Before

```python
def attack(self, target):
    damage = self.roll_damage()
    target.hp -= damage
    cprint(f"{color.RED}{target.name}{color.END} takes {damage} damage!")  # BAD
    return damage
```

### Example: After

```python
def attack(self, target):
    damage = self.roll_damage()
    target.hp -= damage
    return damage  # Your UI handles the message display
```

## Benefits

1. **Reusable**: Use same logic for pygame, ncurses, web, CLI
2. **Testable**: Test game logic without UI
3. **Maintainable**: Clear separation of concerns
4. **Portable**: Package can be installed via pip

## Step-by-Step Migration

1. Install package: `pip install dnd-5e-core`
2. Update imports from `dao_classes` to `dnd_5e_core.*`
3. Remove UI code (cprint, colors) from game logic
4. Move UI code to separate files
5. Create clear interfaces between logic and UI
6. Test thoroughly
