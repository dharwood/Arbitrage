import select, socket, time, collections, sys

activeusers = dict() #sock -> Session objects
activeareas = dict() #areaID -> area def
activenodes = dict() #objectID -> object def

class 


mainsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainsock.bind((host, port))
mainsock.listen(5)

while True:
    out = select.select(activeusers.keys() + [mainsock], [], [])
    for x in out[0]:
        if x == mainsock: #that is, if someone is trying to connect
            activeusers = connector(mainsock, activeusers)
        else: #if we're receiving something from a player who's already connected
            activeusers, activeareas, activenodes = commandhandle(x, activeusers, activeareas, activenodes) #I like python, but it's scope makes no sense...

def connector(sock, users):
    pair = sock.accept()
    if pair == None: #just making sure nothing went wrong during the connection
        pass
    else:
        usersock, addr = pair
        usersock.send("Pleae enter your username:\n")
        usersock. #need to set timeout to make sure things aren't being tied up by one person just holding it
        #although, to be honest, I really should implement threads to handle multiple users trying to connect at the same time

def commandhandle(sock, users, areas, nodes):
    comm = sock.recv(4096)
    user = users[sock]



#this is where the stuff for the users already connected will go, the stuff that's pretty much generate the list of possible actions, send them to the user, wait for the user's reponse, do whatever the user indicated
