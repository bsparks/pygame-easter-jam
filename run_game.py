import pygame
from engine.game import Game

RESOLUTION = (1280, 720)


def start():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    clock = pygame.time.Clock()
    
    game = Game(screen)
    
    game.startup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update(clock.get_time())

        screen.fill("black")
        
        game.draw()

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    start()
