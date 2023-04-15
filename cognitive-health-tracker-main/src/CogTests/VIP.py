import pygame
import random
import time
import pyautogui
import numpy as np
import os
import global_variables as gv
import Cursor
import Box

'''while True: #start loop
    print(pyautogui.position())
    time.sleep(1)'''

windowHeightOffset = 60

class VipTest:
    def __init__(self, user, eye_tracking=False):
        self.bulbar = 0
        self.upperBody = 0
        self.lowerBody = 0
        self.user = user
        self.running = 'False'
        self.frame_counter = 0
        self.current_pos = pyautogui.position()
        self.eye_tracker = None
        self.eye_tracking = eye_tracking
        self.mouse_location = []

    def getRunning(self):
        return self.running

    def setRunning(self, value):
        self.running = value

    def getBulbar(self):
        return self.bulbar

    def getUpperBody(self):
        return self.upperBody

    def getLowerBody(self):
        return self.lowerBody

    def setMouseLocation(self, m_l):
        self.mouse_location = m_l

    def getMouseLocation(self):
        return self.mouse_location

    def gaze_data_callback(self, gaze_data):
        self.frame_counter += 1
        print("papi")
        max_len = 10
        if self.frame_counter >= max_len:
            print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
                gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
                gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

            left_gaze = gaze_data['left_gaze_point_on_display_area']
            right_gaze = gaze_data['right_gaze_point_on_display_area']

            if (np.isnan(left_gaze[0]) and np.isnan(left_gaze[1])) or (np.isnan(right_gaze[0]) and np.isnan(right_gaze[1])):
                monitor_pixels = (np.nan, np.nan)
                return monitor_pixels

            left_gaze = (
                int(left_gaze[0] * self.eye_tracker.monitor_size.width),
                int(left_gaze[1] * self.eye_tracker.monitor_size.height)
            )
            right_gaze = (
                int(right_gaze[0] * self.eye_tracker.monitor_size.width),
                int(right_gaze[1] * self.eye_tracker.monitor_size.height)
            )

            # Take the average of the left and right eye coordinates , not monocular friendly
            avg_x = (left_gaze[0] + right_gaze[0]) / 2
            avg_y = (left_gaze[1] + right_gaze[1]) / 2

            # Are coordinates valid?
            print("x: {0} , y: {1}".format(avg_x, avg_y))
            if avg_x >= 0 and avg_y >= 0:
                # Save current position
                print("old position = {0}".format(self.current_pos))
                self.current_pos = [avg_x, avg_y]
                print("new position = {0}".format(self.current_pos))

                # As per documentation, setting duration < pyautogui.MINIMUM_DURATION makes it move instantaneously
                speed = 0.25  # [s]econds
                pyautogui.moveTo(avg_x, avg_y, duration=speed)

                # Reset
                self.frame_counter = 0
    """
    Main function for VIP
    """
    def VIP(self):
        # # load images

        bitingAndHoldingImg = pygame.image.load(gv.path_to_images + 'vip\\1_1_BitingandHoldingApple2.jpg')
        readingAndWritingImg = pygame.image.load(gv.path_to_images + 'vip\\1_2_ReadingandWriting4.jpg')
        climbingHoldingImg = pygame.image.load(gv.path_to_images + 'vip\\1_3_ClimbingHoldingRailB.jpg')
        walkingAndPushingImg = pygame.image.load(gv.path_to_images + 'vip\\1_4_Walking_Pushing.jpg')
        walkingAndCarryingImg = pygame.image.load(gv.path_to_images + 'vip\\1_5_Walking_Carrying.jpg')
        shoutingAndPointingImg = pygame.image.load(gv.path_to_images + 'vip\\1_6_Shouting_Pointing.jpg')
        pointingAndTalkingImg = pygame.image.load(gv.path_to_images + 'vip\\2_1_Pointing_TalkingB.jpg')
        peelingAndChewingImg = pygame.image.load(gv.path_to_images + 'vip\\2_2_Peeling_ChewingB.jpg')
        kickingAndReachingImg = pygame.image.load(gv.path_to_images + 'vip\\2_3_Kicking_Reaching.jpg')
        sippingAndHolding = pygame.image.load(gv.path_to_images + 'vip\\2_4_Sipping_Holding.jpg')
        slidingHandsUp = pygame.image.load(gv.path_to_images + 'vip\\2_5_SlidinghandsUpB.jpg')
        tyingAndKneeling = pygame.image.load(gv.path_to_images + 'vip\\2_6_Tying_KneelingB.jpg')
        sneezingAndCovering = pygame.image.load(gv.path_to_images + 'vip\\3_1_Sneezing_Covering.jpg')
        buttoningAndLooking = pygame.image.load(gv.path_to_images + 'vip\\3_2_Buttoning_Looking.jpg')
        holdingUmbrella = pygame.image.load(gv.path_to_images + 'vip\\3_3_HoldingUmbrellaB.jpg')
        throwingAndJumping = pygame.image.load(gv.path_to_images + 'vip\\3_4_Throwing_Jumping.jpg')
        ridingAndHolding = pygame.image.load(gv.path_to_images + 'vip\\3_5_Riding_Holding.jpg')
        whistlingAndStopping = pygame.image.load(gv.path_to_images + 'vip\\3_6_Whistling_Stopping.jpg')

        # Set value of selection
        pictureDictionary = {bitingAndHoldingImg: [['Kissing', 'bulbar', 1.43], ['Grasping', 'upper body', 6.26],
                                                   ['Punching', 'upper body', 1.04], ['Biting', 'bulbar', 9.41],
                                                   ['Standing', 'lower body', 4.21]],
                             readingAndWritingImg: [['Reading', 'upper body', 7.46], ['Writing', 'upper body', 9.74],
                                     ['Painting', 'upper body', 1.34], ['Biting', 'bulbar', 1.03],
                                     ['Sitting', 'lower body', 7.94]],
                             climbingHoldingImg: [['Holding', 'upper body', 7.26], ['Writing', 'upper body', 1.01],
                                   ['Whistling', 'bulbar', 1.23], ['Hopping', 'lower body', 1.33],
                                   ['Climbing', 'lower body', 9.41]],
                             walkingAndPushingImg: [['Talking', 'bulbar', 1.21], ['Pushing', 'upper body', 9.36],
                                     ['Climbing', 'lower body', 1.09], ['Lifting', 'upper body', 1.21],
                                     ['Walking', 'lower body', 8.60]],
                             walkingAndCarryingImg: [['Pushing', 'upper body', 1.11], ['Smiling', 'bulbar', 1.53],
                                      ['Dancing', 'lower body', 1.80], ['Grasping', 'upper body', 5.97],
                                      ['Walking', 'lower body', 8.91]],
                             shoutingAndPointingImg: [['Biting', 'bulbar', 1.11], ['Shouting', 'bulbar', 8.40],
                                       ['Walking', 'lower body', 1.33], ['Opening', 'upper body', 1.69],
                                       ['Stomping', 'lower body', 1.37]],
                             pointingAndTalkingImg: [['Standing', 'bulbar', 7.07], ['Shouting', 'bulbar', 2.64],
                                      ['Winking', 'bulbar', 1.30], ['Waving', 'upper body', 7.13],
                                      ['Talking', 'bulbar', 7.13]],
                             peelingAndChewingImg: [['Mixing', 'upper body', 1.17], ['Smelling', 'bulbar', 2.39],
                                     ['Peeling', 'upper body', 9.47], ['Talking', 'bulbar', 1.20],
                                     ['Walking', 'lower body', 1.41]],
                             kickingAndReachingImg: [['Kicking', 'lower body', 9.54], ['Peeling', 'upper body', 1.01],
                                      ['Leaping', 'lower body', 2.56], ['Reaching', 'upper body', 4.54],
                                      ['Looking', 'bulbar', 7.04]],
                             sippingAndHolding: [['Kicking', 'lower body', 1.06], ['Kissing', 'bulbar', 1.09],
                                  ['Holding', 'upper body', 7.89], ['Sipping', 'upper body', 9.69],
                                  ['Kneeling', 'lower body', 1.30]],
                             slidingHandsUp: [['Sipping', 'bulbar', 1.11], ['Raising', 'upper body', 6.99],
                               ['Stepping', 'lower body', 1.19], ['Sliding', 'lower body', 9.66],
                               ['Shouting', 'bulbar', 4.13]],
                             tyingAndKneeling: [['Tying', 'upper body', 9.56], ['Knitting', 'upper body', 1.04],
                                 ['Bending', 'lower body', 8.11], ['Sliding', 'lower body', 1.17],
                                 ['Drooling', 'bulbar', 1.14]],
                             sneezingAndCovering: [['Kneeling', 'bulbar', 1.16], ['Covering', 'upper body', 7.64],
                                    ['Drooling', 'bulbar', 1.86], ['Tying', 'upper body', 1.17],
                                    ['Sneezing', 'bulbar', 8.96]],
                             buttoningAndLooking: [['Zipping', 'upper body', 1.17], ['Standing', 'lower body', 5.30],
                                    ['Buttoning', 'upper body', 9.81], ['Sneezing', 'bulbar', 1.04],
                                    ['Looking', 'bulbar', 7.70]],
                             holdingUmbrella: [['Walking', 'lower body', 8.89], ['Buttoning', 'upper body', 1.03],
                                ['Whistling', 'bulbar', 1.43], ['Lifting', 'upper body', 5.61],
                                ['Hopping', 'lower body', 1.37]],
                             throwingAndJumping: [['Jumping', 'lower body', 3.71], ['Walking', 'lower body', 1.94],
                                   ['Grabbing', 'upper body', 5.79], ['Throwing', 'upper body', 9.07],
                                   ['Cheering', 'bulbar', 1.19]],
                             ridingAndHolding: [['Holding', 'upper body', 1.06], ['Throwing', 'upper body', 1.06],
                                 ['Laughing', 'bulbar', 3.49], ['Cycling', 'lower body', 9.90],
                                 ['Stepping', 'lower body', 1.46]],
                             whistlingAndStopping: [['Cycling', 'lower body', 1.01], ['Blowing', 'bulbar', 9.00],
                                     ['Waving', 'upper body', 6.20], ['Winking', 'bulbar', 1.26],
                                     ['Walking', 'lower body', 4.34]]}



        pictureList2 = list(pictureDictionary.items())
        #random.shuffle(pictureList2)

        # print(pictureList2)
        # print(pictureList2[0][0])

        roundCounter = 0
        total_hold_time = 2500  # [ms]
        hold_timer = 0

        changepic = False
        # bulbar=0
        # upperBody=0
        # lowerBody=0

        cursor = Cursor.Cursor()

        pygame.init()

        # if not instructions.create_instructions('vip'):
        # error occurred ?
        # print("instructions exited with error?")

        # screen = pygame.display.set_mode([800, 500])
        winDimension = pygame.display.Info()
        screen = pygame.display.set_mode([gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT])  # pygame.RESIZABLE
        pygame.display.set_caption('VIP')

        if self.eye_tracking:
            self.eye_tracker = camera.Camera()
            self.eye_tracker.find_eyetrackers()
            self.eye_tracker.start_gaze_data(self.gaze_data_callback)

        # set ROI for buttons
        box1 = Box.Box()
        # box1.changeSize(140, 40)
        box1.changeColor(128, 128, 128)
        box2 = Box.Box()
        box3 = Box.Box()
        box4 = Box.Box()
        box5 = Box.Box()
        box6 = Box.Box()
        # print("box2 rect: " + str(box2.rect))

        boxSprites = pygame.sprite.Group()
        boxSprites.add(box2)
        boxSprites.add(box3)
        boxSprites.add(box4)
        boxSprites.add(box5)
        boxSprites.add(box6)

        boxList = [box2, box3, box4, box5, box6]
        random.shuffle(boxList)
        clock = pygame.time.Clock()
        clock.tick(10)  # #game fps
        currentTick = 0
        prevTick = 0

        screen.blit(cursor.surf, cursor.rect)

        change_rounds = True
        erase = 0

        mouse_location = []
        # game logic loop
        run = True
        while run:
            mouse_location.append(str(pyautogui.position()).replace("Point", "").replace("x=", "").replace(" y=", ""))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if self.eye_tracking and self.eye_tracker is not None:
                        self.eye_tracker.stop_gaze_data()  # Unsubscribe from capturing gaze data

            # Check to see if the eyetracker is connected and turned on
            if self.eye_tracking and self.eye_tracker is None:
                raise ValueError("Lost connection with eye tracker. Stopping the game...")

            # screen.fill((226, 230, 223)) #change this to white
            # update box shape
            screen.fill((255, 255, 255))  # change this to white
            screen.blit(box2.surf, (box2.rect.x, box2.rect.y))
            box2.update(2 * winDimension.current_w / 3, winDimension.current_h / 6)
            screen.blit(box3.surf, box3.rect)
            box3.update(2 * winDimension.current_w / 3, 2 * winDimension.current_h / 6)
            screen.blit(box4.surf, box4.rect)
            box4.update(2 * winDimension.current_w / 3, 3 * winDimension.current_h / 6)
            screen.blit(box5.surf, box5.rect)
            box5.update(2 * winDimension.current_w / 3, 4 * winDimension.current_h / 6)
            screen.blit(box6.surf, box6.rect)
            box6.update(2 * winDimension.current_w / 3, 5 * winDimension.current_h / 6)
            # box1.addText("Example",100,80)

            # Update the player sprite based on user keypresses
            if self.eye_tracking:
                print("current position = {0}".format(self.current_pos))
                mouse = self.current_pos
            else:
                mouse = pygame.mouse.get_pos()

            cursor.rect.x = mouse[0] - 5
            cursor.rect.y = mouse[1] - 5

            pressed_keys = pygame.key.get_pressed()
            screen.blit(cursor.surf, cursor.rect)
            cursor.update(pressed_keys, winDimension.current_w, winDimension.current_h)

            if roundCounter == 18:
                "return the guesses for result calculation"
                # print(correctVerbs)
                # print(guessVerbs)
                #print("bulbar: " + str(bulbar))
                #print("upperbody: " + str(upperBody))
                #print("lowerbody: " + str(lowerBody))
                changepic = None
                roundCounter = 17
                self.setRunning('False')
                if self.eye_tracking and self.eye_tracker is not None:
                    self.eye_tracker.stop_gaze_data()  # Unsubscribe from capturing gaze data
                pygame.quit()
                return 1

            if changepic == None:
                font = pygame.font.SysFont('Times New Roman', 50)
                screen.fill((255, 255, 255))
                if not self.eye_tracking:
                    screen.blit(cursor.surf, cursor.rect)
                screen.blit(font.render('Congrats On Completing the', True, (0, 0, 0)),
                            (winDimension.current_w / 4, (winDimension.current_h / 3) - windowHeightOffset))
                screen.blit(font.render('VIP Test', True, (0, 0, 0)),
                            (winDimension.current_w / 3, (winDimension.current_h / 3) + 50))
                screen.blit(box1.surf, box1.rect.topleft)
                font = pygame.font.SysFont('Times New Roman', 30)
                text = font.render('Next', True, (0, 0, 0))
                screen.blit(text, (690, 455))

                if self.eye_tracking:
                    mouse = self.current_pos
                else:
                    mouse = pygame.mouse.get_pos()

                cursor.rect.x = mouse[0] - 5
                cursor.rect.y = mouse[1] - 5
                # pygame.draw.rect(screen, (128, 128, 128), rect)
                # pygame.quit()
                # if 650 <= mouse[0] <= 800 and 450 <= mouse[1] <= 500:

                # cursor.surf.fill((240, 194, 70))
                # cursorHoldCounter += 1
                # pygame.quit()
                # if cursorHoldCounter == 500:
                # cursorHoldCounter = 0
                # print('Done')
                # pygame.draw.rect(screen, (255,255,255), [650, 450 , 140, 40])

                # else:
                # cursor.surf.fill((153, 186, 128))
                # cursorHoldCounter = 0
            if changepic:
                changepic = False
                random.shuffle(boxList)

            elif changepic == False:
                # screen.blit(pygame.transform.scale(pictureList[roundCounter][0], (400, 300)), [215, 80])
                screen.blit(pygame.transform.scale(pictureList2[roundCounter][0], (
                winDimension.current_w / 3, (winDimension.current_h - windowHeightOffset)))
                            , [winDimension.current_w / 4, windowHeightOffset / 2])
                # correctVerbs[roundCounter]=pictureList[roundCounter][1][0]
                font = pygame.font.SysFont('Helvetica', 28)
                text = font.render(pictureList2[roundCounter][1][0][0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (boxList[0].rect.x, boxList[0].rect.y + 10)
                screen.blit(text, textRect)
                # boxList

                # font = pygame.font.SysFont('Times New Roman', 19)
                # text = font.render(pictureList[roundCounter][1][0], True, (0, 0, 0))
                # textRect = text.get_rect()
                # textRect.topleft = (boxList[boxcounter].length, boxList[boxcounter].width + 10)
                # screen.blit(text, textRect)

                boxList[0].type = pictureList2[roundCounter][1][0][1]
                boxList[0].value = pictureList2[roundCounter][1][0][2]

                text = font.render(pictureList2[roundCounter][1][1][0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (boxList[1].rect.x, boxList[1].rect.y + 10)
                screen.blit(text, textRect)
                boxList[1].type = pictureList2[roundCounter][1][1][1]
                boxList[1].value = pictureList2[roundCounter][1][1][2]

                text = font.render(pictureList2[roundCounter][1][2][0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (boxList[2].rect.x, boxList[2].rect.y + 10)
                screen.blit(text, textRect)
                boxList[2].type = pictureList2[roundCounter][1][2][1]
                boxList[2].value = pictureList2[roundCounter][1][2][2]

                text = font.render(pictureList2[roundCounter][1][3][0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (boxList[3].rect.x, boxList[3].rect.y + 10)
                screen.blit(text, textRect)
                boxList[3].type = pictureList2[roundCounter][1][3][1]
                boxList[3].value = pictureList2[roundCounter][1][3][2]

                text = font.render(pictureList2[roundCounter][1][4][0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (boxList[4].rect.x, boxList[4].rect.y + 10)
                screen.blit(text, textRect)
                boxList[4].type = pictureList2[roundCounter][1][4][1]
                boxList[4].value = pictureList2[roundCounter][1][4][2]

                """
                if type=='bulbar':
                    while counter!=4:
                        if bulbar[typecounter]!=pictureList[roundCounter][1][0]:
                            font = pygame.font.SysFont('Times New Roman', 19)
                            text = font.render(bulbar[typecounter], True, (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.topleft = (boxList[boxcounter].length, boxList[boxcounter].width + 10)
                            screen.blit(text, textRect)
                            boxList[boxcounter].type=bulbar[typecounter]
                            counter+=1
                            boxcounter+=1
                            typecounter+=1
                        else:
                            typecounter+=1

                elif type=='lower body':
                    while counter!=4:
                        if lowerBody[typecounter]!=pictureList[roundCounter][1][0]:
                            font = pygame.font.SysFont('Times New Roman', 19)
                            text = font.render(bulbar[typecounter], True, (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.topleft = (boxList[boxcounter].length, boxList[boxcounter].width + 10)
                            screen.blit(text, textRect)
                            boxList[boxcounter].type=lowerBody[typecounter]
                            counter+=1
                            boxcounter+=1
                            typecounter+=1
                        else:
                            typecounter+=1
                else:
                    while counter!=4:
                        if upperBody[typecounter]!=pictureList[roundCounter][1][0]:
                            font = pygame.font.SysFont('Times New Roman', 19)
                            text = font.render(bulbar[typecounter], True, (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.topleft = (boxList[boxcounter].length, boxList[boxcounter].width + 10)
                            screen.blit(text, textRect)
                            boxList[boxcounter].type = upperBody[typecounter]
                            counter+=1
                            boxcounter+=1
                            typecounter+=1
                        else:
                            typecounter+=1
                """
                counter = 0
                boxcounter = 1
                typecounter = 0

            collided_box = pygame.sprite.spritecollideany(cursor, boxSprites)
            if collided_box and changepic != None:
                cursor.surf.fill(gv.gold)
                if hold_timer == 0:
                    hold_timer = pygame.time.get_ticks()  # clock the timer

                time_elapsed = pygame.time.get_ticks() - hold_timer
                if time_elapsed > total_hold_time:
                    changepic = True

                    if collided_box.type == 'bulbar':
                        self.bulbar += collided_box.value

                    elif collided_box.type == "upper body":
                        self.upperBody += collided_box.value

                    else:
                        self.lowerBody += collided_box.value

                    # guessVerbs[roundCounter]=collided_box.type #line has no funntionality for the test.
                    roundCounter += 1
                    hold_timer = 0
                    cursor.rect.topleft = (0, 0)
                    screen.blit(cursor.surf, cursor.rect)

            else:
                cursor.surf.fill((255, 255, 255))
                hold_timer = 0

            # if roundCounter==16:
            #     "output message that says good job"
            #     print(correctVerbs)
            #     print(guessVerbs)
            #     roundCounter=0
            pygame.display.flip()

        self.setMouseLocation(mouse_location)
        if self.eye_tracking and self.eye_tracker is not None:
            self.eye_tracker.stop_gaze_data()  # Unsubscribe from capturing gaze data
        pygame.quit()
        return 1


testing = False
if testing:
    eye_tracking = False
    vip = VipTest("test", eye_tracking)
    vip.VIP()
