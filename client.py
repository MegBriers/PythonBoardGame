# ------ CLIENT ------
# 2018-02-28
# Megan Briers
# ADVANCED HIGHER COMPUTING PROJECT
# This is the code that is running when a player connects to the server
# -*- coding: cp1252 -*-
#!/usr/bin/env python


#Importing the necessary libraries
#PodSixNet - lightweight multiplayer networking library used for my client and server
#Time - provides various time related functions within my code 
#PyGame - open source library for multimedia applications like a game
#PyGame Font - allows fonts to be used throughtout and text to be rendered to the screen 
#PyGame event - handles all event messaging through an event queue 
#PyGame draw - allows several simple shapes to be drawn to the screen 
#String - library which contains methods to manipulate strings
#Random - This module implements pseudo-random number generators for various distributions
#Buttons - Seperate object orientated code that allows Buttons to be created
#Os - This module provides a portable way of using operating system dependent functionality
import PodSixNet, time, pygame, pygame.font, pygame.event, pygame.draw, string, random, Buttons, os, sys
from pygame.locals import *
from pygame import * 
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from random import randint

#setting dir_path to the directory path of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
#getting the current working directory
cwd = os.getcwd()
#changing the working directory of the file 
os.chdir(dir_path)

# initialise pygame
pygame.init()
# initialise pygame.font
pygame.font.init()
#screen colours of various windows
white = [255,255,255]
black = [0,0,0]
#setting up the size of the screen 
size = [600,600]

#setting the display up at the required size for the start interface 
gameDisplay2 =  pygame.display.set_mode((550, 350))

#Array storing description of all the tiles 
descrp = [ 'Kill',
           'Shield all actions',
           'Swap scores',
           'Mirror the actions',
           'Wild card!',
           'Bomb',
           'Bank',
           'Double',
           'Magnifying Glass',
           'Present',
           'Rob'
          ]

#Loading in the images required for the game
background = pygame.image.load('introscreen.png')
instruct = pygame.image.load('instructions.png')
grid = pygame.image.load('square.png')
logo = pygame.image.load('logo.png')
#NORMAL states
#These are the images displayed when an action hasn't been played yet
twohundred = pygame.image.load('200.png')
thousand = pygame.image.load('1000.png')
threethousand = pygame.image.load('3000.png')
fivethousand = pygame.image.load('5000.png')
bank = pygame.image.load('bank.png')
bomb = pygame.image.load('bomb.png')
double = pygame.image.load('double.png')
magglass = pygame.image.load('magnifinghglassreal.png')
present = pygame.image.load('present.png')
rob = pygame.image.load('rob.png')
shield = pygame.image.load('shield.png')
swap = pygame.image.load('swapscores.png')
kill = pygame.image.load('kill.png')
mirror = pygame.image.load('mirror.png')
wild = pygame.image.load('wildcard.png')
#grid lines
normallinev=pygame.image.load("normalline.png")
normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
#ACTIVE states
#These are the images displayed when an action is being played 
twohundreda = pygame.image.load('200active.png')
thousanda = pygame.image.load('1000active.png')
threethousanda = pygame.image.load('3000active.png')
fivethousanda = pygame.image.load('5000active.png')
banka = pygame.image.load('bankactive.png')
bomba = pygame.image.load('bombactive.png')
doublea = pygame.image.load('doubleactive.png')
magglassa = pygame.image.load('magnifinghglassrealactive.png')
presenta = pygame.image.load('presentactive.png')
roba = pygame.image.load('robactive.png')
shielda = pygame.image.load('shieldactive.png')
swapa = pygame.image.load('swapscoresactive.png')
killa = pygame.image.load('killactive.png')
mirrora = pygame.image.load('mirroractive.png')
wilda = pygame.image.load('wildcardactive.png')
#FINISHED states
#These are the images displayed when an action has been played 
twohundredd = pygame.image.load('200done.png')
thousandd = pygame.image.load('1000done.png')
threethousandd = pygame.image.load('3000done.png')
fivethousandd = pygame.image.load('5000done.png')
bankd = pygame.image.load('bankdone.png')
bombd = pygame.image.load('bombdone.png')
doubled = pygame.image.load('doubledone.png')
magglassd = pygame.image.load('magnifinghglassrealdone.png')
presentd = pygame.image.load('presentdone.png')
robd = pygame.image.load('robdone.png')
shieldd = pygame.image.load('shielddone.png')
swapd = pygame.image.load('swapscoresdone.png')
killd = pygame.image.load('killdone.png')
mirrord = pygame.image.load('mirrordone.png')
wildd = pygame.image.load('wildcarddone.png')


#Setting up an array of all the images
tiles = [[kill,shield,swap,mirror,wild,bomb,bank,double,magglass,present,rob],
         [killa,shielda,swapa,mirrora,wilda,bomba,banka,doublea,magglassa,presenta,roba],
         [killd,shieldd,swapd,mirrord,wildd,bombd,bankd,doubled,magglassd,presentd,robd]]


#Setting the short descriptions so the client can identify what square has been chosen
tilesdescrp = ['kill','shield','swap','mirror','wild','bomb','bank','double','magglass','present','rob']


#Setting up an array of all the money images
money = [[],[],[]]


#Appending the money to the array
money[0].append(fivethousand)
money[1].append(fivethousanda)
money[2].append(fivethousandd)
    
for i in range(2):
    money[0].append(threethousand)
    money[1].append(threethousanda)
    money[2].append(threethousandd)
    
for i in range(10):
    money[0].append(thousand)
    money[1].append(thousanda)
    money[2].append(thousandd)
    
for i in range(25):
    money[0].append(twohundred)
    money[1].append(twohundreda)
    money[2].append(twohundredd)


#Setting the short money (text) descriptions so the client can identify what square has been chosen
moneydescrp = []
moneydescrp.append('5000')
for i in range(2):
    moneydescrp.append('3000')
for i in range(10):
    moneydescrp.append('1000')
for i in range(25):
    moneydescrp.append('200')

#Setting up a 2D array to store where the clients choose to place the squares
arrayofcoords = [[],[]]

# A simple effect of sliding stars to create a deep space sensation.
# by Silveira Neto
# Free under the terms of GPLv3 license

# Constants 
N = 200
SCREEN_W, SCREEN_H = (640, 480)

# ------ WINNER SCREEN ------
# This is the code that will display an interface for the player who has the
# most points at the end of the game
# The user can exit the game by pressing any key 
def mainwinner():
	#setting up a screen 640 by 480
	screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
	#setting up the font
	fontobject = pygame.font.Font(None,30)
	#captioning the screen
	pygame.display.set_caption('You are the winner!')
 
	# create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
 
	# generate N stars
	stars = [
		[random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
		for x in range(N)
	]
 
	# main loop
	#drawing starts onto the screen and having them floating along
	clock = pygame.time.Clock()
	#endless loop 
	while 1:
            #updating the clock
            clock.tick(22)
            #get the pygame event 
            for event in pygame.event.get():
                #if event is quit
                    if event.type == QUIT:
                        #quit 
                            quit()
                    #if a key is pressed
                    elif event.type == KEYDOWN:
                        #quit the game
                            quit()
            #blue screen 
            background.fill((0,0,128))
            #drawing the stars onto the screen
            for star in stars:
                    pygame.draw.line(background,
                            (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
                    star[0] = star[0] - 1
                    if star[0] < 0:
                            star[0] = SCREEN_W
                            star[1] = random.randint(0, SCREEN_H)
            #blitting the background on 
            screen.blit(background, (0,0))
            #blitting the messages onto the screen
            screen.blit(fontobject.render("YOU WON!!!!!!",True,(255,255,255)),(10,70))
            #informing the user how to exit the game 
            screen.blit(fontobject.render("Press any key to exit",True,(255,255,255)),(50,120))
            #flip the display
            pygame.display.flip()
		

# ------ INTRO SCREEN ------
# This subroutine displays the first screen that the users see when they start up the game
# It gives the user the option to move from the intro screen to either rules or game
# The rules interface shows the instructions for how to play the game and lets the user go
# back by pressing the B button
# The game is started when the user presses G
def game_start():
    #Setting up a screen of size 550 by 450
    screen = pygame.display.set_mode((550, 450))
    #filling it in white
    screen.fill(white)
    #Setting up the fontobject
    fontobject = pygame.font.Font(None,30)
    #Blitting the logo of the pirate game to the screen
    screen.blit(logo,(20,0))
    #Blitting a background onto the screen
    screen.blit(background, (0,110))
    #Blitting the text message which informs the user how to move around screens 
    screen.blit(fontobject.render("Press R for rules or G to start game" ,True,(0,0,0)), (140,350))
    #flipping the display
    pygame.display.flip()
    #initial value of Gpressed, to let the user go into the loop 
    Gpressed = False
    #Whilst a key has not been pressed
    while Gpressed == False:
      #get the event 
      event = pygame.event.poll()
      #If a key is pressed
      if event.type == KEYDOWN:
        #If G is pressed
        if event.key == K_g:
          #Set Gpressed to True, dropping it out the loop
          Gpressed = True
        #Else if R is pressed
        elif event.key == K_r:
          #Set up a new screen of size 650 by 350 
          screen = pygame.display.set_mode((650, 350))
          #Fill the screen in white
          screen.fill(white)
          #Blit the image containing the instructions to the screen
          screen.blit(instruct,(0,0))
          #Blit the message telling the user how to go back to the home screen
          screen.blit(fontobject.render("Press B to go back" ,True,(0,0,0)), (420,260))
          #Flipping the display
          pygame.display.flip()
          #Get the event again
          event = pygame.event.poll()
        #Else if B is pressed
        elif event.key == K_b:
          #At this point, cannot call the subroutine again, because of recursion problems
          #but the whole code is repeated
          #Setting screen back to initial size
          screen = pygame.display.set_mode((550, 450))
          #filling it in white
          screen.fill(white)
          #Blitting the logo to the screen
          screen.blit(logo,(20,0))
          #Blitting the original background onto the screen
          screen.blit(background, (0,110))
          #Blitting the text onto the screen with instructions on how to get to each window
          screen.blit(fontobject.render("Press R for rules or G to start game" ,True,(0,0,0)), (140,350))
          #Flipping the display 
          pygame.display.flip()
    # move on with the game when G is pressed
    # Takes the user to the input
    main(tiles,descrp,size)


# ------ TECHNICAL ------
# A subroutine which is used at multiple points throughout the code
def get_key():
  #looping forever
  while 1:
    #getting the current event
    event = pygame.event.poll()
    #if the event is that somebody pressed a key
    if event.type == KEYDOWN:
      #return the key pressed
      return event.key
    #else
    else:
      #don't do anything else
      pass

# ------ VALIDATION ------
# These following subroutines all are used throughout the validation that occurs in the program
# Input Validation1 - Ensures the co-ordinates entered are between 1 and 7 (the grid co-ordinates)
def linearsearch(array,searchkey):
    #setting the pos to the first index of the array
    pos = 0
    #automatic state
    found = False
    #whilst they havent searched the whole array and it hasnt been found 
    while pos < len(array) and found !=True:
        #if the value at the current part for the array is equal to search key
        if array[pos] == searchkey:
            #dropping out the loop
            found = True
            #saving the position, so can use it later
            foundat=pos
        #instead of a for i in range loop 
        pos = pos + 1
    #return the position it is found at 
    return foundat

  
# ------ INPUT VALIDATION 1 ------
#Checks the number is between 1 and 7 to fit on the grid
#Required to ensure that the client doesn't enter grid co-ordinates that aren't avaliable
def inputvalidation(coord):
  #Turning into an integer in order to carry out comparisons 
  coord = int(coord)
  #While the co-ordinates are outside the range
  while coord == 0 or coord>7 or coord < 0:
      #Setting the screen to the correct screen size
      screen = pygame.display.set_mode(size)
      #Setting up the clock in order to put in a delay later  
      clock = pygame.time.Clock()
      #Setting up the font 
      basicfont = pygame.font.SysFont(None, 25)
      #Setting up the text to be blitted to screen
      #Error message
      text = basicfont.render('Invalid Input, please enter a number between 1 and 7', True, (white), (black))
      textrect = text.get_rect()
      #Making sure the text is displayed in the middle of the screen
      textrect.centerx = screen.get_rect().centerx
      textrect.centery = screen.get_rect().centery
      #filling the screen in black
      screen.fill(black)
      #displaying the input validation message to the screen 
      screen.blit(text, textrect)
      #updating the screen
      pygame.display.update()
      #including a delay in the program 
      pygame.time.wait(500)
      #fills the screen in black
      screen.fill(black)
      #asks the user again to enter an x co-ordinate again 
      coord = (ask(screen, "Co-ord"))
      #turns it into an integer 
      coord = int(coord)
  #returns co-ordinate to pass it back to the main subroutine
  return coord   
        
# ------ VALIDATION OF THE INPUTS PART 2 ------
# Compare the two values in the X and Y variables to all the other duples in the arrays
# Need to make sure that they are not entering the same numbers
# Cannot have two tiles in the same square
def inputval2(arrayofcoords,xcoord,ycoord,valid):
  #setting the boolean variable to false, only set to true when found in array
  alreadyhere = False
  #looping round for the whole length of the first array in the 2D array
  for j in range(len(arrayofcoords[0])):
    #compares the values for both X and Y
    if xcoord == arrayofcoords[0][j] and ycoord == arrayofcoords[1][j]:
      #set boolean value to true because the co-ordinate is already there
      alreadyhere = True
      #breaks out of the loop
      break
  #If the value hasn't been found in the array then it is a valid input    
  if alreadyhere == False:
    valid = True
  #returning whether or not the input
  return valid

# -- END OF VALIDATION --

# ------ MAG.GLASS subroutine ------
# This subroutine is called when the client has a magnifying glass tile
# It shows the client the score of the player that they chose to see
# Magnifying glass tile description - allows the player to choose another player and see the score of that chosen player
def show(self,chosen,points):
  #Setting the screen up as the standard size 
  screen = pygame.display.set_mode(size)
  #filling it in white
  screen.fill(white)
  #setting up the font
  basicfont = pygame.font.SysFont(None, 24)
  #showing the player and their score on the screen
  text = basicfont.render("Player " + str(chosen) + " has a score of " + str(points[chosen-1]), True, (255, 0, 0), (255, 255, 255))
  #blitting it to screen
  screen.blit(text,(100,100))
  #updating the display
  pygame.display.flip()
  #short delay
  pygame.time.wait(2000)
  

# ----- INPUT ------ 
#The following subroutines are all related to getting the users to input their co-ordinates for the grid 
#Setting up the screen for asking co-ordinate

#This subroutine sets up a box in the middle of the screen, for the input interface
def display_box(screen, message):
  #Setting the font
  fontobject = pygame.font.Font(None,18)
  #Drawing a Rectangle on the screen
  #These are drawn for the input screens  
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  #Drawing a second rectangle on the screen 
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  
  #If there is no message
  if len(message) != 0:
    #Blit the current message to the screen, in the boxes
    screen.blit(fontobject.render(message, 1, (white)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  #flipping the display 
  pygame.display.flip()
  
# ------ INPUT BOX SCREEN ------
#This subroutine actually displays the window asking for input 
def ask(screen, question):
  #Initialising the font for the input box
  pygame.font.init()
  #This will be an array to take in the current characters 
  current_string = []

  #Joining the current string to a blank space as required by python 3
  #calls the display box subroutine to ask the question 
  display_box(screen, question + ": " + "".join(current_string))
  #forever 
  while 1:
    #get the key pressed
    inkey = get_key()
    #If backspace is pressed
    if inkey == K_BACKSPACE:
      #If a backspace is entered, removes the last string from array 
      current_string = current_string[0:-1]
    #If return is pressed
    elif inkey == K_RETURN:
      #If there is a message present
      if len(current_string) != 0:
          #breaking out of the loop if something has been entered
          break
     #Else if there is not a message present
      else:
          #do nothing
          pass
    #If the key pressed is a character
    elif inkey <= 127:
      #Appending the array with the character
      current_string.append(chr(inkey))
    #If the key pressed is not a character 
    elif inkey > 127:
      #take one off the array
      current_string = current_string[0:-1]
    #Joining the current string  
    testing = question + ": " + "".join(current_string)
    #calls the display box subroutine to ask the question 
    display_box(screen, testing)  
  #returning the values so that they can be used in the next subroutine, joined to a blank string space
  return "".join(current_string[0:1])

# ------ DISPLAYING IMAGE FOR INPUT ------
#This subroutine displays the image to the clients ready for their input
#Also displays the description of what the action does
def firstdisplay(tiles,descrp,i):
  #Setting the size of the screen 
  screen = pygame.display.set_mode((300,300))
  #Getting the current tile in a loop and saving it to a variable to blit 
  currenttile = tiles[0][i]
  #Blitting the image on the screen at 150,150 
  screen.blit(currenttile,(150,150))
  pygame.font.init() 
  myfont = pygame.font.Font(None,25)
  #Getting the description of the current tile and saving it to a variable to blit
  texttodisplay = descrp[i]
  #Rendering the text to screen 
  textsurface = myfont.render(texttodisplay, False, (white))
  #Blitting the screen with the text
  screen.blit(textsurface,(150,100))
  #Updating the display
  pygame.display.flip()
  #Delaying the next screen, so the user has time to read the description 
  pygame.time.delay(1000)

# ------ MAIN INPUT SUBROUTINE ------
#Calls other subroutines to display the tiles, get the input
#then validate the inputs(twice) to ensure it is in range and not been entered before
#Receives the input for all 49 of the tiles that need to be placed on the grid
def main(tiles,descrp,size):
  #Loop 10 times for the number of action tiles
  for i in range(len(tiles[0])):
    #Sets up the screen as required size 
    screen = pygame.display.set_mode(size)
    #Fills the screen in as black
    screen.fill(black)
    #Displays description of the current tile and picture
    firstdisplay(tiles,descrp,i)
    #Making the screen black again
    screen.fill(black)
    #Updating the screen again
    pygame.display.update()
    #Asks you to enter the X co-ordinate for placement of current tile
    xcoord = (ask(screen, " X co-ord"))
    #calls the input validation for the x coord 
    xcoord = inputvalidation(xcoord)
    #Asks you to enter the Y co-ordinate for placement of current tile 
    ycoord = (ask(screen, " Y co-ord"))
    #calls the input validation for the y coord 
    ycoord = inputvalidation(ycoord)
    #have this in because if it is the first time round, there wouldn't be any need to compare and validate against other coords
    if i != 0:
      #assuming the co-ordinate is not valid
      valid = False
      while valid == False:
        #calling the valid subroutine
        valid = inputval2(arrayofcoords,xcoord,ycoord,valid)
        if valid == False:
          #calls everything again and makes them enter co-ordinates again
          screen.fill((0,0,0))
          #setting up the font
          basicfont = pygame.font.SysFont(None, 24)
          #setting up an error message
          text = basicfont.render('Co-ordinate was already entered', True, (255, 255, 255), (0, 0, 0))
          #blitting the message to the screen 
          screen.blit(text,(20,25))
          #updating the display 
          pygame.display.flip()
          #setting a short delay
          pygame.time.wait(2000)
          #filling in the screen 
          screen.fill((255,255,255))
          #calling the grid to be displayed 
          game2(arrayofcoords,tiles,money,False,False,True)
          #updating the display
          pygame.display.flip()
          #calling the co-ordinate input to be called 
          firstdisplay(tiles,descrp,i)
          #Making the screen black again
          screen.fill(black)
          #Updating the screen again
          pygame.display.update()
          #Asks you to enter the X co-ordinate for placement of current tile
          xcoord = (ask(screen, " X co-ord"))
          #calls the input validation for the x coord 
          xcoord = inputvalidation(xcoord)
          #Asks you to enter the Y co-ordinate for placement of current tile 
          ycoord = (ask(screen, " Y co-ord"))
          #calls the input validation for the y coord 
          ycoord = inputvalidation(ycoord)
          #These lines are put in so I can check that the program is responding correctly
      
    #Append to the 2D array, but once it is through validation  
    arrayofcoords[0].append(xcoord)
    arrayofcoords[1].append(ycoord)

    #Calling the game2 subroutine
    game2(arrayofcoords,tiles,money,False,False)

  #this is required for passing an empty array into the first display subroutine
  #an array is required but there is no need for a description for money
  blank = []
  for i in range(len(money[0])):
    blank.append("")
  #loops through the money  
  for i in range(len(money[0])):
    #Sets up the screen as required size 
    screen = pygame.display.set_mode(size)
    #Fills the screen in as black
    screen.fill(black)
    #Displays description of the current tile and picture
    firstdisplay(money,blank,i)
    #Making the screen black again
    screen.fill(black)
    #Updating the screen again
    pygame.display.update()
    #Asks you to enter the X co-ordinate for placement of current tile
    xcoordm = (ask(screen, " X co-ord"))
    #calls the input validation for the x coord 
    xcoordm = inputvalidation(xcoordm)
    #Asks you to enter the Y co-ordinate for placement of current tile 
    ycoordm = (ask(screen, " Y co-ord"))
    #calls the input validation for the y coord 
    ycoordm = inputvalidation(ycoordm)
    #assuming the co-ordinate is not valid 
    valid = False
    while valid == False:
      #making sure that the co-ordinate hasn't already been entered
      valid = inputval2(arrayofcoords,xcoordm,ycoordm,valid)
      if valid == False:
         screen.fill((0,0,0))
         #displaying an error message onto the screen
         basicfont = pygame.font.SysFont(None, 24)
         #setting up a message 
         text = basicfont.render('Co-ordinate was already entered', True, (255, 255, 255), (0, 0, 0))
         #blitting it to the screen
         screen.blit(text,(20,25))
         #flipping the display 
         pygame.display.flip()
         #set a delay of 2000 millisecond 
         pygame.time.wait(2000)
         #fill the screen in white
         screen.fill(white)
         #displaying the grid
         game2(arrayofcoords,tiles,money,False,False,True)
         #flipping the display
         pygame.display.flip() 
        #get them to input the co-ordinate again
         firstdisplay(money,blank,i)
        #Making the screen black again
         screen.fill(black)
        #Updating the screen again
         pygame.display.update()
        #Asks you to enter the X co-ordinate for placement of current tile
         xcoordm = (ask(screen, " X co-ord"))
        #calls the input validation for the x coord 
         xcoordm = inputvalidation(xcoordm)
        #Asks you to enter the Y co-ordinate for placement of current tile 
         ycoordm = (ask(screen, " Y co-ord"))
        #calls the input validation for the y coord 
         ycoordm = inputvalidation(ycoordm)
  
    #Append to the 2D array, once it is through validation  
    arrayofcoords[0].append(xcoordm)
    arrayofcoords[1].append(ycoordm)

    #CALL THE GRID DISPLAY
    game2(arrayofcoords,tiles,money,False,False)
    #Set introdone to True
    introdone = True

# ----- GRID DISPLAY ------
#This subroutine displays the grid to the player with all the co-ordinates they have entered
#It is called in the main client loop
#It can be called at various points during the game, with variable messages displayed at the
#bottom of the screen. In essence, this is the subroutine that displays the grid 
def game2(arrayofcoords,tiles,money,finished,maingame, reenter = None, score = None, rounds = None):
    screen = pygame.display.set_mode(size)
    #filling it in white
    screen.fill(white)
    #adding title text
    basicfont = pygame.font.SysFont(None, 24)
    
    #displaying the grid/tiles
    for x in range(7):
        #putting one of the axis numbers onto the screen
        test = basicfont.render(str(x+1), True,(0,0,0))
        #blitting the text to the screen
        screen.blit(test,((x+1)*70, 50))
        for y in range(8):
             #blitting the lines onto the screen that make up the grid
             screen.blit(normallineh, [(x+1)*64+5, (y+1)*64])

    #displaying the rest of the grid lines       
    for x in range(8):
        for y in range(7):
            test2 = basicfont.render(str(y+1), True,(0,0,0))
            #blitting the other numbers to the screen
            screen.blit(test2,(50, (y+1)*70))
            #adding in grid lines 
            screen.blit(normallinev, [(x+1)*64, (y+1)*64+5])

    # blitting the tiles onto the screen 
    # blits at the right positions 
    for i in range(len(arrayofcoords[0])):
        #blit the action tiles
        if i <= 10:
            #placing current image on the screen
            screen.blit(tiles[0][i], [arrayofcoords[0][i]*64+14, arrayofcoords[1][i]*64+20])
        #blit the money tiles
        else:
            #placing current image on the screen
            screen.blit(money[0][i-11], [arrayofcoords[0][i]*64+14, arrayofcoords[1][i]*64+20])

    #setting up the font
    fontobject = pygame.font.Font(None,30)
    #If still in the input 
    if finished == False and reenter != True:
        #blit a message to the screen
        screen.blit(fontobject.render("Press any key to continue" ,True,(0,0,0)), (20,550))
        #update the display
        pygame.display.flip()
        #set default value
        keypressed = False
        while keypressed == False:
          #collect the event
          event = pygame.event.poll()
          #if event is a key
          if event.type == KEYDOWN:
              #drop out of loop 
            keypressed = True
    #during input but when a co-ordinate has been entered more than once
    elif finished == False and reenter == True:
        #error message
        screen.blit(fontobject.render("Please enter a co-ordinate not already chosen",True,(0,0,0)), (20,550))
        #flip the display
        pygame.display.flip()
        pygame.time.wait(2000)
        
    #when finished input
    elif finished == True and maingame == False:
        #blitting a waiting message to the screen
        screen.blit(fontobject.render("Waiting for other pirates" ,True,(0,0,0)), (20,550))
        #flip the display
        pygame.display.flip()
        #Pump the connection
        connection.Pump()
        #Pump the client 
        client.Pump()
        #Pump the pygame.event 
        pygame.event.pump()
        
    #during the game 
    elif finished == True and maingame == True:
        #pump the connection
        connection.Pump()
        #pump the client 
        client.Pump()
        #blit the current score to the screen
        screen.blit(fontobject.render("Your current score:  " + str(score), True, (0,0,0)),(20,550))
        #blit the current round to the screen
        screen.blit(fontobject.render("Round:  " + str(rounds), True, (0,0,0)), (300,550))
        #flip the display
        pygame.display.flip()

# ------ BUTTONS FOR NORMAL CODE ------

#This class will allow the players to choose who they want to attack with buttons
#It is called when the user has to make a choice in an action (excludes: wildcard)

class Button:
    # adding action to arguments to allow use for different actions
    #Initalizing the values of the classes
    def __init__(self, player, action,points,shields,mirrors,order):
        #players that will be displayed on the buttons
        self.player1 = None
        self.player2 = None
        #setting chosen to None initally 
        chosen = None
        #initializing the font 
        pygame.font.init()
        #calling the main button definition within the class
        self.mainbutton(player, action, points, shields, mirrors,order)
    
    #Create a display
    def display(self):
        #setting up the display 
        self.screen = pygame.display.set_mode((650,370),0,32)

    #Update the display and show the button
    def update_display(self, action):
        #filling in the screen white
        self.screen.fill((255,255,255))
        #setting up font because it is in the class so not set up 
        self.fontobject = pygame.font.Font(None,30)
        #blitting a message to tell the client what they are choosing for
        #these are actions where you cant just say 'who do you want to magglass' etc
        if action != ('present') and action != ('magglass'):
            #blit a default messaging asking for a choice 
            self.screen.blit(self.fontobject.render("Who do you want to " + str(action) + " ?" ,True,(0,0,0)), (20,20))
        #correct statement/grammar for if the action is present
        elif action == ('present'):
            self.screen.blit(self.fontobject.render("Who do you want to give a present to?"  ,True,(0,0,0)), (20,20))
        #correct statement for if the action is magnifying glass
        elif action == ('magglass'):
            self.screen.blit(self.fontobject.render("Whose score do you want to see?",True,(0,0,0)), (20,20))
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,                         text_color
        self.Button1.create_button(self.screen, (107,142,35), 225, 135, 200,    100,    0,        "Player" + str(self.player1), (255,255,255))
        self.Button2.create_button(self.screen, (107,142,35), 225, 250, 200,    100,    0,        "Player" + str(self.player2), (255,255,255))
        #updating the display
        pygame.display.flip()


    #Run the loop
    def mainbutton(self, player, action, points, shields, mirrors, order):
        #creating instances of the buttons 
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        #allows the client to stay in the loop until one of the buttons is clicked
        goround = True

        #setting up the players and who they have to choose between 
        if player == 3:
            self.player1 = 1
            self.player2 = 2
        elif player == 2:
            self.player1 = 1
            self.player2 = 3
        elif player == 1:
            self.player1 = 2
            self.player2 = 3
        #updating the display
        self.display()
        #stays in a loop until button is pressed
        while goround == True:
            pygame.event.pump()
            #updating the displaying with the buttons to choose from 
            self.update_display(action)
            #quit stuff
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #quit the game
                    pygame.quit()
                #when the button is pressed
                elif event.type == MOUSEBUTTONDOWN:
                    #if it was button 1
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                      #setting up a variable with the chosen player
                        chosen = self.player1
                        #Need seperate code for magnifying glass 
                        if action == ('magglass'):
                          #Finding the position of the chosen player in the order array
                          pos = linearsearch(order,chosen)
                          #if they player chosen does not have a shield or a mirror
                          if shields[pos] == False and mirrors[pos] == False: 
                          #call a definition to show the score
                            show(self,chosen,points)
                          #if the player chosen has a shield 
                          elif shields[pos] == True:
                            #action is skipped 
                            pass
                          #if the player chosen has a mirror 
                          elif mirrors[pos] == True:
                            #show the attacker their own score
                            show(self,player,points)
                        
                        #a network action is sent back with action, player chosen and player who chose 
                        connection.Send({'action':'chosen','playera':chosen, 'playern':player,'tobedone':action})
                        #pumping the client and the server to ensure the data gets through 
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        #setting up a variable with the chosen player
                        chosen = self.player2
                        if action == ('magglass'):
                          #finding the position of the player chosen within the order array
                          pos = linearsearch(order,chosen)
                          #If the player chosen does not have a shield or a mirror
                          if shields[pos] == False and mirrors[pos] == False: 
                            #call a definition to show the points of the player chosen
                            show(self,chosen,points)
                          #If the player chosen has a shield 
                          elif shields[pos] == True:
                            #Do nothing 
                            pass
                          #If the player chosen has a mirror
                          elif mirrors[pos] == True:
                             #Show the attacker their own score
                            show(self,player,points) 
                        #sending a network event as above
                        connection.Send({'action':'chosen','playera':chosen, 'playern':player,'tobedone':action})
                        #pumping the connection and the client 
                        connection.Pump()
                        client.Pump()
                        #breaking out of the loop
                        goround = False



# ------ BUTTONS FOR WILD CARDS ------
#This class will allow the players to choose which action they
#want to perform as part of the wild card action tile
#They have the choice from
#- Rob
#- Kill
#- Swap
#- Present
#- Magnifying glass
#- Bank
#- Bomb
#- Double 

class Button_Wild():
    #Initalizing the values of the classes
    def __init__(self):
        #initialize the font (have to do it again because within the class)
        pygame.font.init()
        #calling the main button definition within the class
        self.mainbutton()
    
    #Create a display
    def display(self):
        #setting up the display of size 400 by 400
        self.screen = pygame.display.set_mode((400,400),0,32)

    #Update the display and show the button
    def update_display(self):
        #filling in the screen white
        self.screen.fill((255,255,255))
        #setting up font because it is in the class so not set up 
        self.fontobject = pygame.font.Font(None,10)

        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.Button1.create_button(self.screen, (255,0,0), 75, 30, 100,    50,    0,        "Rob", (255,255,255))
        self.Button2.create_button(self.screen, (255,165,0), 260, 20, 100,    50,    0,        "Kill", (255,255,255))
        self.Button3.create_button(self.screen, (255,255,0), 100, 100, 100,    50,    0,        "Swap", (255,255,255))
        self.Button4.create_button(self.screen, (50,205,50), 280, 200, 100,    50,    0,        "Present", (255,255,255))
        self.Button5.create_button(self.screen, (0,191,255), 20, 210, 100,    50,    0,        "Mag.Glass", (255,255,255))
        self.Button6.create_button(self.screen, (75,0,130), 200, 270, 100,    50,    0,        "Bank", (255,255,255))
        self.Button7.create_button(self.screen, (148,0,211), 50, 320, 100,    50,    0,        "Bomb", (255,255,255))
        self.Button8.create_button(self.screen, (240,128,128), 250, 330, 100,    50,    0,        "Double", (255,255,255))
        #updating the display
        pygame.display.flip()


    #Run the loop
    def mainbutton(self):
        #creating the buttons
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        self.Button4 = Buttons.Button()
        self.Button5 = Buttons.Button()
        self.Button6 = Buttons.Button()
        self.Button7 = Buttons.Button()
        self.Button8 = Buttons.Button()
        #allows the client to stay in the loop until one of the buttons is clicked
        goround = True

        self.display()
        #stays in a loop until button is pressed
        while goround == True:
            pygame.event.pump()
            #updating the displaying with the buttons to choose from 
            self.update_display()
            #quit stuff
            for event in pygame.event.get():
                #if event type is quit
                if event.type == pygame.QUIT:
                    #quit the game
                    pygame.quit()
                #when the button is pressed
                elif event.type == MOUSEBUTTONDOWN:
                    #if button1 was pressed
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        #send back a message to the server saying the action chosen was rob
                        connection.Send({'action':'wildchosen','tobedone':'rob'})
                        #pumping the connection and the client 
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button2 is pressed
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        #telling the server that the action chosen was kill
                        connection.Send({'action':'wildchosen','tobedone':'kill'})
                        #pump the connection and the client 
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button3 is pressed
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        #sending to the server that the action chosen was swap
                        connection.Send({'action':'wildchosen','tobedone':'swap'})
                        #pump connection and client
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button4 is pressed
                    elif self.Button4.pressed(pygame.mouse.get_pos()):
                        #sending present as the action chosen to the server 
                        connection.Send({'action':'wildchosen','tobedone':'present'})
                        #pumping the connection and client  
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button5 is pressed
                    elif self.Button5.pressed(pygame.mouse.get_pos()):
                        #sending magglass as the action chosen to the server
                        connection.Send({'action':'wildchosen','tobedone':'magglass'})
                        #pumping the connection and the client 
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button6 is pressed
                    elif self.Button6.pressed(pygame.mouse.get_pos()):
                        #telling the server that bank was the action chosen 
                        connection.Send({'action':'wildchosen','tobedone':'bank'})
                        #pumping the connection and the client
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button7 is pressed
                    elif self.Button7.pressed(pygame.mouse.get_pos()):
                        #sending through to the server that bomb was the action the client chose
                        connection.Send({'action':'wildchosen','tobedone':'bomb'})
                        #pumping the connection and client 
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    #if button8 is pressed
                    elif self.Button8.pressed(pygame.mouse.get_pos()):
                        #telling the server that double was chosen
                        connection.Send({'action':'wildchosen','tobedone':'double'})
                        #pumping the connection and client
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False

# ------ CLIENT ------
     
#Setting up the Network Listener Class
#This is the client 
class MyNetworkListener(ConnectionListener):
    #Initalizing all the variables for the client
    def __init__(self, host, port):
        # connect to the server
        self.Connect((host, port))
        # open a pygame window
        self.screen = pygame.display.set_mode((550,350))
        # set font
        self.font = pygame.font.SysFont(None,20)
        # --- ALL THE VARIABLES NEED TO BE DECLARED BEFORE USE ---
        # inital value of total players
        self.totalplayers = None
        # player number
        self.num = None
        # the number of ready players
        self.rplay = 0
        # and that I am ready
        self.ready = False
        # are all players ready?
        self.allready = False
        # added extra dimension to pass counter
        self.currentsquare = [0,0,0]
        # players current action
        self.action = None
        # player current points
        self.points = [0,0,0]
        # player who has to chose a person to attack
        self.playernot = 0
        # whether all the actions have been completed
        self.actioncomplete = False
        # the player chosen
        self.playerc = 0
        # an array to store the three clients shield boolean values
        self.shields = []
        # an array to store the three clients mirror boolean values
        self.mirrors = []
        # an array to store the order of the three clients 
        self.orders = []
        # initiating the position
        self.position = 0
        # setting up an empty array to store the summary values
        self.summary = [[],[],[],[],[]]
        # initiating the self.place variable to ten
        self.place = 10
        # setting the summaryflag to False initally 
        self.summaryflag = False
        # setting up self.rounds as one to start
        self.rounds = 1
        # setting up an empty array to store the bank values 
        self.banks = []
        # initalizing the bankflag as False
        self.bankflag = False


    #Necessary network event 
    def Network(self, data):
        # print network data to client console
        print(data)

    #A subroutine used to make sure 3 players are connected to the server before it starts
    #updates a client array
    def Network_players(self,data):
        #receiving the data from the network
        self.totalplayers  = data['playerno']

    #Assigning a player number to the client 
    def Network_number(self,data):
        #getting data from the server
        self.num = data['num']
        # print out player number
        print("I am pirate number " + str(self.num))
        # set window title with player number
        pygame.display.set_caption("Pirate " + str(self.num))

    #Receives information on how many players are ready from server 
    def Network_playrno(self, data):
        # updated to number in the array in the server 
        self.rplay = data['playno']
        #Testing purposes
        print("Number of pirates ready is " + str(self.rplay))

# ----- CHANGING SQUARE ------
# figures out the action the client has at the newly chosen co-ordinate
# sends the action back to the server, so the server can process it 
    def Network_changesquare(self,data):
        #setting the current square array at place zero to the value for x
        self.currentsquare[0] = data['x']
        #setting the current square array at place one to the value for y 
        self.currentsquare[1] = data['y']
        #added to capture counter
        #setting the current square array at place one to the value for counter
        self.currentsquare[2] = data['counter']
        #setting the xcoord variable to the x value in the array
        xcoord = self.currentsquare[0]
        #setting the ycoord variable to y value in the
        ycoord = self.currentsquare[1]
        
        #determining position of the square in arrayofcoords
        for i in range(len(arrayofcoords[0])):
          for j in range(len(arrayofcoords[0])):
            if xcoord == arrayofcoords[0][j] and ycoord == arrayofcoords[1][j]:
              #setting position as where the action tile was found
              self.position = j
              #break out of the loop if the position is required
              break
        # pumping connections and client 
        connection.Pump()
        client.Pump()
        #if position is in the first ten
        if self.position <=10:
          #set the action value to be the tiles descrp 
          self.action = tilesdescrp[self.position]
          #setting it to the active tile
          tiles[0][self.position] = tiles[1][self.position]
          #calling the grid display 
          game2(arrayofcoords,tiles,money,True,True)
          #testing purposes
        else:
          #because it is a money, access the moneydescrp array instead
          self.action = moneydescrp[self.position-11]
          #displaying the active tile
          money[0][self.position-11] = money[1][self.position-11]
          #triggering the game display
          game2(arrayofcoords,tiles,money,True,True,False,self.points[self.num-1],self.rounds)

        #sending the action back to the server
        connection.Send({'action':'actiontodo','actionsarray':self.action, 'number':self.num})
        #Pumping the server and the client to ensure they receive new data
        connection.Pump()
        client.Pump()

# ------ ASSIGNING POINTS ------
# Updates the current points total 
    def Network_current(self,data):
        #player 1s points comes through first in the network event 
        self.points[0] = data[0]
        #then player 2
        self.points[1] = data[1]
        #then player 3
        self.points[2] = data[2]
    
# ----- COMPLETED A ROUND -------
# This subroutine changes the tile icons to finished state icons
# once all the actions have been performed for that round
    def Network_complete(self, data):
      #setting the self.actioncomplete to true 
      self.actioncomplete = data['actc']
      #if the position is less than or equal to 10, this means it is an action tile 
      if self.position <=10:
          #set the action value to be the tiles descrp 
          self.action = tilesdescrp[self.position]
          #now displaying the finished state image
          tiles[0][self.position] = tiles[2][self.position]
      #if the position isn't less than 10 then it is a money tile 
      else:
          #need to access the value in the money array, which would be eleven less than the position value due
          #to length of array
          self.action = moneydescrp[self.position-11]
          #finished state image
          money[0][self.position-11] = money[2][self.position-11]

# ------ CHOOSE A PLAYER TO ATTACK ------
# This subroutine triggers the code which allows the user to
# choose who they want to attack with their current tile 
    def Network_choose(self,data):
      #receiving the data from the client
      #the player who gets to choose
      self.playernot = data['not']
      #receives the action that needs to be performed
      self.action = data['square']
      self.shields = data['shields']
      self.mirrors = data['mirrors']
      self.orders = data['actorder']
      #calls the buttons and displays the button
      #passing in new variables
      Button(self.playernot, self.action,self.points,self.shields,self.mirrors,self.orders)
      #pumping the connection and client
      connection.Pump()
      client.Pump()

# ------ WILD CARD ------
# This subroutine triggers the wild card button interface and allows
# the user to choose which action they want to perform
    def Network_wild(self,data):
      #the player that has to choose the action to play
      self.playernot = data['choose']
      #the action = should always be wild in this subroutine 
      self.action = data['square']
      #calling the button interface for choosing the action
      Button_Wild()

# ------ SUMMARY SCREEN ------
# This subroutine tells the client what actions have been performed
# against them in the current round, it will also tell them if their
# actions have been shielded/mirrored. If no actions have been performed
# against them, they will see their grid.
    def Network_summary(self,data):
      #receiving the array with all the summary details
      #summary of the array
      self.summary = data['array']
      #filling the screen in
      self.screen.fill((255,255,255))
      #setting found to False
      found = False
      #looping round how ever many actions have been performed 
      for i in range(len(self.summary[0])):
          #if you have been attacked
          if self.summary[1][i] == (self.num):
              #set found to equal true 
              found = True
              #blit a summary screen
              #evaluating them seperately to get the correct grammar
              #if the player has been given a present
              if self.summary[0][i] == ('present'):
                self.screen.blit(self.font.render("Player "+ str(self.summary[2][i])+ "gave you a present",True,(0,0,0)),(10,self.place))
              #if someone used a magnifying glass against the player
              elif self.summary[0][i] == ('magglass'):
                self.screen.blit(self.font.render("Player "+ str(self.summary[2][i])+ " saw your score",True,(0,0,0)),(10,self.place))
              #if someone has swapped scores with the player
              elif self.summary[0][i] == ('swap'):
                self.screen.blit(self.font.render("Player "+ str(self.summary[2][i])+ " swapped scores with you",True,(0,0,0)),(10,self.place))
              #all other action
              else:
                self.screen.blit(self.font.render("Player "+ str(self.summary[2][i])+ " used the "+ str(self.summary[0][i]) + " on you",True,(0,0,0)),(10,self.place))
              #increment by fifthteen in case have to diplay another message 
              self.place = self.place + 15
              #if the player has a mirror
              if self.summary[4][i] == True:
                  #blit a mirroring message to the screen
                  self.screen.blit(self.font.render("The action was mirrored",True,(0,0,0)),(10,self.place))
              #if the player has a shield
              elif self.summary[3][i] == True:
                  #blit a shielding message to the screen 
                  self.screen.blit(self.font.render("The action was shielded",True,(0,0,0)),(10,self.place))
      #checking for shield use against client's actions           
      for i in range(len(self.summary[0])):
          #if the client performed the action
          if self.summary[2][i] == (self.num):
              #if the person being attacked used the shield
              if self.summary[3][i] == True:
                  #blit a shielding message
                  self.screen.blit(self.font.render("Player "+ str(self.summary[1][i]) +" used the shield against your action", True, (0,0,0)), (10,self.place))
                  #increment the position of the text by 15
                  self.place = self.place + 15
              #if the person being attacked used the mirror
              elif self.summary[4][i] == True:
                  #blit a mirroring message
                  self.screen.blit(self.font.render("Player "+ str(self.summary[1][i]) +" used the mirror against your action", True, (0,0,0)), (10,self.place))
                  #increment position of the text by 15
                  self.place = self.place + 15

      # money (so you don't just see a blank screen)
      if found == False:
          #show them the grid 
          game2(arrayofcoords,tiles,money,True,True, False,self.points[self.num-1],self.rounds)
          
      #flip the screen
      pygame.display.flip()
      #short delay
      pygame.time.wait(5000)
      #continue to get event updates
      pygame.event.pump() 
      #setting it back to 10 so text goes to top of the screen in the next round
      self.place = 10
      #setting the flag back to true 
      self.summaryflag = True

# ------ BANK ADDED TO FINAL SCORE ------
# This subroutine takes the bank scores from the server
# and adds them to the client's current scores allowing
# the computer to assess who has won the game 
    def Network_bank(self,data):
        #receiving the bank array into the client
        self.banks = data['scores']
        for i in range(3):
            #adding the bank to the score
            #setting the total 
            self.points[i] = self.points[i] + self.banks[i]
        #setting the bankflag to True again
        self.bankflag = True 
          
      
# ------ MAIN CLIENT LOOP ------
# This is the loop that the client goes round throughout the game and is called
# when a new connection has been made

    # main client loop
    def Loop(self):
        #setting up the font
        self.font =  pygame.font.Font(None,30)
        #starting a loop that will go round until the end of the game
        test = True
        while test:
            #Pump the connection
            connection.Pump()
            #pumping the client
            client.Pump()
            #the subroutine that will display the intro screen
            game_start()
            #self.ready is initially false
            if self.ready == False:
                #send the server the player number of the client
                connection.Send({"action": "playready", "playr": self.num})
            #updating the flag
            self.ready = True 
            # while there are less than 3 players, loop
            while self.rplay < 3:
                #pumping the connection and the client
                connection.Pump()
                client.Pump()
                #pump pygame.event
                pygame.event.pump()
                #grid display
                game2(arrayofcoords,tiles,money,True,False)
                # pump to check for changes
                connection.Pump()
                client.Pump()
                #needed 
                pygame.event.pump()
            # once all players are ready, break out of while and send info to server
            self.allready = True
            # game beginning screen
            self.screen.fill((255,0,0))
            #quick loading screen
            self.screen.blit(self.font.render("Game Beginning", True, (0,0,0)),(10,10))
            #flipping the screen 
            pygame.display.flip()
            #short delay
            pygame.time.wait(2000)
            #sending to the server that the client is ready  
            connection.Send({'action':'ready'})
            #Looping round for the number of the tiles in the game
            for i in range(49):
              #while the actions are still being performed 
              while self.actioncomplete == False:
                  #getting events from the queue
                  pygame.event.get()
                  #grid display
                  game2(arrayofcoords,tiles,money,True,True,False,self.points[self.num-1],self.rounds)
                  #flipping the display
                  pygame.display.flip()
                  #pumping the connection, client and getting the pygame events 
                  connection.Pump()
                  client.Pump()
                  pygame.event.get()
              #next round
              self.rounds = self.rounds + 1 
              # change the screen back to white
              self.screen.fill((255,255,255))
              #updating display
              pygame.display.flip()
              #pumping the connection and the client
              connection.Pump()
              client.Pump()
              #while the summary screen has not been displayed yet
              while self.summaryflag == False:
                  #Pump connections and client and get events from the queue
                  pygame.event.get()
                  connection.Pump()
                  client.Pump()
              #send to the server that this client has finished the round
              connection.Send({'action':'loopy'})
              #back to initial value
              self.actioncomplete = False
            #while waiting for the bank scores to be added
            while self.bankflag == False:
                #Pump connection and client and get events from the queue
                pygame.event.get()
                connection.Pump()
                client.Pump()

            #initial value so can go into the loop 
            keypressed = False
            #while a key hasn't been pressed
            while keypressed == False:
              #fill the screen in purple
              self.screen.fill((123,123,255))
              #blit messages to the screen
              self.screen.blit(self.font.render("End of the game..",True,(0,0,0)),(10,10))
              self.screen.blit(self.font.render("Pirate "+str(self.num)+ ", your final total was: "+ str(self.points[self.num-1]),True,(0,0,0)),(10,50))
              #Find the winner
              winner=int(self.points.index(max(self.points)))
              #If the client is the winner 
              if winner==self.num-1:
                #trigger the mainwinner subroutine
                if __name__ == '__main__': mainwinner()
              #otherwise if the client hasn't won 
              else:
                #tell the client who did win and their score
                self.screen.blit(self.font.render("Pirate "+str(winner+1) +" won the game with "+str(self.points[winner])+" points",True,(0,0,0)),(10,70))
              #blit a message on how to exit the game
              self.screen.blit(self.font.render("Press any key to exit",True,(0,0,0)),(10,100))
              #flip the display
              pygame.display.flip()
              #get the current event
              event = pygame.event.poll()
              #if a key has been pressed
              if event.type == KEYDOWN:
                #drop out of the loop 
                keypressed = True
                #quit the game
                quit() 
            #dropping out of the loop 
            test = False  
        

# ------ MAKING A CONNECTION ------ 
# open client, using localhost
# The following lines of code allow the user to enter the IP address of the server
# that they are connecting to and then connect to the server and start the game
# by going into the Loop

#Messages to inform the users what to enter
print ('Enter the server ip address')
print ('Empty for localhost')
# ask the server ip address
server = input('server ip: ')
# if server is empty
if server == (''):
	server = ('localhost')

# initialize the listener
client = MyNetworkListener(server, 31500)
# start the mainloop
client.Loop()
