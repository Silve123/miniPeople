import sys
import pygame





class World:
    def __init__(self, width, height, player, player_group, obstacles):
        self.width = width
        self.height = height
        self.player = player
        self.player_group = player_group
        self.obstacles = obstacles

    def get_world_size(self):
        return self.width, self.height

    def show_visible_area(self, screen):
        visibility_triangle = self.player.getVisibilityTriangle()
        triangle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.polygon(triangle_surface, (255, 255, 255, 100), visibility_triangle)

        for obstacle in self.obstacles:
            if self.check_collision(self.triangle_to_rect(visibility_triangle), obstacle.get_rect()):
                obstacle.draw(triangle_surface)

        screen.blit(triangle_surface, (0, 0))

    def triangle_to_rect(self, triangle):
        x_coords = [x for x, y in triangle]
        y_coords = [y for x, y in triangle]
        min_x, min_y = min(x_coords), min(y_coords)
        max_x, max_y = max(x_coords), max(y_coords)
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def check_collision(self, rect1, rect2):
        return rect1.colliderect(rect2)

    def doPlayerActions(self, screen):
        self.player.addObstacles(self.obstacles)
        self.player.setScreen(screen)
        self.player_group.update(world_width=self.width, world_height=self.height)
        self.obstacles = self.player.getObstacles()
        self.player_group.draw(screen)
        self.player_position = self.player.rect.x, self.player.rect.y
        self.show_visible_area(screen)

    def doToolBarActions(self, screen):
        toolbar_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(toolbar_surface, (0,0,0, 100), (0, 0, self.width, 20))

        # Draw the toolbar text
        font = pygame.font.Font(None, 20)
        food = self.player.inventory["Food"]
        water = self.player.inventory["Water"]
        stone = self.player.inventory["Stone"]
        wood = self.player.inventory["Wood"]
        toolbar = font.render(f"Hunger: {self.player.hunger} || Thurst: {self.player.thirst}\
|| Direction: {self.player.direction}  || Position(X,Y): ({self.player.rect.x},{self.player.rect.y}) \
|| Speed: {self.player.speed} || [Food: {food}, Water: {water}, Stone: {stone}, Wood: {wood}]",
        True, self.black)
        screen.blit(toolbar_surface, (0,0))
        screen.blit(toolbar, (0, 0))

    def run(self):
        # Initialize Pygame
        pygame.init()

        # Set the screen size
        screen = pygame.display.set_mode((self.width, self.height))

        # Set the clock
        clock = pygame.time.Clock()

        # Run the game loop
        running = True
        while running:
            # Kill player if they hungry or thirsty
            if self.player.hunger <= 0 and self.player.thirst <= 0:
                print("You unfortunatly died!!! RIP")
                pygame.quit()
                sys.exit()
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            screen.fill((0, 255, 0))

            border_rect = pygame.Rect(0, 0, self.width, self.height)
            border_color = (255, 0, 0)
            self.red, self.black = (255, 0, 0), (0, 0, 0)

            pygame.draw.rect(screen, border_color, border_rect, 2)  # added 2 as border width
            
            # Do all player actions including drawing the player and visible area
            self.doPlayerActions(screen)
            
            self.doToolBarActions(screen)

            # Update the screen
            pygame.display.update()


        # Quit Pygame
        pygame.quit()
