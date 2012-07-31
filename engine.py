import select, socket, time, collections, sys

class engine:

    def __init__(self):
        activeusers = list() #this might change, depending on how (if?) I decide to store nodes in memory
        activeareas = dict() #areaID -> area def
        activenodes = dict() #objectID -> object def

    def addplayer(self, player):
        self.activeusers.append(player)

    def removeplayer(self, player):
        self.activeusers.remove(player)

    def buildactions(self, player):
        pass #so here, I need to go through the list of stuff in the player's location and determine what all of the possible actions are, the return that list to the player (should I return the list, or maybe just a whole new player object?)

    def performactions(self, player, actions):
        pass #gonna have to work more on this...
