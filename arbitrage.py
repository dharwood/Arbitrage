#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

import sys, time, select, collections, socket, asyncore, asynchat, random, threading

#=====Area class=====
class Area:
    
    def __init__(self, nodes, objects, connections, player):
        self.nodes = nodes.split(',')
        self.objects = objects.split(',')
        self.connections = connections.split(',')
        self.players = [player]

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

    def __init__(self, ntype, name, buyrates, sellrates, size):#int, string, dict, dict, int
        self.ntype = ntype
        self.name = name
        self.buyrates = buyrates
        self.sellrates = sellrates
        self.size = size

    def buying(self, resource, quantity): pass
        #this is for the player buying from the node

#nodeinfofile = open("nodeinfo") #this is just a placeholder for now, will be chnaged when the configuration stuff is done

#this would be where the thing to generate a node belongs, depending on parameters in the nodeinfo file
#...though, come to think of it, this might be better served by being in the world building section, and leave in-game node creation to a different part of the code
#that way, I only have to read in the file once, and it's one less thing to worry about having to import or deal with from another file

#=====Server class=====
class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.inputbuf = list()
        self.set_terminator(b"\r\n\r\n")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def collect_incoming_data(self, data):
        self.inputbuf.append(data)

    def found_terminator(self):
        pass #need to do stuff here for when a player sends a message that isn't a connection

    def handle_accepted(self, sock, addr):
        pass #need to do stuff here, too, and this area is for dealing with incoming connections
    #here's what needs to happen for this part: get player info, create a session object, make sure the player socket is in the map, store everything and put it to use as needed

    def handle_closed(self):
        pass #need to remove the session and player info from the list and do all of the standard closing things to make this happen ALSO, THIS FUNCTION NEEDS TO GO INTO THE VARIOUS ASYNC_CHAT OBJECTS, THIS HAPPENS HERE WHEN THE SERVER SHUTS DOWN AT THE END OF THE GAME

    def handle_read(self):
        pass #I'm really just kinda creating an interface here, aren't I?

    #here's something to think about: the session objects for players, why don't I just make them extended async_chat objects? that way, I can hold all of the player info and trust them to take care of themselves when the player sends an action/connects/quits/whatever. There's probably some reason this is going to fail horibly, but I'll worry about that when I get there since nothing seems to come to mind right now about how things could go wrong...

#=====Session class=====
class Session:
    
    def __init__(self, playerID, playerName, location, turns, vehicle, money):
        self.playerID = playerID
        self.playerName = playerName
        self.location = location
        self.turns = turns
        self.ship = vehicle
        self.money = money
        self.resourcelist = [0,0,0] #this might take some rethinking...
        self.freeholds = 50 #this is something that will be changable with upgrades (eventually)

    state = "" #this holds the last message that was sent to the player
    message = "" #small response to the player doing something that doesn't need everything redone ("Insufficient funds", for example)

#=====functions=====
#def __init__(self):
#    self.activeusers = list() #this might change, depending on how (if?) I decide to store nodes in memory
#    self.activeareas = dict() #areaID -> area def
#    self.activenodes = dict() #objectID -> object def
#    self.activeloc = dict() #locationID -> location def

#def addplayer(users, player):#this whole function needs some more work since I'm not using sql to store player info anymore but am instead using memory, can store player info in a dict when they're not active (and, for that matter, a dict when they are), now that I think about it, do I really need to have an activeplayers list? it would probably still be good to have something set up to keep track of who is logged in and who isn't to keep users from trying to manipulate other people's accounts
#    users.append(player)
#    return users

#def removeplayer(users, player): #it feels like there should be more to this, but if everything is starting out instantiated, then maybe not
#    users.remove(player)
#    return users

def buildactions(player):
    location = activeloc[player.loc]
    #need to go through every object, node, and connection in the area (or just allow for purchasing or leaving if at a node) in order to make this work. there's also the non-loaction specific stuff (send messages, open menu, etc), but I think most of that goes into a different function(s)
    actions = location.buildactions(player.turns) #this should be a list of tuples with format ("identifier", "description")
    actions.append(player.buildactions()) #I know I'm breaking the standard of making pulling info as "getfoo" but I want to use getactions to retrieve the list of actions that's already built, not build the new list of actions
    player.setactions(actions)
    #pass #so here, I need to go through the list of stuff in the player's location and determine what all of the possible actions are, then give (or return?) that list to the player

def performactions(player, action):
    if action.startswith('loc'): #when changing location
        changeloc(player, int(action[3:]))
    elif action.startswith('buy'):
        resourceexchange(player, int(action[3:4]), int(action[4:]), True)
    elif action.startswith('sel'):
        resourceexcahnge(player, int(action[3:4]), int(action[4:]), False)
    else:
        actionlists.perform(player.getaction(action), player) #this line currently does nothing (all of the core actions are here in the engine, and there's nothing else implemented yet)
    #OK, so, given that the action lists aren't really supposed to have access the specific player performing the action, is there a way I can pull out the action that I want to have happen rather than trying to call that code in place? is there something with virtual functions or lambda calculus I can use?
    pass #gonna have to work more on this...

#I'm putting some actions that are tied to nodes and areas (moving, buying, selling) here into the engine. As object and other features are implemented, actions for them can be placed in other areas
def changelocation(player, movingto):
    locID = player.loc
    player.loc = movingto
    activeloc[locID].remove(player)
    activeloc[locID].append(player)

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
        activeloc[player.loc].pricechange(resource, number)
    else: #selling resources to the node
        if number > player.resourcelist[resource]:
            return "Insufficient Supply"
        player.resourcelist[resource] -= number
        player.freeholds += number
        player.money += (activeloc[player.loc].sellprice[resource] * number)
        activeloc[player.loc.pricechange(resource * -1, number)]

def priceupdate():
    for i in areas:
        for j in i.nodes:
            pass #this is where the price updating logic goes
    t = Timer(3600.0, priceupdate)
    t.start()

if __name__ == '__main__': pass
#    for i in range(50): #this seems like a good number to start with
        #steps here: generate area, generate 0-3 (-ish) nodes in that area, then build in...oh let's say 5-10 connections to other areas (should I worry about areas being unreachable? could go through and do a count after the first run)
 #       a = area.area()
 #       for j in random.randrange(3): #this is where the 0-3 nodes are created and placed in the area
 #           n = node.node(random.randint(0,3),"Node " + str(i) + "-" + str(j), )
