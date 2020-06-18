# ------ CLIENT ------

import PodSixNet, time, pygame, pygame.font, pygame.event, pygame.draw, string, random 
from pygame.locals import *
from pygame import * 
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from random import randint


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
size = [1000,800]
#setting up variables for input subroutine 
positionx = 0
positiony = 0
######################
gameDisplay = pygame.display.set_mode((300, 300))

#Array storing description of all the tiles 
descrp = ['Rob Someones Points',
          'Kill Someone, sending their score to zero',
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
grid = pygame.image.load('square.png')
logo = pygame.image.load('logo.png')
twohundred = pygame.image.load('200.png')
thousand = pygame.image.load('1000.png')
threethousand = pygame.image.load('3000.png')
fivethousand = pygame.image.load('5000.png')
bank = pygame.image.load('bank.png')
bomb = pygame.image.load('bomb.png')
choosenextsquare = pygame.image.load('choosenextsquare.png')
double = pygame.image.load('doubke.png')
magglass = pygame.image.load('magnifinghglassreal.png')
present = pygame.image.load('present.png')
rob = pygame.image.load('rob.png')
shield = pygame.image.load('shield.png')
swapscores = pygame.image.load('swapscores.png')
kill = pygame.image.load('kill.png')

#Setting up an array of all the images
tiles = [rob,kill]
tilesdescrp = ['rob','kill']

#Setting up an array of all the money images
money = []
money.append(twohundred)
money.append(thousand)
moneydescrp = ['200','1000']

arrayofcoords = [[],[]]


# ------ TECHNICAL ------

#Technical Stuff
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

# ------ VALIDATION ------
def LinearSearch(searchkey,arrayofcoord):
  position = 0
  found = False 
  while position < len(arrayofcoord) and found !=True:
    if arrayofcoord[position] == searchkey:
        found = True
  if found == True:
    return position

  
#Input Validation
#Checks the number is between 1 and 8 to fit on the grid 
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
      #Got to have a white background 
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
  return coord   
        
#Validation of the inputs
#Compare the two things on the X and Y array to all the other twos
#Need to make sure that they are not entering the same numbers
#Cannot have two pictures in the same square 
#NEED TO COME BACK AND CHANGE THIS ONCE MORE PROGRESS, NOT VERY EFFECIENT


def inputval2(arrayofcoords,xcoord,ycoord,valid):
##  print("valid value is..")
##  print(valid)
  alreadyhere = False
  for j in range(len(arrayofcoords[0])):
##    print("arrayx value")
##    print(arrayofcoords[0][j])
##    print("x value")
##    print(xcoord)
##    print("arrayy value")
##    print(arrayofcoords[1][j])
##    print("y value")
##    print(ycoord)
        
    if xcoord == arrayofcoords[0][j] and ycoord == arrayofcoords[1][j]:
      alreadyhere = True
##      print("ALreadyhere")
      break
      
  if alreadyhere == False:
    valid = True
##    print("valid after loop")
##    print(valid)
  return valid 
      

# ----- INPUT ------ 
  

#Setting up the screen for asking co-ordinate    
def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
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
  
#Actually displaying the window asking for input 
def ask(screen, question):
  "ask(screen, question) -> answer"
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
    #returning the values so that they can be used in the next subroutine 
  return "".join(current_string[0:1])

#Describing the tile to the player before asked for input 
def firstdisplay(tiles,descrp,i):
  #Setting the size of the screen
  screen = pygame.display.set_mode((600,600))
  #Getting the current tile in a loop and saving it to a variable to blit 
  currenttile = tiles[i]
  #Blitting the image on the screen at 100,100 
  screen.blit(currenttile,(300,300))
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
    #These lines are put in so I can check that the program is responding correctly 
##    print(xcoord)
##    print(ycoord)
##    print(i)
    if i != 0: 
      valid = False
      while valid == False:
        valid = inputval2(arrayofcoords,xcoord,ycoord,valid)
##        print("after inputval2")
##        print(valid)
        if valid == False:
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
          #print("new coords in while loop")
##          print(xcoord)
##          print(ycoord)
          
      
    #Append to the 2D array, once it is through validation  
    arrayofcoords[0].append(xcoord)
    arrayofcoords[1].append(ycoord)

  blank = []
  for i in range(2):
    blank.append("")
    
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
    #These lines are put in so I can check that the program is responding correctly 
##    print(xcoordm)
##    print(ycoordm)
##    print(i)
    valid = False
    while valid == False:
      valid = inputval2(arrayofcoords,xcoordm,ycoordm,valid)
      print("after inputval2")
      print(valid)
      if valid == False:
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
        #These lines are put in so I can check that the program is responding correctly
        #print("new coords in while loop")
##        print(xcoordm)
##        print(ycoordm)
##          
      
    #Append to the 2D array, once it is through validation  
    arrayofcoords[0].append(xcoordm)
    arrayofcoords[1].append(ycoordm)

def game(arrayofcoords,tiles):
    print("THE PIRATE GAME ".center(60),"\n")

    print(arrayofcoords)

    size =[500,500]
    white = [255,255,255]

    screen = pygame.display.set_mode(size)

    screen.fill(white)
    pygame.display.flip()

    for i in range(2):
##       print(i)
       screen.blit(tiles[i], ((arrayofcoords[0][i]*100),(arrayofcoords[1][i]*100)))
       pygame.display.flip()

    for i in range(2):
##       print(i)
       screen.blit(money[i], ((arrayofcoords[0][i+2]*100),(arrayofcoords[1][i+2]*100)))
       pygame.display.flip()

    pygame.time.wait(2000)
    
def randomchoice(notplayer,action):
   print("The action this is choosing for is", action)
   if notplayer == 3:
      player1 = (1)
      player2 = (2)
   elif notplayer == 2:
      player1 = (1)
      player2 = (3)
   elif notplayer == 1:
      player1 = (2)
      player2 = (3)
   number = (randint(0,9))
   if number < 5:
      chosen = player1
   elif number >=5:
      chosen = player2

   print("The player chosen to be attacked is", chosen)

   return chosen 
  
###########################################

##class Button_Example:
##    def __init__(self):
##        self.main()
##    
##    #Create a display
##    def display(self):
##        self.screen = pygame.display.set_mode((650,370),0,32)
##        pygame.display.set_caption("Buttons.py - example")
##
##    #Update the display and show the button
##    def update_display(self):
##        #setting up the player1
##      #############################
##      #if :
##      #then
##        player1 = 0
##        #setting up the player2
##        player2 = 0 
##        self.screen.fill((30,144,255))
##        #need to change the x and y co-ordinates 
##        #Parameters:               surface,      color,       x,   y,   length, height, width,    text, text_color
##                                                                                                    #player 1 
##        self.Button1.create_button(self.screen, (107,142,35), 225, 135, 200,    100,    0,        player1, (255,255,255))
##                                                                                                    #player 2 
##        self.Button2.create_button(self.screen, (107,142,35), 225, 250, 200,    100,    0,        player2, (255,255,255))
##        pygame.display.flip()
##
##
##    #Run the loop
##    def main(self):
##        self.Button1 = Buttons.Button()
##        self.Button2 = Buttons.Button()
##        self.display()
##        while True:
##            self.update_display()
##            for event in pygame.event.get():
##                if event.type == pygame.QUIT:
##                    pygame.quit()
##                elif event.type == MOUSEBUTTONDOWN:
##                    if self.Button1.pressed(pygame.mouse.get_pos()):
##                        print ("player 1 ")
##                        #trigger the action
##                    elif self.Button2.pressed(pygame.mouse.get_pos()):
##                        print ("player 2 ")
##                        #trigger the action passing different parameters 
##
### need to change this because already got this in my game 
##if __name__ == '__main__':
##    obj = Button_Example()

##########################################  
     

  
class MyNetworkListener(ConnectionListener):

    def __init__(self, host, port):
        # connect to the server
        self.Connect((host, port))
        # open a pygame window
        self.screen = pygame.display.set_mode((300,300))
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
        self.current = [0,0,0]
        # added extra dimension to pass counter
        self.currentsquare = [0,0,0]
        self.action = None
        self.points = [0,0,0]
        ########
        self.playernot = 0
        self.action = None 

        ##############
        self.actioncomplete = False
        self.playerc = 0 
        self.playernot1 = None 
        


    def Network(self, data):
        # print network data to client console
        print(data)

    def Network_players(self,data):
        self.totalplayers  = data['playerno']
        print("updating total players to " +str(self.totalplayers))
        
    # not needed below
    def Network_players2(self,data):
        self.totalplayers2 = data['']

    def Network_number(self,data):
        self.num = data['num']
        # print out player number
        print("I am player number " + str(self.num))
        # set window title with player number
        pygame.display.set_caption("player " + str(self.num))

    # this collects info on who pressed the key and updates the display
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
        print("Number of players ready is " + str(self.rplay))

    def Network_changesquare(self,data):
        self.currentsquare[0] = data['x']
        self.currentsquare[1] = data['y']
        ########## added to capture counter
        self.currentsquare[2] = data['counter']
        print("Received the updated square")
        print(self.currentsquare)
        xcoord = self.currentsquare[0]
        print("X co-ordinate")
        print(xcoord)
        ycoord = self.currentsquare[1]
        print("Y co-ordinate")
        print(ycoord)
        
        ############################
        #determining position of the square in arrayofcoords
        for i in range(len(arrayofcoords[0])):
          for j in range(len(arrayofcoords[0])):
            if xcoord == arrayofcoords[0][j] and ycoord == arrayofcoords[1][j]:
              position = j
              break
        print("Position of the co-ordinate in array")
        print(position)
        #determine what square the user has
        if position <=1:
          self.action = tilesdescrp[position]
          ###################
          print("Client action: ", self.action)
        else:
          self.action = moneydescrp[position-2]
          ##############
          print("Client action: ", self.action)
        #print(self.action)
          #send the action back
        #self.actions[self.playnum-1] = action
        #update self.actions
        ####### send a different action through
        #connection.Send({"action": "playready", "playr": self.num})
        #connection.Send({'action': 'presskey', 'pressplay': self.num})
        print("bEFORE SEND")
        connection.Send({'action':'actiontodo','actionsarray':self.action, 'number':self.num})
        connection.Pump()
        client.Pump()
        print("AftER SEnd") 
        ###########################


    def Network_actionupdate(self, data):
        self.actioncomplete = True
        
    def Network_current(self,data):
        self.points[0] = data[0]
        self.points[1] = data[1]
        self.points[2] = data[2]
        print(self.points)

    def Network_complete(self, data):
      self.actioncomplete = data['actc']
      print(self.actioncomplete)
      

    ###################################### 13.1

    def Network_choose(self,data):
      self.playernot = data['not']
      self.action = data['square']
      print(self.action) 
      print(self.playernot)
      #UPDATE THE SUBROUTINE (DONE)
      self.playerc = randomchoice(self.playernot,self.action)
      print("Player chosen")
      print(self.playerc)
      print("Player sent the action")
      print(self.playernot)
      # send the playerc and playernot
      #has to be self.player ??? #won't recognize self#
      # UPDATE THE SERVER WITH NEW DATA 
      connection.Send({'action':'chosen','playera':self.playerc, 'playern':self.playernot,'action':self.action})
      
      #update flag 
        #could return it and then pass it here??? 


      ####################################

##    def Network_playerno2(self,data):
##        self.rplay2 = data['play2']
##        print("Numbers of players ready is" + str(self.rplay2))
##
      ###########################
        
# ------ MAIN ------


    # main client loop
    def Loop(self):
        # set infinite loop
        while True:
            # update all
            connection.Pump()
            client.Pump()
            # need to send connection
            if __name__ == '__main__':
                main(tiles,descrp,gridpositions,positionx,positiony,size)
            game(arrayofcoords,tiles)
            # after first loop, send information that this player is ready
            if self.ready == False:
                connection.Send({"action": "playready", "playr": self.num})
            self.ready = True 
            # while there are less than 3 players, loop
            while self.rplay < 3:
                self.screen.fill((0,0,0))
                self.screen.blit(self.font.render("Not all players are ready, please wait...",True,(255,255,255)), (10,10))
                pygame.display.flip()
                # pump to check for changes
                connection.Pump()
                client.Pump()
                # keep window alive
                ###############
                pygame.event.pump()
            # once all players are ready, break out of while and send info to server
            self.allready = True
            connection.Send({'action':'ready'})
            ######## tests that we got out of the loop
            #### new while
            while self.actioncomplete == False:
                self.screen.fill((255,255,255))
                pygame.display.flip()
                connection.Pump()
                client.Pump()
            #print("Number of ready players = ", self.rplay)
            ####used to be while 
            print("Action complete")
            pygame.display.flip()
            connection.Pump()
            client.Pump()
            print("Current totals after action", self.points)
            ##############################
            #wait???
            self.screen.blit(self.font.render(str(self.points[self.num-1]),True,(0,0,0)),(10,10))
            pygame.display.flip() 
            pygame.time.wait(1000000)
            ################# put send here and reset action to None after

                
            ##screen blit
            self.screen.blit(self.font.render(str(self.points[self.num-1]),True,(0,0,0)),(10,10))
            pygame.display.flip()
            pygame.time.wait(1000000)
              
###########################################
# ADD IN MR SHEARERS CODE 
# open client, using localhost
client = MyNetworkListener('localhost', 1337)
client.Loop()
