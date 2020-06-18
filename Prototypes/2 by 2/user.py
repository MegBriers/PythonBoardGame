# ------ SERVER ------
# 2018-01-21 

#THIS PRINTS THE FINAL SCORE

# WORKING 

import PodSixNet, time, random
from random import random 
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import os

#Needed on both the client and the server?
#changes working directory 
dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
os.chdir(dir_path)

#getting stuck in here atm 
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
    
#This subroutine sets up an 3D array in a pre-set order with all the co-ordinates
#It then randomly assigns a number between 0 and 1 to the 3rd column in the array
#The subroutine then sorts the array based on the value in the sort column
#It uses a bubble sort
#This subroutine ensures that the program has a random set of squares it runs through every game
def random_squares():
    #Initialising the 3d array
    setofcoordinates = [[],[],[]]
    #Starting a fixed loop 
    for x in range(2):
        for i in range(2):
            setofcoordinates[0].append(x+1)
            setofcoordinates[1].append(i+1)
            #assinging a number between 0 and 1 to a variable called number
            number = random()
            #appends the variable number to the 3rd column in the array
            setofcoordinates[2].append(number)

    #Ordering the list
    #Loops round 49 times
    for x in range(4):
        #Loops 48 times, in order to avoidn an indexing error as comparing i and i + 1
        for i in range(3):
            #Comparing the two random values
            if setofcoordinates[2][i] <= setofcoordinates[2][i+1]:
               #Looping round for values that need to be swapped
                for n in range(3):
                    #Swapping all the values, so co-ordinates stay together
                    setofcoordinates[n][i], setofcoordinates[n][i+1] = setofcoordinates[n][i+1],setofcoordinates[n][i]
    return setofcoordinates


# client channel represents a single connection of a client to the server
#this happens when client connects to server 
class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.pressnum = None
        
        # id of player ready
        self.play = 0

        self.play2 = 0
        self.action = None
        self.number = None 

        

    # when client does connection.Send(mydata), Network method is called    
    def Network(self, data):
        # prints all passed network data to console
        print(data)
    
    # handles information about which player pressed a key and sends
    # it back to all players
    def Network_presskey(self, data):
        self.pressnum = data['pressplay']
        print("Server info: player " + str(self.pressnum) + " pressed a key")
        # send the information back to all players
        self._server.SendToAll({'action':'keyplay', 'pressno': self.pressnum})

    # when client says its ready, sends which player is ready to here
    def Network_playready(self, data):
        self.play = data['playr']
        # appending the id of the player that's ready 
        self._server.playersready.append(self.play)
        self._server.SendToAll({'action':'playrno', 'playno': len(self._server.playersready)})

    def Network_sendcoord(self,data):
        self.play2 = data['playr2']
        self._server.playersready2.append(self.play)

    def Network_actiontodo(self,data):
        self.action = data['actionsarray']
        self.number = data['number']
        self._server.actions.append(self.action)
        self._server.actionsplayer.append(self.number)

    def Network_ready(self,data):
        self._server.allready = True
    ###################################

    #If choosing someone with a shield doesn't get here 
    def Network_chosen(self,data):
        print("Network action has returned to the server")
        self._server.playerattack = data['playera']
        self._server.playerattacking = data['playern']
        self._server.playeraction = data['tobedone']
        if self._server.playeraction == ('rob'): 
            self._server.robflag = True
        elif self._server.playeraction == ('kill'):
            self._server.killflag = True
        elif self._server.playeraction == ('present'):
            self._server.presentflag = True
        elif self._server.playeraction == ('swap'):
            self._server.swapflag = True
        elif self._server.playeraction == ('magglass'):
            self._server.magflag = True

        self._server.sum[0].append(self._server.playeraction)
        self._server.sum[1].append(self._server.playerattack)
        self._server.sum[2].append(self._server.playerattacking)
        self._server.sum[3].append(self._server.shield[self._server.playerattack-1])
        self._server.sum[4].append(self._server.mirror[self._server.playerattack-1])

        print("Summary screen info so far")
        print(self._server.sum)
        print("Network Chosen event is complete")
        ############ not getting here
        
    ###################
    def Network_loopy(self,data):
        self._server.loopagain.append('ready')
    ###################


    def Network_wildchosen(self,data):
        self._server.wildaction = data['tobedone']
        self._server.wildflag = True
        


def kill(self,i):
    print("Doing Kill")
    print("")
    print(" Current scores before kill")
    print(self.currentscores)
    print("")
    playerinaction = self.players[self.actionsplayer[i]-1]
    print("Player who has kill square")
    print(playerinaction)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # shields array and mirrors etc need to be sent here
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'kill','shields':[], 'mirrors':[],'actorder':[]})
    while self.killflag == False:
        #print("Performing action")
        myserver.Pump()
        #pygame.event.pump()
    #take score of the to be attacked and add it to the attackers score
    print("attacker", self.playerattacking)
    print("")
    print("to be attacked", self.playerattack)
    print("")
    print(self.shield)
    pos = linearsearch(self.actionsplayer,self.playerattack)
    if self.shield[pos] == False and self.shield[pos] == False:
        print("No shield, proceed as normal")
        print("")
        self.currentscores[self.playerattack-1] = 0
        print("CURRENT SCORES AFTER KILL")
        print(self.currentscores)
        print("")
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        myserver.Pump() 
        print("Killing action has been performed")
        print("")
        self.killflag = False

    elif self.shield[pos] == True:
        print("Shield has blocked the action")
        print("CURRENT SCORES AFTER KILL")
        print(self.currentscores)
        print("")
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        myserver.Pump() 
        print("Killing action has been shielded")
        print("")
        self.killflag = False

    elif self.mirror[pos] == True:
        print("")
        print("**************** MIRROR")
        print("Player chosen has mirror")
        print("Action will be reflected")
        #swapping the variables 
        #person to be attacked
        self.newtobeattacked = self.playerattacking
        #person attacking
        self.newattacker = self.playerattack
        print("Person to be attacked", self.newtobeattacked)
        print("Person who is attacking/had shield", self.newattacker)
        #performing the actions
        self.currentscores[self.newtobeattacked-1] = 0
        print("Action (With mirror) has been performed")
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #setting that one back to initial values
        #self.mirror[pos] = False
        self.killflag = False


    self.killflag = False 
        

def rob(self,i):
    print("Doing Rob")
    print("current scores before rob")
    print(self.currentscores)
    print("")
    playerinaction = self.players[self.actionsplayer[i]-1]
    print("Player who is robbing someone ")
    print(playerinaction)
    print("Sending network event")

    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'rob','shields':[], 'mirrors':[],'actorder':[]})
    print("Rob flag is currently",self.robflag)

    
    while self.robflag == False:
        #print("Performing action")
        myserver.Pump()
    #take score of the to be attacked and add it to the attackers score
    print("attacker", self.playerattacking)
    print("to be attacked", self.playerattack)
    print(self.shield)
    pos = linearsearch(self.actionsplayer,self.playerattack)
    if self.shield[pos] == False and self.mirror[pos] == False:
        self.currentscores[self.playerattacking-1] = self.currentscores[self.playerattacking-1] + self.currentscores[self.playerattack-1]
        self.currentscores[self.playerattack-1] = 0
        print("")
        print("CURRENT SCORES AFTER ROB")
        print(self.currentscores)
        print("")
        print("Robbing action has been performed")
        print("")
        print("")
        print("Sending scores back")         
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        myserver.Pump()
        print("")
        print("Robbing action has been performed(wIHTOUT MIRROR OR SHIELD)")
        print("")
        self.robflag = False
    #does this 
    elif self.shield[pos] == True:
        print("Player to be attacked has a shield")
        print("Action is bypassed")
        print("Sending score back")
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #setting all back to initial values
        self.robflag = False
    #mirror action
    elif self.mirror[pos] == True:
        print("")
        print("**************** MIRROR")
        print("Player chosen has mirror")
        print("Action will be reflected")
        #swapping the variables 
        #person to be attacked
        self.newtobeattacked = self.playerattacking
        #person attacking
        self.newattacker = self.playerattack
        print("Person to be attacked", self.newtobeattacked)
        print("Person who is attacking/had shield", self.newattacker)
        #performing the actions
        self.currentscores[self.newattacker-1] = self.currentscores[self.newattacker-1] + self.currentscores[self.newtobeattacked-1]
        self.currentscores[self.newtobeattacked-1] = 0
        print("Action (With mirror) has been performed")
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #setting that one back to initial values
        #self.mirror[pos] = False
        self.robflag = False

    self.robflag = False
    
    #end of mirror action 
    ####################### END OF SHIELD IF STATEMENT
    
def bank(self,i):
    print("******************")
    print("Bank")
    print("Player who has bank", self.actionsplayer[i])
    print("Their current score", self.currentscores[self.actionsplayer[i]-1])
    self.bank[self.actionsplayer[i]-1] = self.bank[self.actionsplayer[i]-1] + self.currentscores[self.actionsplayer[i]-1] 
    print("Their bank score now", self.bank[self.actionsplayer[i]-1])
    self.currentscores[self.actionsplayer[i]-1] = 0
    print("Updated current", self.currentscores[self.actionsplayer[i]-1])
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    myserver.Pump()
    #print bank array??
    print("Bank array")
    print(self.bank)
    print("Bank has been performed")

#def bomb(self,i,self.actionsplayer,self.currentscores):
def bomb(self,i):
    #Need to check if right indexing
    print("*********************")
    print("Bomb")
    #right indexing??
    print("Player who has bomb", self.actionsplayer[i])
    self.currentscores[self.actionsplayer[i]-1] = 0 
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    myserver.Pump()
    print("Bomb has been performed")

#def double(self,self.actionsplayer,self.currentscores,i):
def double(self,i):
    #Need to check if right indexing
    print("**************************")
    print("Double")
    print("Player who has double", self.actionsplayer[i])
    self.currentscores[self.actionsplayer[i]-1] = (self.currentscores[self.actionsplayer[i]-1]) * 2 
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    myserver.Pump()
    print("Double has been performed")
    
#self,i,self.actionsplayer,self.actions,self.presentflag,self.playerattacking,self.playerattack
def present(self,i):
    print("********************")
    print("Present")
    playerinaction = self.players[self.actionsplayer[i]-1]
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'present','shields':[], 'mirrors':[],'actorder':[]})                                 
    while self.presentflag == False:
        myserver.Pump()
    print("Player sending gift")
    print(self.playerattacking)
    print("Player receiving the gift")
    print(self.playerattack)
    print("")
    #Even though it says attack, the player in question is actually being benefited
    self.currentscores[self.playerattack-1] = self.currentscores[self.playerattack-1] + 1000
    self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
    myserver.Pump()
    self.presentflag = False
    print("Present has been performed")

#self,i,self.players,self.actionsplayer,self.swapflag,self.currentscores,self.playerattack,self.playerattacking,self.shield,self.temp
def swap(self,i):
    print("*************")
    print("Swap scores")
    #setting up the player who has the swap
    playerinaction = self.players[self.actionsplayer[i]-1]
    #sending the action back to the server to choose from the other players 
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'swap','shields':[], 'mirrors':[],'actorder':[]})
    ## NEED TO SET UP A FLAG (done)
    ## NEED TO SET UP IN THE FLAG SUBROUTINE (done)
    while self.swapflag == False:
        myserver.Pump()
    #receiving the player chosen and the player attacking back from server
    #set a temporary variable
    #swap the scores
    print("")
    print("Current score of the player attacking" , self.currentscores[self.playerattacking-1])

    print("Current score of the player being attacked" , self.currentscores[self.playerattack-1])

    ########### SHIELD IF
    print(self.shield)
    pos = linearsearch(self.actionsplayer,self.playerattack)
    if self.shield[pos] == False and self.mirror[pos] == False:
        #print("Current score of the player attacking" , self.currentscores[self.playerattacking-1])
        self.temp = self.currentscores[self.playerattacking-1]
        #player who is getting attacked
        #print("Current score of the player being attacked" , self.currentscores[self.playerattack-1])
        self.currentscores[self.playerattacking-1] = self.currentscores[self.playerattack]
        self.currentscores[self.playerattack-1] = self.temp
        print("After action score of the player attacking" , self.currentscores[self.playerattacking-1])
        print("After action score of the player being attacked" , self.currentscores[self.playerattack-1])  
        #sending the scores back to the client 
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pumping the server to make sure that they receive the data 
        myserver.Pump()
        self.swapflag = False
        print("Swap score has been performed without shield or mirror")
    #Testing purposes
    elif self.shield[pos] == True:
        print("Action has been shielded")
        print("No change to scores")
        print("After action score of the player attacking" , self.currentscores[self.playerattacking-1])
        print("After action score of the player being attacked" , self.currentscores[self.playerattack-1])  
        #sending the scores back to the client 
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        #pumping the server to make sure that they receive the data 
        myserver.Pump()
        self.swapflag = False 
        print("Swap score has not been performed")

    elif self.mirror[pos] == True:
        #MAKE SURE THIS GOES IN THE RULES
        print("Mirroring a swap means no swap takes place")
        self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
        self.swapflag = False

    self.swapflag = False 
        

def magglass(self,i):
    #assinging the player who performs the action
    playerinaction = self.players[self.actionsplayer[i]-1]
    #sending the action back to the server to choose from the other players
    playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':'magglass','shields':self.shield, 'mirrors':self.mirror,'actorder':self.actionsplayer})
    while self.magflag == False:
        myserver.Pump()
    print("Magnifying glass has been performed")


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# this is the server definition, which handles and propagates Network events
class MyServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        # initialise an empty array of players
        self.players = []
        print("Server initialised")

        # empty array of players ready
        self.playersready = []
        self.playersready2 = []
        self.currentscores = [789,235,185]
        self.actions = []
        self.actionsplayer = []
        self.square = random_squares()
        self.allready = False
        self.pactions = []
        self.robflag = False
        self.playerattack = None
        self.playerattacking = None
        self.killflag = False
        self.playeraction = None
        self.presentflag = None 
        self.bank = [0,0,0]
        self.magflag = False 
        self.playerscore = None
        self.loopagain = []
        self.swapflag = False
        self.temp = None

        #NEW

        self.sum = [[],[],[],[],[]]

        # Setting up the shield array
        self.shield = [False,False,False]

        # Setting up the mirror array 
        self.mirror = [False,False,False]
        self.newtobeattacked = None
        self.newattacker = None

        ###########
        self.wildflag = False
        self.wildaction = None 
        
    def Connected(self, player, addr):
        print("new connection:", player)
        print("address: ", addr)
        # appends a new player to the player array
        self.players.append(player)
        # assigns player number to new connection
        player.Send({'action':'number', 'num' : len(self.players)})
        print("Sent player their number")
        # print total number of players
        print("total players " + str(len(self.players)))
        # update total of players to all clients
        self.SendToAll({'action':'players', 'playerno': len(self.players)})

    def SendToAll(self,data):
        # function to update all data to all players
        [p.Send(data) for p in self.players]

    def Loop(self):
        while True:
            myserver.Pump()
            sleep(0.0001)
            if len(self.playersready) == 3:   
                #myserver.Pump()
                if self.allready == True:
                    for i in range(4):
                        self.loopagain = []
                        print("Turn number", i)
                        print(self.square)
                        # added counter to the data sent back so that we can stop it after 4 iterations
                        self.SendToAll({'action':'changesquare', 'x':self.square[0][i], 'y':self.square[1][i], 'counter':i})
                        myserver.Pump()
                        # gather actions (set up an array)
                        ##################
                        while len(self.actions) < 3 :
                            #print(len(self.actions))
                            #print("Waiting for actions")
                            #print("")
                            myserver.Pump()
                            #time.sleep(1000)

                        print("These are the actions" , self.actions)
                        #Prioritising Money
                        for i in range(3): # size of action array
                            print("iteration ", i)
                            print("")
                            print("player whose turn it is", self.actionsplayer[i])
                            print("")
                            ############# Mirror Action
                            if self.actions[i] == ('mirror'):
                                print("Mirror action")
                                print("")
                                self.mirror[i] = True
                                print(self.mirror)
                                print("Player", self.actionsplayer[i], "has a mirror")
                            ############# End of Mirror action

                            ############## Shield action
                            if self.actions[i] == ('shield'):
                                #change display(later)
                                print("Shield action")
                                print("")
                                self.shield[i] = True
                                print(self.shield[i])
                                print("Player", self.actionsplayer[i], "has a shield")
                            ############### End of Shield action
                                
                            if self.actions[i] == ('200'):
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 200
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            if self.actions[i] == ('1000'):
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 1000
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            if self.actions[i] == ('3000'):
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 3000
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                            if self.actions[i] == ('5000'):
                                self.currentscores[self.actionsplayer[i]-1] = self.currentscores[self.actionsplayer[i]-1] + 5000
                                self.SendToAll({'action':'current', 0: self.currentscores[0], 1: self.currentscores[1], 2: self.currentscores[2]})
                                
                            if self.actions[i] == ('double'):
                                double(self,i)

                            if self.actions[i] == ('bank'):
                                bank(self,i)

                        for i in range(3):

                            if self.actions[i] == ('wild'):
                                #trigger network action to choose
                                playerinaction = self.players[self.actionsplayer[i]-1]
                                playerinaction.Send({'action':'wild', 'choose':self.actionsplayer[i],'square':self.actions[i],'shields':[], 'mirrors':[],'actorder':[]})
                                #get data back in
                                #compare the action
                                #perform the action
                                while self.wildflag == False:
                                    myserver.Pump()
                                    
                                # !!!!!!
                                # need to change self.action[i] from wild to what
                                # ever was chosen
                                #self.actions[i] = self.wildaction
                                #myserver.Pump
                                if self.wildaction == ('rob'):
                                    rob(self,i)

                                if self.wildaction == ('kill'):
                                    kill(self,i)
                                    
                                # No need for shield 
                                if self.wildaction == ('present'):
                                    present(self,i)
                                
                                # No need for shield if, never going to get bomb and shield on same square  
                                if self.wildaction == ('bomb'):
                                    bomb(self,i)

                                if self.wildaction == ('swap'):
                                    swap(self,i)

                                if self.wildaction == ('magglass'):
                                    magglass(self,i)

                                if self.wildaction == ('double'):
                                    double(self,i)

                                if self.wildaction == ('bank'):
                                    bank(self,i)

                                print("WILD CARD complete")
                                    
                            
                        for i in range(3):
                            if self.actions[i] == ('rob'):
                                rob(self,i)
                            
                            if self.actions[i] == ('kill'):
                                kill(self,i)
                                
                            # No need for shield 
                            if self.actions[i] == ('present'):
                                present(self,i)
                            
                            # No need for shield if, never going to get bomb and shield on same square  
                            if self.actions[i] == ('bomb'):
                                bomb(self,i)

                            if self.actions[i] == ('swap'):
                                swap(self,i)

                            if self.actions[i] == ('magglass'):
                                magglass(self,i)

                            myserver.Pump()
                            #cleared array to prepare for next action
                            self.robflag = False 
                            self.killflag = False
                            self.magflag = False 
                            self.presentflag = False 
                            self.swapflag = False
                            self.wildflag = False

                            myserver.Pump()
                            

                        self.actions = []
                        self.actionsplayer = []

                        self.SendToAll({'action':'complete', 'actc': True})
                        #set shield array back to three falses

                        #sending the summary screen
                        #NEW 
                        self.SendToAll({'action':'summary','array':self.sum})
                                        
                        self.shield = [False,False,False]
                        self.mirror = [False,False,False]

                        self.sum = [[],[],[],[],[]]
                        
                        print("End of Actions")
                        while len(self.loopagain) <3:
                            myserver.Pump()
                    self.SendToAll({'action':'bank', 'scores' : self.bank})

# create server
# use the localaddr keyword to tell the server to listen on port 1337
myserver = MyServer(localaddr=('localhost', 1337))
myserver.Loop()
