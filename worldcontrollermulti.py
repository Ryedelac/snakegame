import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import events as ev
import entities as en
import globals as glob
import snakecontrollermulti as scm
import collisionhandler as ch


class WorldMulti:
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
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=1, direction=(0, -1)))
                elif event.key == pygame.K_DOWN:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=1, direction=(0, 1)))
                elif event.key == pygame.K_RIGHT:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=1, direction=(1, 0)))
                elif event.key == pygame.K_LEFT:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=1, direction=(-1, 0)))
                elif event.key == pygame.K_w:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=2, direction=(0, -1)))
                elif event.key == pygame.K_s:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=2, direction=(0, 1)))
                elif event.key == pygame.K_d:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=2, direction=(1, 0)))
                elif event.key == pygame.K_a:
                    self.message_queue.append(ev.SnakeMultiChangeDirectionMessage(player=2, direction=(-1, 0)))
                elif event.key == pygame.K_p:
                    self.paused = not self.paused  # toggle pause

        if self.paused:
            self.message_queue.clear()
            return

        # handle collisions
        ch.handlecollisions(self)

        # update entities
        new_messages: List[ev.Message] = []
        living_snakes = False

        for entity in self.entities:
            tmp = entity.update(self.message_queue)
            if isinstance(entity, scm.SnakeMulti):
                living_snakes = True
            new_messages.extend(tmp)

        if not living_snakes:
            new_messages.append(ev.GameOverMessage("all players are out of the game"))

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

