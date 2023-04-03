import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import events as ev
import entities as en
import globals as glob
import snakecontrollersingle as scs
import collisionhandler as ch

class WorldSingle:
    def __init__(self, surface: pygame.Surface):
        self.width: int = surface.get_width()
        self.height: int = surface.get_height()
        self.surface = surface
        self.entities: List[en.Entity] = []
        self.message_queue: List[ev.Message] = []
        self.running = True
        self.paused = False

    def render(self):
        for entity in self.entities:
            entity.render(self.surface)

    def update(self):
        pygame_events = pygame.event.get()

        # handle outside events
        for event in pygame_events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.message_queue.append(ev.SnakeSingleChangeDirectionMessage((0, -1)))
                elif event.key == pygame.K_DOWN:
                    self.message_queue.append(ev.SnakeSingleChangeDirectionMessage((0, 1)))
                elif event.key == pygame.K_RIGHT:
                    self.message_queue.append(ev.SnakeSingleChangeDirectionMessage((1, 0)))
                elif event.key == pygame.K_LEFT:
                    self.message_queue.append(ev.SnakeSingleChangeDirectionMessage((-1, 0)))
                elif event.key == pygame.K_p:
                    self.paused = not self.paused  # toggle pause

        if self.paused:
            self.message_queue.clear()
            return

        # handle collisions
        ch.handlecollisions(self)

        # update entities
        new_messages: List[ev.Message] = []

        for entity in self.entities:
            tmp = entity.update(self.message_queue)
            new_messages.extend(tmp)

        # handle global messages, clear queue
        self.message_queue.extend(new_messages)

        for message in self.message_queue:
            print(message)  # XXX

            if isinstance(message, ev.GameOverMessage):
                self.running = False
                return
            elif isinstance(message, ev.RemoveEntityMessage):
                self.entities.remove(message.entity)
            elif isinstance(message, ev.SpawnFoodMessage):
                for _ in range(100):
                    new_food = en.Food(position=(random.randrange(self.width), random.randrange(self.height)))
                    ok = True
                    for entity in self.entities:
                        if entity.collides_with(new_food):
                            ok = False
                            break
                    if ok:
                        break
                else:
                    raise RuntimeError("Failed to put food into empty space")

                self.entities.append(new_food)

        self.message_queue.clear()



