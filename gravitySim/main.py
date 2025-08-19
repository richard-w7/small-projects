import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1425, 840
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

# Constants
PLANET_MASS = 100
SHIP_MASS = 5
G = 5                  
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100       

WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK  = (0, 0, 0)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(win, YELLOW, (self.x, self.y), PLANET_SIZE)

# User launched
class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.color = RED
        self.orbiting = False
        self.path = []  # stores trajectory points

    def move(self, planet):
        # Calculate gravitational force
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2
        
        # Decompose acceleration into x and y components
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        # Update velocity and position
        self.vel_x += acceleration_x
        self.vel_y += acceleration_y
        self.x += self.vel_x
        self.y += self.vel_y

        # Track orbit path
        if self.orbiting:
            self.path.append((int(self.x), int(self.y)))
            if len(self.path) > 1500:  # memory cap
                self.path.pop(0)

    def draw(self):
        if self.orbiting and len(self.path) > 2:
            pygame.draw.lines(win, WHITE, False, self.path, 1)
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), OBJ_SIZE)

    def check_orbit(self, planet):
        if self.orbiting:  
            return  # Already orbiting
        
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)

        if PLANET_SIZE + 10 < distance < 300:
            speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
            escape_velocity = math.sqrt(2 * G * planet.mass / distance)

            # Orbit if speed is between 50–95% of escape velocity
            if escape_velocity * 0.5 < speed < escape_velocity * 0.95:
                self.orbiting = True
                self.color = GREEN
                self.path = [(int(self.x), int(self.y))]  # reset path

def create_ship(location, mouse_pos):
    # Spacecraft based on users clicks
    start_x, start_y = location
    mouse_x, mouse_y = mouse_pos

    vel_x = (mouse_x - start_x) / VEL_SCALE
    vel_y = (mouse_y - start_y) / VEL_SCALE

    return Spacecraft(start_x, start_y, vel_x, vel_y, SHIP_MASS)

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    spacecrafts = []
    temp_obj_pos = None  # temporary starting point for new ship

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse handling for creating spacecraft
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    # Launch spacecraft
                    spacecrafts.append(create_ship(temp_obj_pos, mouse_pos))
                    temp_obj_pos = None
                else:
                    # Set starting point
                    temp_obj_pos = mouse_pos

        win.fill(BLACK)

        # Show preview line while setting trajectory
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        # Update and draw all spacecraft
        for obj in spacecrafts[:]:
            obj.move(planet)
            obj.check_orbit(planet)
            obj.draw()

            # Remove objects if they collide with planet or go off-screen
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.dist((obj.x, obj.y), (planet.x, planet.y)) <= PLANET_SIZE
            if collided or (off_screen and not obj.orbiting):
                spacecrafts.remove(obj)

        planet.draw()

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
