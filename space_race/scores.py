"""
scores.py

Render the scores of each player on the screen.
"""

# Third Party
import pygame
pygame.font.init()


class Score:
    color = (253, 94, 83)  # Periwinkle
    background = (0, 0, 0)
    font_name = 'latin1'
    font_size = 75

    def __init__(self, entity, x, y):
        self.entity = entity
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.font = pygame.font.SysFont(Score.font_name, Score.font_size)
        self.score = self.entity.score

    def draw(self, screen):
        surface = self.font.render(
            str(self.score),
            True,
            Score.color,
            Score.background
        )
        screen.blit(surface, self.position)

    @staticmethod
    def handle_input(event):
        _ = event
        return None

    def update(self):
        self.score = self.entity.score
