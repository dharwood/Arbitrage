#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

#nodes need to have a name, a type, the various resource prices, a size (however that's measured for the skin in question), and a point at which it was last accessed
#every time the node is queried, we can compare the last access point with the current time and (if the difference is greater than some amount of time) we can then use some formula to determine what the new size and resource prices should be, as well as apply the most recent time to the string to make sure that we're not reading the same node info a bunch of time
#this is kind of simple, but we can modify it later (nodes that produce one kind of resource could engage in small amounts of local trade with nodes in the same area, for example, and that could influence prices)

import time

nodeinfofile = open("nodeinfo") #this is just a placeholder for now, will be chnaged when the configuration stuff is done

#this would be where the thing to generate a node belongs, depending on parameters in the nodeinfo file
#...though, come to think of it, this might be better served by being in the world building section, and leave in-game node creation to a different part of the code
#that way, I only have to read in the file once, and it's one less thing to worry about having to import or deal with from another file

