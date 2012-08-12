#Copyright (c) 2012 David Harwood

#####
#This code is licensed under the terms of the MIT license.
#You should have received a copy of this license in an included file
#named COPYING. If you did not receive this file, you may obtain a
#copy of the license at http://opensource.org/licenses/MIT
#####

import asyncore, socket, asynchat
from . import engine, session

class server(asyncore.dispatcher):

    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.inputbuf = []
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
    #I mean, I'll still need to store a list of active players and such to keep garbage collecting from getting it (wait, is there a built in garbage collector for python? I should double check that. If not, I could just leave them floating around out there and trust the loop to keep looking after them until the user disconnects), as well as the active areas and nodes (those I definitely need to get done)
