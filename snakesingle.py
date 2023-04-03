import pygame
from dataclasses import dataclass
from typing import List, Tuple
import random
import events as ev
import entities as en
import worldcontrollersingle as wcs
import snakecontrollersingle as scs
import worldbuilder as wb
import settings 
import globals as glob
import gamelogic as gl
import gameoverhandler as goh

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
    world = wb.buildWorldSingle(surface)
    
    world.update()

    # run game
    gl.runWorldSingle(font, display, surface, world, clock)

    # end screen
    goh.gameover(font,display,clock)


if __name__ == "__main__":
    main()
