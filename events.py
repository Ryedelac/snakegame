import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random


# ----------------------------------------------------------------------
# MESSAGES (EVENTS)
# ----------------------------------------------------------------------

@dataclass
class Message:
    pass

@dataclass
class SnakeMultiChangeDirectionMessage(Message):
    player: int
    direction: Tuple[int, int]

@dataclass
class SnakeSingleChangeDirectionMessage(Message):
    direction: Tuple[int, int]

@dataclass
class SpawnFoodMessage(Message):
    pass

@dataclass
class RemoveEntityMessage(Message):
    entity: "Entity"

@dataclass
class EntityCollisionMessage(Message):
    entity: "Entity"
    other: "Entity"

@dataclass
class GameOverMessage(Message):
    reason: str
