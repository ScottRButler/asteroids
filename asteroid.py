import pygame
from circleshape import CircleShape
from constants import * # Import everything from constants.py
import random  # Import random module
import math    # Import math for sin/cos

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.shape_points = self._generate_jagged_shape() # Generate and store the shape

    def _generate_jagged_shape(self):
        """Generates a list of points for a jagged polygon shape."""
        points = []
        num_vertices = ASTEROID_VERTICES # Use constant for number of vertices
        angle_step = 360 / num_vertices

        for i in range(num_vertices):
            angle = math.radians(i * angle_step)
            # Vary the distance (radius) for this point randomly
            dist_variation = self.radius * random.uniform(1.0 - ASTEROID_RADIUS_VARIATION, 1.0 + ASTEROID_RADIUS_VARIATION)
            
            # Calculate the point's offset from the center
            x_offset = dist_variation * math.cos(angle)
            y_offset = dist_variation * math.sin(angle)
            
            # Store the relative offset vector
            points.append(pygame.Vector2(x_offset, y_offset))
            
        return points

    def draw(self, screen):
        # Calculate absolute screen points based on current position and stored shape
        absolute_points = []
        for point in self.shape_points:
            absolute_points.append(self.position + point)
            
        # Draw the polygon using the calculated screen points
        pygame.draw.polygon(screen, "white", absolute_points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        
        # Screen wrapping (optional but common in Asteroids)
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius


    def split(self):
        """Splits the asteroid into two smaller asteroids, or destroys it if it's too small."""
        original_radius = self.radius # Store original radius before killing
        self.kill() # Kill the current asteroid

        if original_radius <= ASTEROID_MIN_RADIUS:
            return

        # New asteroid properties
        random_angle = random.uniform(20, 50) #get a random angle between 20 and 50
        # Calculate new radius based on the original radius, not self.radius which might be invalid after kill()
        new_radius = original_radius - ASTEROID_MIN_RADIUS 
        # Ensure new radius is at least the minimum
        new_radius = max(new_radius, ASTEROID_MIN_RADIUS) 

        # Calculate new velocities by rotating the original velocity vector
        velocity_1 = self.velocity.rotate(random_angle)
        velocity_2 = self.velocity.rotate(-random_angle)

        # Scale the speed up
        velocity_1 *= 1.2
        velocity_2 *= 1.2

        # Create 2 new asteroids - they will generate their own jagged shapes in their __init__
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        #assign the vector to asteroid velocity.
        asteroid1.velocity = velocity_1
        asteroid2.velocity = velocity_2

