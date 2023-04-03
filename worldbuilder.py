import pygame
from dataclasses import dataclass
from typing import List, Tuple
import events as ev
import entities as en
import worldcontrollersingle as wcs
import worldcontrollermulti as wcm
import snakecontrollersingle as scs
import snakecontrollermulti as scm
import globals as glob

def buildWorldSingle(surface):
    world = wcs.WorldSingle(surface)
    snake = scs.SnakeSingle(body=[(10, 10), (9, 10), (8, 10)], direction=(1, 0), max_length=3)
    wall = en.Wall([(x, 0) for x in range(glob.WIDTH)] + [(x, glob.HEIGHT-1) for x in range(glob.WIDTH)] +
                [(0, x) for x in range(glob.HEIGHT)] + [(glob.WIDTH-1, x) for x in range(glob.HEIGHT)])
    world.entities.append(snake)
    world.entities.append(wall)
    world.message_queue.append(ev.SpawnFoodMessage())
    return world

def buildWorldMulti(surface):
    world = wcm.WorldMulti(surface)
    snake1 = scm.SnakeMulti(body=[(10, 10), (9, 10), (8, 10)], direction=(1, 0), max_length=3, player=1, color=(0, 255, 0))
    snake2 = scm.SnakeMulti(body=[(10, 30), (9, 30), (8, 30)], direction=(1, 0), max_length=3, player=2, color=(112, 214, 255))
    wall = en.Wall([(x, 0) for x in range(glob.WIDTH)] + [(x, glob.HEIGHT-1) for x in range(glob.WIDTH)] +
                [(0, x) for x in range(glob.HEIGHT)] + [(glob.WIDTH-1, x) for x in range(glob.HEIGHT)])
    
    world.entities.append(snake1)
    world.entities.append(snake2)
    world.entities.append(wall)
    world.message_queue.append(ev.SpawnFoodMessage())
    return world