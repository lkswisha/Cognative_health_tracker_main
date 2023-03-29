import pygame
import random
import math
from src import global_variables as gv
from src import Cursor
from src import instructions

"""
Object of interest.
"""
class Node(pygame.sprite.Sprite):
    def __init__(self, img, val):
        super(Node, self).__init__()
        self.image = pygame.image.load(img)
        #self.image.fill((226, 230, 223))  # 'invisible'
        self.rect = self.image.get_rect()
        self.color = (153, 186, 128)
        self.value = val

    def update(self, x, y, c):
        self.rect.y = y
        self.rect.x = x
        #pygame.draw.circle(self.image, c, (25, 25), 25)

def draw_circle(n):
    # (x-h)^2 + (y-k)^2 = r^2
    # x = r * cos(theta) + h
    # y = r - sin(theta) + k

    h = gv.SCREEN_WIDTH / 2
    k = gv.SCREEN_HEIGHT / 2
    r = 100

    positions = []
    step_size = (2 * math.pi) / n
    theta = 0

    while theta < 2 * math.pi:
        positions.append((r * math.cos(theta) + h, r * math.sin(theta) + k))
        theta += step_size

    return positions

class TrailBlazerTest:
    """
    Game Logic
    """
    def rules(self):
        # Find the ground truth
        # During play, keep track of nodes chosen and keep in list

        # Either correct node by node
        # or
        # Check entire list
        return

    """
    Validate the user's choice
    """
    def validate(self, node, ground_truth):
        # Compare the user's choice with the answer key
        index = ground_truth["index"]
        if node.value == ground_truth["answer"][index]:
            ground_truth["index"] += 1
            return True

        return False

    """
    TrailBlazer Test
    """
    def TrailBlazer(self, num_of_nodes, alpha_numeric=False):
        pygame.init()

        instructions.create_instructions("TrailBlazer")

        screen = pygame.display.set_mode([gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT])
        pygame.display.set_caption("TrailBlazer baby!")
        positions = draw_circle(num_of_nodes)
        random.shuffle(positions)  # randomize the nodes

        nodes = {}
        all_nodes = pygame.sprite.Group()
        for x in range(num_of_nodes):
            print(gv.path_to_images + "trailblazer\{0}.png".format(x + 16))
            nodes["node{0}".format(x)] = Node(gv.path_to_images + "trailblazer\{0}.png".format(x+16), x)
            all_nodes.add(nodes["node{0}".format(x)])

        cursor = Cursor.Cursor()
        MAX_GAME_TIME = 300 # seconds
        start_time = pygame.time.get_ticks()
        total_time = 0
        collision_time = 0

        ground_truth = {
            "index": 0,
            "answer": []
        }
        for i in range(num_of_nodes):
            ground_truth["answer"].append(i)

        user_choice = set()
        incorrect = 0

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            seconds = (pygame.time.get_ticks() - start_time)/1000

            # User took too long --> stop the game
            if seconds >= MAX_GAME_TIME:
                break

            screen.fill((226, 230, 223))

            # Draw ROI on screen
            index = 0
            for i in range(num_of_nodes):
                nodes["node{0}".format(i)].update(positions[index][0], positions[index][1], (153, 186, 128))
                screen.blit(nodes["node{0}".format(i)].image, [positions[index][0], positions[index][1]])
                index += 1

            # Draw cursor on the screen
            screen.blit(cursor.surf, cursor.rect)

            # Update the player sprite based on user key presses
            pressed_keys = pygame.key.get_pressed()
            cursor.update(pressed_keys, gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT)

            # Update the display
            pygame.display.flip()

            # If collision occurred, return the node where collision occurred
            collided_node = pygame.sprite.spritecollideany(cursor, all_nodes)
            if collided_node:
                collision_time += 1
                if collision_time > 1000:
                    collided_time = 0
                    all_nodes.remove(collided_node)

                    # Validate user's answer
                    if validate(collided_node, ground_truth):
                        user_choice.add(collided_node)
                        collided_node.image.fill((69,139,0))
                        if all_nodes.empty():
                            break
                    else:
                        # Tell user it was wrong
                        incorrect += 1
                        all_nodes.add(collided_node)
                        print("Wrong answer")

            else:
                collision_time = 0
