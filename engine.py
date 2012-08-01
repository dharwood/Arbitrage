#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

import select, socket, time, collections, sys

class engine:

    def __init__(self):
        self.activeusers = list() #this might change, depending on how (if?) I decide to store nodes in memory
        self.activeareas = dict() #areaID -> area def
        self.activenodes = dict() #objectID -> object def
        self.activeloc = dict() #locationID -> location def

    def addplayer(self, player):
        self.activeusers.append(player)
        locID = player.getloc()
        if locID not in self.activeloc():
            if locID > 1000000:
                self.activeloc[locID] = #sql for nodes needs to go here
            else:
                self.activeloc[locID] = #sql for areas needs to go here
        self.activeloc[locID].addplayer(player)
        self.buildactions(player)

    def removeplayer(self, player):
        self.activeusers.remove(player)
        locID = player.getloc()
        if locID not in self.activeloc:
            if

    def buildactions(self, player): #the way this turned out, it's realy just a helper function to act as a go-between
        locID = player.getloc()
        location = self.activeloc[locID]
        player.setactions(location.getactions())
        #pass #so here, I need to go through the list of stuff in the player's location and determine what all of the possible actions are, then return that list to the player (should I return the list, or maybe just a whole new player object?)

    def performactions(self, player, action):
        if action.startswith('loc'):
            self.changeloc(player, int(action[3:]))
        else:
            actionlists.perform(player.getaction(action), player)
        self.turnuse()
        #OK, so, given that the action lists aren't really supposed to have access the specific player performing the action, is there a way I can pull out the action that I want to have happen rather than trying to call that code in place? is there something with virtual functions or lambda calculus I can use?
        pass #gonna have to work more on this...

    def changelocation(self, player, movingto):
        locID = player.getloc()
        player.setloc(movingto)
        self.activeloc[locID].removeplayer(player)
        if len(self.activeloc[locID].players) is 0:
            if locID > 1000000:
                #need to write node state to node table
            else:
                #need to write area state to area table
            del self.activeloc[locID]
        if movingto not in self.activeloc:
            if locID > 1000000:
                self.activeloc[movingto] = #sql for nodes needs to go here
            else:
                self.activeloc[movingto] = #sql for areas needs to go here
        self.activeloc[locID].addplayer(player)
        self.turnuse()

