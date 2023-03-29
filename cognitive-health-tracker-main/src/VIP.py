import pygame
import sys
sys.path.append('C:\\Users\\user\\PycharmProjects\\cognitive-health-trackerTestExe\\src\\CogTests')
import random
import time
from src import global_variables as gv
from src import Cursor
from src import Box
from src import instructions

windowHeightOffset = 60

class VipTest:
    def __init__(self,user):
        self.bulbar = 0
        self.upperBody = 0
        self.lowerBody = 0
        self.user=user
        self.running='False'

    def getRunning(self):
        return self.running

    def setRunning(self,value):
        self.running=value

    def getBulbar(self):
        return self.bulbar

    def getUpperBody(self):
        return self.upperBody

    def getLowerBody(self):
        return self.lowerBody

    def VIP(self):
        bulbar=['Swallowing','Speech','Yawning','Thinking','Blinking','Touching']
        upperBody=['Stretching','Waving','Throwing','Shaking Hands','Punching','Slapping']
        lowerBody=['Running','Walking','Kicking','Dancing','Stomping','Jumping']

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

        pictureDictionary={bitingAndHoldingImg:[['Kissing','bulbar',1.43],['Grasping','upper body',6.26], ['Punching','upper body',1.04],['Biting','bulbar',9.41],['Standing','lower body',4.21]]
                            ,readingAndWritingImg:[['Reading','upper body',7.46],['Writing','upper body',9.74], ['Painting','upper body',1.34],['Biting','bulbar',1.03],['Sitting','lower body',7.94]]
                           ,climbingHoldingImg:[['Holding','upper body',7.26],['Writing','upper body',1.01], ['Whistling','bulbar',1.23],['Hopping','lower body',1.33],['Climbing','lower body',9.41]]
                           ,walkingAndPushingImg:[['Talking','bulbar',1.21],['Pushing','upper body',9.36], ['Climbing','lower body',1.09],['Lifting','upper body',1.21],['Walking','lower body',8.60]]
                           ,walkingAndCarryingImg:[['Pushing','upper body',1.11],['Smiling','bulbar',1.53], ['Dancing','lower body',1.80],['Grasping','upper body',5.97],['Walking','lower body',8.91]]
                            ,shoutingAndPointingImg:[['Biting','bulbar',1.11],['Shouting','bulbar',8.40], ['Walking','lower body',1.33],['Opening','upper body',1.69],['Stomping','lower body',1.37]]
                           ,pointingAndTalkingImg:[['Standing','bulbar',7.07],['Shouting','bulbar',2.64], ['Winking','bulbar',1.30],['Waving','upper body',7.13],['Talking','bulbar',7.13]]
                           ,peelingAndChewingImg:[['Mixing','upper body',1.17],['Smelling','bulbar',2.39], ['Peeling','upper body',9.47],['Talking','bulbar',1.20],['Walking','lower body',1.41]]
                           ,kickingAndReachingImg:[['Kicking','lower body',9.54],['Peeling','upper body',1.01], ['Leaping','lower body',2.56],['Reaching','upper body',4.54],['Looking','bulbar',7.04]]
                           ,sippingAndHolding:[['Kicking','lower body',1.06],['Kissing','bulbar',1.09], ['Holding','upper body',7.89],['Sipping','upper body',9.69],['Kneeling','lower body',1.30]]
                           ,slidingHandsUp:[['Sipping','bulbar',1.11],['Raising','upper body',6.99], ['Stepping','lower body',1.19],['Sliding','lower body',9.66],['Shouting','bulbar',4.13]]
                           ,tyingAndKneeling:[['Tying','upper body',9.56],['Knitting','upper body',1.04], ['Bending','lower body',8.11],['Sliding','lower body',1.17],['Drooling','bulbar',1.14]]
                           ,sneezingAndCovering:[['Kneeling','bulbar',1.16],['Covering','upper body',7.64], ['Drooling','bulbar',1.86],['Tying','upper body',1.17],['Sneezing','bulbar',8.96]]
                           ,buttoningAndLooking:[['Zipping','upper body',1.17],['Standing','lower body',5.30], ['Buttoning','upper body',9.81],['Sneezing','bulbar',1.04],['Looking','bulbar',7.70]]
                           ,holdingUmbrella:[['Walking','lower body',8.89],['Buttoning','upper body',1.03], ['Whistling','bulbar',1.43],['Lifting','upper body',5.61],['Hopping','lower body',1.37]]
                           ,throwingAndJumping:[['Jumping','lower body',3.71],['Walking','lower body',1.94], ['Grabbing','upper body',5.79],['Throwing','upper body',9.07],['Cheering','bulbar',1.19]]
                           ,ridingAndHolding:[['Holding','upper body',1.06],['Throwing','upper body',1.06], ['Laughing','bulbar',3.49],['Cycling','lower body',9.90],['Stepping','lower body',1.46]]
                           ,whistlingAndStopping:[['Cycling','lower body',1.01],['Blowing','bulbar',9.00], ['Waving','upper body',6.20],['Winking','bulbar',1.26],['Walking','lower body',4.34]]}

        swallowingImg   = pygame.image.load(gv.path_to_images + '\\vip\\swallowing.jpg')
        blinkingImg     = pygame.image.load(gv.path_to_images + '\\vip\\blinking.jpg')
        dancingImg      = pygame.image.load(gv.path_to_images + '\\vip\\dancing.jpg')
        jumpingImg      = pygame.image.load(gv.path_to_images + '\\vip\\jumping.jpg')
        kickingImg      = pygame.image.load(gv.path_to_images + '\\vip\\kicking.jpg')
        punchingImg     = pygame.image.load(gv.path_to_images + '\\vip\\punching.png')
        runningImg      = pygame.image.load(gv.path_to_images + '\\vip\\running.jpg')
        shakinghandsImg = pygame.image.load(gv.path_to_images + '\\vip\\shaking hands.jpg')
        slappingImg     = pygame.image.load(gv.path_to_images + '\\vip\\slapping.jpg')
        stompingImg     = pygame.image.load(gv.path_to_images + '\\vip\\stomping.jpg')
        stretchingImg   = pygame.image.load(gv.path_to_images + '\\vip\\stretching.jpg')
        talkingImg      = pygame.image.load(gv.path_to_images + '\\vip\\talking.jpg')
        thinkingImg     = pygame.image.load(gv.path_to_images + '\\vip\\thinking.jpg')
        throwingImg     = pygame.image.load(gv.path_to_images + '\\vip\\throwing.jpg')
        touchingImg     = pygame.image.load(gv.path_to_images + '\\vip\\touching.jpg')
        walkingImg      = pygame.image.load(gv.path_to_images + '\\vip\\walking.jpg')
        wavingImg       = pygame.image.load(gv.path_to_images + '\\vip\\waving.png')
        yawningImg      = pygame.image.load(gv.path_to_images + '\\vip\\yawning.jpg')

        correctVerbs=['','','','','','','','','','','','','','','','']
        guessVerbs=['','','','','','','','','','','','','','','','']
        pictureDict={swallowingImg:['Swallowing','bulbar'],blinkingImg:['Blinking','bulbar'],dancingImg:['Dancing','lower body'],jumpingImg:['Jumping','lower body'],
                     kickingImg:['Kicking','lower body'],punchingImg:['Punching','upper body'],runningImg:['Running','lower body'],shakinghandsImg:['Shaking Hands','upper body'],
                     slappingImg:['Slapping','lower body'],stompingImg:['Stomping','lower body'], stretchingImg:['Stretching','upper body'],talkingImg:['Speech','bulber'],
                     throwingImg:['Throwing','upper body'],thinkingImg:['Thinking','bulbar'],touchingImg:['Touching','bulbar'],walkingImg:['Walking','lower body'],
                     wavingImg:['Waving','upper body'],yawningImg:['Yawning','bulbar']}

        pictureList=list(pictureDict.items())
        random.shuffle(pictureList)

        pictureList2=list(pictureDictionary.items())
        random.shuffle(pictureList2)

        #print(pictureList2)
        #print(pictureList2[0][0])

        roundCounter=0
        cursorHoldCounter = 0

        typecounter = 0
        boxcounter = 1
        counter = 0
        printcounter=0

        changepic=False
        #bulbar=0
        #upperBody=0
        #lowerBody=0

        pygame.init()

        if not instructions.create_instructions('vip'):
            # error occurred ?
            print("instructions exited with error?")

        #screen = pygame.display.set_mode([800, 500])
        winDimension=pygame.display.Info()
        screen = pygame.display.set_mode((winDimension.current_w, winDimension.current_h), pygame.RESIZABLE)
        pygame.display.set_caption('VIP')

        cursor = Cursor.Cursor()

        box1 = Box.Box()
        #box1.changeSize(140, 40)
        box1.changeColor(128, 128, 128)

        box2 = Box.Box()

        box3 = Box.Box()

        box4 = Box.Box()

        box5 = Box.Box()

        box6 = Box.Box()
        #print("box2 rect: " + str(box2.rect))
        boxSprites=pygame.sprite.Group()
        boxSprites.add(box2)
        boxSprites.add(box3)
        boxSprites.add(box4)
        boxSprites.add(box5)
        boxSprites.add(box6)


        boxList=[box2,box3,box4,box5,box6]
        random.shuffle(boxList)
        clock = pygame.time.Clock()
        clock.tick(10)  # #game fps
        currentTick=0
        prevTick=0
        screen.blit(cursor.surf, cursor.rect)
        change_rounds = True
        erase=0

        run=True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            #screen.fill((226, 230, 223)) #change this to white
            screen.fill((255, 255, 255))  # change this to white
            screen.blit(box2.surf, (box2.rect.x, box2.rect.y))
            box2.update(2*winDimension.current_w/3,winDimension.current_h/6)
            screen.blit(box3.surf, box3.rect)
            box3.update(2*winDimension.current_w/3, 2*winDimension.current_h/6)
            screen.blit(box4.surf, box4.rect)
            box4.update(2*winDimension.current_w/3, 3*winDimension.current_h/6)
            screen.blit(box5.surf, box5.rect)
            box5.update(2*winDimension.current_w/3, 4*winDimension.current_h/6)
            screen.blit(box6.surf, box6.rect)
            box6.update(2*winDimension.current_w/3, 5*winDimension.current_h/6)
            #box1.addText("Example",100,80)
            screen.blit(cursor.surf, cursor.rect)
            # Update the player sprite based on user keypresses
            mouse = pygame.mouse.get_pos()
            cursor.rect.x = mouse[0] - 5
            cursor.rect.y = mouse[1] - 5
            pressed_keys = pygame.key.get_pressed()
            cursor.update(pressed_keys, winDimension.current_w, winDimension.current_h)

            if roundCounter==18:
                "return the guesses for result calculation"
                #print(correctVerbs)
                #print(guessVerbs)
                print("bulbar: " + str(bulbar))
                print("upperbody: " + str(upperBody))
                print("lowerbody: " + str(lowerBody))
                changepic=None
                roundCounter=17
                self.setRunning('False')

            if changepic==None:
                font = pygame.font.SysFont('Times New Roman', 50)
                screen.fill((255, 255, 255))
                screen.blit(cursor.surf, cursor.rect)
                screen.blit(font.render('Congrats On Completing the',True,(0,0,0)),(winDimension.current_w/4,(winDimension.current_h/3)-windowHeightOffset))
                screen.blit(font.render('VIP Test', True, (0, 0, 0)), (winDimension.current_w/3, (winDimension.current_h/3)+50))
                screen.blit(box1.surf, box1.rect.topleft)
                font = pygame.font.SysFont('Times New Roman', 30)
                text = font.render('Next', True, (0, 0, 0))
                screen.blit(text, (690, 455))
                mouse = pygame.mouse.get_pos()
                cursor.rect.x = mouse[0] - 5
                cursor.rect.y = mouse[1] - 5
                # pygame.draw.rect(screen, (128, 128, 128), rect)
                #pygame.quit()
                #if 650 <= mouse[0] <= 800 and 450 <= mouse[1] <= 500:

                    #cursor.surf.fill((240, 194, 70))
                    #cursorHoldCounter += 1
                    #pygame.quit()
                    #if cursorHoldCounter == 500:
                        #cursorHoldCounter = 0
                        #print('Done')
                    # pygame.draw.rect(screen, (255,255,255), [650, 450 , 140, 40])

                #else:
                    #cursor.surf.fill((153, 186, 128))
                    #cursorHoldCounter = 0
            if changepic:
                changepic=False
                random.shuffle(boxList)

            elif changepic==False:
                #screen.blit(pygame.transform.scale(pictureList[roundCounter][0], (400, 300)), [215, 80])
                screen.blit(pygame.transform.scale(pictureList2[roundCounter][0], (winDimension.current_w/3, (winDimension.current_h - windowHeightOffset)))
                            , [winDimension.current_w/4, windowHeightOffset/2])
                #correctVerbs[roundCounter]=pictureList[roundCounter][1][0]
                font = pygame.font.SysFont('Helvetica',28)
                text = font.render(pictureList2[roundCounter][1][0][0], True, (0,0,0))
                textRect = text.get_rect()
                textRect.topleft=(boxList[0].rect.x, boxList[0].rect.y + 10)
                screen.blit(text, textRect)
                #boxList

                #font = pygame.font.SysFont('Times New Roman', 19)
                #text = font.render(pictureList[roundCounter][1][0], True, (0, 0, 0))
                #textRect = text.get_rect()
                #textRect.topleft = (boxList[boxcounter].length, boxList[boxcounter].width + 10)
                #screen.blit(text, textRect)

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

                type=pictureList[roundCounter][1][1]
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
                counter=0
                boxcounter=1
                typecounter=0

            collided_box = pygame.sprite.spritecollideany(cursor, boxSprites)
            if collided_box and changepic != None:
                cursor.surf.fill((240, 194, 70))
                cursorHoldCounter += 1
                #print("collided with " + str(collided_box.type))
                if cursorHoldCounter == 450:
                    changepic = True

                    if collided_box.type == 'bulbar':
                        self.bulbar += collided_box.value

                    elif collided_box.type == "upper body":
                        self.upperBody += collided_box.value

                    else:
                        self.lowerBody += collided_box.value

                    #guessVerbs[roundCounter]=collided_box.type #line has no funntionality for the test.
                    roundCounter += 1
                    cursorHoldCounter = 0
                    cursor.rect.topleft = (0, 0)
                    screen.blit(cursor.surf, cursor.rect)

            else:
                cursor.surf.fill((255, 255, 255))
                cursorHoldCounter=0

            # if roundCounter==16:
            #     "output message that says good job"
            #     print(correctVerbs)
            #     print(guessVerbs)
            #     roundCounter=0
            pygame.display.flip()
        pygame.quit()
        return 1
