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

