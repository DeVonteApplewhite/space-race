"""
asteroids.py.

Implements obstacles in the game.
"""

# Third Party
import pygame

# Local
from . import base


class MovementState(base.BasePlayerState):
    """
    Handles asteroid movement.
    """
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.out_of_bounds = False
        self.direction = 'right' if self.entity.dx > 0 else 'left'
        print(self.entity.x, self.entity.y, __file__, "In Movement state.")

    def handle_input(self, event):
        return None

    def resolve_collisions(self):
        if not self.entity.game_area.contains(self.entity.rect):
            if not self.entity.game_area.colliderect(self.entity.rect):
                self.out_of_bounds = True

    def update(self):
        if self.out_of_bounds:
            self.entity.x = 1 if self.direction == 'right' else self.entity.game_area.right - 1
            self.out_of_bounds = False
            return

        self.resolve_collisions()
        self.entity.x += self.entity.dx


class Asteroid:
    player_width = 12
    player_height = 4
    color = (255, 255, 255)

    def __init__(self, game_area, x, y, dx=2, dy=0, max_velocity=5):
        self.game_area = game_area
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.max_velocity = max_velocity
        self.state = MovementState(self)
        self.surface = pygame.Surface((Asteroid.player_width, Asteroid.player_height))
        self.surface.fill(Asteroid.color)
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def handle_input(self, event):
        new_state = self.state.handle_input(event)
        if new_state is not None:
            self.state = new_state

    def update(self):
        self.state.update()
        self.rect.x = self.x
        self.rect.y = self.y
