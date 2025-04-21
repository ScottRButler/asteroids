import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
import random  # Import random module


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        """Splits the asteroid into two smaller asteroids, or destroys it if it's too small."""
        self.kill() #kill after creating the method as requested

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # New asteroid properties
        random_angle = random.uniform(20, 50) #get a random angle between 20 and 50
        new_radius = self.radius - ASTEROID_MIN_RADIUS #as per instructions

        # Calculate new velocities by rotating the original velocity vector
        velocity_1 = self.velocity.rotate(random_angle)
        velocity_2 = self.velocity.rotate(-random_angle)

        # Scale the speed up
        velocity_1 *= 1.2
        velocity_2 *= 1.2

        # Create 2 new asteroids
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        #assign the vector to asteroid velocity. Then add to the container after as adding to sprite group adds and then updates for new coordinates so have to assign the new object.
        asteroid1.velocity = velocity_1
        asteroid2.velocity = velocity_2

        #add the objects to all relevant sprite groups
        self.containers[0].add(asteroid1)
        self.containers[1].add(asteroid1)
        self.containers[2].add(asteroid1)
        self.containers[0].add(asteroid2)
        self.containers[1].add(asteroid2)
        self.containers[2].add(asteroid2)