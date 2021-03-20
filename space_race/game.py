"""
game.py.

Implements gameplay.
"""
# Standard
import sys

# Third Party
import pygame

# Local
from .asteroid_field import AsteroidField
from .player import Player
from .aiplayer import AIPlayer
from .scores import Score
from .time_limit import TimeLimit


class GameArea:
    background_color = (0, 0, 0)
    asteroid_count = 20
    margin = 105

    def __init__(self, width=900, height=600, frame_rate=10):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.rect = self.screen.get_rect()
        self.entities = list()
        self.asteroids = list()
        self.player = None
        self.opponent = None
        self.setup()
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()

    def setup(self):
        asteroid_field = AsteroidField(self.rect, GameArea.asteroid_count, GameArea.margin)
        self.asteroids.extend(asteroid_field.create_field())
        self.entities.extend(self.asteroids)

        player = Player(self.rect, self.asteroids, (self.width//4), (self.height - Player.player_height))
        self.player = player
        self.entities.append(
            player
        )
        self.entities.append(
            Score(player, (self.width // 4) + 100, (self.height - 50))
        )
        aiplayer = AIPlayer(self.rect, self.asteroids, (self.width // 4)*3, (self.height - AIPlayer.player_height))
        self.opponent = aiplayer
        self.entities.append(
            aiplayer
        )
        self.entities.append(
            Score(aiplayer, (self.width // 4)*3 - 100, (self.height - 50))
        )
        self.entities.append(TimeLimit(self.rect, self.width // 2 - 10, self.height // 4, 20, self.height // 4 * 3, 30))

    def run(self):
        while 1:
            self.screen.fill(GameArea.background_color)
            for entity in self.entities:
                entity.draw(self.screen)
                entity.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                for entity in self.entities:
                    entity.handle_input(event)

            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == '__main__':
    game_area = GameArea()
    game_area.run()
