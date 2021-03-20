"""
scores.py

Render the scores of each player on the screen.
"""

# Standard
import time

# Third Party
import pygame


class TimeLimit:
    color = (0, 0, 128)  # Periwinkle
    background = (0, 0, 0)

    def __init__(self, entity, x, y, width, height, duration):
        self.entity = entity
        self.x = x
        self.y = y
        self.bottom = height
        self.position = (self.x, self.y)
        self.surface = pygame.Surface((width, height))
        self.initial_height = height
        self.height = height
        self.width = width
        self.surface.fill(TimeLimit.color)
        self.rect = self.surface.get_rect()
        self.duration = duration
        self.start_time = time.time()

    def draw(self, screen):
        screen.blit(self.surface, self.position)

    @staticmethod
    def handle_input(event):
        _ = event
        return None

    def update(self):
        elapsed = time.time() - self.start_time
        new_height = int(self.initial_height * (1 - elapsed / self.duration))
        if new_height > 0 and new_height != self.height:
            self.height = new_height
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(TimeLimit.color)
            self.rect = self.surface.get_rect()
