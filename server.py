# ------ SERVER ------
# 2018-02-28
# Megan Briers
# ADVANCED HIGHER COMPUTING PROJECT
# This is the server code

#Importing the necessary libraries
#PodSixNet - lightweight multiplayer networking library used for my client and server
#Time - provides various time related functions within my code
#Random - This module implements pseudo-random number generators for various distributions
#Os - This module provides a portable way of using operating system dependent functionality
import PodSixNet, time, random, os 
from random import random 
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

#setting dir_path to the directory path of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
#getting the current working directory
cwd = os.getcwd()
#changing the working directory of the file 
os.chdir(dir_path)

# Linear Search
def linearsearch(array,searchkey):
    #Setting pos to the first index in the array
    pos = 0
    #initial value of found 
    found = False
    #while it's not the end of the array and the searchkey hasn't been found
    while pos < len(array) and found !=True:
        #if the current place in the array is the searchkey
        if array[pos] == searchkey:
            #it has been found 
            found = True
            #the index where the searchkey is in the array
            foundat=pos
        #looping round each position in the array
        pos = pos + 1
    #returning the place the searchkey was found
    return foundat
    
#This subroutine sets up an 2D array in a pre-set order with all the co-ordinates
#It then randomly assigns a number between 0 and 1 to the 3rd column in the array
#The subroutine then sorts the array based on the value in the sort column
#It uses a bubble sort
#This subroutine ensures that the program has a random set of squares it runs through every game
def random_squares():
    #Initialising the 2d array
    setofcoordinates = [[],[],[]]
    #Starting a fixed loop 
    for x in range(7):
        for i in range(7):
            #Appending the numbers to the arrays
            setofcoordinates[0].append(x+1)
            setofcoordinates[1].append(i+1)
            #assigning a number between 0 and 1 to a variable called number
            number = random()
            #appends the variable number to the 3rd column in the array
            setofcoordinates[2].append(number)

    #Ordering the list
    #Loops round 49 times
    for x in range(49):
        #Loops 48 times, in order to avoid an indexing error as comparing i and i + 1
        for i in range(48):
            #Comparing the two random values
            if setofcoordinates[2][i] <= setofcoordinates[2][i+1]:
               #Looping round for values that need to be swapped
                for n in range(3):
                    #Swapping all the values, so co-ordinates stay together
                    setofcoordinates[n][i], setofcoordinates[n][i+1] = setofcoordinates[n][i+1],setofcoordinates[n][i]
    #returning the randomly ordered list of co-ordinates to run through
    return setofcoordinates

# ------ CLIENT CHANNEL ------
#Client channel represents a single connection of a client to the server
#This subroutine happens when client connects to server 
class ClientChannel(Channel):
    #Initializing values
    def __init__(self, *args, **kwargs):
        #Initializing the channel
        Channel.__init__(self, *args, **kwargs)
        
        #Id of player ready
        self.play = 0

        #Initial values (empty) for self.action and self.number
        self.action = None
        self.number = None 

    #When client does connection.Send(mydata), Network method is called    
    def Network(self, data):
        # prints all passed network data to console
        print(data)

    # when client says it is ready, sends which player is ready to here
    def Network_playready(self, data):
        #receiving data from the client
        self.play = data['playr']
        # appending the id of the player that's ready 
        self._server.playersready.append(self.play)
        #Sending to all the current number of playersready
        self._server.SendToAll({'action':'playrno', 'playno': len(self._server.playersready)})

    # when a client knows what action is has, sends which action and their player number to here
    def Network_actiontodo(self,data):
        #receiving the action
        self.action = data['actionsarray']
        #receiving the playersnumber 
        self.number = data['number']
        #appending the values to server arrays
        self._server.actions.append(self.action)
        self._server.actionsplayer.append(self.number)
        
    # helps server know when to progress with next round 
    def Network_ready(self,data):
        #boolean value 
        self._server.allready = True
        
    # when a client chooses which player to attack, sends all relevant data here
    def Network_chosen(self,data):
        #the player that will be attacked
        self._server.playerattack = data['playera']
        #the player that is attacking
        self._server.playerattacking = data['playern']
        #the action to be performed
        self._server.playeraction = data['tobedone']
        #If the action is rob
        if self._server.playeraction == ('rob'):
            #set the rob flag to True
            self._server.robflag = True
        #If the action is kill 
        elif self._server.playeraction == ('kill'):
            #set the kill flag to True
            self._server.killflag = True
        #If the action is present
        elif self._server.playeraction == ('present'):
            #set the present flag to True
            self._server.presentflag = True
        #If the action is swap
        elif self._server.playeraction == ('swap'):
            #set the swap flag to True
            self._server.swapflag = True
        #If the action is magnifying glass
        elif self._server.playeraction == ('magglass'):
            #set the mag.glass flag to True
            self._server.magflag = True
            
        #Appending the values onto the summary array which is used to
        #produce the summary screen in the client later
        #the action being performed
        self._server.sum[0].append(self._server.playeraction)
        #the player who is being attacked
        self._server.sum[1].append(self._server.playerattack)
        #the player who is attacking
        self._server.sum[2].append(self._server.playerattacking)
        #Boolean value to indicate whether the player being attacked has a shield
        self._server.sum[3].append(self._server.shield[self._server.playerattack-1])
        #Boolean value to indicate whether the player being attacked has a mirror
        self._server.sum[4].append(self._server.mirror[self._server.playerattack-1])

    # comes here when a client has finished a round
    def Network_loopy(self,data):
        #Appending to an array, server waits until the array has a length of 3
        self._server.loopagain.append('ready')

    # comes here when the client sends back which action they want to be performed
    # as part of their choice in wildcard
    def Network_wildchosen(self,data):
        #action to be performed
        self._server.wildaction = data['tobedone']
        #setting the wildflag to True 
        self._server.wildflag = True
        
# ------ KILL subroutine ------
# comes here when the client has a kill action
# definition - the attacker gets to choose someone and their current score will go to 0 
def kill(self,i):
    #the player with the kill action
    playerinaction = self.players[self.actionsplayer[i]-1]
    #sending them a network event on the client to get them to choose who they want to kill
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'kill','shields':[], 'mirrors':[],'actorder':[]})
    #wait until they send back who they want to kill
    while self.killflag == False:
        #pump the server to receive the information
        myserver.Pump()
    #find the position of the player to be attacked in the array storing the players
    pos = linearsearch(self.actionsplayer,self.playerattack)
    #if the person being attacked does not have a shield or a mirror
    if self.shield[pos] == False and self.mirror[pos] == False:
        #set the score to zero of the player being attacked
        self.currentscores[self.playerattack-1] = 0
        #send back all the current scores of the players
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pump the server
        myserver.Pump()
        #set the kill flag to False
        self.killflag = False
    #if the player being attacked has a shield
    elif self.shield[pos] == True:
        #send to all the current scores(do nothing basically)
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pumping the server
        myserver.Pump()
        #set the kill flag to False
        self.killflag = False
    #if the player being attacked has a mirror
    elif self.mirror[pos] == True:
        #swapping the variables 
        #person to be attacked
        self.newtobeattacked = self.playerattacking
        #person attacking
        self.newattacker = self.playerattack
        #performing the actions
        self.currentscores[self.newtobeattacked-1] = 0
        #sending the current scores to all the clients
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #setting that flag back to initial values
        self.killflag = False

    #again, just to make sure that is was set False 
    self.killflag = False 
        
# ------ ROB subroutine ------
# comes to this subroutine when the client has a rob action
# def - the client chooses a player to attack and they will rob the chosen players score
# the chosen players score goes back to zero 
def rob(self,i):
    #setting up the player who has the rob
    playerinaction = self.players[self.actionsplayer[i]-1]
    #triggering a network action on the client who has rob asking them to choose a player to rob
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'rob','shields':[], 'mirrors':[],'actorder':[]})
    #while waiting for the client to send back choice 
    while self.robflag == False:
        #pump the server 
        myserver.Pump()
    #find the position of the player being attacked in an array storing players
    pos = linearsearch(self.actionsplayer,self.playerattack)
    #if the player being attacked does not have a shield or a mirror
    if self.shield[pos] == False and self.mirror[pos] == False:
        #perform the rob
        self.currentscores[self.playerattacking-1] = self.currentscores[self.playerattacking-1] + self.currentscores[self.playerattack-1]
        self.currentscores[self.playerattack-1] = 0
        #send back the current scores
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pump the server 
        myserver.Pump()
        #set the rob flag to False
        self.robflag = False
    #else if the player being attacked does have a shield 
    elif self.shield[pos] == True:
        #send the current scores to all the players
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #setting all back to initial values
        self.robflag = False
    #else if the player being attacked does have a mirror
    elif self.mirror[pos] == True:
        #swapping the variables 
        #person to be attacked
        self.newtobeattacked = self.playerattacking
        #person attacking
        self.newattacker = self.playerattack
        #performing the actions
        self.currentscores[self.newattacker-1] = self.currentscores[self.newattacker-1] + self.currentscores[self.newtobeattacked-1]
        self.currentscores[self.newtobeattacked-1] = 0
        #send to all the current scores
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #setting that one back to initial values
        self.robflag = False
    #setting the rob flag back to false
    self.robflag = False
    
# ------ BANK subroutine ------
# adding the players current score to the bank array
# should be added on to total scores at the end 
def bank(self,i):
    #adding the score to the bank 
    self.bank[self.actionsplayer[i]-1] = self.bank[self.actionsplayer[i]-1] + self.currentscores[self.actionsplayer[i]-1]
    #setting the current score back to zero
    self.currentscores[self.actionsplayer[i]-1] = 0
    #sending the current scores back to the clients
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    #pump the server 
    myserver.Pump()


# ------ BOMB subroutine ------
# takes the current score of the player and sets it back to zero 
def bomb(self,i):
    # 'blowing up'
    self.currentscores[self.actionsplayer[i]-1] = 0
    # sending the current scores back to the client 
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    # pumping the server to ensure the data gets across 
    myserver.Pump()


# ------ DOUBLE subroutine ------
# doubling the score of the player who has the double action
def double(self,i):
    # multiplying the score by two 
    self.currentscores[self.actionsplayer[i]-1] = (self.currentscores[self.actionsplayer[i]-1]) * 2
    # sending the current scores back to the client
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    # pumping the server 
    myserver.Pump()

# ------ PRESENT subroutine ------
# this allows the player to gift another player 1000 points
# this 1000 points does not come out of the client's current score
def present(self,i):
    #setting up the player in action (player performing the action)
    playerinaction = self.players[self.actionsplayer[i]-1]
    #asking the player to make a choice
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'present','shields':[], 'mirrors':[],'actorder':[]})
    #waiting for the player to send back their choice 
    while self.presentflag == False:
        #pumping the server to ensure data gets through
        myserver.Pump()
    #Even though it says attack, the player in question is actually getting the present
    #gifting 1000 points
    self.currentscores[self.playerattack-1] = self.currentscores[self.playerattack-1] + 1000
    #sending the updated current scores back to the clients 
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    #pumping the server
    myserver.Pump()
    #setting the present flag back to it's inital value
    self.presentflag = False

# ------ SWAP subroutine ------
# this subroutine allows the player with the swap tile to
# choose a player to swap scores with
def swap(self,i):
    #setting up the player who has the swap
    playerinaction = self.players[self.actionsplayer[i]-1]
    #sending the action back to the server to choose from the other players 
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'swap','shields':[], 'mirrors':[],'actorder':[]})
    #waiting for the player to send back their choice
    while self.swapflag == False:
        #pump the server 
        myserver.Pump()
    # STEPS IN THE SWAP 
    #receiving the player chosen and the player attacking back from server
    #set a temporary variable
    #swap the scores
    #finding the position of the player to be attacked in the array of the players
    pos = linearsearch(self.actionsplayer,self.playerattack)
    #if the player being attacked does not have a shield or a mirror
    if self.shield[pos] == False and self.mirror[pos] == False:
        #set a temporary variable to store the points of the person attacking
        self.temp = self.currentscores[self.playerattacking-1]
        #player who is getting attacked
        #swap the scores
        self.currentscores[self.playerattacking-1] = self.currentscores[self.playerattack-1]
        self.currentscores[self.playerattack-1] = self.temp
        #sending the scores back to the client 
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pumping the server to make sure that they receive the data 
        myserver.Pump()
        #set the swap flag back to initial value 
        self.swapflag = False
    #if the player being attacked does have a shield, do nothing
    elif self.shield[pos] == True: 
        #sending the scores back to the client 
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pumping the server to make sure that they receive the data 
        myserver.Pump()
        self.swapflag = False 
    # if the player being attacked does have a mirror, do nothing too
    # no point swapping 
    elif self.mirror[pos] == True:
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        self.swapflag = False
    # just in case ! want to always make sure its back to false 
    self.swapflag = False 
        
# ------ MAGNIFYING GLASS ------
# lets a player choose someone and get to see their score
# magnifying glass is an action that is actually performed client side 
def magglass(self,i):
    #assigning the player who performs the action
    playerinaction = self.players[self.actionsplayer[i]-1]
    #sending the action back to the server to choose from the other players
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'magglass','shields':self.shield, 'mirrors':self.mirror,'actorder':self.actionsplayer})
    #waiting to here back from client 
    while self.magflag == False:
        #pump the server 
        myserver.Pump()


# this is the server definition, which handles and propagates Network events
class MyServer(Server):
    #assinging class ClientChannel to the class property channelClass 
    channelClass = ClientChannel
    #Initializng values 
    def __init__(self, *args, **kwargs):
        #Init. the server
        Server.__init__(self, *args, **kwargs)
        # initialise an empty array of players
        self.players = []
        print("Server initialised")
        # empty array of players ready
        self.playersready = []
        #setting up an array to store the scores of the players 
        self.currentscores = [0,0,0]
        #an array to store the actions of the player each round 
        self.actions = []
        #a parallel array to store the numbers of the players with their actions
        self.actionsplayer = []
        #setting up the co-ordinates
        self.square = random_squares()
        #stores whether the clients are all ready
        self.allready = False
        #rob flag
        self.robflag = False
        #stores the player chosen to be attacked
        self.playerattack = None
        #stores the player attacking
        self.playerattacking = None
        #kill flag
        self.killflag = False
        #the action of the player
        self.playeraction = None
        #present flag
        self.presentflag = None
        #setting up an array to store the bank scores
        self.bank = [0,0,0]
        #mag. flag
        self.magflag = False
        #stores individual scores 
        self.playerscore = None
        #an array to tell when all the clients are ready for the next round
        self.loopagain = []
        #swap flag
        self.swapflag = False
        #used in the swap subroutine 
        self.temp = None
        #used to send a summary of what has happened in the round
        self.sum = [[],[],[],[],[]]
        # Setting up the shield array
        self.shield = [False,False,False]
        # Setting up the mirror array 
        self.mirror = [False,False,False]
        #use when the player being attacked has a mirror
        self.newtobeattacked = None
        self.newattacker = None
        #wild card flag
        self.wildflag = False
        #used to store the action chosen by the player with a wild card
        self.wildaction = None 

    # This subroutine allows players to connect and sends them their player number
    def Connected(self, player, addr):
        #Printing out information in the console
        print("new connection:", player)
        print("address: ", addr)
        # appends a new player to the player array
        self.players.append(player)
        # assigns player number to new connection
        player.Send({'action':'number', 'num' : len(self.players)})
        # print total number of players
        print("total players " + str(len(self.players)))
        # update total of players to all clients
        self.SendToAll({'action':'players', 'playerno': len(self.players)})
        
    # Allows data to be sent to players throughout the game
    def SendToAll(self,data):
        # function to update all data to all players
        [p.Send(data) for p in self.players]

    # Main client loop
    def Loop(self):
        #infinite loop 
        while True:
            #pump the server 
            myserver.Pump()
            #very small sleep 
            sleep(0.0001)
            #if all the players are ready
            if len(self.playersready) == 3:
                #if all ready again(?)
                if self.allready == True:
                    #for all the tiles in the grid
                    for i in range(49):
                        #reset the array
                        self.loopagain = []
                        #send the new co-ordinate back to the clients
                        self.SendToAll({'action':'changesquare', 'x':self.square[0][i], 'y':self.square[1][i], 'counter':i})
                        #pump the server 
                        myserver.Pump()
                        #while waiting for the actions to be sent back
                        while len(self.actions) < 3 :
                            #pump the server 
                            myserver.Pump()

                        #Prioritising Money
                        for i in range(3): # size of action array
                            #if the action is mirror
                            if self.actions[i] == ('mirror'):
                                #set the position in the mirror array to True
                                self.mirror[i] = True
                            #if the action is shield
                            if self.actions[i] == ('shield'):
                                #set the position in the shield array to True 
                                self.shield[i] = True
                            #if the action is 200 
                            if self.actions[i] == ('200'):
                                #add 200 to the current score
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 200
                                #sending back the current scores
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            #if the action is 1000 
                            elif self.actions[i] == ('1000'):
                                #add 1000 to the current score
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 1000
                                #send back the current scores
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            #if the action is 3000
                            elif self.actions[i] == ('3000'):
                                #add 3000 to the current score
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 3000
                                #send back the current scores
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            #if the action is 5000
                            elif self.actions[i] == ('5000'):
                                #add 5000 to the current score
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 5000
                                #send back the current scores
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            #if the action is double   
                            elif self.actions[i] == ('double'):
                                #call the double subroutine
                                double(self,i)
                            #if the action is bank
                            elif self.actions[i] == ('bank'):
                                #call the bank subroutine
                                bank(self,i)
                                
                             # No need for shield if, never going to get bomb and shield on same square
                            #if the action is bomb
                            elif self.actions[i] == ('bomb'):
                                #call the bomb subroutine 
                                bomb(self,i)
                        #wild card action tiles
                        for i in range(3):
                            #if the action is wild
                            if self.actions[i] == ('wild'):
                                #trigger network action to choose
                                playerinaction = self.players[self.actionsplayer[i]-1]
                                #update the summary array
                                playerinaction.Send({'action':'wild', 'choose':self.actionsplayer[i],'square':self.actions[i],'shields':[], 'mirrors':[],'actorder':[]})
                                #wait for the action to come back in
                                while self.wildflag == False:
                                    #pump the server
                                    myserver.Pump()
                                #if the action chosen was rob    
                                if self.wildaction == ('rob'):
                                    #trigger the rob subroutine
                                    rob(self,i)
                                #else if the action chosen was kill 
                                elif self.wildaction == ('kill'):
                                    #trigger the kill subroutine 
                                    kill(self,i)
                                    
                                #else if the action chosen was present
                                elif self.wildaction == ('present'):
                                    #trigger the present subroutine
                                    present(self,i)
                                
                                #else if the action chosen was bomb
                                elif self.wildaction == ('bomb'):
                                    #trigger the bomb subroutine
                                    bomb(self,i)
                                    
                                #else if the action chosen was swap
                                elif self.wildaction == ('swap'):
                                    #trigger the swap subroutine
                                    swap(self,i)

                                #else if the action chosen was magnifying glass 
                                elif self.wildaction == ('magglass'):
                                    #trigger the mag.glass subroutine
                                    magglass(self,i)

                                #else if the action chosen was double 
                                elif self.wildaction == ('double'):
                                    #trigger the double subroutine
                                    double(self,i)

                                #else if the action chosen was bank
                                elif self.wildaction == ('bank'):
                                    #trigger the bank subroutine
                                    bank(self,i)

                        #actual action tiles (-wild card) 
                        for i in range(3):
                            #if the current action is rob
                            if self.actions[i] == ('rob'):
                                #trigger the rob subroutine
                                rob(self,i)
                            #if the current action is kill 
                            if self.actions[i] == ('kill'):
                                #trigger the kill subroutine
                                kill(self,i)
                            #if the current action is present 
                            if self.actions[i] == ('present'):
                                #trigger the present subroutine 
                                present(self,i)
                            #if the current action is swap
                            if self.actions[i] == ('swap'):
                                #trigger the swap subroutine
                                swap(self,i)
                            #if the current action is magnifying glass 
                            if self.actions[i] == ('magglass'):
                                #trigger the magglass subroutine
                                magglass(self,i)
                            #pump the server 
                            myserver.Pump()
                            #reset the flags to prepare for next action
                            self.robflag = False 
                            self.killflag = False
                            self.magflag = False 
                            self.presentflag = False 
                            self.swapflag = False
                            self.wildflag = False
                            #pump the server 
                            myserver.Pump()
                            
                        #clear the actions array ready for next action
                        self.actions = []
                        #clear the actionsplayer array ready for the next action
                        self.actionsplayer = []
                        #send to all that the actions have been completed
                        self.SendToAll({'action':'complete', 'actc': True})
                        #sending the summary screen info to the clients
                        self.SendToAll({'action':'summary','array':self.sum})
                        #resetting the shield and mirror arrays ready for the next round            
                        self.shield = [False,False,False]
                        self.mirror = [False,False,False]
                        #clearing the summary array ready for the next round
                        self.sum = [[],[],[],[],[]]
                        #whilst waiting for the go signal from all of the clients 
                        while len(self.loopagain) <3:
                            #pump the server 
                            myserver.Pump()
                    #send the bank scores to the clients when all the actions have been completed
                    self.SendToAll({'action':'bank', 'scores' : self.bank})


# use the localaddr keyword to tell the server to listen on port 1337
# messages to inform the user of what they are meant to be entering
print ('Enter the ip address of the server.')
print ('example: localhost or 192.168.0.2')
print ('Empty for localhost')
# ip address of the server (normally the ip address of the computer)
addresse = input('Server ip: ')

# control if address is left empty
if addresse == (''):
        #setting up the localhost
	addresse = ('localhost')

# inizialize the server
myserver = MyServer(localaddr=(addresse, 31500))
# start mainloop
myserver.Loop()
