#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

import select, time, collections, sys

class engine:

    def __init__(self):
        self.activeusers = list() #this might change, depending on how (if?) I decide to store nodes in memory
        self.activeareas = dict() #areaID -> area def
        self.activenodes = dict() #objectID -> object def
        self.activeloc = dict() #locationID -> location def

    def addplayer(self, player):#this whole function needs some more work since I'm not using sql to store player info anymore but am instead using memory (though I might go back to sql if keeping track of this in memory is too painful), can store player info in a dict when they're not active (and, for that matter, a dict when they are), now that I think about it, do I really need to have an activeplayers list? it was originally put in to keep active players in memory an avoid having to update sql tables all the time, but if I'm not using sql anymore...though it would probably still be good to have something set up to keep track of who is logged in and who isn't to keep users from trying to manipulate other people's accounts
        self.activeusers.append(player)
#        locID = player.getloc()
#        if locID not in self.activeloc():
#            if locID > 1000000:
#                self.activeloc[locID] = #sql for nodes needs to go here
#            else:
#                self.activeloc[locID] = #sql for areas needs to go here
#        self.buildactions(player) #this will now work by storing the available actions in the player's "file" and just reading them as usual from there when a player logs in

    def removeplayer(self, player): #it feels like there should be more to this, but if everything is starting out instantiated
        self.activeusers.remove(player)

    def buildactions(self, player):
        location = self.activeloc[player.getloc()]
        #need to go through every object, node, and warp in the area (or just allow for purchasing or leaving if at a node) in order to make this work. there's also the non-loaction specific stuff (send messages, open menu, etc), but I think most of that goes into a different function(s)
        actions = location.buildactions(player.turns) #this should be a list of tuples with format ("identifier", "description")
        actions.append(player.buildactions()) #I know I'm breaking the standard of making pulling info as "getfoo" but I want to use getactions to retrieve the list of actions that's already built, not build the new list of actions
        player.setactions(actions)
        #pass #so here, I need to go through the list of stuff in the player's location and determine what all of the possible actions are, then give (or return?) that list to the player

    def performactions(self, player, action):
        if action.startswith('loc'): #when changing location
            self.changeloc(player, int(action[3:]))
        else:
            actionlists.perform(player.getaction(action), player)
        #OK, so, given that the action lists aren't really supposed to have access the specific player performing the action, is there a way I can pull out the action that I want to have happen rather than trying to call that code in place? is there something with virtual functions or lambda calculus I can use?
        pass #gonna have to work more on this...

    def changelocation(self, player, movingto):
        if not self.turnuse(): #if the player doesn't have enough turns left
            return 'Action not completed: insufficient turns.'
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

#    def turnuse(self, player, turns=1):
#        if player.turns < turns:
#            player.turns -= turns
#            return True
#        else:
#            return False
