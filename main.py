import random
import sys
import pygame
from obstacle import Obstacle
from player import Player
from world import World

# ========================================================================
# Create a player instance
player = Player(390, 290,[])

# Create a sprite group for the player
player_group = pygame.sprite.Group()
player_group.add(player)

obstacle_x, obstacle_y = 1, 15

def startApp(args):
    arguments = args
    if '-S' in arguments:
        index = arguments.index('-S')
        try:
            world_width, world_height = map(int, arguments[index + 1].split(','))
        except:
            print("Invalid world size argument. Using default world size of 800x600.")
            world_width, world_height = 800, 600
    else:
        world_width, world_height = 800, 600

    world = World(world_width, world_height, player, player_group, randomObstacles())
    world.run()

def threeObstacles():
    obstacles = []
    obstacles.append(Obstacle(10, 10, Obstacle.ObstacleType.TREE, 10, 10, (0,100,0), obstacles))
    obstacles.append(Obstacle(40, 25, Obstacle.ObstacleType.WATER, 10, 10, (0, 0, 255), obstacles))
    return obstacles

def randomObstacles():
    obstacles = []
    obstacle_types = [Obstacle.ObstacleType.TREE, Obstacle.ObstacleType.WATER, Obstacle.ObstacleType.STONE]
    colors = [(0,100,0), (0,0,255), (0,0,100)]
    widths = [10, 10, 10]
    heights = [10, 10, 10]

    for i in range(random.randint(200,600)):
        obstacle_type = random.choice(obstacle_types)
        if obstacle_type == Obstacle.ObstacleType.TREE:
            color = colors[0]
        elif obstacle_type == Obstacle.ObstacleType.WATER:
            color = colors[1]
        elif obstacle_type == Obstacle.ObstacleType.STONE:
            color = colors[2]
        width = random.choice(widths)
        height = random.choice(heights)
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        obstacle = Obstacle(x, y, width, height, color, obstacle_type)
        if obstacle.checkAvailability(obstacles):
            obstacles.append(obstacle)

    return obstacles





if __name__ == "__main__":
    startApp(sys.argv)


