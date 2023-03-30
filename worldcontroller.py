import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import snakeevents as ev
import snakeentities as en
import globals as glob

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
        for i in range(len(self.entities)):
            for j in range(i, len(self.entities)):
                if self.entities[i].collides_with(self.entities[j]):
                    self.message_queue.append(ev.EntityCollisionMessage(self.entities[i], self.entities[j]))
                    self.message_queue.append(ev.EntityCollisionMessage(self.entities[j], self.entities[i]))

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
        for i in range(len(self.entities)):
            for j in range(i, len(self.entities)):
                if self.entities[i].collides_with(self.entities[j]):
                    self.message_queue.append(ev.EntityCollisionMessage(self.entities[i], self.entities[j]))
                    self.message_queue.append(ev.EntityCollisionMessage(self.entities[j], self.entities[i]))

        # update entities
        new_messages: List[ev.Message] = []
        living_snakes = False

        for entity in self.entities:
            tmp = entity.update(self.message_queue)
            if isinstance(entity, en.SnakeMulti):
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

def buildWorldSingle(surface):
    world = WorldSingle(surface)
    snake = en.SnakeSingle(body=[(10, 10), (9, 10), (8, 10)], direction=(1, 0), max_length=3)
    wall = en.Wall([(x, 0) for x in range(glob.WIDTH)] + [(x, glob.HEIGHT-1) for x in range(glob.WIDTH)] +
                [(0, x) for x in range(glob.HEIGHT)] + [(glob.WIDTH-1, x) for x in range(glob.HEIGHT)])
    world.entities.append(snake)
    world.entities.append(wall)
    world.message_queue.append(ev.SpawnFoodMessage())
    return world

def buildWorldMulti(surface):
    world = WorldMulti(surface)
    snake1 = en.SnakeMulti(body=[(10, 10), (9, 10), (8, 10)], direction=(1, 0), max_length=3, player=1, color=(0, 255, 0))
    snake2 = en.SnakeMulti(body=[(10, 30), (9, 30), (8, 30)], direction=(1, 0), max_length=3, player=2, color=(112, 214, 255))
    wall = en.Wall([(x, 0) for x in range(glob.WIDTH)] + [(x, glob.HEIGHT-1) for x in range(glob.WIDTH)] +
                [(0, x) for x in range(glob.HEIGHT)] + [(glob.WIDTH-1, x) for x in range(glob.HEIGHT)])
    
    world.entities.append(snake1)
    world.entities.append(snake2)
    world.entities.append(wall)
    world.message_queue.append(ev.SpawnFoodMessage())
    return world