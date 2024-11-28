########################################
# File Name: PongGame.py
# Description: This program is a Pong style game themed around outer space
# Author: Marcus Ng
# Date: 2022 - 09 - 26
#########################################

from timeit import repeat
import pygame
import random
pygame.init()
pygame.font.init()

gameIsRunning = False #boolean for checking if pong game is running or not
length = 1000 #length of screen
width = 600 #width of screen
brickX = 985 #starting x-coordinate for player 2's brick
brickY = 250 #starting y-coordinate for player 2's brick
secondBrickX = 0 #starting x-coordinate for player 1's brick
secondBrickY = 250 #starting y-coordinate for player 2's brick
brickLength = 15 #length of brick 
brickWidth = 100 #width of brick
ballX = 500 #starting x-coordinate for ball
ballY = 300 #starting y-coordinate for ball
ballYAngle = 0 #starting angle for ball
ballRadius = 10 #radius of ball
player1BrickSpeedY = 4 #speed of player 1's brick
player2BrickSpeedY = 4 #speed of player 2's brick
ballSpeed = 0 #default speed of ball
ballSpeedDifficultyPickedVariable = 0 #this is the ball speed that is picked in the difficulty menu
player1Score = 0 #score of player 1
player2Score = 0 #score of player 2
cheatCanBeActivatedByPlayer1 = False #bool to check if the cheat can be activated by player 1
cheatCanBeActivatedByPlayer2 = False #bool to check if the cheat can be activated by player 2
cheatActivatedByPlayer1 = False #bool to check if the cheat is activated by player 1
cheatActivatedByPlayer2 = False #bool to check if the cheat is activated by player 2
array = [] #initializes array used later on in program
menuBool = True #boolean to check if the menu is open or not
creditsMenu = False #boolean to check if the credits menu is open or not
endMenuBool = False #boolean to check if the end menu is open or not
repeatProgram = True #boolean to check if the whole program should be repeated or not
difficultyMenu = False #boolean to check whether the difficulty menu should be opened or not
clock = pygame.time.Clock() #clock variable which is used for limited frame rate (fps)
window = pygame.display.set_mode((length, width)) #setting size of window
pic = pygame.image.load("spacebg.png") #background of window
earthDestroyed = pygame.image.load("EarthDestroyedScreen.png")
marsDestroyed = pygame.image.load("MarsDestroyedScreen.png")
#below are the fonts and sizes used in game
font = pygame.font.Font(("Pixeboy-z8XGD.ttf"), 100) #size 100 font used for in-game text
fontSize75 = pygame.font.Font(("Pixeboy-z8XGD.ttf"), 75) #size 75 font used for in-game text
fontSize60 = pygame.font.Font(("Pixeboy-z8XGD.ttf"), 60) #size 60 font used for in-game text
#below are the music and sound FX used in game 
pygame.mixer.music.load('PanGalactic.mp3') #background music for game
pygame.mixer.music.set_volume(1) #sets volume of music
pygame.mixer.music.play(-1) #loops the music
get_point = pygame.mixer.Sound('getPoint.mp3') #sound played when point is earned
get_point.set_volume(1)
hit_paddle = pygame.mixer.Sound('Oof.mp3') #sound played when ball hits brick
hit_paddle.set_volume(1)
Win = pygame.mixer.Sound('Win.mp3') #sound used when a player wins
Win.set_volume(1)

#########################################
# The showMenu() function shows the main menu
# Args: buttonType (used to return the type of button that was pressed)
# Returns: "playButtonType" or "creditsButtonType" (They are both types of buttons that can be pressed by player)
#########################################

def showMenu(buttonType):
    window.blit(pic, (0, 0)) #makes the surface a background
    window.blit(font.render('Space Pong', False, (255, 255, 255)), (275, 75)) #creates the title for the main menu
    playButton = pygame.draw.rect(window, (255, 255, 255), (345, 200, 300, 100), 2) #creates an area for the player to press the button
    window.blit(font.render('Play', False, (255, 255, 255)), (400, 223)) #creates the play button for the main menu
    creditsButton = pygame.draw.rect(window, (255, 255, 255), (345, 350, 300, 100), 2) #creates an area for the player to press the button
    window.blit(fontSize75.render('Credits', False, (255, 255, 255)), (375, 380)) #creates the credits button for the main menu
    window.blit(fontSize60.render('ESC to Quit', False, (255, 255, 255)), (720, 550)) #tells the user what button to press to quit the game
    if buttonType == "playButtonType":
        return playButton #returns type of button pressed to main program
    elif buttonType == "creditsButtonType":
        return creditsButton #returns type of button pressed to main program
    pygame.display.update()

#########################################
# The showDifficultyMenu() function shows the difficulty menu after the play button is pressed
# Args: buttonType (used to return the type of button that was pressed)
# Returns: "easyButton" or "mediumButton" or "hardButton" (They are all types of buttons that can be pressed by player)
#########################################

def showDifficultyMenu(buttonType):
    window.blit(pic, (0, 0)) #makes the surface a background
    window.blit(font.render('Difficulty', False, (255, 255, 255)), (260, 75)) #creates title for difficulty menu
    easyButton = pygame.draw.rect(window, (255, 255, 255), (345, 190, 300, 100), 2)
    window.blit(fontSize75.render('Easy', False, (255, 255, 255)), (425, 220)) #creates easy button for difficulty menu
    mediumButton = pygame.draw.rect(window, (255, 255, 255), (345, 315, 300, 100), 2)
    window.blit(fontSize75.render('Medium', False, (255, 255, 255)), (395, 345)) #creates medium button for difficulty menu
    hardButton = pygame.draw.rect(window, (255, 255, 255), (345, 440, 300, 100), 2)
    window.blit(fontSize75.render('Hard', False, (255, 255, 255)), (425, 470)) #creates hard button for difficulty menu
    window.blit(fontSize60.render('ESC to Quit', False, (255, 255, 255)), (720, 550)) #tells the user what button to press to quit the game
    if buttonType == "easyButton":
        return easyButton #returns type of button pressed to main program
    elif buttonType == "mediumButton":
        return mediumButton #returns type of button pressed to main program
    elif buttonType == "hardButton":
        return hardButton #returns type of button pressed to main program
    pygame.display.update()

#########################################
# The showCredits() function shows the credits menu
# Args: buttonType (used to return the type of button that was pressed)
# Returns: "backButton" (It's a type of button that can be pressed by player)
#########################################

def showCredits(buttonType):
    window.blit(pic, (0, 0)) #makes the surface a background
    window.blit(font.render('Credits', False, (255, 255, 255)), (330, 60)) #creates the title for the credits menu
    window.blit(fontSize75.render('Marcus Ng', False, (255, 255, 255)), (347, 175)) #shows marcus's name in credits menu
    window.blit(fontSize75.render('Chris Xu', False, (255, 255, 255)), (360, 275)) #shows chris's name in credits menu
    window.blit(fontSize75.render('Herman Huynh', False, (255, 255, 255)), (290, 375)) #shows herman's name in credits menu
    window.blit(fontSize75.render('Back', False, (255, 255, 255)), (423, 490)) #creates the back button for the credits menu
    backButton = pygame.draw.rect(window, (255, 255, 255), (340, 460, 300, 100), 2)
    window.blit(fontSize60.render('ESC to Quit', False, (255, 255, 255)), (720, 550)) #tells the user what button to press to quit the game
    if buttonType == "backButton":
        return backButton #returns type of button pressed to main program
    pygame.display.update()

#########################################
# The showEndMenu() function shows the end menu
# Args: buttonType (used to return the type of button that was pressed), player1Score, and player2Score
# Returns: "playAgainButtonType" or "endCreditsButtonType" or "quitButtonType" (They are all types of buttons that can be pressed by player)
#########################################

def showEndMenu(buttonType, player1Score, player2Score):
    window.blit(pic, (0, 0)) #makes the surface a background
    if player1Score == 7: #if the player 1's score is equal to 7, then display "Mars Wins!"
        window.blit(font.render('Mars Wins!', False, (255, 255, 255)), (285, 75))
    elif player2Score == 7: #if the player 1's score is equal to 7, then display "Earth Wins!"
        window.blit(font.render('Earth Wins!', False, (255, 255, 255)), (285, 75))
    playAgainButton = pygame.draw.rect(window, (255, 255, 255), (345, 200, 300, 100), 2)
    window.blit(fontSize60.render('Play Again', False, (255, 255, 255)), (367, 235)) #creates the play again button for end menu
    quitButton = pygame.draw.rect(window, (255, 255, 255), (345, 325, 300, 100), 2)
    window.blit(fontSize75.render('Quit', False, (255, 255, 255)), (425, 355)) #creates the quit button for end menu
    endCreditsButton = pygame.draw.rect(window, (255, 255, 255), (345, 450, 300, 100), 2)
    window.blit(fontSize75.render('Credits', False, (255, 255, 255)), (375, 480)) #creates the credits button for end menu
    window.blit(fontSize60.render('ESC to Quit', False, (255, 255, 255)), (720, 550)) #tells the user what button to press to quit the game
    if buttonType == "playAgainButtonType":
        return playAgainButton #returns type of button pressed to main program
    elif buttonType == "endCreditsButtonType":
        return endCreditsButton #returns type of button pressed to main program
    elif buttonType == "quitButtonType":
        return quitButton #returns type of button pressed to main program
    pygame.display.update()

#########################################
# The hitPaddleEventFunction() function is called when the ball hits one of the paddles
# Args: ballSpeed and ballYAngle
# Returns: none
#########################################

def hitPaddleEventFunction(ballSpeed, ballYAngle):
    pygame.mixer.Sound.play(hit_paddle)
    ballSpeed = -ballSpeed
    randNumber = random.randrange(1, 11) #all the random numbers from 1-10 are used to choose which angle the ball will bounce after it hits a paddle. it chooses the angle randomly
    if randNumber == 1:
        ballYAngle = 1
    elif randNumber == 2:
        ballYAngle = -1
    elif randNumber == 3:
        ballYAngle = 2
    elif randNumber == 4:
        ballYAngle = -2
    elif randNumber == 5:
        ballYAngle = 3
    elif randNumber == 6:
        ballYAngle = -3
    elif randNumber == 7:
        ballYAngle = 4
    elif randNumber == 8:
        ballYAngle = -4
    elif randNumber == 9:
        ballYAngle = 5
    elif randNumber == 10:
        ballYAngle = -5
    return [ballSpeed, ballYAngle]

#########################################
# The playerScoresPointEventFunction() function is called when a player scores a point
# Args: player (which player, player 1 or player 2), player2Score, player1Score, ballX, ballY, ballYAngle, ballSpeed
# Returns: player2Score, player1Score, ballX, ballY, ballYAngle, ballSpeed
#########################################

def playerScoresPointEventFunction(player, player2Score, player1Score, ballX, ballY, ballYAngle, ballSpeed):
    ballX = 500 #resets the ball's X position to 500
    ballY = 300 #resets the ball's Y position to 300
    randNumber = random.randrange(1, 3) #random numbers from 1-2 are used to determine which way the ball goes after a player scores and the ball is reset to its original position
    if randNumber == 1:
        ballYAngle = 1
    elif randNumber == 2:
        ballYAngle = -1
    ballSpeed = -ballSpeed #reverses the ball's direction
    if player == "player2": #if the player is player 2, add 1 to their score
        player2Score = player2Score + 1
    elif player == "player1": #if the player is player 1, add 1 to their score
        player1Score = player1Score + 1
    pygame.mixer.Sound.play(get_point) #plays the sound for a player getting a point
    pygame.time.delay(500)
    return [player2Score, player1Score, ballX, ballY, ballYAngle, ballSpeed] #returns all variables that were modified in the function back to the main program

while repeatProgram: #main program
    showMenu("null") #calls the showMenu function that displays the main menu
    while menuBool: #this loop keeps looping until the menu is not displayed anymore
        for event in pygame.event.get(): #loops through all pygame events
            keyPressDetection = pygame.key.get_pressed() #function used to detect whether a key was pressed or not
            if event.type == pygame.QUIT or keyPressDetection[pygame.K_ESCAPE]: #if the python window is exited or ESC is pressed, exit the program
                menuBool, repeatProgram = False, False #sets the bool values of menus open from True to False, which quits the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if showMenu("playButtonType").collidepoint(event.pos):
                    menuBool = False
                    difficultyMenu = True
                    showDifficultyMenu("null")
                    while difficultyMenu:
                        for event in pygame.event.get(): #loops through all pygame events
                            keyPressDetection = pygame.key.get_pressed() #function used to detect whether a key was pressed or not
                            if event.type == pygame.QUIT or keyPressDetection[pygame.K_ESCAPE]: #if the python window is exited or ESC is pressed, exit the program
                                menuBool, repeatProgram, difficultyMenu = False, False, False #sets the bool values of menus open from True to False, which quits the game
                            if event.type == pygame.MOUSEBUTTONDOWN: #if the mouse left click is pressed, the event checks if the mouse click was located in any of the easy, medium, or hard difficulty buttons
                                if showDifficultyMenu("easyButton").collidepoint(event.pos): #if the mouse click collides with the hitbox of the easy button, set the ball speed to 2, hide the menu, and set the gameIsRunning bool to True which runs the game
                                    ballSpeed = 2
                                    gameIsRunning = True 
                                    difficultyMenu = False
                                elif showDifficultyMenu("mediumButton").collidepoint(event.pos): #if the mouse click collides with the hitbox of the medium button, set the ball speed to 4, hide the menu, and set the gameIsRunning bool to True which runs the game
                                    ballSpeed = 4
                                    gameIsRunning = True
                                    difficultyMenu = False
                                elif showDifficultyMenu("hardButton").collidepoint(event.pos): #if the mouse click collides with the hitbox of the hard button, set the ball speed to 6, hide the menu, and set the gameIsRunning bool to True which runs the game
                                    ballSpeed = 6
                                    gameIsRunning = True
                                    difficultyMenu = False
                elif showMenu("creditsButtonType").collidepoint(event.pos): #if the mouse click collides with the hitbox of the credits button, call the showCredits() menu and set the creditsMenu bool to True
                    showCredits("null") #calls the showCredits() menu which shows the credits menu
                    creditsMenu = True
                    while creditsMenu: #while the credits menu is open, check if the back button is pressed
                        for event in pygame.event.get(): #loops through all pygame events
                            if event.type == pygame.MOUSEBUTTONDOWN: #if the player clicks the mouse left click, check if the mouse click collided with the back button hitbox
                                if showCredits("backButton").collidepoint(event.pos): #if the mouse click collided with the back button hitbox, hide the credits menu and call the showMenu() function which shows the main menu
                                    creditsMenu = False #hides the credits menu
                                    showMenu("null") #calls the showMenu() function which shows the main menu again
                        clock.tick(100) #sets the fps to 100
        clock.tick(100) #sets the fps to 100 

    while gameIsRunning: #loop that runs while the actual "pong" game is running
        pygame.display.update()
        for event in pygame.event.get(): #loops through all pygame events
            keyPressDetection = pygame.key.get_pressed() #function used to detect whether a key was pressed or not
            if event.type == pygame.QUIT or keyPressDetection[pygame.K_ESCAPE]: #if the python window is exited or ESC is pressed, exit the program
                gameIsRunning, repeatProgram = False, False #sets the bool values of menus open from True to False, which quits the game
        window.blit(pic, (0, 0)) #makes the background the space picture
        window.blit(fontSize60.render('/ for Cheat', False, (255, 255, 255)), (720, 550)) #keybind guide for cheat on lower right corner
        window.blit(fontSize60.render('Q for Cheat', False, (255, 255, 255)), (20, 550)) #keybind guide for cheat on lower left corner
        window.blit(fontSize60.render('ESC to Quit', False, (255, 255, 255)), (720, 20)) #keybind guide to quit the game on top right corner
        pygame.draw.rect(window, (255, 255, 255), (brickX, brickY, brickLength, brickWidth), 0) #makes the paddle on the left
        pygame.draw.rect(window, (255, 255, 255), (secondBrickX, secondBrickY, brickLength, brickWidth), 0) #makes the paddle on the right
        pygame.draw.circle(window, (255, 255, 255), (ballX, ballY), ballRadius, 0) #makes the ball
        ballX = ballX + ballSpeed #moves the ball on the x axis
        ballY = ballY + ballYAngle #moves the ball on the y axis
        
        if (ballY>= brickY and ballY <= brickY + brickWidth) and (ballX > brickX + ballRadius): #if the ball hits the paddle on the right, call the hitPaddleEventFunction()
            array = hitPaddleEventFunction(ballSpeed, ballYAngle)
            ballSpeed = array[0]
            ballYAngle = array[1]
        elif (ballY>= secondBrickY and ballY <= secondBrickY + brickWidth) and (ballX < secondBrickX + ballRadius): #if the ball hits the paddle on the left, call the hitPaddleEventFunction()
            array = hitPaddleEventFunction(ballSpeed, ballYAngle)
            ballSpeed = array[0]
            ballYAngle = array[1]
        elif ballY <= 0 or ballY >= 600: #if the ball hits the top or bottom of the screen, reverse the ball's angle
            ballYAngle = -ballYAngle
        elif ballX <= 0: #if the ball is scored on the left hand side, call the playerScoresPointEventFunction() and set the cheatCanBeActivatedByPlayer1 variable to True since they scored. Also reset the paddle speeds to 4
            array = playerScoresPointEventFunction("player2", player2Score, player1Score, ballX, ballY, ballYAngle, ballSpeed)
            player2Score, ballX, ballY, ballYAngle, ballSpeed = array[0], array[2], array[3], array[4], array[5]
            cheatCanBeActivatedByPlayer1, cheatCanBeActivatedByPlayer2 = True, False #allows player 1 to activate cheat now since they scored
            player1BrickSpeedY, player2BrickSpeedY = 4, 4 #resets both paddle speeds to 4 in case cheat was activated during turn
        elif ballX >= 1000: #if the ball is scored on the left hand side, call the playerScoresPointEventFunction() and set the cheatCanBeActivatedByPlayer2 variable to True since they scored. Also reset the paddle speeds to 4
            array = playerScoresPointEventFunction("player1", player2Score, player1Score, ballX, ballY, ballYAngle, ballSpeed)
            player1Score, ballX, ballY, ballYAngle, ballSpeed = array[1], array[2], array[3], array[4], array[5]
            cheatCanBeActivatedByPlayer1, cheatCanBeActivatedByPlayer2 = False, True #allows player 2 to activate cheat now since they scored
            player1BrickSpeedY, player2BrickSpeedY = 4, 4 #resets both paddle speeds to 4 in case cheat was activated during turn
        window.blit(font.render(str(player1Score)+" - "+str(player2Score), False, (255, 255, 255)), (430, 50)) #show the updated score on the screen
        
        if cheatActivatedByPlayer1: #if the cheat is activated by player 1, halve player 2's paddle speed by setting it to 2 and set the cheatActivatedByPlayer1 to False since they already activated the cheat in their turn
            player2BrickSpeedY = 2 #sets player 2's paddle speed to 2
            cheatActivatedByPlayer1 = False #turns the bool back to False ensuring the player can't activated the cheat again in that turn
        elif cheatActivatedByPlayer2: #if the cheat is activated by player 2, halve player 1's paddle speed by setting it to 2 and set the cheatActivatedByPlayer2 to False since they already activated the cheat in their turn
            player1BrickSpeedY = 2 #sets player 1's paddle speed to 2
            cheatActivatedByPlayer2 = False #turns the bool back to False ensuring the player can't activated the cheat again in that turn

        if player1Score == 7: #if player 1's score is equal to 7, they win
            pygame.display.update()
            window.blit(earthDestroyed, (0, 0)) #earthDestroyed screen is shown
            window.blit(font.render('Mars Wins!', False, (255, 255, 255)), (285, 300)) #Mars Wins! text is shown
            pygame.mixer.Sound.play(Win) #Win sound is played
            pygame.display.update()
            pygame.time.delay(5000)
            gameIsRunning = False #sets the gameIsRunning bool to False, ensuring the Pong game won't run until it is True again
            endMenuBool = True #sets the endMenuBool to True, showing the End Menu on the player's screen
            cheatCanBeActivatedByPlayer1, cheatCanBeActivatedByPlayer2, cheatActivatedByPlayer1, cheatActivatedByPlayer2 = False, False, False, False #sets all the cheat variables to False ensuring no cheat can be activated
        elif player2Score == 7: #if player 2's score is equal to 7, they win
            pygame.display.update()
            window.blit(marsDestroyed, (0, 0)) #marsDestroyed screen is shown
            window.blit(font.render('Earth Wins!', False, (255, 255, 255)), (285, 300)) #Earth Wins! text is shown
            pygame.mixer.Sound.play(Win) #Win sound is played
            pygame.display.update()
            pygame.time.delay(3000)
            gameIsRunning = False #sets the gameIsRunning bool to False, ensuring the Pong game won't run until it is True again
            endMenuBool = True #sets the endMenuBool to True, showing the End Menu on the player's screen
            cheatCanBeActivatedByPlayer1, cheatCanBeActivatedByPlayer2, cheatActivatedByPlayer1, cheatActivatedByPlayer2 = False, False, False, False #sets all the cheat variables to False ensuring no cheat can be activated

        keyPressDetection = pygame.key.get_pressed() #function used to detect whether a key was pressed or not
        if keyPressDetection[pygame.K_UP]: #if the up button is pressed, make player 1's paddle go up
            brickY = brickY - player1BrickSpeedY
            if brickY < 0: #if the paddle's Y position exceeds 0, stop the paddle from going up even more
                brickY = 0
        if keyPressDetection[pygame.K_DOWN]: #if the down button is pressed, make player 1's paddle go down
            brickY = brickY + player1BrickSpeedY
            if brickY > 500: #if the paddle's Y position exceeds 500, stop the paddle from going down even more
                brickY = 500
        if keyPressDetection[pygame.K_w]: #if the W button is pressed, make player 2's paddle go up
            secondBrickY = secondBrickY - player2BrickSpeedY
            if secondBrickY < 0: #if the paddle's Y position exceeds 0, stop the paddle from going up even more
                secondBrickY = 0
        if keyPressDetection[pygame.K_s]: #if the S button is pressed, make player 2's paddle go down
            secondBrickY = secondBrickY + player2BrickSpeedY
            if secondBrickY > 500: #if the paddle's Y position exceeds 500, stop the paddle from going down even more
                secondBrickY = 500
        if cheatCanBeActivatedByPlayer1: #if the cheat can be activated by player 1, and if player 1 presses the / key, activate the cheat
            if keyPressDetection[pygame.K_SLASH]: #if player 1 presses the slash key, the cheat will be activated
                cheatActivatedByPlayer1 = True
        elif cheatCanBeActivatedByPlayer2: #if the cheat can be activated by player 2, and if player 2 presses the Q key, activate the cheat
            if keyPressDetection[pygame.K_q]: #if player 2 presses the Q key, the cheat will be activated
                cheatActivatedByPlayer2 = True

        clock.tick(150) #sets the fps to 150

    showEndMenu("null", player1Score, player2Score) #calls the showEndMenu() function, which shows the end menu

    while endMenuBool: #while the end menu is shown
        for event in pygame.event.get(): #loops through all pygame events
            keyPressDetection = pygame.key.get_pressed() #function used to detect whether a key was pressed or not
            if event.type == pygame.QUIT or keyPressDetection[pygame.K_ESCAPE]: #if the python window is exited or ESC is pressed, exit the program
                endMenuBool, repeatProgram = False, False #sets the bool values of menus open from True to False, which quits the game
            if event.type == pygame.MOUSEBUTTONDOWN: #if the mouse left click is clicked, check if the mouse click collided with any of the buttons on the end menu
                if showEndMenu("playAgainButtonType", player1Score, player2Score).collidepoint(event.pos): #if the mouse left click collided with the play again button
                    endMenuBool , menuBool = False, True #hide the end menu and show the main menu
                    player1Score, player2Score = 0, 0 #reset the scores of the players to 0
                elif showEndMenu("quitButtonType", player1Score, player2Score).collidepoint(event.pos): #if the mouse left click collided with the quit button
                    endMenuBool, repeatProgram = False, False #sets the bool values of menus open from True to False, which quits the game
                elif showEndMenu("endCreditsButtonType", player1Score, player2Score).collidepoint(event.pos): #if the mouse left click collided with the end credits button
                    showCredits("null") #call the showCredits() function, which shows the credits menu
                    creditsMenu = True #initializes the creditsMenu bool to True
                    while creditsMenu: #while the credits menu is open and the creditsMenu bool is True
                        for event in pygame.event.get(): #loops through all pygame events
                            if event.type == pygame.MOUSEBUTTONDOWN: #if the mouse left click was pressed
                                if showCredits("backButton").collidepoint(event.pos): #if the mouse left click collided with the back button
                                    creditsMenu = False #hide the credits menu
                                    showEndMenu("null", player1Score, player2Score) #show the end menu again
        clock.tick(100) #sets the fps to 100
pygame.quit() #quits the game

