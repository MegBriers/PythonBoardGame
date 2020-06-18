# ------ CLIENT ------
# 2018-01-21
#Current client working code
#This is the code that is running when a player connects to the server
# -*- coding: cp1252 -*-


#THIS PRINTS THE FINAL SCORE

#WORKING

# does not have the problem of the magnifying glass/shield solved yet 

#Importing the necessary libraries
#PodSixNet - lightweight multiplayer networking library used for my client and server
#Time - provides various time related functions within my code 
#PyGame - open source library for multimedia applications like a game(!)
#PyGame Font - allows fonts to be used throughtout and text to be rendered to the screen 
#PyGame event - handles all event messaging through an event queue 
#PyGame draw - allows several simple shapes to be drawn to the screen 
#String - library which contains methods to manipulate strings
#Random - This module implements pseudo-random number generators for various distributions
#Buttons -
#Os - This module provides a portable way of using operating system dependent functionality
import PodSixNet, time, pygame, pygame.font, pygame.event, pygame.draw, string, random, Buttons, os, sys
from pygame.locals import *
from pygame import * 
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from random import randint

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
os.chdir(dir_path)

# CHANGE GLOBAL VARIABLES

# initialise pygame
pygame.init()
pygame.font.init()
# this is the client interface
#screen colours of various windows
white = [255,255,255]
black = [0,0,0]
#setting up an array with all the grid co-ordinates 
gridpositions = [[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
#setting up the size of the screen 
size = [500,500]
#setting up variables for input subroutine 
positionx = 0
positiony = 0

#Setting the size of the window that the clients will see
gameDisplay = pygame.display.set_mode((500, 500))

#Array storing description of all the tiles 
descrp = [ 'Kill',
           'Shield',
          'Give someone 1000 points',
          'Give someone 1000 points',
          'Swap scores with another player',
          'Choose the next square',
          'Block the bad',
          'See the score of another player',
          'Your score goes back to zero',
          'Double your score',
          'Bank your score, makes it protected'
          ]

#Loading in the images of the tiles
#normal states
grid = pygame.image.load('square.png')
logo = pygame.image.load('logo.png')
twohundred = pygame.image.load('200.png')
thousand = pygame.image.load('1000.png')
threethousand = pygame.image.load('3000.png')
fivethousand = pygame.image.load('5000.png')
bank = pygame.image.load('bank.png')
bomb = pygame.image.load('bomb.png')
choosenextsquare = pygame.image.load('choosenextsquare.png')
double = pygame.image.load('double.png')
magglass = pygame.image.load('magnifinghglassreal.png')
present = pygame.image.load('present.png')
rob = pygame.image.load('rob.png')
shield = pygame.image.load('shield.png')
swap = pygame.image.load('swapscores.png')
kill = pygame.image.load('kill.png')
mirror = pygame.image.load('mirror.png')
wild = pygame.image.load('wildcard.png')
#instructions
instruct = pygame.image.load('instructions.png')
logo = pygame.image.load('logo.png')
normallinev=pygame.image.load("normalline.png")
normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
#ACTIVE
twohundreda = pygame.image.load('200active.png')
thousanda = pygame.image.load('1000active.png')
threethousanda = pygame.image.load('3000active.png')
fivethousanda = pygame.image.load('5000active.png')
banka = pygame.image.load('bankactive.png')
bomba = pygame.image.load('bombactive.png')
choosenextsquarea = pygame.image.load('choosenextsquareactive.png')
doublea = pygame.image.load('doubleactive.png')
magglassa = pygame.image.load('magnifinghglassrealactive.png')
presenta = pygame.image.load('presentactive.png')
roba = pygame.image.load('robactive.png')
shielda = pygame.image.load('shieldactive.png')
swapa = pygame.image.load('swapscoresactive.png')
killa = pygame.image.load('killactive.png')
mirrora = pygame.image.load('mirroractive.png')
#wilda = pygame.image.load('wildcardactive.png')
#FINISHED
twohundredd = pygame.image.load('200done.png')
thousandd = pygame.image.load('1000done.png')
threethousandd = pygame.image.load('3000done.png')
fivethousandd = pygame.image.load('5000done.png')
bankd = pygame.image.load('bankdone.png')
bombd = pygame.image.load('bombdone.png')
choosenextsquared = pygame.image.load('choosenextsquaredone.png')
doubled = pygame.image.load('doubledone.png')
magglassd = pygame.image.load('magnifinghglassrealdone.png')
presentd = pygame.image.load('presentdone.png')
robd = pygame.image.load('robdone.png')
shieldd = pygame.image.load('shielddone.png')
swapd = pygame.image.load('swapscoresdone.png')
killd = pygame.image.load('killdone.png')
mirrord = pygame.image.load('mirrordone.png')
#wildd = pygame.image.load('wildcarddone.png')


#Setting up an array of all the images
tiles = [[kill,shield],[killa,shielda],[killd,shieldd]]
#tiles = [[kill,shield],[killa,shielda],[killd,shieldd]]
#Setting the short descriptions so the client can identify what square has been chosen
tilesdescrp = ['kill','shield']
#CHANGE TO SWAP

#Setting up an array of all the money images
money = [[],[],[]]
#Appending the money to the array
money[0].append(twohundred)
money[0].append(thousand)
money[1].append(twohundreda)
money[1].append(thousanda)
money[2].append(twohundredd)
money[2].append(thousandd)
#Setting the short (text)descriptions so the client can identify what square has been chosen
moneydescrp = ['200','1000']

#Setting up a 2D array to store where the clients choose to place the squares
arrayofcoords = [[],[]]

# ------ INTRO SCREEN CODE ------


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def game_start():
    #updated size of the display
    size =[500,500]
    #initalising some colours that can be used later
    white = [255,255,255]
    #again initalizing the sreen
    screen = pygame.display.set_mode(size)
    #filling it in white
    screen.fill(white)
    #updating the display
    fontobject = pygame.font.Font(None,30)
    screen.blit(logo,(0,50))
    screen.blit(fontobject.render("Press any key to continue" ,True,(0,0,0)), (150,300))
    pygame.display.flip()
    keypressed = False
    while keypressed == False:
      #pygame.event.get()
      event = pygame.event.poll()
      if event.type == KEYDOWN:
        keypressed = True
    # move on with the game
    main(tiles,descrp,gridpositions,positionx,positiony,size)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# ------ TECHNICAL ------

#Technical Stuff
#Not really sure what this does 
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

# ------ VALIDATION ------
def linearsearch(array,searchkey):
    #foundat = None 
    print("In linear search")
    pos = 0
    found = False 
    while pos < len(array) and found !=True:
        if array[pos] == searchkey:
            found = True
            foundat=pos
        pos = pos + 1
    print("Player is at position", foundat)
    return foundat

  
# ------ INPUT VALIDATION 1 ------
#Checks the number is between 1 and 8 to fit on the grid
#Required to ensure that the client doesn't enter grid co-ordinates that aren't avaliable
def inputvalidation(coord):
  #Turning into an integer in order to carry out comparisons 
  coord = int(coord)
  while coord == 0 or coord>8:
      #Setting the screen to the correct screen size
      screen = pygame.display.set_mode(size)
      #Setting up the clock in order to put in a delay later  
      clock = pygame.time.Clock()
      #Setting up the font 
      basicfont = pygame.font.SysFont(None, 25)
      #Setting up the text to be blitted to screen
      #Error message
      text = basicfont.render('Invalid Input, please enter a number between 1 and 10', True, (white), (black))
      textrect = text.get_rect()
      #Making sure the text is displayed in the middle of the screen
      textrect.centerx = screen.get_rect().centerx
      textrect.centery = screen.get_rect().centery
      #filling the screen in black
      screen.fill(black)
      #displaying the input validation mess age to the screen 
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
#Compare the two values in the X and Y variables to all the other duples in the arrays
#Need to make sure that they are not entering the same numbers
#Cannot have two pictures in the same square
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

def show(self,chosen,points):
  #updated size of the display
  #Keep this the same for display purposes?
  size =[500,500]
  #initalising some colours that can be used later
  white = [255,255,255]
  #again initalizing the sreen
  screen = pygame.display.set_mode(size)
  #filling it in white
  screen.fill(white)
  basicfont = pygame.font.SysFont(None, 24)
  text = basicfont.render(str(points[chosen-1]), True, (255, 0, 0), (255, 255, 255))
  screen.blit(text,(100,100))
  #updating the display
  pygame.display.flip()
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
    screen.blit(fontobject.render(message, 1, (white)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  #refreshing the display 
  pygame.display.flip()
  
#This subroutine actually displays the window asking for input 
def ask(screen, question):
  #Initialising the font for the input box
  pygame.font.init()
  #This will be an array to take in the current characters 
  current_string = []
  
  #Joining the current string to a blank space as required by python 3
  #calls the display box subroutine to ask the question 
  display_box(screen, question + ": " + "".join(current_string))
  #Technical Stuff
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      #If a backspace is entered, removes the last string from array 
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      #Putting in a break if there is a space bar 
      break
    elif inkey <= 127:
      #Appending the array with the character
      current_string.append(chr(inkey))
    #Joining the current string  
    testing = question + ": " + "".join(current_string)
    #calls the display box subroutine to ask the question 
    display_box(screen, testing)  
  #returning the values so that they can be used in the next subroutine, joined to a blank string space
  return "".join(current_string[0:1])

#This subroutine displays the image to the clients ready for there input
#Also displays the description of what the action does
def firstdisplay(tiles,descrp,i):
  #Setting the size of the screen
  #CHANGED THE SIZE OF THIS SCREEN 20.1 
  screen = pygame.display.set_mode((300,300))
  #Getting the current tile in a loop and saving it to a variable to blit 
  currenttile = tiles[0][i]
  #Blitting the image on the screen at 100,100 
  screen.blit(currenttile,(150,150))
  #Updating the display 
  pygame.display.flip()
  pygame.font.init() 
  myfont = pygame.font.Font(None,25)
  #Getting the description of the current tile and saving it to a variable to blit
  texttodisplay = descrp[i]
  #Rendering the text to screen 
  textsurface = myfont.render(texttodisplay, False, (white))
  #Blitting the screen with the text
  screen.blit(textsurface,(250,150))
  #Updating the display
  pygame.display.flip()
  #Delaying the next screen, so the user has time to read the description 
  pygame.time.delay(1000)

# ------ MAIN INPUT SUBROUTINE ------
#Calls many other subroutines to display the tiles, get the input
# then validate the inputs(twice) to ensure it is in range and not been entered before
def main(tiles,descrp,gridpositions,positionx,positiony,size):
  #Loop 10 times for the number of action tiles
  for i in range(2):
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
    #have this in because if it is the first time round, there wouldn't be any need to compare and validate
    if i != 0:
      #assuming the co-ordinate is not valid
      valid = False
      while valid == False:
        #calling the valid subroutine
        valid = inputval2(arrayofcoords,xcoord,ycoord,valid)
        if valid == False:
          #calls everything again and makes them enter co-ordinates again
          screen.fill((0,0,0))
          basicfont = pygame.font.SysFont(None, 24)
          text = basicfont.render('Co-ordinate was already entered, as seen on the grid', True, (255, 255, 255), (0, 0, 0))
          screen.blit(text,(20,25))
          pygame.display.flip()
          pygame.time.wait(2000)
          screen.fill((255,255,255))
          game2(arrayofcoords,tiles,money,False,False)
          text2 = basicfont.render('Please enter a co-ordinate not already chosen', True, (0, 0, 0), (255, 255, 255))
          screen.blit(text2,(20,25))
          pygame.display.flip()
          pygame.time.wait(2000)
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

    #CALL THE GRID DISPLAY
    game2(arrayofcoords,tiles,money,False,False)

  #this is required for passing an empty array into the first display subroutine
  #an array is required but there is no need for a description for money
  blank = []
  for i in range(2):
    blank.append("")
  #loops through the money  
  for i in range(2):
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
         basicfont = pygame.font.SysFont(None, 24)
         text = basicfont.render('Co-ordinate was already entered', True, (255, 255, 255), (0, 0, 0))
         screen.blit(text,(20,25))
         pygame.display.flip()
         pygame.time.wait(2000)
         screen.fill((255,255,255))
         game2(arrayofcoords,tiles,money,False,False)
         text2 = basicfont.render('Please enter a co-ordinate not already chosen', True, (0, 0, 0), (255, 255, 255))
         screen.blit(text2,(20,25))
         pygame.display.flip()
         pygame.time.wait(2000) 
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

# ----- START OF THE GAME ------
#this subroutine displays the grid to the player with all the co-ordinates they have entered
#it is called in the main client loop
def game2(arrayofcoords,tiles,money,finished,maingame, score = None, rounds = None):
    #updated size of the display
    #Keep this the same for display purposes?
    size =[600,600]
    #initalising some colours that can be used later
    white = [255,255,255]
    #again initalizing the sreen
    screen = pygame.display.set_mode(size)
    #filling it in white
    screen.fill(white)
    #adding title text
    basicfont = pygame.font.SysFont(None, 24)
    text = basicfont.render('The Pirate Game', True, (255, 0, 0), (255, 255, 255))
    screen.blit(text,(225,25))

    #displaying the action tiles
    for x in range(2):
        for y in range(3):
             screen.blit(normallineh, [(x+1)*64+5, (y+1)*64])
         
    for x in range(3):
        for y in range(2):
            screen.blit(normallinev, [(x+1)*64, (y+1)*64+5])

    # BLITTING THE TILES ONTO THE GRID
    # blits at the right positions 
    for i in range(len(arrayofcoords[0])):
        if i <= 1:
            screen.blit(tiles[0][i], [arrayofcoords[0][i]*64+12, arrayofcoords[1][i]*64+20])
        else:
            screen.blit(money[0][i-2], [arrayofcoords[0][i]*64+12, arrayofcoords[1][i]*64+20])


    fontobject = pygame.font.Font(None,30)
    #press any key to continue code
    if finished == False: 
        screen.blit(fontobject.render("Press any key to continue" ,True,(0,0,0)), (20,500))
        pygame.display.flip()
        keypressed = False
        while keypressed == False:
          #pygame.event.get()
          event = pygame.event.poll()
          if event.type == KEYDOWN:
            keypressed = True
    elif finished == True and maingame == False:
        screen.blit(fontobject.render("Waiting for other players" ,True,(0,0,0)), (20,500))
        pygame.display.flip()
        connection.Pump()
        client.Pump()
        #needed 
        pygame.event.pump()
    elif finished == True and maingame == True:
        connection.Pump()
        client.Pump()
        screen.blit(fontobject.render("Your current score:  " + str(score), True, (0,0,0)),(20,500))
        screen.blit(fontobject.render("Round:  " + str(rounds), True, (0,0,0)), (300,500))
        pygame.display.flip()
        #score
        #rounds
         ############### = ################ 

# ------ BUTTONS FOR NORMAL CODE ------

#This class will allow the players to choose who they want to attack with buttons
class Button_Example:
    # adding action to arguments to allow use for different actions
    #Initalizing the values of the classes
    def __init__(self, player, action,points,shields,mirrors,order):
        self.player1 = None
        self.player2 = None
        chosen = None
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
        self.screen.blit(self.fontobject.render("Who do you want to " + str(action)  ,True,(0,0,0)), (20,20))

        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.Button1.create_button(self.screen, (107,142,35), 225, 135, 200,    100,    0,        "Player" + str(self.player1), (255,255,255))
        self.Button2.create_button(self.screen, (107,142,35), 225, 250, 200,    100,    0,        "Player" + str(self.player2), (255,255,255))
        #updating the display
        pygame.display.flip()


    #Run the loop
    def mainbutton(self, player, action, points, shields, mirrors, order):
        #creating the buttons
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
                    pygame.quit()
                #when the button is pressed
                elif event.type == MOUSEBUTTONDOWN:
                    #if it was button 1
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                      #setting up a variable with the chosen player
                      ######################################
                      ####################################

                      # MAY NEED TO MAKE THIS -1 
                      ###################################
                        chosen = self.player1
                        if action == ('magglass'):
                          #VALIDATION
                          pos = linearsearch(order,chosen)
                          if self.shield[pos] == False and self.shield[pos] == False: 
                          #call a definition
                            show(self,chosen,points)
                          elif self.shield[pos] == True:
                            #tell the client its been blocked
                            print("****************")
                            print("Blocked the shield")
                            print("****************")
                          elif self.mirror[pos] == True:
                            #CHECK THIS WORKS
                            ##############################
                            ##############################
                            print("*******************")
                            print("Mirrored the shield")
                            show(self,player,points)
                            ##############################
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
                          # VALIDATION
                          #VALIDATION
                          pos = linearsearch(order,chosen)
                          if self.shield[pos] == False and self.shield[pos] == False: 
                          #call a definition
                            show(self,chosen,points)
                          elif self.shield[pos] == True:
                            #tell the client its been blocked
                            print("****************")
                            print("Blocked the shield")
                            print("****************")
                          elif self.mirror[pos] == True:
                            show(self,player,points)
                          #call a definition
                        #sending a network event as above
                        connection.Send({'action':'chosen','playera':chosen, 'playern':player,'tobedone':action})
                        connection.Pump()
                        client.Pump()
                        #breaking out of the loop
                        goround = False
        #testing purposes 
        print("The value of chosen is", chosen)

# ------ BUTTONS FOR WILD CARDS ------

#This class will allow the players to choose who they want to attack with buttons
class Button_Wild():
    # adding action to arguments to allow use for different actions
    #Initalizing the values of the classes
    def __init__(self):
        
        pygame.font.init()
        #calling the main button definition within the class
        self.mainbutton()
    
    #Create a display
    def display(self):
        #setting up the display 
        self.screen = pygame.display.set_mode((400,400),0,32)

    #Update the display and show the button
    def update_display(self):
        #filling in the screen white
        self.screen.fill((255,255,255))
        #setting up font because it is in the class so not set up 
        self.fontobject = pygame.font.Font(None,10)
        #blitting a message to tell the client what they are choosing for
        self.screen.blit(self.fontobject.render("Wild Card!"  ,True,(0,0,0)), (20,20))

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
                if event.type == pygame.QUIT:
                    pygame.quit()
                #when the button is pressed
                elif event.type == MOUSEBUTTONDOWN:
                    #if it was button 1
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        print("rob")
                        connection.Send({'action':'wildchosen','tobedone':'rob'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        print("kill")
                        connection.Send({'action':'wildchosen','tobedone':'kill'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        print("swap")
                        connection.Send({'action':'wildchosen','tobedone':'swap'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button4.pressed(pygame.mouse.get_pos()):
                        print("present")
                        connection.Send({'action':'wildchosen','tobedone':'present'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button5.pressed(pygame.mouse.get_pos()):
                        print("magglass")
                        connection.Send({'action':'wildchosen','tobedone':'magglass'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button6.pressed(pygame.mouse.get_pos()):
                        print("bank")
                        connection.Send({'action':'wildchosen','tobedone':'bank'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button7.pressed(pygame.mouse.get_pos()):
                        print("bomb")
                        connection.Send({'action':'wildchosen','tobedone':'bomb'})
                        connection.Pump()
                        client.Pump()
                        #stops the loop going round 
                        goround = False
                    elif self.Button8.pressed(pygame.mouse.get_pos()):
                        print("double")
                        connection.Send({'action':'wildchosen','tobedone':'double'})
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
        self.screen = pygame.display.set_mode((500,500))
        # set font
        self.font = pygame.font.SysFont('sans, freesans,courier,arial',10,True)
        # inital value of total players
        self.totalplayers = None
        # player number
        self.num = None
        # this is who pressed a key
        self.pressedkey = None
        pygame.display.set_caption("Player " + str(self.num))
        # the number of ready players
        self.rplay = 0
        # and that I am ready
        self.ready = False
        # are all players ready?
        self.allready = False
        #players current scores
        #might not be being used 
        self.current = [0,0,0]
        # added extra dimension to pass counter
        self.currentsquare = [0,0,0]
        #players current action
        self.action = None
        #player current points
        self.points = [789,235,385]
        #player who has to chose a person to attack
        self.playernot = 0
        #needed?
        self.action = None
        

        ##############
        #whether all the actions have been completed
        self.actioncomplete = False
        #the player chosen
        self.playerc = 0
        #the player who gets to make the choice
        self.playernot1 = None

        #mag glass 
        self.shields = []
        self.mirrors = []
        self.orders = []

        self.position = 0

        self.summary = [[],[],[],[],[]]
        self.place = 10
        self.summaryflag = False

        self.rounds = 1

        self.banks = []

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
        #testing purposes
        print("updating total players to " +str(self.totalplayers))

    #Assigning a player number to the client 
    def Network_number(self,data):
        #getting data from the server
        self.num = data['num']
        # print out player number
        print("I am player number " + str(self.num))
        # set window title with player number
        pygame.display.set_caption("player " + str(self.num))

    # this collects info on who pressed the key and updates the display
    # may not be  needed 
    def Network_keyplay(self, data):
        self.pressedkey = data['pressno']
        print("Server says player " + str(self.pressedkey) + " pressed a key")
        self.screen.fill((0,0,0))
        self.screen.blit(self.font.render("Total players: " + str(self.totalplayers),True,(255,255,255)), (10,10))
        self.screen.blit(self.font.render("Player " + str(self.pressedkey) + " pressed a key",True,(255,255,255)), (10,50))
        pygame.display.flip()

    # receives information on how many players are ready from server 
    def Network_playrno(self, data):
        # updated to number in the array in the server 
        self.rplay = data['playno']
        #testing purposes
        print("Number of players ready is " + str(self.rplay))

    # receives information from the server and finds out what action tile is at that co-ordinate
    def Network_changesquare(self,data):
      #print for testing purposes
        print("CHANGING SQUARE")
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
        # update values
        connection.Pump()
        client.Pump()
        #if position is in the first two
        if self.position <=1:
          #set the action value to be the tiles descrp 
          self.action = tilesdescrp[self.position]
             ############## ACCESS TO TILES 
          tiles[0][self.position] = tiles[1][self.position]
          game2(arrayofcoords,tiles,money,True,True)
          #testing purposes
          print("Client action: ", self.action)
        else:
          self.action = moneydescrp[self.position-2]
          money[0][self.position-2] = money[1][self.position-2]
          #self.points is an array
          game2(arrayofcoords,tiles,money,True,True,self.points[self.num-1],self.rounds)
          #testing purposes
          print("Client action: ", self.action)
        
        #sending the action back to the server
          #is self.num 2 for player 2 or 1???
          # player 2 for player 2 
        connection.Send({'action':'actiontodo','actionsarray':self.action, 'number':self.num})
        #Pumping the server and the client to ensure they receive new data
        connection.Pump()
        client.Pump()

    #A subroutine to assign points to the right players in the client
    #allows me to display them later 
    def Network_current(self,data):
        #player 1s points comes through first in the network event 
        self.points[0] = data[0]
        #then player 2
        self.points[1] = data[1]
        #then player 3
        self.points[2] = data[2]
        #testing purposes
        print("Current points totals")
        print(self.points)
        
    #comes here after all the actions have been performed
    def Network_complete(self, data):
      #setting the self.actioncomplete to true 
      self.actioncomplete = data['actc']
      #testing purposes
      print(self.actioncomplete)
      if self.position <=1:
          #set the action value to be the tiles descrp 
          self.action = tilesdescrp[self.position]
             ############## ACCESS TO TILES 
          tiles[0][self.position] = tiles[2][self.position]
      else:
          #need to access the value in the money array, which would be two less than the position value due
          #to length of array
          self.action = moneydescrp[self.position-2]
          money[0][self.position-2] = money[2][self.position-2]
          #testing purposes
      print("All the actions have supposably been completed")
      
    #This subroutine triggers the clients to choose a player to attack
    def Network_choose(self,data):
      #testing purposes
      print("DATA HAS BEEN RECEIVED INTO THE CLIENT FOR ACTION")
      #receiving the data from the client
      #the player who gets to choose
      self.playernot = data['not']
      #receives the action that needs to be performed
      self.action = data['square']
      self.shields = data['shields']
      self.mirrors = data['mirrors']
      self.orders = data['actorder']
      #testing purposes
      print("Action being performed", self.action)
      print("Action being performed by:", self.playernot)
      #calls the buttons and displays the button
      #passing in new variables
      Button_Example(self.playernot, self.action,self.points,self.shields,self.mirrors,self.orders)
      #pumping the connection and client
      connection.Pump()
      client.Pump()

    def Network_wild(self,data):
      self.playernot = data['choose']
      self.action = data['square']
      Button_Wild()

# NEW

# ------ SUMMARY SCREEN ------

    def Network_summary(self,data):
      self.summary = data['array']
      self.screen.fill((255,255,255))
      for i in range(len(self.summary[0])):
          #may not work
          if self.summary[1][i] == (self.num):
              self.screen.blit(self.font.render("Player "+ str(self.summary[2][i])+ " used the "+ str(self.summary[0][i]) + " on you",True,(0,0,0)),(10,self.place))
              self.place = self.place + 10
              if self.summary[4][i] == True:
                  self.screen.blit(self.font.render("The action was mirrored",True,(0,0,0)),(10,self.place))
              elif self.summary[3][i] == True:
                  self.screen.blit(self.font.render("The action was shielded",True,(0,0,0)),(10,self.place))

      

      for i in range(len(self.summary[0])):
          if self.summary[2][i] == (self.num):
              if self.summary[3][i] == True:
                  self.screen.blit(self.font.render("Player "+ str(self.summary[1][i]) +" used the shield against your action", True, (0,0,0)), (10,self.place))
                  self.place = self.place + 10
              elif self.summary[4][i] == True:
                  self.screen.blit(self.font.render("Player "+ str(self.summary[1][i]) +" used the mirror against your action", True, (0,0,0)), (10,self.place))
                  self.place = self.place + 10
     

      pygame.display.flip()
      pygame.time.wait(5000)
      self.place = 10
      self.summaryflag = True

# ------ BANK ADDED TO FINAL SCORE ------

    def Network_bank(self,data):
        self.banks = data['scores']
        for i in range(3):
            #adding the bank to the score
            self.points[i] = self.points[i] + self.banks[i]
        self.bankflag = True 
          
      
# ------ MAIN ------

    # main client loop
    def Loop(self):
        # set infinite loop
        # set chosen player for choice actions to None
        test = True
        while test:
            # update all
            connection.Pump()
            #pumping the client and the connection 
            client.Pump()
            # need to send connection
            #game_intro()
            game_start()
            #triggers the game
            # after first loop, send information that this player is ready
            if self.ready == False:
                connection.Send({"action": "playready", "playr": self.num})
            self.ready = True 
            # while there are less than 3 players, loop
            while self.rplay < 3:
                connection.Pump()
                client.Pump()
                #needed 
                pygame.event.pump()
                #filling in the screen white
                #self.screen.fill((0,0,0))
                #telling the client that they still have other players to wait for
                game2(arrayofcoords,tiles,money,True,False)
                #pygame.display.flip()
                # pump to check for changes
                connection.Pump()
                client.Pump()
                #needed 
                pygame.event.pump()
            # once all players are ready, break out of while and send info to server
            self.allready = True
            # beginning game screen 
            #tells the server that this client is ready
            # 
            # game beginning screen
            self.screen.fill((255,0,0))
            self.screen.blit(self.font.render("Game Beginning", True, (0,0,0)),(10,10))
            pygame.display.flip()
            pygame.time.wait(2000)
            # 
            connection.Send({'action':'ready'})
            #Looping round for the number of the tiles in the game
            for i in range(4):
              while self.actioncomplete == False:
                  pygame.event.get()
                  game2(arrayofcoords,tiles,money,True,True,self.points[self.num-1],self.rounds)
                  pygame.display.flip()
                  connection.Pump()
                  client.Pump()
                  pygame.event.get()
              self.rounds = self.rounds + 1 
              ####used to be while 
              print("Action complete")
              # change the screen back to white
              self.screen.fill((255,255,255))
              pygame.display.flip()
              connection.Pump()
              client.Pump()
              print("Current totals after action", self.points)
              self.screen.blit(self.font.render(str(self.points[self.num-1]),True,(0,0,0)),(10,10))
              pygame.display.flip() 
              while self.summaryflag == False:
                  pygame.event.get()
                  connection.Pump()
                  client.Pump()
                  
              connection.Send({'action':'loopy'})
              print("Sent to the network I am ready")
              # SEND NETWORK EVENT
              self.actioncomplete = False

            while self.bankflag == False:
                pygame.event.get()
                connection.Pump()
                client.Pump()

            
            keypressed = False
            while keypressed == False:
              self.screen.fill((123,123,255))
              self.screen.blit(self.font.render("End of the game..",True,(0,0,0)),(10,10))
              self.screen.blit(self.font.render("Player "+str(self.num)+ ", your final total was: "+ str(self.points[self.num-1]),True,(0,0,0)),(10,50))
              #winning screen
              winner=int(self.points.index(max(self.points)))
              
              if winner==self.num-1:
                self.screen.blit(self.font.render("YOU WON!!!!!!",True,(0,0,0)),(10,70))
              else:
                self.screen.blit(self.font.render("Player "+str(winner+1) +" won the game with "+str(self.points[winner])+" points",True,(0,0,0)),(10,70))
              
              self.screen.blit(self.font.render("Press any key to exit",True,(0,0,0)),(10,100))
              pygame.display.flip()
              event = pygame.event.poll()
              if event.type == KEYDOWN:
                keypressed = True

            test = False  
            ################# put send here and reset action to None after
        

# ------ CALLING THE GAME ------ 
# open client, using localhost
# NEED TO ADD IN CODE TO RUN ON THREE COMPUTERS
client = MyNetworkListener('localhost', 1337)
client.Loop()
