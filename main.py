# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *  # Import everything from constants.py
from player import Player
from circleshape import CircleShape # Base class needed if not implicitly imported elsewhere
from asteroid import Asteroid
from asteroidfield import AsteroidField # Import AsteroidField
import sys #add this to exit the game
from shot import Shot

def main():
    print("Starting Asteroids!")

    pygame.init()  # Initialize pygame
    pygame.font.init() # Explicitly initialize font module (good practice)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids") # Set window title

    clock = pygame.time.Clock()  # Create a pygame.time.Clock object
    dt = 0  # Initialize delta time

    # --- Score Initialization ---
    score = 0
    # Create a font object: Use default system font, size 36
    # You can replace None with a specific font file path or system font name like 'arial'
    score_font = pygame.font.Font(None, 36)
    score_color = "white"
    # --------------------------

    # Create sprite groups
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group() #create the asteroids sprite group
    shots = pygame.sprite.Group() #shots sprite group

    # Instantiate a Player object.  Tell the object about the shots group
    player_x = SCREEN_WIDTH / 2
    player_y = SCREEN_HEIGHT / 2
    player = Player(player_x, player_y, shots)

    # It's generally better to set class variables *before* instantiation
    # Or pass containers during __init__ if designing that way
    Player.containers = updatables, drawables # Set Player containers
    Asteroid.containers = asteroids, updatables, drawables  # Set Asteroid containers
    AsteroidField.containers = updatables  # Set AsteroidField container
    Shot.containers = shots, updatables, drawables # Set the shot's containers

    # Now add the player instance specifically
    updatables.add(player)
    drawables.add(player)


    asteroid_field = AsteroidField() #create an instance of AsteroidField

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add to event handling.  Now the player takes an event list and processes the event.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
              player.shoot() #call shoot Player input is handled within player.update based on key state

        # Update the game state
        updatables.update(dt) # Use group update method

        # --- Collision Detection (Manual Loops) ---
        # Check Player vs Asteroids
        for asteroid in pygame.sprite.Group.sprites(asteroids): # Iterate safely over a copy
            if player.alive() and player.collides_with(asteroid): # Check if player still alive
                print(f"Game over! Final Score: {score}")
                player.kill() # Remove player from groups
                running = False # Stop the game loop
                break # Exit asteroid loop once player hit

        # Check Shots vs Asteroids only if player is still alive
        if player.alive(): # Check if player still alive
            # Need temporary lists or copies if modifying groups while iterating
            shots_to_remove = []
            asteroids_to_split = [] # Keep track of which asteroids were hit this frame

            for shot in pygame.sprite.Group.sprites(shots):
                shot_hit_something = False # Flag to kill shot only once
                for asteroid in pygame.sprite.Group.sprites(asteroids):
                    # Check if this asteroid was already marked for split by another shot this frame
                    if asteroid in asteroids_to_split:
                        continue # Skip already processed asteroid

                    if shot.collides_with(asteroid):
                        # Mark for splitting and score
                        asteroids_to_split.append(asteroid)

                        # --- Increment Score ---
                        # Award points based on asteroid size
                        if asteroid.radius > ASTEROID_MIN_RADIUS * 2: # Large
                            score += 10
                        elif asteroid.radius > ASTEROID_MIN_RADIUS: # Medium
                            score += 20
                        else: # Smallest
                            score += 50
                        # print(f"Hit! Score: {score}") # Optional console log

                        # Mark shot for removal
                        shots_to_remove.append(shot)
                        shot_hit_something = True # Mark that this shot hit something
                        break # A shot typically only hits one asteroid

                # If shot hit an asteroid, stop checking this shot against others
                if shot_hit_something:
                     # We already marked it for removal, no need to check further asteroids
                     pass


            # Now perform the actions based on the collected lists
            for shot in shots_to_remove:
                 if shot.alive(): # Check if it wasn't already killed (e.g., by going off-screen)
                    shot.kill()

            for asteroid in asteroids_to_split:
                 if asteroid.alive(): # Check if it wasn't already killed (e.g., by player collision earlier)
                    asteroid.split() # split() also calls kill()


        # Drawing the game
        screen.fill("black")  # Fill the screen with black

        for entity in drawables:
            entity.draw(screen)
            
        # --- Draw Score ---
        score_text = f"Score: {score}"
        score_surface = score_font.render(score_text, True, score_color) # Render the text
        # Position the text. Get the rect, then set its topright corner.
        score_rect = score_surface.get_rect()
        score_rect.topright = (SCREEN_WIDTH - 15, 10) # 15px from right edge, 10px from top
        screen.blit(score_surface, score_rect) # Draw the score surface onto the screen
        # ------------------

        pygame.display.flip()  # Refresh the screen

        dt = clock.tick(60) / 1000  # Limit to 60 FPS and calculate delta time

    # --- Quit Pygame ---
    pygame.font.quit() # Uninitialize font module
    pygame.quit()  # Uninitialize pygame to clean up
    sys.exit() # Ensure the program exits cleanly

if __name__ == "__main__":
    main()