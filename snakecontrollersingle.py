import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import events as ev
import entities as en

@dataclass
class SnakeSingle(en.Entity):
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
                elif isinstance(message.other, en.Wall):
                    new_messages.append(ev.GameOverMessage("Snake hit wall"))
                elif isinstance(message.other, en.Food):
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