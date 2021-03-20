"""
player.py.

Implements gameplay.
"""

# Third Party
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
    KEYUP
)

# Local
from . import base


class ResetPositionState(base.BasePlayerState):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.entity.y = self.entity.game_area.bottom
        self.dy = -1
        print(self.entity.x, self.entity.y, __file__, "In Reset Position state.")

    def handle_input(self, event):
        return None

    def update(self):
        if self.entity.rect.bottom < self.entity.game_area.bottom:
            self.entity.state = NavigationState(self.entity)
            return
        self.entity.y += self.dy


class ShipHitState(base.BasePlayerState):
    """
    Handles the details of the ship getting hit.
    """

    duration = 10

    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.frames = 0
        # self.entity.y = self.entity.game_area.bottom
        print(self.entity.x, self.entity.y, __file__, "In Ship Hit state.")

    def handle_input(self, event):
        return None

    def update(self):
        if self.frames >= ShipHitState.duration:
            self.entity.y = self.entity.game_area.bottom
            self.entity.state = ResetPositionState(self.entity)
            return
        self.frames += 1


class NavigationState(base.BasePlayerState):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.movement_keys = [K_UP, K_DOWN]
        self.velocities = {
            K_UP: entity.max_velocity * -1,
            K_DOWN: entity.max_velocity
        }
        self.moving = False
        self.out_of_bounds = False
        self.hit = False
        print(self.entity.x, self.entity.y, __file__, "In Navigation state.")

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key in self.movement_keys:
                self.entity.dy = self.velocities[event.key]
            self.moving = True
        elif event.type == KEYUP:
            self.moving = False
        return None

    def resolve_collisions(self):
        if not self.entity.game_area.contains(self.entity.rect):
            if not self.entity.game_area.colliderect(self.entity.rect):
                self.out_of_bounds = True
                return

        if self.entity.rect.collidelist(self.entity.obstacles) > -1:
            self.hit = True

    def update(self):
        if self.out_of_bounds:
            if self.entity.y <= self.entity.game_area.y:
                self.entity.score += 1

            self.entity.y = self.entity.game_area.bottom
            self.entity.state = ResetPositionState(self.entity)
            return
        if self.hit:
            self.entity.state = ShipHitState(self.entity)
            return

        self.resolve_collisions()
        if not self.moving:
            return
        self.entity.y += self.entity.dy


class Player:
    player_width = 14
    player_height = 24
    color = (0, 204, 204)  # Periwinkle

    def __init__(self, game_area, obstacles, x, y, dx=0, dy=-5, max_velocity=5):
        self.game_area = game_area
        self.obstacles = obstacles
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.max_velocity = max_velocity
        self.state = NavigationState(self)
        self.surface = pygame.Surface((Player.player_width, Player.player_height))
        self.surface.fill(Player.color)
        self.rect = self.surface.get_rect()
        self.score = 0

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
