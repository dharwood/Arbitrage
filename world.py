#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

#so this is the area where I need to build the big graph to represent the world

from . import engine
from . import area
from . import node
from . import server
import random

if __name__ == "__main__":
    for i in range(50): #this seems like a good number to start with
        #steps here: generate area, generate 0-3 (-ish) nodes in that area, then build in...oh let's say 5-10 connections to other areas (should I worry about areas being unreachable? could go through and do a count after the first run)
        a = area.area()
        for j in random.randrange(3): #this is where the 0-3 nodes are created and placed in the area
            n = node.node(random.randint(0,3),"Node " + str(i) + "-" + str(j), )

