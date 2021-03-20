"""
strategies.py.

Implement strategies for the AI player.
"""

# Standard
import math
import random

# Third Party
# import pygame

# Local
from .base import BaseAIStrategy

# Globals
BACKWARDS = 'back'
FORWARD = 'forward'
STATIONARY = 'stationary'


class MostlyForwardStrategy(BaseAIStrategy):
    weights = {
        FORWARD: 70,
        STATIONARY: 10,
        BACKWARDS: 20
    }
    choice_duration = 10

    def __init__(self, entity, obstacles):
        self.entity = entity
        self.obstacles = obstacles
        self.options = self.init_options()
        self.frames = 0
        self.dy = 0

    def init_options(self):
        max_velocity = self.entity.max_velocity
        movement = {
            FORWARD: -max_velocity,
            STATIONARY: 0,
            BACKWARDS: max_velocity
        }
        options = []
        for direction, weight in MostlyForwardStrategy.weights.items():
            options.extend([movement[direction]] * (weight//10))
        print(options)
        return options

    def strategy(self):
        if 0 < self.frames < MostlyForwardStrategy.choice_duration:
            self.frames += 1
        else:
            self.dy = random.choice(self.options)
            self.frames = 1
        return self.dy


class SafeSpotStrategy(BaseAIStrategy):
    weights = {
        FORWARD: 70,
        STATIONARY: 20,
        BACKWARDS: 10
    }
    choice_duration = 10

    def __init__(self, entity, obstacles):
        self.entity = entity
        self.obstacles = obstacles
        self.frames = 0
        self.dy = 0
        self.executing_strategy = False
        self.target_y = 0

    def is_near(self, obstacle, future_frame):
        obstacle_y = obstacle[3].y
        obstacle_y_bottom = obstacle[3].rect.bottom
        y = self.entity.y - (self.entity.max_velocity * future_frame)
        if obstacle_y <= y <= obstacle_y_bottom and abs(obstacle[2] - future_frame) <= 10:
            return True
        return False

    def get_nearby_obstacles(self, obstacle_stats, future_frame):
        nearby_obstacles = [obstacle for obstacle in obstacle_stats if self.is_near(obstacle, future_frame)]
        return nearby_obstacles

    def best_safe_position(self, obstacle_stats):
        lookahead_frames = 6
        target_frame = lookahead_frames
        for frame in range(lookahead_frames+1):
            nearby_obstacles = self.get_nearby_obstacles(obstacle_stats, frame)
            print('Frame:', frame, 'Obstacles:', nearby_obstacles)
            if nearby_obstacles:
                target_frame = frame - 1
                break
        print('Target frame:', target_frame)
        self.target_y = self.entity.y - ((frame - 1) * self.entity.max_velocity)
        self.dy = -self.entity.max_velocity
        self.executing_strategy = True

    def increment_execution(self):
        if (self.target_y - self.entity.y) <= self.entity.max_velocity:
            print('Finished executing strategy.')
            self.executing_strategy = False

    def strategy(self):
        if self.executing_strategy:
            self.increment_execution()
            return self.dy

        obstacle_stats = []
        entity_y = self.entity.y
        for obstacle in self.obstacles:
            current_x = obstacle.x
            current_y = obstacle.y
            frames_to_collision = abs((current_x - entity_y)//obstacle.max_velocity)
            obstacle_stats.append((current_x, current_y, frames_to_collision, obstacle))
        print(obstacle_stats[0])
        self.best_safe_position(obstacle_stats)
        return self.dy


class LookaheadLookbehindStrategy(BaseAIStrategy):
    def __init__(self, entity, obstacles):
        self.entity = entity
        self.obstacles = obstacles
        self.frames = 0
        self.dy = 0
        self.executing_strategy = False
        self.target_y = 0

    def strategy(self):
        pass
