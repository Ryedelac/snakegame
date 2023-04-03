import pygame
from dataclasses import dataclass
from typing import List, Tuple
import events as ev
import entities as en
import globals as glob
import worldcontrollersingle
import worldcontrollermulti

def runWorldSingle(font, display, surface, world: worldcontrollersingle.WorldSingle, clock):
    # for every frame
    while world.running:
        # handle game logic
        world.update()

        # render in low resolution
        surface.fill("white")
        world.render()

        # render in high resolution
        display.blit(pygame.transform.scale(surface, display.get_rect().size), (0, 0))
        display.blit(font.render(f"Snake Length: {world.entities[0].max_length}", True, (0, 0, 0)), (10, 10))
        if world.paused:
            text = font.render(f"PAUSE (press P to continue)", True, (0, 0, 0))
            display.blit(text, ((glob.SCALE * glob.WIDTH - text.get_width()) / 2, (glob.SCALE * glob.HEIGHT - text.get_height()) / 2))
        pygame.display.flip()

        # wait till next frame
        default_speed = 10  # fps
        speed_factor = min(3.0, 1.0 + 0.1*world.entities[0].max_length)
        clock.tick(int(default_speed * speed_factor))

def runWorldMulti(font, display, surface, world: worldcontrollermulti.WorldMulti, clock):
     while world.running:
        # handle game logic
        world.update()

        # render in low resolution
        surface.fill("white")
        world.render()

        # render in high resolution
        display.blit(pygame.transform.scale(
            surface, display.get_rect().size), (0, 0))
        # display.blit(font.render(
        #     f"PLAYER 1 SCORE: {world.entities[0].max_length}", True, (0, 0, 0)), (15, 15))
        # display.blit(font.render(f"PLAYER 2 SCORE: {world.entities[1].max_length}", True, (
        #     0, 0, 0)), (glob.WIDTH*glob.SCALE - 215, 15))
        if world.paused:
                text = font.render(f"PAUSE (press P to continue)", True, (0, 0, 0))
                display.blit(text, ((glob.SCALE * glob.WIDTH - text.get_width()) /
                            2, (glob.SCALE * glob.HEIGHT - text.get_height()) / 2))
        pygame.display.flip()

        # wait till next frame
        default_speed = 10  # fps
        speed_factor = min(3.0, 1.0 + 0.1*world.entities[0].max_length)
        clock.tick(int(default_speed * speed_factor))