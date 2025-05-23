import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, shots):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots = shots #store the shots group, we'll need to add to it
        self.shoot_timer = 0  # Initialize shoot timer
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        self.shots.add(shot) #add the shot to the sprite group
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN #after creating a shot, set it to cooldown

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)  # Rotate left (counter-clockwise)
        if keys[pygame.K_d]:
            self.rotate(dt)   # Rotate right (clockwise)
        if keys[pygame.K_w]:
            self.move(dt)     # Move forward
        if keys[pygame.K_s]:
            self.move(-dt)    # Move backward
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0: #only shoot if timer <= 0
            self.shoot()


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "red", self.triangle(), 2)