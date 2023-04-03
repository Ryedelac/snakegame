import pygame
import settings 
import globals as glob

def gameover(font,display,clock):
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
