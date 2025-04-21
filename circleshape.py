import pygame

class CircleShape(pygame.sprite.Sprite):
    # Class variable to hold containers. Subclasses should set this *before* instantiation,
    # or groups should be passed to __init__. Ensure this is set in main.py before creating objects.
    containers = pygame.sprite.Group()

    def __init__(self, x, y, radius):
        # Call the parent Sprite's initializer, adding the sprite to the groups
        # defined in the class variable 'containers'.
        # This requires 'containers' to be set correctly *before* this init is called.
        super().__init__(self.containers)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

        # --- Ensure image and rect are created ---
        # Create a placeholder transparent surface. Size doesn't strictly matter if
        # drawing is overridden, but it gives the rect its initial dimensions.
        # Using radius * 2 for width/height is sensible.
        # pygame.SRCALPHA makes the surface initially transparent.
        self.image = pygame.Surface([max(1, self.radius * 2), max(1, self.radius * 2)], pygame.SRCALPHA)

        # Create the rect attribute, centered on the initial position.
        # This is REQUIRED by many pygame sprite collision functions.
        self.rect = self.image.get_rect(center=self.position)
        # -----------------------------------------

    def collides_with(self, other):
        """Manual circle collision check (alternative to pygame.sprite.collide_circle)."""
        # Ensure the other object also has position and radius attributes
        if hasattr(other, 'position') and hasattr(other, 'radius'):
            distance = self.position.distance_to(other.position)
            return distance < self.radius + other.radius
        return False # Cannot perform circle collision if attributes missing

    def update(self, dt):
        """Base update method. Updates the rect position based on the vector position."""
        # Update the sprite's rect center to match its vector position.
        # Essential for accurate collision detection when using self.rect or
        # Pygame collision functions that rely on the rect.
        self.rect.center = self.position
        # Subclasses should call super().update(dt) in their own update methods
        # *after* they have finished updating self.position for the frame.

    def draw(self, screen):
        """Must be overridden by subclasses to draw the actual visual representation."""
        # Example: Draw the bounding box or circle for debugging
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1) # Draw bounding box
        # pygame.draw.circle(screen, (0, 255, 0), self.rect.center, self.radius, 1) # Draw bounding circle
        pass # Subclasses must implement their drawing logic.