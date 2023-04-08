import pygame

RESOLUTION = (1280, 720)


def start():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    start()
