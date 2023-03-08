import random

import pygame

class Obstacle:
    class ObstacleType:
        TREE = 100
        WATER = 200
        STONE = 300

    def __init__(self, x, y, width, height, color, obstacle_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.type = obstacle_type

    def checkAvailability(self, obstacles):
        for obstacle in obstacles:
            if self.x + self.width >= obstacle.x and self.x <= obstacle.x + obstacle.width and self.y + self.height >= obstacle.y and self.y <= obstacle.y + obstacle.height:
                return False
        return True

    def getType(self):
        return self.type

    def draw(self, screen):
        if self.getType() == self.ObstacleType.TREE:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.getType() == self.ObstacleType.WATER:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.getType() == self.ObstacleType.STONE:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.width//2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def interaction(self, player):
        if self.getType() == self.ObstacleType.TREE:
            player.inventory["Food"] += 1
            player.inventory["Wood"] += 1

        elif self.getType() == self.ObstacleType.WATER:
            player.inventory["Water"] += 1

        elif self.getType() == self.ObstacleType.STONE:
            player.inventory["Stone"] += 1
        

