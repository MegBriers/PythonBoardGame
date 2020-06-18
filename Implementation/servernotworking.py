# ------ SERVER ------

# doesn't perform any actions apart from money 
import PodSixNet, time, random
from random import random 
from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

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
        print("Server info: player " + str(self.play) + " is ready")
        # print number of players ready
        print("Total number of players ready = " + str(len(self._server.playersready)))
        # send the information back to all players
        self._server.SendToAll({'action':'playrno', 'playno': len(self._server.playersready)})

    def Network_sendcoord(self,data):
        self.play2 = data['playr2']
        self._server.playersready2.append(self.play)
        print("Total number of players ready to start - " + len(self.__server.playersready2))
        #self.__server.SendToAll({'action':'', 'play2':len(self.__server.playersready2)})

    def Network_actiontodo(self,data):
        self.action = data['actionsarray']
        self.number = data['number']
        print("Player ", self.number)
        print("Action ", self.action) 
        self._server.actions.append(self.action)
        self._server.actionsplayer.append(self.number)

    def Network_ready(self,data):
        self._server.allready = True
    ###################################
        
    def Network_chosen(self,data):
        self._server.playerattack = data['playera']
        self._server.playerattacking = data['playern']
        self._server.playeraction = data['action']
        if self._server.playeraction == ('rob'): 
            self._server.robflag = True
        elif self._server.playeraction == ('kill'):
            self._server.killflag = True
        print("Network Chosen event is complete")
        

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
        #############################
        self.playersready2 = []
        #############################
        self.currentscores = [0,0,0]
        self.actions = []
        self.actionsplayer = []
        self.square = random_squares()
        self.allready = False
        self.pactions = []
        ##################
        #print(self.square)
        self.robflag = False
        self.playerattack = None
        self.playerattacking = None
        self.killflag = False
        self.playeraction = None 
        


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
                #print("Got to the next step")
                if self.allready == True:
                    for i in range(1):
                        print("counter value", i)
                        print(self.square)
                        # added counter to the data sent back so that we can stop it after 4 iterations
                        self.SendToAll({'action':'changesquare', 'x':self.square[0][i], 'y':self.square[1][i], 'counter':i})
                        print("After send")
                        myserver.Pump()
                        ###################
                        print("After pump")
                        print(len(self.actions))
    #                    time.sleep(1000000)
                        # gather actions (set up an array)
                        ##################
                        while len(self.actions) < 3 :
                            #print(len(self.actions))
                            #print("Waiting for actions")
                            myserver.Pump()
                            #time.sleep(1000)
                        
                        for i in range(3): # size of action array
                            print("iteration ", i)
                            print("player it is being added to is ", self.actionsplayer[i])
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
                            if self.actions[i] == ('rob'):
                                #################################
                                print("Rob")
                                print("current scores before rob")
                                print(self.currentscores)
                                #NOT SEND TO ALL
                                playerinaction = self.players[self.actionsplayer[i]-1]
                                playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':self.actions[i]})
                                while self.robflag == False:
                                    #print("Performing action")
                                    myserver.Pump()
                                #take score of the to be attacked and add it to the attackers score
                                print("attacker", self.playerattacking)
                                print("to be attacked", self.playerattack)
                                self.currentscores[self.playerattacking-1] = self.currentscores[self.playerattacking-1] + self.currentscores[self.playerattack-1]
                                self.currentscores[self.playerattack-1] = 0
                                print("CURRENT SCORES AFTER ROB")
                                print(self.currentscores)
                                self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
                                myserver.Pump() 
                                print("Robbing action has been performed")
                                self.robflag = False  
                                ################################
                                #sends all the scores back
                    ######################################################## 13.1 
                            if self.actions[i] == ('kill'):
                                print("Kill")
                                print(" Current scores before kill")
                                print(self.currentscores)
                                playerinaction = self.players[self.actionsplayers[i]-1]
                                playerinaction.Send({'action':'choose', 'not':self.actionsplayer[i],'square':self.actions[i]})
                                while self.killflag == False:
                                    #print("Performing action")
                                    myserver.Pump()
                                #take score of the to be attacked and add it to the attackers score
                                print("attacker", self.playerattacking)
                                print("to be attacked", self.playerattack)
                                self.currentscores[self.playerattack-1] = 0
                                print("CURRENT SCORES AFTER KILL")
                                print(self.currentscores)
                                self.SendToAll({'action':'current', 0:self.currentscores[0],1: self.currentscores[1], 2: self.currentscores[2]})
                                myserver.Pump() 
                                print("Killing action has been performed")
                                self.killflag = False 
                    ######################################################## 13.1             
                                
                        self.SendToAll({'action':'complete', 'actc': True})
                        #cleared array to prepare for next action
                        self.actions = []
                        pygame.time.wait(100000)

       

# create server
# use the localaddr keyword to tell the server to listen on port 1337
myserver = MyServer(localaddr=('localhost', 1337))
myserver.Loop()
