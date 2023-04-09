import pygame
from game.game import Game

RESOLUTION = (1280, 720)
GAME_NAME = "Easter Survivors"
FPS = 60


def start():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(GAME_NAME)
    clock = pygame.time.Clock()
    
    game = Game(screen)
    
    game.startup()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.handle_events(events)
        game.update(clock.get_time())

        screen.fill("black")
        
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    start()
