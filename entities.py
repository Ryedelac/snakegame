import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import events as ev
# ----------------------------------------------------------------------
# ENTITIES
# ----------------------------------------------------------------------

@dataclass
class Entity:
    def render(self, surface: pygame.Surface):
        pass

    def update(self, messages: List[ev.Message]) -> List[ev.Message]:
        return []

    def get_extent(self) -> List[Tuple[int, int]]:
        return []

    def collides_with(self, other: "Entity") -> bool:
        if other is self:
            return False  # no self collision by default
        else:
            return bool(set(self.get_extent()) & set(other.get_extent()))

@dataclass
class Food(Entity):
    position: Tuple[int, int]

    def render(self, surface: pygame.Surface):
        surface.set_at(self.position, "red")

    def get_extent(self) -> List[Tuple[int, int]]:
        return [self.position]

@dataclass
class Wall(Entity):
    positions: List[Tuple[int, int]]

    def render(self, surface: pygame.Surface):
        for position in self.positions:
            x, y = position
            if (x + y) % 2 == 0:
                surface.set_at(position, (100, 100, 100))
            else:
                surface.set_at(position, (120, 120, 120))

    def get_extent(self) -> List[Tuple[int, int]]:
        return self.positions