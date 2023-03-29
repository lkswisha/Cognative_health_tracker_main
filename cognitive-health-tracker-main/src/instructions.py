import pygame
import os
import Cursor
import Box
import global_variables as gv

windowOffset=60
VIP_INSTRUCTIONS = "There are 18 Images with 5 options. " \
                   "The user must hover over what verb they think is being " \
                   "performed in the image for 5 seconds."

SACCADE_INSTRUCTIONS = "This test will have 16 rounds. You will be given a screen with two dots. " \
                       "One of the dots will be flashing and the other dot will not. For the first 8 rounds you will " \
                       "be looking for the flashing dot. Starting round 9 you will be looking at the non-flashing dot. " \
                       "If you understand the instructions click on the go to test button to take the test."

TB_INSTRUCTIONS = "Numbers and/or letters will appear on the screen. Please select them in ascending order." \
                  "If AlphaNumber, select the number and letter in pairs in ascending order. Good luck fam."

"""
Split text onto multiple lines, if line exceeds width of window
"""
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    word_height = 0
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


"""
Instructions screen for cognitive tests.
"""
def create_instructions(game):
    pygame.init()
    winDimension = pygame.display.Info()
    WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (winDimension.current_w, winDimension.current_h-windowOffset)  # arbitrary numbers
    screen = pygame.display.set_mode(WINDOW_SIZE)
    #screen=pygame.display.set_mode(pygame.display.Info().current_w,pygame.display.Info().current_h)
    pygame.display.set_caption(game + " instructions")
    cursor = Cursor.Cursor()

    font = pygame.font.SysFont('Times New Roman', 30)
    small_font = pygame.font.SysFont('Times New Roman', 30)

    next_btn = Box.Box()  # pygame.Rect(650, 450, 140, 40)
    screen.blit(next_btn.surf,next_btn.rect)
    next_btn.update(WINDOW_WIDTH-3*windowOffset,WINDOW_HEIGHT-2*windowOffset)
    next_text = small_font.render('Next', True, (0, 0, 0))
    next_text_rect = next_text.get_rect()
    next_text_rect.x = next_btn.rect.centerx - (next_text_rect.width / 2)
    next_text_rect.y = next_btn.rect.centery - (next_text_rect.h / 2)

    #next_btn.changeSize(450, 650)
    next_btn.changeColor(128, 128, 128)

    cursorHoldCounter = 0
    proceed = False

    #buttonSprite = pygame.sprite.Group()
    #buttonSprite.add

    # Figure out which instructions to display
    if game.lower() == 'vip':
        instructions = VIP_INSTRUCTIONS
    elif game.lower() == 'saccade':
        instructions = SACCADE_INSTRUCTIONS
    elif game.lower() == 'trailblazer':
        instructions = TB_INSTRUCTIONS
    else:
        instructions = "Who you?"

    instruction_text = font.render(instructions, True, (0, 0, 0))
    textRect = instruction_text.get_rect()
    textRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    screen.blit(screen,(textRect.center[0],textRect.center[1]),textRect) #doesn't change the location of instructions *need to fix

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if proceed:
            print("leaving instructions...")
            return True

        screen.fill((226, 230, 223))
        screen.blit(cursor.surf, cursor.rect)

        # Update the player sprite based on user key presses
        pressed_keys = pygame.key.get_pressed()
        cursor.update(pressed_keys, screen.get_width(), screen.get_height())

        # Print text
        blit_text(screen, instructions, (screen.get_rect().x, screen.get_rect().y), font)

        mouse = pygame.mouse.get_pos()
        cursor.rect.x = mouse[0]-5
        cursor.rect.y = mouse[1]-5
        pressed_keys = pygame.key.get_pressed()
        cursor.update(pressed_keys, WINDOW_WIDTH, WINDOW_HEIGHT)

        #screen.blit(next_btn.surf, (650, 450))
        pygame.draw.rect(screen, (128,128,128), next_btn)

        if next_btn.rect.x <= mouse[0] <= next_btn.rect.x + next_btn.width \
                and next_btn.rect.y <= mouse[1] <= next_btn.rect.y + next_btn.length: #idk why i put the attribute as length instead of height need to fix
            cursor.surf.fill((240, 194, 70))
            cursorHoldCounter += 1
            if cursorHoldCounter == 500:
                cursorHoldCounter = 0
                proceed = True
            #pygame.draw.rect(screen, (255,255,255), [650, 450 , 140, 40])

        else:
            cursor.surf.fill((153, 186, 128))
            cursorHoldCounter = 0
        #else:
            #pygame.draw.rect(screen, (0,0,0), [650, 450, 140, 40])


        #next_btn.addText(screen, 'Next', next_btn.rect.x + (next_btn.rect.centerx/2), next_btn.rect.y + (next_btn.rect.centery/4))
        #next_btn.addText(screen, 'Next', ))

        screen.blit(next_text, next_text_rect)

        pygame.display.flip()
    pygame.quit()
    return 1