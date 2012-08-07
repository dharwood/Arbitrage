#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

class Area:
    
    def __init__(self, nodes, objects, connections, player):
        self.nodes = nodes.split(',')
        self.objects = objects.split(',')
        self.connections = connections.split(',')
        self.players = [player]

    def buildactions(self, turns):
        out = []
        for x in nodes:
            out.append(("loc" + str(x.idnum), "Enter node " + x.name))
        for y in connections:
            out.append(("loc" + str(y), "Go to area " + str(y))
        #if there's anything else that we want to pull actions from, this is where the code for that would go
        return out
