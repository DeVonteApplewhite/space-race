"""
asteroid_field.py.

Create asteroid objects on the game board.
"""

# Standard
import random
# Local
from .asteroids import Asteroid


class AsteroidField:
    def __init__(self, game_area, count, bottom_space):
        self.game_area = game_area
        self.count = count
        self.bottom = self.game_area.bottom - bottom_space

    def create_field(self):
        asteroids = list()
        width = self.game_area.width
        x_choices = range(1, width, Asteroid.player_width + 3)
        y_choices = list(range(5, self.bottom, Asteroid.player_height + 3))
        random.shuffle(y_choices)

        for _ in range(self.count//2):
            x = random.choice(x_choices)
            y = random.choice(y_choices[:len(y_choices)//2])
            asteroids.append(Asteroid(self.game_area, x, y))

        for _ in range(self.count//2, self.count):
            x = random.choice(x_choices)
            y = random.choice(y_choices[len(y_choices)//2:])
            asteroids.append(Asteroid(self.game_area, x, y, dx=-5))

        return asteroids
