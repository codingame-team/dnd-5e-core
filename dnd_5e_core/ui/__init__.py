"""
D&D 5e Core - UI Helper Module
Provides UI helper functions for displaying game messages
WITHOUT coupling the core game logic to specific UI frameworks

This module provides utility functions that were previously scattered
in dao_classes.py (cprint, print statements). The core classes now
return data instead of printing, and UI layers can use these helpers.
"""
from typing import Optional


class Color:
    """ANSI color codes for terminal output"""
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_PURPLE = '\033[95m'
    BRIGHT_CYAN = '\033[96m'

    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'

    # Special
    END = '\033[0m'
    DARKCYAN = '\033[36m'  # Alias

    @classmethod
    def strip_colors(cls, text: str) -> str:
        """Remove all color codes from text"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)


# Global alias for backward compatibility
color = Color


def cprint(message: str, color_code: Optional[str] = None, end: str = '\n') -> None:
    """
    Colored print - prints a message with optional color.

    This is a UI helper function. Core game logic should NOT call this directly.
    Instead, core logic should return data, and UI layers should format/display it.

    Args:
        message: Message to print
        color_code: Optional color code (from Color class)
        end: String appended after the message

    Example:
        >>> cprint("Critical hit!", Color.RED)
        >>> cprint(f"{Color.GREEN}Victory!{Color.END}")
    """
    if color_code:
        print(f"{color_code}{message}{Color.END}", end=end)
    else:
        print(message, end=end)


def format_damage_message(attacker_name: str, target_name: str, damage: int,
                          damage_type: str = "") -> str:
    """
    Format a damage message for display.

    Args:
        attacker_name: Name of the attacker
        target_name: Name of the target
        damage: Amount of damage dealt
        damage_type: Type of damage (slashing, piercing, etc.)

    Returns:
        Formatted message string
    """
    type_str = f" {damage_type}" if damage_type else ""
    return f"{attacker_name} deals {damage}{type_str} damage to {target_name}!"


def format_attack_message(attacker_name: str, target_name: str,
                          attack_type: str = "attacks") -> str:
    """
    Format an attack message.

    Args:
        attacker_name: Name of the attacker
        target_name: Name of the target
        attack_type: Type of attack (attacks, strikes, etc.)

    Returns:
        Formatted message string
    """
    return f"{attacker_name} {attack_type} {target_name}!"


def format_death_message(character_name: str) -> str:
    """Format a death message"""
    return f"{character_name} is KILLED!"


def format_victory_message(character_name: str, xp_gained: int, gold_gained: int = 0) -> str:
    """Format a victory message"""
    msg = f"{character_name} gained {xp_gained} XP"
    if gold_gained > 0:
        msg += f" and found {gold_gained} gp"
    return msg + "!"


def format_heal_message(character_name: str, hp_restored: int, is_full: bool = False) -> str:
    """Format a healing message"""
    if is_full:
        return f"{character_name} is fully healed!"
    return f"{character_name} recovered {hp_restored} hit points!"


def format_level_up_message(character_name: str, new_level: int, hp_gained: int) -> str:
    """Format a level up message"""
    return f"{character_name} reached level {new_level}! Gained {hp_gained} HP!"


def format_spell_cast_message(caster_name: str, spell_name: str,
                              target_name: Optional[str] = None) -> str:
    """Format a spell casting message"""
    base = f"{caster_name} casts {spell_name.upper()}"
    if target_name:
        base += f" on {target_name}"
    return base + "!"


def format_saving_throw_message(character_name: str, succeeded: bool,
                                save_type: str = "") -> str:
    """Format a saving throw message"""
    result = "succeeds" if succeeded else "fails"
    type_str = f" {save_type.upper()}" if save_type else ""
    return f"{character_name} {result}{type_str} saving throw!"


def format_condition_message(character_name: str, condition: str, applied: bool = True) -> str:
    """Format a condition status message"""
    action = "is" if applied else "is no longer"
    return f"{character_name} {action} {condition}!"


def format_inventory_message(character_name: str, item_name: str,
                             action: str = "found") -> str:
    """Format an inventory action message"""
    return f"{character_name} {action} {item_name}!"


def format_gold_message(amount: int, action: str = "found") -> str:
    """Format a gold transaction message"""
    return f"{action.capitalize()} {amount} gold!"


def format_hp_status(character_name: str, current_hp: int, max_hp: int) -> str:
    """Format HP status for display"""
    percentage = int((current_hp / max_hp) * 100) if max_hp > 0 else 0
    return f"{character_name}: {current_hp}/{max_hp} HP ({percentage}%)"


def format_combat_round(round_number: int) -> str:
    """Format combat round header"""
    return f"=== Round {round_number} ==="


def format_encounter_header(monster_names: list) -> str:
    """Format encounter start message"""
    monsters = ", ".join(monster_names)
    return f"=== New Encounter! ===\nEncountered: {monsters}"


def format_combat_end(victory: bool, reward_xp: int = 0, reward_gold: int = 0) -> str:
    """Format combat end message"""
    if victory:
        msg = "=== VICTORY! ==="
        if reward_xp or reward_gold:
            msg += f"\nEarned {reward_xp} XP"
            if reward_gold:
                msg += f" and {reward_gold} gold"
        return msg
    return "=== DEFEAT! ==="


# Example usage and migration guide
"""
MIGRATION GUIDE:

OLD CODE (in dao_classes.py):
    def attack(self, target):
        damage = self.calculate_damage()
        cprint(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

NEW CODE (in dnd-5e-core):
    def attack(self, target):
        damage = self.calculate_damage()
        target.take_damage(damage)
        return {
            'attacker': self.name,
            'target': target.name,
            'damage': damage,
            'damage_type': self.damage_type
        }

UI LAYER (in main.py, main_ncurses.py, etc.):
    from dnd_5e_core.ui import cprint, Color, format_damage_message
    
    result = monster.attack(character)
    msg = format_damage_message(
        result['attacker'], 
        result['target'], 
        result['damage'],
        result.get('damage_type', '')
    )
    cprint(msg, Color.RED)
"""

