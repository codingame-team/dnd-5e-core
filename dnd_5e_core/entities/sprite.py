"""
D&D 5e Core - Sprite Entity
Base class for all positioned entities (monsters, characters)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Sprite:
    """
    Base class for entities with position in 2D space.
    Used by Monster and Character classes.
    """
    id: int
    image_name: str
    x: int
    y: int
    old_x: int
    old_y: int

    def __repr__(self):
        return f"#{self.id} {self.image_name} ({self.x}, {self.y})"

    @property
    def pos(self) -> tuple:
        """Current position as (x, y) tuple"""
        return self.x, self.y

    @property
    def old_pos(self) -> tuple:
        """Previous position as (x, y) tuple"""
        return self.old_x, self.old_y

    def check_collision(self, other: 'Sprite') -> bool:
        """Check if this sprite collides with another sprite"""
        return self.x == other.x and self.y == other.y

    def move(self, dx: int, dy: int):
        """Move sprite by delta x and delta y"""
        self.old_x, self.old_y = self.x, self.y
        self.x += dx
        self.y += dy

    def set_position(self, x: int, y: int):
        """Set absolute position"""
        self.old_x, self.old_y = self.x, self.y
        self.x, self.y = x, y

