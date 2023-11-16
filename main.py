import pygame
import sys
from snake import Snake


MIDNIGHT_BLUE = (25, 25, 112)
ROYAL_BLUE = (65, 105, 225)


class Game(object):
    def __init__(self):
        self.max_fps = 10  # 60
        self.width, self.height = 500, 500

        pygame.init()
        pygame.display.set_caption('Snake')

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.fps_clock = pygame.time.Clock()
        self.fps_delta = 0

        self.player = Snake(self)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit(0)

            self.fps_delta += self.fps_clock.tick()
            while self.fps_delta > 1000.0 / self.max_fps:
                self.tick()
                self.fps_delta -= 1000.0 / self.max_fps

                self.screen.fill((0, 0, 0))

                pygame.draw.rect(self.screen, MIDNIGHT_BLUE, [0, 0, self.width, self.width / 40])
                pygame.draw.rect(self.screen, MIDNIGHT_BLUE, [0, self.height - self.width / 40, self.width, self.height])
                pygame.draw.rect(self.screen, MIDNIGHT_BLUE, [0, 0, self.width / 40, self.height])
                pygame.draw.rect(self.screen, MIDNIGHT_BLUE, [self.width - self.width / 40, 0, self.width, self.height])

                self.draw()
                pygame.display.flip()

    def tick(self):
        self.player.tick()

    def draw(self):
        self.player.draw()

    def game_over(self):
        f = open("score.txt", "r")
        best = int(f.read())
        my_font = pygame.font.SysFont('times new roman', 15)

        if best > self.player.size:
            game_over_surface = my_font.render(f'Your score this time was : {str(self.player.size)}. '
                                               f'Best score : {best}', True, ROYAL_BLUE)
        if best == self.player.size:
            game_over_surface = my_font.render(f'You achieved the previous record of : {str(self.player.size)}', True,
                                               ROYAL_BLUE)
        if best < self.player.size:
            game_over_surface = my_font.render(f'You bet the previous best with the score of: {str(self.player.size)}. '
                                               f'Previous best : {best}', True, ROYAL_BLUE)
            f = open("score.txt", "w")
            f.write(str(self.player.size))
            f.close()

        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.width / 2, self.height / 4)
        self.screen.blit(game_over_surface, game_over_rect)

        restart_surface = my_font.render('Do you want to try again? (y/n)', True, ROYAL_BLUE)
        restart_rect = restart_surface.get_rect()
        restart_rect.midbottom = (self.width / 2, self.height / 3)
        self.screen.blit(restart_surface, restart_rect)

        pygame.display.flip()

        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                Game()
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_n):
                sys.exit(0)


if __name__ == "__main__":
    Game()
