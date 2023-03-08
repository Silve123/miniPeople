import math
import time
import pygame




red = (255,0,0)
# Create a Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacles):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "NORTH"
        self.obstacles = obstacles
        self.hunger = 100
        self.thirst = 100
        self.time = pygame.time.get_ticks()
        self.inventory = {"Stone":0,"Water":0,"Food":0, "Wood":0}


    def update(self, world_width, world_height):

        # Implement hunger and Thirst
        self.hungerThirstImplementation()
        keys = pygame.key.get_pressed()

        # speed of player 
        self.speedImplementation(keys)

        # Interaction of obstacle
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.callObstacleInteraction(self.rect.copy())

        self.movementImplementation(keys, world_width, world_height)

        # Player rotation
        self.rotationImplementation(keys)

        self.inventoryImplementation(keys)


    def inventoryImplementation(self, keys):
        if keys[pygame.K_c]:
            self.displayInventory(self.getCrafts(), False)
            if keys[pygame.K_1]:
                time.sleep(0.4)
                if self.inventory["Food"]>0 and self.hunger<=90:
                    self.hunger += 10
                    self.inventory["Food"]-=1
                
            elif keys[pygame.K_2]:
                time.sleep(0.4)
                if self.inventory["Water"]>0 and self.thirst<=90:
                    self.thirst += 10
                    self.inventory["Water"]-=1
            elif keys[pygame.K_3]:
                time.sleep(0.4)
                self.displayInventory(self.getcraftables(), True)
                if keys[pygame.K_F1]:
                    print("building woodern wall")
                elif keys[pygame.K_F2]:
                    print("building stone wall")
                elif keys[pygame.K_F3]:
                    print("building fire")


    def displayInventory(self, text_lines, _left):
        toolbar_surface = pygame.Surface((200,200), pygame.SRCALPHA)
        pygame.draw.rect(toolbar_surface, (255,255,255, 150), (0, 0, 200, 200))

        # Draw the toolbar text
        font = pygame.font.SysFont("Arial", 18)
        background_location = (self.rect.x-215,self.rect.y) if _left else (self.rect.x-10,self.rect.y)
        self.screen.blit(toolbar_surface,background_location)

        text_height = 0
        for line in text_lines:
            text = font.render(line, True, (0, 0, 0))
            text_location = (self.rect.x-210, self.rect.y+5 + text_height) if _left else (self.rect.x+15, self.rect.y+5 + text_height)
            self.screen.blit(text, text_location)
            text_height += text.get_height()


    def getcraftables(self):
        craftables = ["Craftables:"]
        craftCount = 0
        for key in self.inventory.keys():
            if key == "Wood" and self.inventory[key]>10:
                craftables.append(f"(F1) Wooden Wall")
            elif key == "Stone" and self.inventory[key]>10:
                craftables.append(f"(F2) Stone Wall")
            elif self.inventory["Stone"]>10 and self.inventory["Wood"]>10 and craftCount<1:
                craftables.append(f"(F3) fire")
                craftCount+=1
        return craftables
    
    
    def getCrafts(self):
        craftables = ["Commands:"]
        craftCount = 0
        for key in self.inventory.keys():
            if key == "Food" and self.inventory[key]>0:
                craftables.append(f"({1}) Eat")
            elif key == "Water" and self.inventory[key]>0:
                craftables.append(f"({2}) Drink")
            elif self.inventory["Stone"]>0 and self.inventory["Wood"]>0 and craftCount<1:
                craftables.append(f"({3}) Craft")
                craftCount+=1
        return craftables


    def setScreen(self, screen):
        self.screen = screen


    def rotationImplementation(self, keys):
        if keys[pygame.K_q]:
            time.sleep(0.4)
            if self.direction == "NORTH":
                self.direction = "WEST"
            elif self.direction == "WEST":
                self.direction = "SOUTH"
            elif self.direction == "SOUTH":
                self.direction = "EAST"
            else:
                self.direction = "NORTH"
        if keys[pygame.K_e]:
            time.sleep(0.4)
            if self.direction == "NORTH":
                self.direction = "EAST"
            elif self.direction == "EAST":
                self.direction = "SOUTH"
            elif self.direction == "SOUTH":
                self.direction = "WEST"
            else:
                self.direction = "NORTH"


    def speedImplementation(self, keys):
        if keys[pygame.K_LSHIFT]:
            self.speed = 3
        else:
            self.speed = 1


    def hungerThirstImplementation(self):
        if pygame.time.get_ticks() - self.time >= 5000:
            self.hunger -= 1 if self.hunger > 0 else 0
            self.thirst -= 1 if self.thirst > 0 else 0
            self.time = pygame.time.get_ticks()  # Reset the elapsed time


    def movementImplementation(self, keys, world_width, world_height):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.y > 0:
                new_rect = self.rect.copy()
                new_rect.y -= self.speed
                if not self.collides_with_obstacle(new_rect):
                    self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.y < world_height - self.rect.height:
                new_rect = self.rect.copy()
                new_rect.y += self.speed
                if not self.collides_with_obstacle(new_rect):
                    self.rect.y += self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.x < world_width - self.rect.width:
                new_rect = self.rect.copy()
                new_rect.x += self.speed
                if not self.collides_with_obstacle(new_rect):
                    self.rect.x += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.x > 0:
                new_rect = self.rect.copy()
                new_rect.x -= self.speed
                if not self.collides_with_obstacle(new_rect):
                    self.rect.x -= self.speed


    def collides_with_obstacle(self, new_rect):
        for obstacle in self.obstacles:
            if new_rect.colliderect(obstacle.get_rect()):
                return True
        return False


    def collides_with_interaction(self, new_rect):
        for obstacle in self.obstacles:
            if new_rect.colliderect(obstacle.get_rect()):
                return obstacle
        return None
        

    def callObstacleInteraction(self, new_rect):
        collided_obstacle = self.collides_with_interaction(self.getExtended(new_rect))
        if collided_obstacle:
            collided_obstacle.interaction(self)
            self.obstacles.remove(collided_obstacle)
            return


    def getExtended(self, new_rect):
        if self.direction == "NORTH":
            new_rect.y -= 1
        elif self.direction == "SOUTH":
            new_rect.y += 1
        elif self.direction == "EAST":
            new_rect.x += 1
        elif self.direction == "WEST":
            new_rect.x -= 1
        return new_rect


    def addObstacles(self, obstacles):
        self.obstacles = obstacles


    def getObstacles(self):
        return self.obstacles


    def getVisibilityTriangle(self):
        x, y = self.rect.x, self.rect.y
        direction = self.direction
        width, height = 80, 60
        if direction == "NORTH":
            return [(x, y), (x - width / 2, y - height), (x + width / 2, y - height)]
        elif direction == "EAST":
            return [(x, y), (x + height, y - width / 2), (x + height, y + width / 2)]
        elif direction == "SOUTH":
            return [(x, y), (x + width / 2, y + height), (x - width / 2, y + height)]
        elif direction == "WEST":
            return [(x, y), (x - height, y + width / 2), (x - height, y - width / 2)]
