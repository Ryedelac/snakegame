import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import snakeevents as ev
import snakeentities as en
import worldcontroller as wc
import settings 
import globals as glob
import gamelogic as gl


# ----------------------------------------------------------------------
# MAIN LOGIC
# ----------------------------------------------------------------------

def main():

    glob.init()
    settings.default()

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Ubuntu Sans', 30)

    pygame.display.set_caption("Snake game")
    display = pygame.display.set_mode((glob.SCALE*glob.WIDTH, glob.SCALE*glob.HEIGHT))  # actual game window
    surface = pygame.Surface((glob.WIDTH, glob.HEIGHT))  # lower resolution surface to render into
    clock = pygame.time.Clock()

    # prepare world
    world = wc.buildWorldMulti(surface)
    world.update()

    # run game
    gl.runWorldMulti(font, display, surface, world, clock)

    # end screen
    text = font.render("GAME OVER", True, (0, 0, 0))
    display.blit(text, ((glob.SCALE * glob.WIDTH - text.get_width()) / 2, (glob.SCALE * glob.HEIGHT - text.get_height()) / 2))
    pygame.display.flip()
    endscreen_running = True
    while endscreen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endscreen_running = False
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
