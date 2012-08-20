#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

import sys, time, random
from threading import Timer
from twisted.internet.protocol import Factory
import twisted.protocols.telnet
from twisted.internet import reactor

#=====Area class=====
class Area:
    
    def __init__(self, idnum): #int
        self.idnum = idnum
        self.nodes = []
        self.objects = [] #not that I've got objects working yet...
        self.connections = []
        self.players = []

    def buildactions(self, turns):
        out = list()
        for x in nodes:
            out.append(("loc" + str(x.idnum), "Enter node " + x.name))
        for y in connections:
            out.append(("loc" + str(y), "Go to area " + str(y)))
        return out

#=====Node class=====
#nodes need to have a name, a type, the various resource prices, a size (however that's measured for the skin in question), and a point at which it was last accessed
#every time the node is queried, we can compare the last access point with the current time and (if the difference is greater than some amount of time) we can then use some formula to determine what the new size and resource prices should be, as well as apply the most recent time to the string to make sure that we're not reading the same node info a bunch of time
#this is kind of simple, but we can modify it later (nodes that produce one kind of resource could engage in small amounts of local trade with nodes in the same area, for example, and that could influence prices)

class Node:

    def __init__(self, idnum, area, ntype, name, buyrates, sellrates):#int, int, string, dict, dict
        self.ntype = ntype
        self.name = name
        self.buyrates = buyrates
        self.sellrates = sellrates
        self.size = 10 #this will be changed later
        self.idnum = idnum
        self.area = area
        self.players = []

    def buildactions(self):
        out = list()
        for x in buyrates:
            out.append(("buy" + str(buyrates.index(x)) + "1", "Buy Resource " + str(buyrates.index(x))))
        for y in sellrates:
            out.append(("sel" + str(sellrates.index(x)) + "1", "Sell Resource " + str(sellrates.index(x))))
        out.append(("loc" + self.area, "Leave node"))

#=====WorldServ class=====

class WorldServ(twisted.protocols.telnet.Telnet):

    mode = "AskNew"
    username = ""

    def __init__(self, game):
        self.game = game
        self.userpass = dict()
        t = Timer(game.gamelength, endgame)

    def welcomeMessage(self):
        return "Welcome to Arbitrage!\n"

    def loginPrompt(self):
        return "Are you a new player? (yes/no) "

    def connectionLost(self, reason):
        if self.username in self.game.userinfo:
            self.game.userinfo[self.username].active = False

    def endgame(self):
        self.game.gameend()
        self.mode = "Done"

    def telnet_AskNew(self, new):
        if new == "yes":
            self.write("Welcome! Please choose a username: ")
            return "NewName"
        elif new == "no":
            self.write("Username: ")
            return "User"
        else:
            return

    def telnet_NewName(self, name):
        if name in self.userpass:
            self.write("That username is already in use. Please choose another: ")
            return
        self.username = name
        self.write(twisted.protocols.telnet.IAC + twisted.protocols.telnet.WILL + twisted.protocols.telnet.ECHO + "Choose a password (min. length 3 chars): ")
        return "NewPassOne"

    def telnet_NewPassOne(self, pswd):
        if len(pswd) < 3:
            self.write("\r\nPassword too short. Please choose another: ")
            return
        self.newpass = pswd
        self.write("\r\nEnter it again to confirm: ")
        return "NewPassTwo"

    def telnet_NewPassTwo(self, pswd):
        if pswd != self.newpass:
            self.write("\r\nPasswords don't match. Please try again: ")
            return "NewPassOne"
        self.write(twisted.protocols.telnet.IAC + twisted.protocols.telnet.WONT + twisted.protocols.telnet.ECHO + "*****\r\n")
        self.userpass[self.username] = pswd #I'm pretty sure this is anti-security here, but since I'm just dealing with telnet...
        self.game.newuser(self.username)
        self.write(self.game.userwelcome)
        self.loggedIn()
        return "Command"

    def telnet_Command(self, cmd):
        if cmd.startswith("ServComm;"):
            commlist = cmd.split(";") #this can be easily manipulated to cause bad things to happen. I'll worry about that after I get core functionality working
            self.mini = int(commlist[2])
            self.maxi = int(commlist[3])
            self.write(commlist[4])
            return commlist[1]
        else:
            self.write(self.game.actiontaken(self.username, cmd))
            return

    def telnet_AskNum(self, num):
        if num.isdigit() and (num >= self.mini and num <= self.maxi):
            self.write(getattr(self.game, self.numaction)(self.username, num))
            return "Command"
        else:
            return

    def telnet_AskStr(self, string):
        if len(string) >= self.mini and len(string) <= self.maxi:
            self.write(getattr(self.game, self.straction)(self.username, string))
            return "Command"
        else:
            return

    def loggedIn(self):
        self.write(self.game.userinfo[self.username].state)
        self.write(self.game.userinfo[self.username].actiondesc)
        return "Command"

class WorldServFactory(Factory):
    
    def __init__(self, game):
        self.game = Game(5, 600) #this is blatently non-functional...for now

    def buildProtocol(self, addr):
        return WorldServ(self.game)

#=====Player class=====
class Player:
    
    def __init__(self, playerName): #int, string, area/node, int, int
        self.playerName = playerName
        self.location = 0
        self.turns = 50
        self.money = 200
        self.resourcelist = [0,0,0,0] #this might take some rethinking...
        self.freeholds = 50 #default, this is something that will be changable with upgrades (eventually)
        self.state = "" #this holds the last message that was sent to the player
        self.message = "" #small response to the player doing something that doesn't need everything redone ("Insufficient funds", for example)
        self.actions = [] #holds the list of actions that a player may perform at any given time
        self.active = True
    
    def buildactions(self):
        return #this will come later

    def actiondesc(self):
        out = ""
        for i in actions:
            out += i[1] + "\r\n"
        return "Availaible actions:\r\n\r\n" + out

class Game:

    userwelcome = "Hi!\r\n"
    userinfo = {}
    locations = {}

    def __init__(self, size, time):
        print "starting game of " + str(size) + " areas for " + str(time) + " seconds"
        for i in range(size):
            print "Creating area " + str(i)
            a = Area(i)
            for j in range(random.randint(0,3)):
                print "Creating node " + str(j) + " in area " + str(i)
                n = Node(10000 + (100*i) + j, random.randint(0,3), a.idnum, "Node " + str(i) + "-" +str(j), {"1":1, "2":1, "3":1, "4":1}, {"1":1, "2":1, "3":1, "4":1})
                #those are lame buy/sell rates. fine for an alpha, though
                a.nodes.append(n)
                self.locations[str(n.idnum)] = n
            conns = range(size)
            conns.remove(i)
            for k in range(int(size / random.randint(2,4))):
                del conns[random.randint(0, len(conns) - 1 )]
            print "creating connections to " + str(conns)
            a.connections = conns
            self.locations[str(a.idnum)] = a
            self.gamelength = time
        print "starting turnadd timer"
        t = Timer(900.0, self.turnadd)
        t.start()
        print "starting game length timer"
        u = Timer(3600.0, self.priceupdate)
        u.start()
        print "Game initialization complete"

    def buildactions(self, name):
        actions = self.userinfo[name].location.buildactions() #this should be a list of tuples with format ("identifier", "description")
        actions.append(self.userinfo[name].buildactions())
        self.userinfo[name].actions = actions
        #pass #so here, I need to go through the list of stuff in the player's location and determine what all of the possible actions are, then give (or return?) that list to the player

    def performactions(self, player, action):
        if action.startswith('loc'): #when changing location
            player.state = changeloc(player, int(action[3:]))
        elif action.startswith('buy'):
            player.state = resourceexchange(player, int(action[3:4]), int(action[4:]), True)
        elif action.startswith('sel'):
            player.state = resourceexchange(player, int(action[3:4]), int(action[4:]), False)
        else:
            player, location, state = getattr(actions, player.actions[action])(player, location[player.location]) #this line currently does nothing (all of the core actions are here and there's nothing else implemented yet)
        self.buildactions(player) #gonna have to work more on this...
    
    def priceupdate(self):
        for i in areas:
            for j in i.nodes:
                pass #this is where the price updating logic goes, skip it for the first release (couldn't come up with an algorithm I liked...)
        t = Timer(3600.0, priceupdate) #every hour, update prices
        t.start()

    def turnadd(self):
        for i in self.userinfo.keys():
            self.userinfo[i].turns += 1
        t = Timer(900.0, turnadd) #every 15 minutes, add turns
        t.start()

    def gameend(self):
        pass #right now, there's not much to the game ending. It can be changed to dump info out at the end, or something to that effect later

    def newuser(self,name):
        p = Player(name)
        p.state = "You are now in area 0.\r\n"
        p.actiondesc, p.actions = self.buildactions(p)
        self.userinfo[name] = p
        self.locations[str(p.location)].players.append(name)

    #I'm putting some actions that are tied to nodes and areas (moving, buying, selling) here for now. As object and other features are implemented, actions for them can be placed in other areas
    def changeloc(player, movingto):
        locID = player.loc
        player.loc = movingto
        locations[locID].remove(player)
        locations[movingto].append(player)

    def resourceexchange(player, resource, number, buying):
        #hmm, I wonder how python will like just going "location.changeprice" That seems like it should fail, but it might not...
        if buying: #buying resources from the node
            if number > player.freeholds:
                return "Insufficient Space"
            if player.money < (activeloc[player.loc].buyprice[resource] * number):
                return "Insufficient Funds"
            player.resourcelist[resource] += number
            player.freeholds -= number
            player.money -= (activeloc[player.loc].buyprice[resource] * number)
            #activeloc[player.loc].pricechange(resource, number)
        else: #selling resources to the node
            if number > player.resourcelist[resource]:
                return "Insufficient Supply"
            player.resourcelist[resource] -= number
            player.freeholds += number
            player.money += (activeloc[player.loc].sellprice[resource] * number)
            #activeloc[player.loc.pricechange(resource * -1, number)]
        self.userinfo[player.name] = player



if __name__ == '__main__':
    reactor.listenTCP(8090, WorldServFactory(Game(5, 10)))
    reactor.run()

