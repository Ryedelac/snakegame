import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import snakeevents as ev
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

@dataclass
class SnakeMulti(Entity):
    body: List[Tuple[int, int]]  # [head, ..., tail]
    direction: Tuple[int, int]  # (1, 0) or such
    max_length: int
    player: int
    color: Tuple[int, int, int]  # RGB

    def render(self, surface: pygame.Surface):
        r, g, b = self.color

        for i, position in enumerate(self.body):
            if i == 0:
                surface.set_at(position, (int(0.8*r), int(0.8*g), int(0.8*b)))  # make head slightly darker
            else:
                surface.set_at(position, (r, g, b))

    def update(self, messages: List[ev.Message]) -> List[ev.Message]:
        new_messages = []

        # handle events
        for message in messages:
            if isinstance(message, ev.SnakeMultiChangeDirectionMessage):
                # make sure we don't allow changing to opposite direction, which would self-collide our hero
                if message.player == self.player and any(x+y != 0 for x, y in zip(message.direction, self.direction)):
                    self.direction = message.direction
            elif isinstance(message, ev.EntityCollisionMessage) and message.entity is self:
                if message.other is self:
                    new_messages.append(ev.RemoveEntityMessage(self))
                    # new_messages.append(GameOverMessage("Snake bit its tail"))
                elif isinstance(message.other, Wall):
                    new_messages.append(ev.RemoveEntityMessage(self))
                    # new_messages.append(GameOverMessage("Snake hit wall"))
                elif isinstance(message.other, Food):
                    self.max_length += 1
                    new_messages.append(ev.RemoveEntityMessage(message.other))
                    new_messages.append(ev.SpawnFoodMessage())

        # move snake
        old_head = self.body[0]
        new_head = (old_head[0] + self.direction[0],
                    old_head[1] + self.direction[1])
        self.body.insert(0, new_head)

        while len(self.body) > self.max_length:
            self.body.pop()

        return new_messages

    def get_extent(self) -> List[Tuple[int, int]]:
        return self.body

    def collides_with(self, other: "Entity") -> bool:
        if other is self:
            return len(set(self.body)) != len(self.body)  # detect snake self-collision
        else:
            return super(SnakeMulti, self).collides_with(other)  # defer to default implementation

@dataclass
class SnakeSingle(Entity):
    body: List[Tuple[int, int]]  # [head, ..., tail]
    direction: Tuple[int, int]  # (1, 0) or such
    max_length: int

    def render(self, surface: pygame.Surface):
        for i, position in enumerate(self.body):
            if i == 0:
                surface.set_at(position, (0, 200, 0))  # make head slightly darker
            else:
                surface.set_at(position, (0, 255, 0))

    def update(self, messages: List[ev.Message]) -> List[ev.Message]:
        new_messages = []

        # handle events
        for message in messages:
            if isinstance(message, ev.SnakeSingleChangeDirectionMessage):
                # make sure we don't allow changing to opposite direction, which would self-collide our hero
                if any(x+y != 0 for x, y in zip(message.direction, self.direction)):
                    self.direction = message.direction
            elif isinstance(message, ev.EntityCollisionMessage) and message.entity is self:
                if message.other is self:
                    new_messages.append(ev.GameOverMessage("Snake bit its tail"))
                elif isinstance(message.other, Wall):
                    new_messages.append(ev.GameOverMessage("Snake hit wall"))
                elif isinstance(message.other, Food):
                    self.max_length += 1
                    new_messages.append(ev.RemoveEntityMessage(message.other))
                    new_messages.append(ev.SpawnFoodMessage())

        # move snake
        old_head = self.body[0]
        new_head = (old_head[0] + self.direction[0],
                    old_head[1] + self.direction[1])
        self.body.insert(0, new_head)

        while len(self.body) > self.max_length:
            self.body.pop()

        return new_messages

    def get_extent(self) -> List[Tuple[int, int]]:
        return self.body

    def collides_with(self, other: "Entity") -> bool:
        if other is self:
            return len(set(self.body)) != len(self.body)  # detect snake self-collision
        else:
            return super(SnakeSingle, self).collides_with(other)  # defer to default implementation