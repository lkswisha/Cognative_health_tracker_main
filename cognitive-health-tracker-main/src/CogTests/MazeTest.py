import pygame, sys
import os
parent_dir=os.path.abspath(os.path.join(os.getcwd(),'..'))
import sys
sys.path.append(parent_dir)
import global_variables as gv

# Define the screen width and height
screen_width = 900
screen_height = 900

# Initialize Pygame and create a screen with the defined size
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the background image and scale it to fit the screen

bg = pygame.image.load(gv.path_to_images + 'mazetest\\black_bg.jpg')
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# Define the path of the maze using a list of tuples that represent the coordinates of the start and end points of each segment
path = [((0, 400), (200, 30)), ((200, 400), (30, 200)), ((200, 600), (300, 30)), ((500, 300), (30, 330)), ((530, 300), (250, 30))]

# Set the mouse position to the starting point of the maze
pygame.mouse.set_pos((50, 415))

# Create a clock object to control the frame rate of the game
clock = pygame.time.Clock()

# Create a font object to display text on the screen
font = pygame.font.Font(None, 60)

# Set a flag to indicate whether the game loop should continue running
run = True

while run:
    # Limit the frame rate to 15 FPS
    clock.tick(15)

    # Check for events (such as quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if the mouse is at the end point of the maze
    if ((pygame.mouse.get_pos()[0] - 615)**2 + (pygame.mouse.get_pos()[1] - 130)**2) <= 100:
        # Display a message on the screen if the player wins
        text = font.render("Test Finished", True, (255, 255, 255))
        screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
        pygame.display.update()

        # Wait for 3 seconds before quitting the game
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    # Check if the mouse is inside a wall segment
    for b in path:
        # Check for collision with walls along the x-axis
        if b[0][0] < pygame.mouse.get_pos()[0] < b[0][0] + b[1][0] and b[0][1] < pygame.mouse.get_pos()[1] < b[0][1] + b[1][1]:
            # End the game if there is a collision with a wall segment
          #  run = False
            break

    # Clear the screen with the background image
    screen.blit(bg, (0, 0))

    # Draw the walls of the maze
    for x in path:
        pygame.draw.rect(screen, (255, 255, 255), (x[0], x[1]))

    # Draw the end point of the maze as a circle
    pygame.draw.circle(screen, (255, 0, 0), (770, 315), 26)
    pygame.draw.circle(screen, (0, 255, 0), (15, 415), 26)

    # Update the display
    pygame.display.update()
