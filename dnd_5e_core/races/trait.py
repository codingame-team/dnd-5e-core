"""
D&D 5e Core - Trait System
Racial traits for D&D 5e
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Trait:
    """
    A racial trait in D&D 5e (e.g., Darkvision, Fey Ancestry, Brave).

    Traits provide special abilities or bonuses to races.
    """
    index: str
    name: str
    desc: str

    def __repr__(self):
        return f"{self.name}"

