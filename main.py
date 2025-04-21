# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *  # Import everything from constants.py
from player import Player
from circleshape import CircleShape
from asteroid import Asteroid
from asteroidfield import AsteroidField # Import AsteroidField
import sys #add this to exit the game
from shot import Shot

def main():
    print("Starting Asteroids!")

    pygame.init()  # Initialize pygame

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()  # Create a pygame.time.Clock object
    dt = 0  # Initialize delta time

    # Create sprite groups
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group() #create the asteroids sprite group
    shots = pygame.sprite.Group() #shots sprite group

    # Instantiate a Player object.  Tell the object about the shots group
    player_x = SCREEN_WIDTH / 2
    player_y = SCREEN_HEIGHT / 2
    player = Player(player_x, player_y, shots)

    player.containers = updatables, drawables  # set the player's containers
    updatables.add(player)
    drawables.add(player)

    # Asteroid related initializations
    Asteroid.containers = asteroids, updatables, drawables  # Set Asteroid containers
    AsteroidField.containers = updatables  # Set AsteroidField container
    Shot.containers = shots, updatables, drawables #set the shot's containers

    asteroid_field = AsteroidField() #create an instance of AsteroidField

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add to event handling.  Now the player takes an event list and processes the event.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
              player.shoot() #call shoot

        # Update the game state
        for entity in updatables: #loop through entities in updatables group and call their update method
            entity.update(dt)

        #Check for collision. First asteroids, then shots, and kill them on hit
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit() #need to uninit before exiting
                sys.exit()  # Exit the program

            for shot in shots: #loop throu ad    gh shots to check for collisions with the asteroid
                if shot.collides_with(asteroid):
                    asteroid.split() #use the sprite group's built in kill method to remove the asteroid
                    shot.kill() #remove the shot


        # Drawing the game
        screen.fill("black")  # Fill the screen with black

        for entity in drawables: #loop through entities in drawables group and call their draw method
            entity.draw(screen)  # Draw all entities in drawables
        pygame.display.flip()  # Refresh the screen

        dt = clock.tick(60) / 1000  # Limit to 60 FPS and calculate delta time

    pygame.quit()  # Uninitialize pygame to clean up

if __name__ == "__main__":
    main()